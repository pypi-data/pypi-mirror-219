from abaqus import mdb
from abml.abml_helpers import convert_abaqus_constants, convert_geometry_repository, convert_region
import interaction

from abml.abml_logger import Logger

logger = Logger().get_logger(__name__)

class Abml_Constraint():
    def __init__(self, model, name, **kwargs):
        self.model = model
        self.name = name
        self.type_ = kwargs.pop("type")

        self.kwargs = convert_abaqus_constants(**kwargs)
        self.access = mdb.models[self.model]

        self.constraint_map = {
            "EmbeddedRegion": self.access.EmbeddedRegion,
            "Equation": self.access.Equation,
            "MultipointConstraint": self.access.MultipointConstraint,
            "RigidBody": self.access.RigidBody,
            "ShellSolidCoupling": self.access.ShellSolidCoupling,
            "Tie": self.access.Tie,
        }

        self.constraint_map = {k.lower():v for k,v in self.constraint_map.items()}

        self.create()

    def create(self):
        a = mdb.models[self.model].rootAssembly
        self.kwargs = convert_region(access=a, keys=["surface", "master", "slave"], **self.kwargs)
        logger.debug("constraint: {} type: {}".format(self.name, self.type_))
        self.constraint_map[self.type_.lower()](name=self.name, **self.kwargs)




