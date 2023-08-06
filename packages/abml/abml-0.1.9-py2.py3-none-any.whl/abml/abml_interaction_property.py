from abaqus import mdb
from abml.abml_helpers import convert_abaqus_constants, cprint
import logging

logger = logging.getLogger(__name__)

class Abml_Interaction_Property():
    def __init__(self, model, name, **kwargs):
        self.model = model
        self.name = name

        self.kwargs = kwargs

        self.prop_map = {
            "contact": Abml_Contact_Property
        }

        self.create()

    def create(self):
        type_ = next(iter(self.kwargs))
        self.prop_map[type_](model=self.model, name=self.name, **self.kwargs[type_])

class Abml_Contact_Property():
    def __init__(self, model,name, **kwargs):
        self.model = model
        self.name = name
        self.kwargs = kwargs


        self.create()

        self.access = mdb.models[self.model].interactionProperties[self.name]
        self.behavior_map = {
                        "TangentialBehavior":  self.access.TangentialBehavior,
                        "NormalBehavior":self.access.NormalBehavior,
                        "Damping":self.access.Damping,
                        "Damage":self.access.Damage,
                        "FractureCriterion":self.access.FractureCriterion,
                        "CohesiveBehavior":self.access.CohesiveBehavior,
                        "ThermalConductance":self.access.ThermalConductance,
                        "HeatGeneration":self.access.HeatGeneration,
                        "Radiation":self.access.Radiation,
                        "GeometricProperties":self.access.GeometricProperties,
                        "ElectricalConductance":self.access.ElectricalConductance,
        }

        self.behavior_map = {k.lower():v for k,v in self.behavior_map.items()}

        self.create_behaviors()
    
    def create(self):
        mdb.models[self.model].ContactProperty(self.name)
    
    def create_behaviors(self):
        for type_, data in self.kwargs.items():
            if "table" in data:
                data["table"] = tuple(data["table"])
            self.behavior_map[type_.lower()](**convert_abaqus_constants(**data))
            

