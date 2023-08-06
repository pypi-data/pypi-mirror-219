from abaqus import mdb
import logging
from abml.abml_helpers import convert_abaqus_constants

logger = logging.getLogger(__name__)

class Abml_Section:
    def __init__(self, model, type,**kwargs):  # noqa
        self.model = model
        self.type = type
        self.kwargs = convert_abaqus_constants(**kwargs)
        self.map = {}

        mdb_model = mdb.models[self.model]

        self.section_map = {
            "acousticInfiniteSection": mdb_model.AcousticInfiniteSection,
            "acousticInterfaceSection": mdb_model.AcousticInterfaceSection,
            "beamSection": mdb_model.BeamSection,
            "cohesiveSection": mdb_model.CohesiveSection,
            "compositeShellSection": mdb_model.CompositeShellSection,
            "compositeSolidSection": mdb_model.CompositeSolidSection,
            "connectorSection": mdb_model.ConnectorSection,
            "eulerianSection": mdb_model.EulerianSection,
            "gasketSection": mdb_model.GasketSection,
            "generalStiffnessSection": mdb_model.GeneralStiffnessSection,
            "homogeneousShellSection": mdb_model.HomogeneousShellSection,
            "homogeneousSolidSection": mdb_model.HomogeneousSolidSection,
            "membraneSection": mdb_model.MembraneSection,
            "mPCSection": mdb_model.MPCSection,
            "pEGSection": mdb_model.PEGSection,
        }
        self.section_map = {k.lower(): v for k, v in self.section_map.items()}

        self.create()

    def create(self):
        self.section_map[self.type.lower()](**self.kwargs)

