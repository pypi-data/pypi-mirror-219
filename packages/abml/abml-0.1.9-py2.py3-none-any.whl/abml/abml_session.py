from abaqus import session, mdb
import odbAccess
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior
from caeModules import *
from abaqusConstants import (
    PNG,
    ON,
    OFF,
    COMPONENT,
    INVARIANT,
    NODAL,
    INTEGRATION_POINT,
    ELEMENT_NODAL,
    POINT_LIST,
    PATH_POINTS,
    UNDEFORMED,
    TRUE_DISTANCE,
)
from abml.abml_helpers import (
    convert_abaqus_constants,
    sort_dict_by_suffix,
    remove_order_indices,
    convert_abaqus_constant,
    cprint,
)
from numpy import array, min, max, mean, empty, savetxt, concatenate, all
from os import path
import logging
import glob
import itertools
from copy import deepcopy


class Abml_Session:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

        self.viewports = self.kwargs.pop("viewports", {})
        self.odbs = self.kwargs.pop("odbs", [])

        if isinstance(self.odbs, str):
            self.odbs = list(glob.glob(self.odbs))

        self.paths = self.kwargs.pop("paths", {})
        self.extractions = self.kwargs.pop("extractions", {})

        self.aggregate_map = {
            "min": min,
            "max": max,
            "mean": mean,
            "envelope": envelope,
        }

        self.create_odbs(*self.odbs)
        self.create_paths(**self.paths)
        self.create_viewports(**self.viewports)
        self.create_extractions(**self.extractions)

    def create_viewports(self, **viewports):
        current = viewports.pop("current", "Viewport: 1")
        for viewport, kwargs in viewports.items():
            Abml_Viewport(name=viewport, **kwargs)
        session.viewports[current].makeCurrent()

    def create_odbs(self, *odbs):
        for name in odbs:
            session.openOdb(name=name)

    def create_paths(self, **paths):
        for path, kwargs in paths.items():
            kwargs = convert_abaqus_constants(**kwargs)
            session.Path(name=path, **kwargs)

    def historyoutput(self, data, odb):
        if isinstance(data["step"], str):
            step = data["step"]
            step_time = odb.steps[step].totalTime + odb.steps[step].timePeriod
        elif isinstance(data["step"], (int, float)):
            step = odb.steps.keys()[data["step"]]
            step_time = (
                odb.steps[odb.steps.keys()[data["step"]]].totalTime
                + odb.steps[odb.steps.keys()[data["step"]]].timePeriod
            )

        outputVariableName_map = {"allse": "Strain energy: ALLSE for Whole Model"}

        xydata = session.XYDataFromHistory(
            name="allse_whole",
            odb=odb,
            outputVariableName=outputVariableName_map[data["outputvariablename"]],
            steps=[step],
            __linkedVpName__="Viewport: 1",
        )

        return array(xydata)[-1, -1]

    def fieldoutput(self, data, odb):
        data["nodesets"] = [k.upper() for k in data["nodesets"]]
        data["outputposition"] = convert_abaqus_constant(data["outputposition"])

        if isinstance(data["step"], str):
            step = odb.steps[data["step"]].number
            step_time = odb.steps[step].totalTime + odb.steps[step].timePeriod
        elif isinstance(data["step"], (int, float)):
            step = data["step"]
            step_time = (
                odb.steps[odb.steps.keys()[data["step"]]].totalTime
                + odb.steps[odb.steps.keys()[data["step"]]].timePeriod
            )

        variable = (
            (
                data["variable"]["fieldoutput"],
                convert_abaqus_constant(data["variable"]["location"]),
                (
                    (
                        convert_abaqus_constant(data["variable"]["type"]),
                        data["variable"]["label"].upper(),
                    ),
                ),
            ),
        )

        avg = data.get("avg", 0)
        if isinstance(avg, bool):
            session.viewports["Viewport: 1"].odbDisplay.basicOptions.setValues(
                averageElementOutput=avg
            )
        elif isinstance(avg, (float, int)):
            session.viewports["Viewport: 1"].odbDisplay.basicOptions.setValues(
                averagingThreshold=avg
            )

        xydatalist = session.xyDataListFromField(
            odb=odb,
            outputPosition=data["outputposition"],
            variable=variable,
            nodeSets=data["nodesets"],
        )
        table_data = concatenate(
            map(get_data, xydatalist, [step_time] * len(xydatalist))
        ).flatten()
        extraction = self.aggregate_map[data["aggregate"]](table_data)

        return extraction

    def path_(self, data, odb):
        aggregate = data.pop("aggregate")
        avg = data.pop("avg", 0)


        if isinstance(avg, bool):
            session.viewports["Viewport: 1"].odbDisplay.basicOptions.setValues(
                averageElementOutput=avg
            )
        elif isinstance(avg, (float, int)):
            session.viewports["Viewport: 1"].odbDisplay.basicOptions.setValues(
                averagingThreshold=avg
            )

        variable = data.pop("variable")

        session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
        variableLabel=variable["fieldoutput"], outputPosition=convert_abaqus_constant(variable["location"]), refinement=(
        convert_abaqus_constant(variable["type"]), variable["label"].upper()))

        if isinstance(data["path"], str):
            data["path"] = session.paths[data["path"]]
        elif isinstance(data["path"], (tuple, list)):
            session.Path(
                name="Path-Extraction", type=POINT_LIST, expression=data["path"]
            )
            data["path"] = session.paths["Path-Extraction"]

        if "step" in data.keys():
            if isinstance(data["step"], str):
                data["step"] = odb.steps[data["step"]].number-1
            elif data["step"] < 0:
                data["step"] = odb.steps[odb.steps.keys()[data["step"]]].number-1

        if "frame" in data.keys():
            if data["frame"] < 0:
                data["frame"] = odb.steps[odb.steps.keys()[data["step"]]].frames[data["frame"]].frameId

        kwargs = {
            "includeIntersections": False,
            "projectOntoMesh": False,
            "pathStyle": PATH_POINTS,
            "labelType": TRUE_DISTANCE,
            "shape": UNDEFORMED,
            "removeDuplicateXYPairs": True,
            "includeAllElements": False,
        }
        kwargs.update(data)
        kwargs = convert_abaqus_constants(**kwargs)

        data = array(session.XYDataFromPath(name="XY-DATA", **kwargs).data, dtype=float)[
            :, -1
        ]

        extraction = self.aggregate_map[aggregate](data)



        return extraction

    def create_extractions(self, **extractions):
        filename = extractions.pop("filename", "extraction.csv")
        df = empty((len(self.odbs), len(extractions) + 1), dtype=object)

        type_map = {
            "fieldoutput": self.fieldoutput,
            "historyoutput": self.historyoutput,
            "path": self.path_,
        }

        for line, odb_name in enumerate(session.odbs.keys()):
            df[line, 0] = odb_name
            odb = session.odbs[odb_name]
            session.viewports["Viewport: 1"].setValues(displayedObject=odb)
            for col, data in enumerate(extractions.values()):
                data = deepcopy(data)
                if data["type"] != "path":
                    data = {k.lower(): v for k, v in data.items()}
                type_ = data.pop("type", "fieldoutput")
                extraction = type_map[type_](data, odb)
                if isinstance(extraction, (int, float)):
                    df[line, col + 1] = extraction

        header = ["odb"]
        header = header + extractions.keys()
        header = ", ".join(header)

        savetxt(
            filename,
            df,
            header=header,
            delimiter=",",
            fmt="%s",
        )


class Abml_Viewport:
    def __init__(self, name, **kwargs):
        self.name = name
        self.commands = kwargs.pop("commands", [])
        self.kwargs = convert_abaqus_constants(**kwargs)
        self.create()

        self.access = session.viewports[self.name]

        self.command_map = {
            "bringToFront": self.access.bringToFront,
            "disableMultipleColors": self.access.disableMultipleColors,
            "disableRefresh": self.access.disableRefresh,
            "disableColorCodeUpdates": self.access.disableColorCodeUpdates,
            "enableMultipleColors": self.access.enableMultipleColors,
            "enableRefresh": self.access.enableRefresh,
            "enableColorCodeUpdates": self.access.enableColorCodeUpdates,
            # "getActiveElementLabels": self.access.getActiveElementLabels,
            # "getActiveNodeLabels": self.access.getActiveNodeLabels,
            # "getPrimVarMinMaxLoc": self.access.getPrimVarMinMaxLoc,
            "makeCurrent": self.access.makeCurrent,
            "maximize": self.access.maximize,
            "minimize": self.access.minimize,
            "offset": self.access.offset,
            "restore": self.access.restore,
            "sendToBack": self.access.sendToBack,
            "setColor": self.access.setColor,
            "forceRefresh": self.access.forceRefresh,
            "setValues": self.access.setValues,
            "addDrawings": self.access.addDrawings,
            "removeDrawings": self.access.removeDrawings,
            "timeDisplay": self.access.timeDisplay,
            "printtofile": self.print_to_file,
        }

        self.command_map = {k.lower(): v for k, v in self.command_map.items()}

        self.call_commands()

    def create(self):
        session.Viewport(name=self.name, **self.kwargs)

    def call_commands(self):
        for command in self.commands:
            type_ = next(iter(command))
            kwargs = convert_abaqus_constants(**command[type_])

            if "displayedObject" in kwargs:
                kwargs["displayedObject"] = convert_displayed_object(
                    kwargs["displayedObject"]
                )

            self.command_map[type_.lower()](**kwargs)

    def print_to_file(self, **kwargs):
        vpDecorations = kwargs.pop("vpDecorations", OFF)
        vpBackground = kwargs.pop("vpBackground", ON)
        compass = kwargs.pop("vpBackground", OFF)
        session.printOptions.setValues(
            vpDecorations=vpDecorations, vpBackground=vpBackground, compass=compass
        )
        kwargs.update({"canvasObjects": (session.viewports[self.name],), "format": PNG})

        session.printToFile(**kwargs)


def convert_displayed_object(dict_):
    model = dict_["model"]
    part = dict_.get("part")
    assembly = dict_.get("assembly")

    if part is not None:
        return mdb.models[model].parts[part]
    elif assembly is not None:
        return mdb.models[model].rootAssembly


def get_data(data, step_time):
    extract = array(data.data, dtype=float)
    mask = extract[:, 0] == step_time
    return extract[mask, -1]


def envelope(data):
    if all(data >= 0):
        return max(data)
    elif all(data < 0):
        return min(data)
    else:
        raise ValueError("Array contains both positive and negative values.")
