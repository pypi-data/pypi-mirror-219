from abaqus import mdb, AbaqusException
from regionToolset import Region
import logging

from abml.abml_helpers import convert_abaqus_constants, convert_geometry_repository
from abml.abml_helpers import sort_dict_by_suffix, sort_dict_with_fixed_order, cprint
from abml.abml_parts import Abml_Feature, Abml_Mesh
from abml.abml_logger import Logger

from abaqusConstants import CARTESIAN
from collections import Counter
from numpy import array
import re

from copy import deepcopy


logger = Logger().get_logger(__name__)

class Abml_Assembly:
    def __init__(self, model, **data):
        self.model = model
        self.data = data
        
        self.sets = data.get("sets", {})
        self.surfaces = data.get("surfaces", {})
        self.instances = data.get("instances", {})
        self.features = data.get("features", {})

        self.create_instances()
        self.create_features()
        self.create_surfaces()
        self.create_sets()
    
    def create_instances(self):
        for instance in sort_dict_by_suffix(self.instances.keys()):
            Abml_Instance(model=self.model, name=instance, **self.data["instances"][instance])

    def create_features(self):
        a = mdb.models[self.model].rootAssembly
        for feature in self.features:
            Abml_Feature(model=self.model, name=feature,access=a, **self.data["features"][feature])

    def create_sets(self):
        for set_ in self.sets:
            Abml_Assembly_Sets(mdb.models[self.model].rootAssembly, set_, **self.sets[set_])

    def create_surfaces(self):
        for surface in self.surfaces:
            if isinstance(self.surfaces[surface], dict):
                Abml_Assembly_Surfaces(mdb.models[self.model].rootAssembly, surface, **self.surfaces[surface])
            elif isinstance(self.surfaces[surface], str):
                Abml_Assembly_Surfaces(mdb.models[self.model].rootAssembly, surface, regex=self.surfaces[surface])
            else:
                Abml_Assembly_Surfaces(mdb.models[self.model].rootAssembly, surface, *self.surfaces[surface])


class Abml_Instance:
    def __init__(self, model, name, part, **kwargs):
        self.model = model
        self.name = name
        self.part = part

        self.kwargs = convert_abaqus_constants(**kwargs)

        sorted_keys = sort_dict_by_suffix(self.kwargs.keys())
        self.transform_list = []
        for key in sorted_keys:
            if "translate" in key:
                self.transform_list.append({"translate":self.kwargs.pop(key, [0, 0, 0])})
            elif "rotate" in key:
               self.transform_list.append({"rotate": self.kwargs.pop(key, [0, 0, 0])})

        self.boolcut_params = self.kwargs.pop("boolcut", {})

        self.arange = self.kwargs.pop("arange", None)

        self.part_obj = mdb.models[self.model].parts[self.part]
        self.a = mdb.models[self.model].rootAssembly

        if self.arange is None:
            if self.name not in self.a.instances.keys():
                self.create(name=self.name, part=self.part_obj, **self.kwargs)
            for transform in self.transform_list:
                self.rotate_translate(self.name, **transform)
        else:
            global_boolcut_params = self.arange.pop("boolcut", {})

            for i, instance in enumerate(self.arange["instances"]):
                prefix = instance.pop("prefix", "")
                suffix = instance.pop("suffix", "")
                part = instance.pop("part", self.part)
                # if part is None:
                #     part = self.part
                part_obj = mdb.models[self.model].parts[part]
                if prefix == "" and suffix == "":
                    suffix = "-{}".format(i+1)
                name = "{}{}{}".format(prefix,self.name, suffix)

                sorted_keys = sort_dict_by_suffix(instance.keys())
                transform_list = []
                for key in sorted_keys:
                    if "translate" in key:
                        transform_list.append({"translate":instance.pop(key, [0, 0, 0])})
                    elif "rotate" in key:
                        transform_list.append({"rotate": instance.pop(key, [0, 0, 0])})

                boolcut_params = {}
                boolcut_params.update(deepcopy(global_boolcut_params))
                boolcut_params.update(instance.pop("boolcut", {}))
                
                local_kwargs = deepcopy(self.kwargs)
                local_kwargs.update(instance)
                
                if name not in self.a.instances.keys():
                    self.create(name=name, part=part_obj, **local_kwargs)

                for transform in transform_list:
                    self.rotate_translate(name, **transform)

                if boolcut_params != {}:
                    self.boolcut(name, **boolcut_params)


        for instance in mdb.models[self.model].rootAssembly.instances.keys():
            if len(mdb.models[self.model].rootAssembly.instances[instance].cells) == 0:
                del self.a.features[instance]
                
        for part_ in mdb.models[self.model].parts.keys():
            if len(mdb.models[self.model].parts[part_].cells) == 0:
                del mdb.models[self.model].parts[part_]


    def create(self, name, part, **kwargs):
        logger.debug("assembly instance: {}, part: {}".format(name, part.name))
        self.a.DatumCsysByDefault(CARTESIAN)
        
        self.a.Instance(name=name, part=part, **kwargs)

    def boolcut(self, name, **kwargs):
        self.a.features.changeKey(fromName=name, toName="{}-xx".format(name))
        kwargs["instanceToBeCut"] = self.a.instances["{}-xx".format(name)]
        kwargs["name"] = name
        kwargs = convert_abaqus_constants(**kwargs)
        cuttingInstances = (self.a.instances[i] for i in kwargs["cuttingInstances"])
        kwargs["cuttingInstances"] = tuple(cuttingInstances)
        mesh_commands = kwargs.pop("mesh", None)
        
        
        self.a.regenerate()
        for cuttinginstance in kwargs["cuttingInstances"]:
            self.a.features[cuttinginstance.name].resume()
        
        try:
            self.a.InstanceFromBooleanCut(**kwargs)
            self.a.features.changeKey(fromName="{}-1".format(name), toName=name)
        except AbaqusException:
            self.a.features[cuttinginstance.name].suppress()
            self.a.features.changeKey(fromName="{}-xx".format(name), toName=name)
        
        if "{}-xx".format(name) in self.a.features.keys():
            del self.a.features["{}-xx".format(name)]
        
        if name in mdb.models[self.model].parts.keys() and mesh_commands is not None:
            Abml_Mesh(self.model, mdb.models[self.model].parts[name], *mesh_commands)
            
        

    
    def rotate_translate(self, instance, translate=None, rotate=None):
        if rotate is not None:
            if len(rotate) != 0:
                for rot_param in rotate:
                    rot_param = {k.lower(): v for k, v in rot_param.items()}
                    angle = float(rot_param.get("angle"))

                    axisDirection = rot_param.get("axisDirection".lower())
                    axisPoint = rot_param.get("axisPoint".lower())
                    self.a.rotate(
                        angle=angle,
                        axisDirection=axisDirection,
                        axisPoint=axisPoint,
                        instanceList=(instance,),
                    )

        if translate is not None:
            translate = array(translate, dtype=float)
            self.a.instances[instance].translate(vector=translate)

    def instanceFromBooleanCut(self, instance, **kwargs):
        self.a.instances[instance].InstanceFromBooleanCut(**kwargs)
    
class Abml_Assembly_Sets():
    def __init__(self, access, name, **kwargs):
        self.access = access
        self.name = name
        self.kwargs = Counter()
        for instance in access.instances.keys():
            updated = convert_geometry_repository(access.instances[instance], **kwargs)
            updated = {k: v for k, v in updated.items() if v is not None}
            self.kwargs.update(updated)
        self.kwargs = dict(self.kwargs)
        self.create()


    def create(self):
        logger.debug("assembly sets: {} ".format(self.name))
        if "sets" in self.kwargs:
            self.access.SetByBoolean(name=self.name, **self.kwargs)
        else:
            self.access.Set(name=self.name, **self.kwargs)
        

class Abml_Assembly_Surfaces():
    def __init__(self, access, name, **kwargs):
        self.access = access
        self.name = name
        self.regex = kwargs.pop("regex", None)
 
        if self.regex is None and "surfaces" not in kwargs.keys():
            self.kwargs = Counter()
            for instance in access.instances.keys():
                updated = convert_geometry_repository(access.instances[instance], **kwargs)
                updated = {k: v for k, v in updated.items() if v is not None}
                self.kwargs.update(updated)

            self.kwargs = dict(self.kwargs)
        elif "surfaces" in kwargs.keys():
            self.kwargs = {}
            if isinstance(kwargs["surfaces"], list):
                self.kwargs["surfaces"] = [mdb.models[self.access.modelName].rootAssembly.allSurfaces[sname] for sname in kwargs["surfaces"]]
            elif isinstance(kwargs["surfaces"], str):
                self.kwargs["surfaces"] = [mdb.models[self.access.modelName].rootAssembly.allSurfaces[kwargs["surfaces"]]]
        else:
            self.regex_compile = re.compile(self.regex)
            instances = list(filter(self.regex_compile.match, self.access.allSurfaces.keys()))
            if len(instances) == 0:
                raise ValueError("regex: {} does not match any surface in {}".format(self.regex, self.access.allSurfaces.keys()))
            self.kwargs = Counter()
            for instance in instances:
                 updated = {"side1Faces": access.allSurfaces[instance].faces}
                 updated = {k: v for k, v in updated.items() if v is not None}
                 self.kwargs.update(updated)
            self.kwargs = dict(self.kwargs)

        self.create()

    def create(self):
        logger.debug("assembly surface: {} ".format(self.name))

        if "surfaces" in self.kwargs:
            self.access.SurfaceByBoolean(name=self.name, **self.kwargs)
        else:
            self.access.Surface(name=self.name, **self.kwargs)