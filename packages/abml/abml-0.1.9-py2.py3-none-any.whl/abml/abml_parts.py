from abaqus import mdb
import logging
from abml.abml_helpers import (
    convert_abaqus_constants,
    convert_abaqus_constant,
    convert_geometry_repository,
    cprint,
    # convert_geometry_repository,
    sort_dict_by_suffix
)
from abml.abml_logger import Logger

from regionToolset import Region
from part import PartType
from mesh import ElemType
import sys

logger = Logger().get_logger(__name__)

class Abml_Part:
    def __init__(self, model, name, **kwargs):
        self.model = model
        self.name = name

        kwargs = {k.lower(): v for k, v in kwargs.items()}

        self.features = kwargs.get("features", [])
        self.sets = kwargs.get("sets", [])
        self.surfaces = kwargs.get("surfaces", [])
        self.sectionAssignments = kwargs.get("sectionAssignments".lower(), [])
        self.mesh = kwargs.get("mesh".lower(), [])

        self.kwargs = convert_abaqus_constants(**kwargs)

        self.dimensionality = convert_abaqus_constant(
            self.kwargs.get("dimensionality", "THREE_D")
        )
        self.type = convert_abaqus_constant(self.kwargs.get("type", "DEFORMABLE_BODY"))
        self.twist = convert_abaqus_constant(self.kwargs.get("twist", "OFF"))

        if self.name not in mdb.models[self.model].parts.keys():
            self.create()
            
        self.create_features()
        self.create_sets()
        self.create_surfaces()
        self.create_section_assignments()
        self.create_mesh()

    def create(self):
        mdb.models[self.model].Part(
            self.name, self.dimensionality, self.type, self.twist
        )

    def create_features(self):
        p = mdb.models[self.model].parts[self.name]
        for feature_name in sort_dict_by_suffix(self.features):
            Abml_Feature(
                model=self.model,
                access=p,
                name=feature_name,
                **self.features[feature_name]
            )

    def create_sets(self):
        for set_ in self.sets:
            
            Abml_Sets(mdb.models[self.model].parts[self.name], set_, **self.sets[set_])

    def create_surfaces(self):
        for surface in self.surfaces:
            Abml_Surfaces(
                mdb.models[self.model].parts[self.name],
                surface,
                **self.surfaces[surface]
            )

    def create_mesh(self):
        p = mdb.models[self.model].parts[self.name]
        Abml_Mesh(self.model, p, *self.mesh)

    def create_section_assignments(self):
        for section in self.sectionAssignments:
            section_name = next(iter(section))
            p = mdb.models[self.model].parts[self.name]

            if "sets" in section[section_name]:
                sets = section[section_name].pop("sets")
                for set_ in sets:
                    try:
                        region += p.sets[set_]
                    except UnboundLocalError:
                        region = p.sets[set_]
                kwargs = {"region": region}
            else:
                kwargs = {
                    "region": Region(
                        **convert_geometry_repository(access=p, **section[section_name])
                    )
                }

            p.SectionAssignment(sectionName=section_name, **kwargs)


class Abml_Mesh:
    def __init__(self, model, access, *commands):
        self.model = model
        self.access = access
        self.commands = commands
        
        self.command_map = {
            "assignStackDirection": self.access.assignStackDirection,
            "associateMeshWithGeometry": self.access.associateMeshWithGeometry,
            "createVirtualTopology": self.access.createVirtualTopology,
            "deleteBoundaryLayerControls": self.access.deleteBoundaryLayerControls,
            "deleteMesh": self.access.deleteMesh,
            "deleteMeshAssociationWithGeometry": self.access.deleteMeshAssociationWithGeometry,
            "deletePreviewMesh": self.access.deletePreviewMesh,
            "deleteSeeds": self.access.deleteSeeds,
            "generateMesh": self.access.generateMesh,
            "generateBottomUpExtrudedMesh": self.access.generateBottomUpExtrudedMesh,
            "generateBottomUpSweptMesh": self.access.generateBottomUpSweptMesh,
            "generateBottomUpRevolvedMesh": self.access.generateBottomUpRevolvedMesh,
            "getEdgeSeeds": self.access.getEdgeSeeds,
            "getElementType": self.access.getElementType,
            "getIncompatibleMeshInterfaces": self.access.getIncompatibleMeshInterfaces,
            "getMeshControl": self.access.getMeshControl,
            "getMeshStats": self.access.getMeshStats,
            "getPartSeeds": self.access.getPartSeeds,
            "getUnmeshedRegions": self.access.getUnmeshedRegions,
            "ignoreEntity": self.access.ignoreEntity,
            "restoreIgnoredEntity": self.access.restoreIgnoredEntity,
            "seedEdgeByBias": self.access.seedEdgeByBias,
            "seedEdgeByNumber": self.access.seedEdgeByNumber,
            "seedEdgeBySize": self.access.seedEdgeBySize,
            "seedPart": self.access.seedPart,
            "setBoundaryLayerControls": self.access.setBoundaryLayerControls,
            "setElementType": self.setElementType,
            "setLogicalCorners": self.access.setLogicalCorners,
            "setMeshControls": self.access.setMeshControls,
            "setSweepPath": self.access.setSweepPath,
            "verifyMeshQuality": self.access.verifyMeshQuality,
        }

        self.command_map = {k.lower():v for k,v in self.command_map.items()}

        self.create()

    def setElementType(self,**kwargs):
        if "regions" in kwargs:
            kwargs["regions"] = Region(**convert_geometry_repository(self.access, **kwargs["regions"]))
        if "elemTypes" in kwargs:
            types = []
            for element_type in kwargs["elemTypes"]:
                element_type = convert_abaqus_constants(**element_type)
                types.append(ElemType(**element_type))
            kwargs["elemTypes"] = types
        self.access.setElementType(**kwargs)

    def create(self):
        for command in self.commands:
            type_ = next(iter(command))
            command[type_].update(convert_geometry_repository(self.access, **command[type_]))
            
            logger.debug("part:{} command:{}".format(self.access.name, command))
            self.command_map[type_.lower()](**command[type_])
        self.access.generateMesh()


class Abml_Feature:
    def __init__(self, model, name, access, **data):
        self.model = model
        self.name = name
        self.type = data.pop("type")
        self.data = data

        self.access = access

        self.feature_map = {
            "AttachmentPoints": self.access.AttachmentPoints,
            "AttachmentPointsAlongDirection": self.access.AttachmentPointsAlongDirection,
            "AttachmentPointsOffsetFromEdges": self.access.AttachmentPointsOffsetFromEdges,
            "DatumAxisByCylFace": self.access.DatumAxisByCylFace,
            "DatumAxisByNormalToPlane": self.access.DatumAxisByNormalToPlane,
            "DatumAxisByParToEdge": self.access.DatumAxisByParToEdge,
            "DatumAxisByPrincipalAxis": self.access.DatumAxisByPrincipalAxis,
            "DatumAxisByRotation": self.access.DatumAxisByRotation,
            "DatumAxisByThreePoint": self.access.DatumAxisByThreePoint,
            "DatumAxisByThruEdge": self.access.DatumAxisByThruEdge,
            "DatumAxisByTwoPlane": self.access.DatumAxisByTwoPlane,
            "DatumAxisByTwoPoint": self.access.DatumAxisByTwoPoint,
            "DatumCsysByDefault": self.access.DatumCsysByDefault,
            "DatumCsysByOffset": self.access.DatumCsysByOffset,
            "DatumCsysByThreePoints": self.access.DatumCsysByThreePoints,
            "DatumCsysByTwoLines": self.access.DatumCsysByTwoLines,
            "DatumPlaneByPrincipalPlane": self.access.DatumPlaneByPrincipalPlane,
            "DatumPlaneByOffset": self.access.DatumPlaneByOffset,
            "DatumPlaneByRotation": self.access.DatumPlaneByRotation,
            "DatumPlaneByThreePoints": self.access.DatumPlaneByThreePoints,
            "DatumPlaneByLinePoint": self.access.DatumPlaneByLinePoint,
            "DatumPlaneByPointNormal": self.access.DatumPlaneByPointNormal,
            "DatumPlaneByTwoPoint": self.access.DatumPlaneByTwoPoint,
            "DatumPointByCoordinate": self.access.DatumPointByCoordinate,
            "DatumPointByOffset": self.access.DatumPointByOffset,
            "DatumPointByMidPoint": self.access.DatumPointByMidPoint,
            "DatumPointByOnFace": self.access.DatumPointByOnFace,
            "DatumPointByEdgeParam": self.access.DatumPointByEdgeParam,
            "DatumPointByProjOnEdge": self.access.DatumPointByProjOnEdge,
            "DatumPointByProjOnFace": self.access.DatumPointByProjOnFace,
            "MakeSketchTransform": self.access.MakeSketchTransform,
            "PartitionCellByDatumPlane": self.access.PartitionCellByDatumPlane,
            "PartitionCellByExtendFace": self.access.PartitionCellByExtendFace,
            "PartitionCellByExtrudeEdge": self.access.PartitionCellByExtrudeEdge,
            "PartitionCellByPatchNCorners": self.access.PartitionCellByPatchNCorners,
            "PartitionCellByPatchNEdges": self.access.PartitionCellByPatchNEdges,
            "PartitionCellByPlaneNormalToEdge": self.access.PartitionCellByPlaneNormalToEdge,
            "PartitionCellByPlanePointNormal": self.access.PartitionCellByPlanePointNormal,
            "PartitionCellByPlaneThreePoints": self.access.PartitionCellByPlaneThreePoints,
            "PartitionCellBySweepEdge": self.access.PartitionCellBySweepEdge,
            "PartitionEdgeByDatumPlane": self.access.PartitionEdgeByDatumPlane,
            "PartitionEdgeByParam": self.access.PartitionEdgeByParam,
            "PartitionEdgeByPoint": self.access.PartitionEdgeByPoint,
            "PartitionFaceByAuto": self.access.PartitionFaceByAuto,
            "PartitionFaceByCurvedPathEdgeParams": self.access.PartitionFaceByCurvedPathEdgeParams,
            "PartitionFaceByCurvedPathEdgePoints": self.access.PartitionFaceByCurvedPathEdgePoints,
            "PartitionFaceByDatumPlane": self.access.PartitionFaceByDatumPlane,
            "PartitionFaceByExtendFace": self.access.PartitionFaceByExtendFace,
            "PartitionFaceByIntersectFace": self.access.PartitionFaceByIntersectFace,
            "PartitionFaceByProjectingEdges": self.access.PartitionFaceByProjectingEdges,
            "PartitionFaceByShortestPath": self.access.PartitionFaceByShortestPath,
            "PartitionFaceBySketch": self.access.PartitionFaceBySketch,
            "PartitionFaceBySketchDistance": self.access.PartitionFaceBySketchDistance,
            "PartitionFaceBySketchRefPoint": self.access.PartitionFaceBySketchRefPoint,
            "PartitionFaceBySketchThruAll": self.access.PartitionFaceBySketchThruAll,
        }

        if isinstance(access, PartType):
            self.feature_map.update(
                {
                    "AnalyticRigidSurf2DPlanar": self.access.AnalyticRigidSurf2DPlanar,
                    "AnalyticRigidSurfExtrude": self.access.AnalyticRigidSurfExtrude,
                    "AnalyticRigidSurfRevolve": self.access.AnalyticRigidSurfRevolve,
                    "BaseSolidExtrude": self.access.BaseSolidExtrude,
                    "BaseSolidRevolve": self.access.BaseSolidRevolve,
                    "BaseSolidSweep": self.access.BaseSolidSweep,
                    "BaseShell": self.access.BaseShell,
                    "BaseShellExtrude": self.access.BaseShellExtrude,
                    "BaseShellRevolve": self.access.BaseShellRevolve,
                    "BaseShellSweep": self.access.BaseShellSweep,
                    "BaseWire": self.access.BaseWire,
                    "Chamfer": self.access.Chamfer,
                    "Mirror": self.access.Mirror,
                    "Cut": self.access.Cut,
                    "CutExtrude": self.access.CutExtrude,
                    "CutLoft": self.access.CutLoft,
                    "CutRevolve": self.access.CutRevolve,
                    "CutSweep": self.access.CutSweep,
                    "FaceFromElementFaces": self.access.FaceFromElementFaces,
                    "HoleBlindFromEdges": self.access.HoleBlindFromEdges,
                    "HoleFromEdges": self.access.HoleFromEdges,
                    "HoleThruAllFromEdges": self.access.HoleThruAllFromEdges,
                    "Round": self.access.Round,
                    "Shell": self.access.Shell,
                    "ShellExtrude": self.access.ShellExtrude,
                    "ShellLoft": self.access.ShellLoft,
                    "ShellRevolve": self.access.ShellRevolve,
                    "ShellSweep": self.access.ShellSweep,
                    "SolidExtrude": self.access.SolidExtrude,
                    "SolidLoft": self.access.SolidLoft,
                    "SolidRevolve": self.access.SolidRevolve,
                    "SolidSweep": self.access.SolidSweep,
                    "Wire": self.access.Wire,
                    "WireSpline": self.access.WireSpline,
                    "WirePolyLine": self.access.WirePolyLine,
                    "WireFromEdge": self.access.WireFromEdge,
                }
            )

        self.standard_key_map = {
            "AnalyticRigidSurf2DPlanar": "",
            "AnalyticRigidSurfExtrude": "",
            "AnalyticRigidSurfRevolve": "",
            "BaseSolidExtrude": "Solid extrude-1",
            "BaseSolidRevolve": "Solid revolve-1",
            "BaseSolidSweep": "Solid sweep-1",
            "BaseShell": "",
            "BaseShellExtrude": "Shell extrude-1",
            "BaseShellRevolve": "Shell revolve-1",
            "BaseShellSweep": "Shell sweep-1",
            "BaseWire": "",
            "Chamfer": "",
            "Mirror": "",
            "Cut": "",
            "CutExtrude": "",
            "CutLoft": "",
            "CutRevolve": "",
            "CutSweep": "",
            "FaceFromElementFaces": "",
            "HoleBlindFromEdges": "",
            "HoleFromEdges": "",
            "HoleThruAllFromEdges": "",
            "Round": "",
            "Shell": "",
            "ShellExtrude": "",
            "ShellLoft": "",
            "ShellRevolve": "",
            "ShellSweep": "",
            "SolidExtrude": "",
            "SolidLoft": "",
            "SolidRevolve": "",
            "SolidSweep": "",
            "Wire": "",
            "WireSpline": "",
            "WirePolyLine": "",
            "WireFromEdge": "",
            "DatumPlaneByPrincipalPlane": "Datum plane-1",
            "DatumCsysByOffset": "Datum csys-1",
            "DatumAxisByCylFace": "Datum axis-1",
            "DatumPointByCoordinate": "Datum pt-1",
            "PartitionFaceByDatumPlane": "Partition face-1",
            "PartitionCellByDatumPlane": "Partition cell-1",
        }

        self.feature_map = {k.lower(): v for k, v in self.feature_map.items()}
        self.standard_key_map = {k.lower(): v for k, v in self.standard_key_map.items()}

        self.create()

    def create(self):
        if "sketch" in self.data:
            self.data["sketch"] = mdb.models[self.model].sketches[self.data["sketch"]]
        if "datumPlane" in self.data:
            id_ = self.access.features[self.data["datumPlane"]].id
            self.data["datumPlane"] = self.access.datums[id_]
            
        self.data = convert_geometry_repository(access=self.access, **self.data)

        logger.debug("part:{} feature:{}".format(self.access.name, self.name))

        if self.type.lower() != "PartitionCellByDatumPlane".lower():
            self.feature_map[self.type.lower()](**convert_abaqus_constants(**self.data))
            self.access.features.changeKey(
                fromName=self.standard_key_map[self.type.lower()], toName=self.name
            )
        else:
            try:
                self.feature_map[self.type.lower()](**convert_abaqus_constants(**self.data))
                self.access.features.changeKey(
                    fromName=self.standard_key_map[self.type.lower()], toName=self.name
                )
            except Exception:
                pass

   


class Abml_Sets:
    def __init__(self, access, name, **kwargs):
        self.access = access
        self.name = name

        self.kwargs = convert_abaqus_constants(**kwargs)
        self.kwargs = convert_geometry_repository(access, **kwargs)
        self.create()

    def create(self):
        logger.debug("set:{}".format(self.name))
        self.access.Set(name=self.name, **self.kwargs)


class Abml_Surfaces:
    def __init__(self, access, name, **kwargs):
        self.access = access
        self.name = name
        self.kwargs = convert_abaqus_constants(**kwargs)
        logger.debug(self.kwargs)
        self.kwargs = convert_geometry_repository(access, **kwargs)

        self.create()

    def create(self):
        logger.debug("part:{} surface:{}".format(self.access.name, self.name))
        logger.debug(self.kwargs)
        self.access.Surface(name=self.name, **self.kwargs)
