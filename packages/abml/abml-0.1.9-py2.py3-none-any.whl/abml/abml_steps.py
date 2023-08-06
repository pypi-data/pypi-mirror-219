from abaqus import mdb
from abml.abml_helpers import convert_abaqus_constants
import logging

logger = logging.getLogger(__name__)


class Abml_Step:
    def __init__(self, model, name, **kwargs):
        self.model = model
        self.name = name
        self.kwargs = convert_abaqus_constants(**kwargs)

        self.step_map = {
            "AnnealStep": mdb.models[self.model].AnnealStep,
            "BuckleStep": mdb.models[self.model].BuckleStep,
            "ComplexFrequencyStep": mdb.models[self.model].ComplexFrequencyStep,
            "CoupledTempDisplacementStep": mdb.models[self.model].CoupledTempDisplacementStep,
            "CoupledThermalElectricalStructuralStep": mdb.models[self.model].CoupledThermalElectricalStructuralStep,
            "CoupledThermalElectricStep": mdb.models[self.model].CoupledThermalElectricStep,
            "DirectCyclicStep": mdb.models[self.model].DirectCyclicStep,
            "EmagTimeHarmonicStep": mdb.models[self.model].EmagTimeHarmonicStep,
            "ExplicitDynamicsStep": mdb.models[self.model].ExplicitDynamicsStep,
            "FrequencyStep": mdb.models[self.model].FrequencyStep,
            "GeostaticStep": mdb.models[self.model].GeostaticStep,
            "HeatTransferStep": mdb.models[self.model].HeatTransferStep,
            "ImplicitDynamicsStep": mdb.models[self.model].ImplicitDynamicsStep,
            "MassDiffusionStep": mdb.models[self.model].MassDiffusionStep,
            "ModalDynamicsStep": mdb.models[self.model].ModalDynamicsStep,
            "RandomResponseStep": mdb.models[self.model].RandomResponseStep,
            "ResponseSpectrumStep": mdb.models[self.model].ResponseSpectrumStep,
            "SoilsStep": mdb.models[self.model].SoilsStep,
            "StaticLinearPerturbationStep": mdb.models[self.model].StaticLinearPerturbationStep,
            "StaticRiksStep": mdb.models[self.model].StaticRiksStep,
            "StaticStep": mdb.models[self.model].StaticStep,
            "SteadyStateDirectStep": mdb.models[self.model].SteadyStateDirectStep,
            "SteadyStateModalStep": mdb.models[self.model].SteadyStateModalStep,
            "SteadyStateSubspaceStep": mdb.models[self.model].SteadyStateSubspaceStep,
            "SubspaceDynamicsStep": mdb.models[self.model].SubspaceDynamicsStep,
            "SubstructureGenerateStep": mdb.models[self.model].SubstructureGenerateStep,
            "TempDisplacementDynamicsStep": mdb.models[self.model].TempDisplacementDynamicsStep,
            "ViscoStep": mdb.models[self.model].ViscoStep,
        }

        self.step_map = {k.lower(): v for k, v in self.step_map.items()}

        self.create()

    def create(self):
        type_ = next(iter(self.kwargs))
        self.step_map[type_.lower()](name=self.name, **self.kwargs[type_])
        # mdb.models[self.model].fieldOutputRequests['F-Output-1'].setValues(variables=('S', 
        # 'PE', 'PEEQ', 'PEMAG', 'LE', 'U', 'RF', 'CF', 'CSTRESS', 'CDISP', 
        # 'COORD'))
