from abaqus import mdb
from abml.abml_helpers import convert_geometry_repository
from regionToolset import Region
from assembly import AssemblyType
from part import PartType
from collections import Counter
import logging
import assembly

logger = logging.getLogger(__name__)

class Abml_Region:
    def __init__(self, model, access, **kwargs):
        self.model = model
        self.access = access
        
        if isinstance(access, AssemblyType):
            self.kwargs = Counter()
            mdb.models[self.model].rootAssembly.regenerate()
            for instance in self.access.instances.keys():
                updated = convert_geometry_repository(access.instances[instance], **kwargs)
                updated = {k: v for k, v in updated.items() if v is not None}

                self.kwargs.update(updated)

        elif isinstance(access, PartType):
            self.kwargs = convert_geometry_repository(access, **kwargs)
        else:
            raise TypeError("access is no Part Instance or rootAssembly")
        self.region = Region(**self.kwargs)

    @property
    def faces(self):
        return self.region.faces

    @property
    def elements(self):
        return self.region.elements

    @property
    def nodes(self):
        return self.region.nodes

    @property
    def vertices(self):
        return self.region.vertices

    @property
    def edges(self):
        return self.region.edges

    @property
    def cells(self):
        return self.region.cells
    
    @property
    def side1Faces(self):
        return self.region.side1Faces

    @property
    def referencePoints(self):
        return self.region.referencePoints

    @property
    def xVertices(self):
        return self.region.xVertices

    @property
    def xEdges(self):
        return self.region.xEdges

    @property
    def xVertices(self):
        return self.region.xVertices

    @property
    def xFaces(self):
        return self.region.xFaces

    @property
    def skinFaces(self):
        return self.region.skinFaces

    @property
    def skinEdges(self):
        return self.region.skinEdges

    @property
    def stringerEdges(self):
        return self.region.stringerEdges
