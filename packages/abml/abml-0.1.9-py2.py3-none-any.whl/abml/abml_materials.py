from abaqus import mdb
import logging
from abml.abml_helpers import convert_abaqus_constants, cprint, reduce_dimensions

logger = logging.getLogger("test_materials")


class Abml_Material:
    def __init__(self, name, model, members, description=""):
        self.name = name
        self.model = model
        self.members = members
        self.description = description

        self.create_material()
        self.create_members()

    def create_material(self):
        mdb.models[self.model].Material(name=self.name, description=self.description)

    def create_members(self):
        for member in self.members:
            Abml_Material_Member(self.model, self.name,member, **self.members[member])


class Abml_Material_Member:

    def __init__(self, model, material, member,**kwargs):
        self.model = model
        self.material = material
        self.member = member
        self.kwargs = convert_abaqus_constants(**kwargs)
        mdb_mat = mdb.models[self.model].materials[self.material]

        self.member_map = {
            "AcousticMedium": mdb_mat.AcousticMedium,
            "BrittleCracking": mdb_mat.BrittleCracking,
            "CapPlasticity": mdb_mat.CapPlasticity,
            "CastIronPlasticity": mdb_mat.CastIronPlasticity,
            "ClayPlasticity": mdb_mat.ClayPlasticity,
            "Concrete": mdb_mat.Concrete,
            "ConcreteDamagedPlasticity": mdb_mat.ConcreteDamagedPlasticity,
            "Conductivity": mdb_mat.Conductivity,
            "Creep": mdb_mat.Creep,
            "CrushableFoam": mdb_mat.CrushableFoam,
            "Damping": mdb_mat.Damping,
            "DeformationPlasticity": mdb_mat.DeformationPlasticity,
            "Density": mdb_mat.Density,
            "Depvar": mdb_mat.Depvar,
            "Dielectric": mdb_mat.Dielectric,
            "Diffusivity": mdb_mat.Diffusivity,
            "DruckerPrager": mdb_mat.DruckerPrager,
            "DuctileDamageInitiation": mdb_mat.DuctileDamageInitiation,
            "Elastic": mdb_mat.Elastic,
            "ElectricalConductivity": mdb_mat.ElectricalConductivity,
            "Eos": mdb_mat.Eos,
            "Expansion": mdb_mat.Expansion,
            "FldDamageInitiation": mdb_mat.FldDamageInitiation,
            "FlsdDamageInitiation": mdb_mat.FlsdDamageInitiation,
            "FluidLeakoff": mdb_mat.FluidLeakoff,
            "GapFlow": mdb_mat.GapFlow,
            "GasketMembraneElastic": mdb_mat.GasketMembraneElastic,
            "GasketThicknessBehavior": mdb_mat.GasketThicknessBehavior,
            "GasketTransverseShearElastic": mdb_mat.GasketTransverseShearElastic,
            "Gel": mdb_mat.Gel,
            "HashinDamageInitiation": mdb_mat.HashinDamageInitiation,
            "HeatGeneration": mdb_mat.HeatGeneration,
            "Hyperelastic": mdb_mat.Hyperelastic,
            "Hyperfoam": mdb_mat.Hyperfoam,
            "Hypoelastic": mdb_mat.Hypoelastic,
            "InelasticHeatFraction": mdb_mat.InelasticHeatFraction,
            "JohnsonCookDamageInitiation": mdb_mat.JohnsonCookDamageInitiation,
            "JouleHeatFraction": mdb_mat.JouleHeatFraction,
            "LatentHeat": mdb_mat.LatentHeat,
            "LowDensityFoam": mdb_mat.LowDensityFoam,
            "MagneticPermeability": mdb_mat.MagneticPermeability,
            "MaxeDamageInitiation": mdb_mat.MaxeDamageInitiation,
            "MaxpeDamageInitiation": mdb_mat.MaxpeDamageInitiation,
            "MaxpsDamageInitiation": mdb_mat.MaxpsDamageInitiation,
            "MaxsDamageInitiation": mdb_mat.MaxsDamageInitiation,
            "MeanFieldHomogenization": mdb_mat.MeanFieldHomogenization,
            "MkDamageInitiation": mdb_mat.MkDamageInitiation,
            "MohrCoulombPlasticity": mdb_mat.MohrCoulombPlasticity,
            "MoistureSwelling": mdb_mat.MoistureSwelling,
            "MsfldDamageInitiation": mdb_mat.MsfldDamageInitiation,
            "MullinsEffect": mdb_mat.MullinsEffect,
            "Permeability": mdb_mat.Permeability,
            "Piezoelectric": mdb_mat.Piezoelectric,
            "Plastic": mdb_mat.Plastic,
            "PoreFluidExpansion": mdb_mat.PoreFluidExpansion,
            "PorousBulkModuli": mdb_mat.PorousBulkModuli,
            "PorousElastic": mdb_mat.PorousElastic,
            "PorousMetalPlasticity": mdb_mat.PorousMetalPlasticity,
            "QuadeDamageInitiation": mdb_mat.QuadeDamageInitiation,
            "QuadsDamageInitiation": mdb_mat.QuadsDamageInitiation,
            "Regularization": mdb_mat.Regularization,
            "ShearDamageInitiation": mdb_mat.ShearDamageInitiation,
            "SoftRockPlasticity": mdb_mat.SoftRockPlasticity,
            "Solubility": mdb_mat.Solubility,
            "Sorption": mdb_mat.Sorption,
            "SpecificHeat": mdb_mat.SpecificHeat,
            "SuperElasticity": mdb_mat.SuperElasticity,
            "Swelling": mdb_mat.Swelling,
            "UserDefinedField": mdb_mat.UserDefinedField,
            "UserMaterial": mdb_mat.UserMaterial,
            "UserOutputVariables": mdb_mat.UserOutputVariables,
            "Viscoelastic": mdb_mat.Viscoelastic,
            "Viscosity": mdb_mat.Viscosity,
            "Viscous": mdb_mat.Viscous,
        }
        self.member_map = {k.lower(): v for k, v in self.member_map.items()}

        self.create()

    def create(self):
        capehardening = None
        if "CapPlasticity".lower() == self.member.lower():
            if "CapHardening" in self.kwargs.keys():
                capehardening = convert_abaqus_constants(**self.kwargs.pop("CapHardening"))

        self.member_map[self.member.lower()](**self.kwargs)

        if capehardening is not None:
            capehardening["table"] = reduce_dimensions(capehardening["table"])
            mdb.models[self.model].materials[self.material].capPlasticity.CapHardening(**capehardening)
