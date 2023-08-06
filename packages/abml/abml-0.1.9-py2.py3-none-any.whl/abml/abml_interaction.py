from abaqus import mdb
from regionToolset import Region
from part import FaceArray
from numpy import sort, lexsort

from abml.abml_logger import Logger
from abml.abml_helpers import (
    convert_abaqus_constants,
    convert_abaqus_constant,
    convert_geometry_repository,
    cprint,
)
from collections import Counter
import re
from numpy import array, empty, mean, argmin, unique, sum, unique, where, dot
from numpy.linalg import svd

logger = Logger().get_logger(__name__)


class Abml_Interaction:
    def __init__(self, model, name, **kwargs):
        self.model = model
        self.name = name
        self.kwargs = kwargs
        self.type_ = next(iter(self.kwargs))

        mdb_model = mdb.models[self.model]

        self.interaction_map = {
            "SurfaceToSurfaceContactExp": mdb_model.SurfaceToSurfaceContactExp,
            "SurfaceToSurfaceContactStd": mdb_model.SurfaceToSurfaceContactStd,
            "surfacetosurfacecontactstd_auto": mdb_model.SurfaceToSurfaceContactStd,
            "surfacetosurfacecontactexp_auto": mdb_model.SurfaceToSurfaceContactExp,
            "SelfContactExp": mdb_model.SelfContactExp,
            "SelfContactStd": mdb_model.SelfContactStd,
            "ElasticFoundation": mdb_model.ElasticFoundation,
        }

        self.interaction_map = {k.lower(): v for k, v in self.interaction_map.items()}

        self.create()

    def elastic_foundation(self):
        access = mdb.models[self.model].rootAssembly
        regex  = self.kwargs[self.type_]["surface"]

        surface = Counter()
        if isinstance(regex, list):
            instances = regex
            for instance in instances:
                updated = {"surface": access.allSurfaces[instance].faces}
                updated = {k: v for k, v in updated.items() if v is not None}
                surface.update(updated)
        else:
            regex_compile = re.compile(regex)
            instances = list(filter(regex_compile.match, access.allSurfaces.keys()))
            if len(instances) == 0:
                raise ValueError("regex: {} does not match any surface in {}".format(regex, access.allSurfaces.keys()))

            for instance in instances:
                updated = {"surface": access.allSurfaces[instance].faces}
                updated = {k: v for k, v in updated.items() if v is not None}
                surface.update(updated)
        # surface = Region(faces=dict(surface))

        kwargs = {"createStepName": self.kwargs[self.type_]["createStepName"], 
                  "stiffness":  self.kwargs[self.type_]["stiffness"],
                  "name":  self.name,
                  "surface": Region(side1Faces=surface["surface"])
                  }
        # kwargs.update(surface)

        mdb.models[self.model].ElasticFoundation(**kwargs)

    def create(self):
        logger.debug("interaction: {}".format(self.name))
        access = mdb.models[self.model].rootAssembly

        # todo sort with map
        if "sliding" in self.kwargs[self.type_]:
            self.kwargs[self.type_]["sliding"] = convert_abaqus_constant(self.kwargs[self.type_]["sliding"])
        if "enforcement" in self.kwargs[self.type_]:
            self.kwargs[self.type_]["enforcement"] = convert_abaqus_constant(self.kwargs[self.type_]["enforcement"])

        if (
            self.type_ == "surfacetosurfacecontactstd_auto"
            or self.type_ == "surfacetosurfacecontactexp_auto"
        ):
            pairs = self.find_pairs()
            for i, pair in enumerate(pairs):
                self.kwargs[self.type_]["master"] = pair[0]
                self.kwargs[self.type_]["slave"] = pair[1]
                
                self.interaction_map[self.type_](
                    name="{}-{}".format(self.name, i), **self.kwargs[self.type_]
                )
        elif self.type_.lower() == "ElasticFoundation".lower():
            self.elastic_foundation()
        else:
            if isinstance(self.kwargs[self.type_]["master"], str):
                self.kwargs[self.type_]["master"] = access.allSurfaces[
                    self.kwargs[self.type_]["master"]
                ]
            elif isinstance(self.kwargs[self.type_]["master"], dict) and "surface" in self.kwargs[self.type_]["master"]:
                self.kwargs[self.type_]["master"] = access.allSurfaces[
                    self.kwargs[self.type_]["master"]["surface"]
                ]
            else:
                master = Counter()
                for instance in access.instances.keys():
                    updated = convert_geometry_repository(
                        access.instances[instance], **self.kwargs[self.type_]["master"]
                    )
                    updated = {k: v for k, v in updated.items() if v is not None}
                    master.update(updated)
                self.kwargs[self.type_]["master"] = Region(**master)

            if isinstance(self.kwargs[self.type_]["slave"], str):
                if self.kwargs[self.type_]["slave"] in access.allSets.keys():
                    self.kwargs[self.type_]["slave"] = access.allSets[
                        self.kwargs[self.type_]["slave"]
                    ]
                elif self.kwargs[self.type_]["slave"] in access.allSurfaces.keys():
                    self.kwargs[self.type_]["slave"] = access.allSurfaces[
                        self.kwargs[self.type_]["slave"]
                    ]
            elif isinstance(self.kwargs[self.type_]["slave"], dict) and "set" in self.kwargs[self.type_]["slave"]:
                self.kwargs[self.type_]["slave"] = access.allSets[
                    self.kwargs[self.type_]["slave"]["set"]
                ]
            elif isinstance(self.kwargs[self.type_]["slave"], dict) and "surface" in self.kwargs[self.type_]["slave"]:
                self.kwargs[self.type_]["slave"] = access.allSurfaces[
                    self.kwargs[self.type_]["slave"]["surface"]
                ]
            elif isinstance(self.kwargs[self.type_]["slave"], dict) and "surface" in self.kwargs[self.type_]["slave"]:
                self.kwargs[self.type_]["slave"] = access.allSets[
                    self.kwargs[self.type_]["slave"]["set"]
                ]
            else:
                slave = Counter()
                for instance in access.instances.keys():
                    updated = convert_geometry_repository(
                        access.instances[instance], **self.kwargs[self.type_]["slave"]
                    )
                    updated = {k: v for k, v in updated.items() if v is not None}
                    slave.update(updated)

                self.kwargs[self.type_]["slave"] = Region(**slave)

            self.interaction_map[self.type_](name=self.name, **self.kwargs[self.type_])

    def find_pairs(self):
        access = mdb.models[self.model].rootAssembly
        regex = re.compile(self.kwargs[self.type_].pop("regex"))
        instances_master = list(filter(regex.match, access.instances.keys()))

        surface_map = {}
        instance_map = dict(enumerate(instances_master))

        num_faces = int(sum(
            [len(access.instances[instance].faces) for instance in instances_master]
        ))

        if num_faces == 0:
            return []

        surface_norms = empty((num_faces, 3))
        surface_instances = empty(num_faces, dtype=object)
        surface_indices = empty(num_faces)

        counter = 0
        for k, instance_name in instance_map.items():
            surface_map[instance_name] = dict(
                enumerate(access.instances[instance_name].faces)
            )
            for j, face in surface_map[instance_name].items():
                surface_vertices = empty((len(face.getVertices()), 3))
                for i, vertex in enumerate(face.getVertices()):
                    point = access.instances[instance_name].vertices[vertex].pointOn
                    surface_vertices[i, :] = point[0]

                center = mean(surface_vertices, axis=0)
                sorted_indices = lexsort((surface_vertices[:, 2], surface_vertices[:, 1], surface_vertices[:, 0]))
                _, _, V = svd(surface_vertices[sorted_indices] - center)
                normal_vector = V[-1]
                if dot(normal_vector, center) < 0:
                    normal_vector = -normal_vector
                surface_norms[counter, :] = normal_vector + center
                surface_instances[counter] = instance_name
                surface_indices[counter] = j

                counter += 1

        surface_norms = surface_norms.round(decimals=10)
        _, inverse_indices, counts = unique(
            surface_norms, axis=0, return_inverse=True, return_counts=True
        )
        duplicate_indices = where(counts > 1)[0]


        pairs = []
        for i, index in enumerate(duplicate_indices):
            row_indices = where(inverse_indices == index)[0]
            instance = surface_instances[row_indices[0]]
            index = surface_indices[row_indices[0]]
            master = surface_map[instance][index]
            instance = surface_instances[row_indices[1]]
            index = surface_indices[row_indices[1]]
            slave = surface_map[instance][index]

            pairs.append(
                [
                    Region(side1Faces=FaceArray(faces=(master,))[:]),
                    Region(side1Faces=FaceArray(faces=(slave,))[:]),
                ]
            )
        return pairs


def group_vertices(vertices):
    unique_vertices, indices = unique(vertices, axis=0, return_inverse=True)
    groups = {}

    for i, vertex in enumerate(unique_vertices):
        if indices[i] not in groups:
            groups[indices[i]] = []

        groups[indices[i]].append(vertex)

    filtered_groups = {key: value for key, value in groups.items() if len(value) > 1}

    return filtered_groups

    # return groups
