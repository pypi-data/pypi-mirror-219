from abaqus import mdb
from abaqusConstants import CLOCKWISE, COUNTERCLOCKWISE
from numpy import array, issubdtype, number
from abml.abml_helpers import cprint

class Abml_Sketch:
    def __init__(self, name, model_name, cmds):
        self.name = name
        self.model_name = model_name
        self.cmds = cmds
        self.map = {
            "rectangle": self.rectangle,
            "rect": self.rectangle,
            "line": self.line,
            "circle": self.cirlce,
            "circ": self.cirlce,
            "ellipse": self.ellipse,
            "arc_c2p": self.arc_c2p,
            "arc_3p": self.arc_3p,
            "polyline": self.create_sketch_pline,
            "pline": self.create_sketch_pline,
            "constructionline": self.construction_line,
        }

        self.create()

    def create(self):
        mdb.models[self.model_name].ConstrainedSketch(name=self.name, sheetSize=200.0)
        for cmd in self.cmds:
            type_ = next(iter(cmd))
            kwargs = cmd[type_]

            if isinstance(kwargs, dict):
                self.map[type_](**kwargs)
            elif isinstance(kwargs, list):
                self.map[type_](*kwargs)

    def construction_line(self, point1, point2):
        s = mdb.models[self.model_name].sketches[self.name]
        s.ConstructionLine(point1=point1, point2=point2)

    def create_sketch_pline(self, points=None, *points_list):
        s = mdb.models[self.model_name].sketches[self.name]
        if points is not None:
            points_list = points
        lines = self.create_lines_from_points(array(points_list))
        for line in lines:
            kwargs = {"point1": line[0].astype(float), "point2": line[1].astype(float)}
            s.Line(**kwargs)

    def rectangle(self, point1, point2):
        point1 = array(point1)
        point2 = array(point2)
        kwargs = {
            "point1": point1,
            "point2": point2,
        }
        isnumber = issubdtype(point1.dtype, number) and issubdtype(point2.dtype, number)
        issize = (point1.size == 2) and (point2.size == 2)
        if isnumber and issize:
            mdb.models[self.model_name].sketches[self.name].rectangle(**kwargs)
        elif not isnumber:
            raise TypeError(
                "point 1: {point1} or point 2: {point2} is not a int or float".format(
                    **kwargs
                )
            )
        elif not issize:
            raise TypeError(
                "point 1: {point1} or point 2: {point2} is not 2D".format(**kwargs)
            )

    def line(self, point1, point2):
        point1 = array(point1)
        point2 = array(point2)
        kwargs = {
            "point1": point1,
            "point2": point2,
        }
        isnumber = issubdtype(point1.dtype, number) and issubdtype(point2.dtype, number)
        issize = (point1.size == 2) and (point2.size == 2)
        if isnumber and issize:
            mdb.models[self.model_name].sketches[self.name].Line(**kwargs)
        elif not isnumber:
            raise TypeError(
                "point 1: {point1} or point 2: {point2} is not a int or float".format(
                    **kwargs
                )
            )
        elif not issize:
            raise TypeError(
                "point 1: {point1} or point 2: {point2} is not 2D".format(**kwargs)
            )

    def cirlce(self, center, point1):
        center = array(center)
        point1 = array(point1)

        kwargs = {
            "center": center,
            "point1": point1,
        }
        isnumber = issubdtype(center.dtype, number) and issubdtype(point1.dtype, number)
        issize = (center.size == 2) and (point1.size == 2)
        if isnumber and issize:
            mdb.models[self.model_name].sketches[self.name].CircleByCenterPerimeter(
                **kwargs
            )
        elif not isnumber:
            raise TypeError(
                "center: {center} or point 1: {point1} is not a int or float".format(
                    **kwargs
                )
            )
        elif not issize:
            raise TypeError(
                "center: {center} or point 1: {point1} is not 2D".format(**kwargs)
            )

    def ellipse(self, center, axisPoint1, axisPoint2):
        center = array(center)
        axisPoint1 = array(axisPoint1)
        axisPoint2 = array(axisPoint2)
        kwargs = {
            "center": center,
            "axisPoint1": axisPoint1,
            "axisPoint2": axisPoint2,
        }
        isnumber = (
            issubdtype(center.dtype, number)
            and issubdtype(axisPoint1.dtype, number)
            and issubdtype(axisPoint2.dtype, number)
        )
        issize = (
            (center.size == 2) and (axisPoint1.size == 2) and (axisPoint2.size == 2)
        )
        if isnumber and issize:
            mdb.models[self.model_name].sketches[self.name].CircleByCenterPerimeter(
                **kwargs
            )
        elif not isnumber:
            raise TypeError(
                "center: {center} or axisPoint1: {axisPoint1}, axisPoint2: {axisPoint2} is not a int or float".format(
                    **kwargs
                )
            )
        elif not issize:
            raise TypeError(
                "center: {center}, axisPoint1: {axisPoint1}, axisPoint2: {axisPoint2} is not 2D".format(
                    **kwargs
                )
            )

        mdb.models[self.model_name].sketches[self.name].EllipseByCenterPerimeter(
            **kwargs
        )

    def arc_c2p(self, center, point1, point2, direction="ccw"):
        center = array(center)
        point1 = array(point1)
        point2 = array(point2)

        direction_reg = {
            "ccw": COUNTERCLOCKWISE,
            "counterclockwise": COUNTERCLOCKWISE,
            "cw": CLOCKWISE,
            "clockwise": CLOCKWISE,
        }

        kwargs = {
            "center": center,
            "point1": point1,
            "point2": point2,
            "direction": direction_reg[direction.lower()],
        }

        isnumber = (
            issubdtype(center.dtype, number)
            and issubdtype(point1.dtype, number)
            and issubdtype(point2.dtype, number)
        )
        issize = (center.size == 2) and (point1.size == 2) and (point2.size == 2)
        if isnumber and issize:
            mdb.models[self.model_name].sketches[self.name].ArcByCenterEnds(**kwargs)
        elif not isnumber:
            raise TypeError(
                "center: {center} or point1: {point1}, point2: {point2} is not a int or float".format(
                    **kwargs
                )
            )
        elif not issize:
            raise TypeError(
                "center: {center}, point1: {point1}, point2: {point2} is not 2D".format(
                    **kwargs
                )
            )

    def arc_3p(self, point1, point2, point3):
        point1 = array(point1)
        point2 = array(point2)
        point3 = array(point3)

        kwargs = {
            "point1": point1,
            "point2": point2,
            "point3": point3,
        }

        isnumber = (
            issubdtype(point1.dtype, number)
            and issubdtype(point2.dtype, number)
            and issubdtype(point3.dtype, number)
        )

        issize = (point1.size == 2) and (point2.size == 2) and (point3.size == 2)
        if isnumber and issize:
            mdb.models[self.model_name].sketches[self.name].Arc3Points(**kwargs)
        elif not isnumber:
            raise TypeError(
                "point1: {point1}, point2: {point2} or point3: {point3} is not a int or float".format(
                    **kwargs
                )
            )
        elif not issize:
            raise TypeError(
                "point1: {point1}, point2: {point2} or point3: {point3} is not 2D".format(
                    **kwargs
                )
            )

    def create_lines_from_points(self, points, lines=[]):
        if len(points) == 0:
            return lines

        if len(lines) == 0:
            if len(points) == 1:
                raise ValueError("Cannot create line from one point")
            return self.create_lines_from_points(points[2:], [(points[0], points[1])])
        return self.create_lines_from_points(
            points[1:], lines + [(lines[-1][1], points[0])]
        )
