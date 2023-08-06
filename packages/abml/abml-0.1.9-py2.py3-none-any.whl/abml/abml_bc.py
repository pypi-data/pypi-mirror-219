from abaqus import mdb#
from abml.abml_helpers import convert_abaqus_constants, convert_region
from abml.abml_region import Abml_Region
import logging

class Abml_Bc():
    def __init__(self, model, name, **kwargs):
        self.model = model
        self.name = name
        self.type_ = kwargs.pop("type")
        self.kwargs = convert_abaqus_constants(**kwargs)

        self.access = mdb.models[self.model]

        if "region" in self.kwargs.keys():
            if isinstance(self.kwargs["region"], str):
                self.kwargs["region"] = mdb.models[self.model].rootAssembly.allSets[self.kwargs["region"]]
            else:
                self.kwargs["region"] = Abml_Region(model=self.model, access=self.access.rootAssembly, **self.kwargs["region"]).region

        self.bc_map = {
            "EncastreBC":self.access.EncastreBC,
            "PinnedBC":self.access.PinnedBC,
            "XsymmBC":self.access.XsymmBC,
            "YsymmBC":self.access.YsymmBC,
            "ZsymmBC":self.access.ZsymmBC,
            "XasymmBC":self.access.XasymmBC,
            "YasymmBC":self.access.YasymmBC,
            "ZasymmBC":self.access.ZasymmBC,
            "AccelerationBaseMotionBC":self.access.AccelerationBaseMotionBC,
            "AccelerationBC":self.access.AccelerationBC,
            "AcousticPressureBC":self.access.AcousticPressureBC,
            "ConcentrationBC":self.access.ConcentrationBC,
            "ConnAccelerationBC":self.access.ConnAccelerationBC,
            "ConnDisplacementBC":self.access.ConnDisplacementBC,
            "ConnVelocityBC":self.access.ConnVelocityBC,
            "DisplacementBaseMotionBC":self.access.DisplacementBaseMotionBC,
            "DisplacementBC":self.access.DisplacementBC,
            "ElectricPotentialBC":self.access.ElectricPotentialBC,
            "EulerianBC":self.access.EulerianBC,
            "EulerianMotionBC":self.access.EulerianMotionBC,
            "FluidCavityPressureBC":self.access.FluidCavityPressureBC,
            "MagneticVectorPotentialBC":self.access.MagneticVectorPotentialBC,
            "MaterialFlowBC":self.access.MaterialFlowBC,
            "PorePressureBC":self.access.PorePressureBC,
            "RetainedNodalDofsBC":self.access.RetainedNodalDofsBC,
            "SecondaryBaseBC":self.access.SecondaryBaseBC,
            "SubmodelBC":self.access.SubmodelBC,
            "TemperatureBC":self.access.TemperatureBC,
            "VelocityBaseMotionBC":self.access.VelocityBaseMotionBC,
            "VelocityBC":self.access.VelocityBC,
        }

        self.create()
    
    def create(self):
        self.bc_map[self.type_](name=self.name, **self.kwargs)