from abaqus import mdb
from abml.abml_region import Abml_Region
from abml.abml_helpers import convert_abaqus_constants

import logging

class Abml_Load():
    def __init__(self, model, name, **kwargs):
        self.model = model
        self.name = name
        self.type_ = kwargs.pop("type")

        self.kwargs = convert_abaqus_constants(**kwargs)

        self.access = mdb.models[self.model]

        self.load_map = {
            "BodyCharge":self.access.BodyCharge,
            "BodyConcentrationFlux":self.access.BodyConcentrationFlux,
            "BodyCurrent":self.access.BodyCurrent,
            "BodyCurrentDensity":self.access.BodyCurrentDensity,
            "BodyForce":self.access.BodyForce,
            "BodyHeatFlux":self.access.BodyHeatFlux,
            "BoltLoad":self.access.BoltLoad,
            "ConcCharge":self.access.ConcCharge,
            "ConcConcFlux":self.access.ConcConcFlux,
            "ConcCurrent":self.access.ConcCurrent,
            "ConcentratedForce":self.access.ConcentratedForce,
            "ConcentratedHeatFlux":self.access.ConcentratedHeatFlux,
            "ConcPoreFluid":self.access.ConcPoreFluid,
            "ConnectorForce":self.access.ConnectorForce,
            "ConnectorMoment":self.access.ConnectorMoment,
            "CoriolisForce":self.access.CoriolisForce,
            "Gravity":self.access.Gravity,
            "InertiaRelief":self.access.InertiaRelief,
            "InwardVolAccel":self.access.InwardVolAccel,
            "LineLoad":self.access.LineLoad,
            "Moment":self.access.Moment,
            "PEGLoad":self.access.PEGLoad,
            "PipePressure":self.access.PipePressure,
            "Pressure":self.access.Pressure,
            "RotationalBodyForce":self.access.RotationalBodyForce,
            "ShellEdgeLoad":self.access.ShellEdgeLoad,
            "SubmodelSB":self.access.SubmodelSB,
            "SubstructureLoad":self.access.SubstructureLoad,
            "SurfaceCharge":self.access.SurfaceCharge,
            "SurfaceConcentrationFlux":self.access.SurfaceConcentrationFlux,
            "SurfaceCurrent":self.access.SurfaceCurrent,
            "SurfaceCurrentDensity":self.access.SurfaceCurrentDensity,
            "SurfaceHeatFlux":self.access.SurfaceHeatFlux,
            "SurfacePoreFluid":self.access.SurfacePoreFluid,
            "SurfaceTraction":self.access.SurfaceTraction,
        }


        if "region" in self.kwargs:
            if isinstance(self.kwargs["region"], dict):
                # cleanup - remove redundant code
                region = Abml_Region(self.model, self.access.rootAssembly, **self.kwargs["region"])
                region_map = {
                    "Pressure": region.region
                }
                region_map = {k.lower():v for k,v in region_map.items()}
                self.kwargs["region"] = region_map.get(self.type_.lower(), region.region)
            elif isinstance(self.kwargs["region"], str):
                region =  self.access.rootAssembly.surfaces[self.kwargs["region"]]
                self.kwargs["region"] = region
            else:
                raise NotImplemented("input of type {} is not implemented yet".format(type(self.kwargs["region"])))
            
        self.load_map = {k.lower():v for k,v in self.load_map.items()}

        self.create()

    def create(self):
        self.load_map[self.type_.lower()](name=self.name, **self.kwargs)
