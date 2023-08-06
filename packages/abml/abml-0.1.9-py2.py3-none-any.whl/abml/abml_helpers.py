from abaqus import mdb, AbaqusException
import abaqusConstants
from regionToolset import Region

import logging
import sys
from numpy import array
from part import FaceArray
from copy import deepcopy
from collections import Counter
import part 

from abaqus import mdb, session

logger = logging.getLogger(__name__)

region_list = ["cells","faces", "vertices", "edges"]

def convert_coords_to_objects(type_, access, coords):
    geometry_array = {
                    "cells":access.cells, 
                    "faces":access.faces,
                    "side1Faces":access.faces,
                    "side2Faces":access.faces,
                    "side12Faces":access.faces,
                    "vertices":access.vertices,
                    "nodes":access.nodes,
                    "edges":access.edges,
                    "xFaces":access.faces,
                    "xVertices":access.vertices,
                    "xEdges":access.edges,
                    "referencePoints":access.referencePoints,
                    }
    
    geometry_array = {k.lower(): v for k, v in geometry_array.items()}

    if hasattr(access, "regenerate"):
        access.regenerate()
    geometry_map = {"getByBoundingSphere":geometry_array[type_.lower()].getByBoundingSphere,
                    "getByBoundingCylinder": geometry_array[type_.lower()].getByBoundingCylinder, 
                    "getByBoundingBox": geometry_array[type_.lower()].getByBoundingBox, 
                    "getbykey": get_sequence_by_keys, 
    }

    if type_.lower() != "nodes":
        geometry_map.update({"findAt": geometry_array[type_.lower()].findAt})

    geometry_map = {k.lower(): v for k, v in geometry_map.items()}

    error = None
    if isinstance(coords, list):
        for command_dict in coords:
            command = next(iter(command_dict))
            kwargs  = deepcopy(command_dict[command])

            if error is None and isinstance(kwargs, dict):
                error = kwargs.pop("error", "raise")

            if command.lower() == "findat":
                if isinstance(kwargs, list):
                    kwargs = {"coordinates": kwargs}
                if array(kwargs["coordinates"]).shape == (3, ):
                    kwargs["coordinates"] = [kwargs["coordinates"]]
                find = geometry_map[command.lower()](**kwargs)
            elif command.lower() == "getbyboundingbox":
                if isinstance(kwargs, list):
                    if len(kwargs) == 6:
                        keys = ["xMin", "yMin", "zMin", "xMax", "yMax", "zMax"]
                        kwargs = dict(zip(keys, kwargs))
                    else:
                        raise ValueError("Dimension mismatch - dimension is {} and should be 6".format(len(kwargs)))
                find = geometry_map[command.lower()](**kwargs)
            elif command.lower() == "getbykey":
                if isinstance(kwargs, str):
                    kwargs = [kwargs]
                find = geometry_map[command.lower()](access, *kwargs)
            else:
                find = geometry_map[command.lower()](**kwargs)


            # if error == "raise":
            #     if find is None or len(find) == 0:
            #         raise ValueError("command: {} could not find any sequence with coordinates {}".format(command, kwargs))
            try:
                seq += find
            except UnboundLocalError:
                seq = find
        return seq
        
    raise NotImplementedError("to convert coords with non list command input is not implemented yet")

def remove_order_indices(name):
    return name.split("::")[0]


def get_sequence_by_keys(access, *args):
    model = access.modelName
    for seq_name in args:
        faces = mdb.models[model].rootAssembly.allSurfaces[seq_name].faces
        # cprint(mdb.models[model].rootAssembly.allSurfaces.keys())
        try:
            seq += faces
        except UnboundLocalError:
            seq = faces
        # if "." in seq_name:
        #     instance_name, surface_name = seq_name.split(".")
        #     if instance_name == access.name and surface_name in access.surfaces.keys():
        #         faces = access.surfaces[surface_name].faces
        #         try:
        #             seq += faces
        #         except UnboundLocalError:
        #             seq = faces
        # else:
        #     faces = mdb.models.surfaces[seq_name].faces
        #     try:
        #         seq += faces
        #     except UnboundLocalError:
        #         seq = faces
    try:
        return seq
    except UnboundLocalError:
        return None



def convert_geometry(access, **set_):
    for type_ in set_:
        object_ = convert_coords_to_objects(type_=type_, access=access, coords=set_[type_])
        if object_ is not None:
            set_[type_] = set_
    return set_

def issequence(t):
    return hasattr(t, '__len__') and hasattr(t, '__getitem__')

def reduce_dimensions(lst):
    if isinstance(lst, list) and lst:
        if isinstance(lst[0], list):
            if len(lst) == 1:
                return reduce_dimensions(lst[0])
            else:
                return [reduce_dimensions(sublist) for sublist in lst]
        else:
            return lst
        
def get_dimensions(lst):
    dimensions = []
    if isinstance(lst, list):
        dimensions.append(len(lst))
        get_dimensions(lst[0])
    return dimensions

def convert_region(access, keys=["surface", "master", "slave"], **kwargs):
    for map_ in keys:
        region = kwargs.get(map_, None)
        if region is not None:
            if isinstance(region, str) and region in access.allSets.keys():
                kwargs[map_] = access.allSets[region]
            elif isinstance(region, str) and region in access.allSurfaces.keys():
                kwargs[map_] = access.allSurfaces[region]
            elif isinstance(region, dict) and "surface" in region:
                kwargs[map_] = access.allSurfaces[kwargs[map_]["surface"]]
            elif isinstance(region, dict) and "set" in region:
                kwargs[map_] = access.allSurfaces[kwargs[map_]["set"]]
            elif isinstance(region, dict):
                counter = Counter()
                for instance in access.instances.keys():
                    updated = convert_geometry_repository(access.instances[instance], **kwargs[map_])
                    updated = {k: v for k, v in updated.items() if v is not None}
                    counter.update(updated)
 
                kwargs[map_] = Region(**counter)
    
    return kwargs

def convert_geometry_repository(access, **kwargs):

    geometry_array = ["cells",
                    "faces",
                    "nodes",
                    "side1Faces",
                    "side2Faces",
                    "side12Faces",
                    "vertices",
                    "edges",
                    "xFaces",
                    "xVertices",
                    "xEdges",
                    "referencePoints"]
    
    geometry_array = [k.lower() for k in geometry_array]

    for type_ in kwargs:
        if type_.lower() in geometry_array:
            object_ = convert_coords_to_objects(type_=type_, access=access, coords=kwargs[type_])
            kwargs[type_] = object_
        elif type_.lower() == "sets":
            if isinstance(kwargs[type_], str):
                kwargs[type_] = mdb.models[access.modelName].rootAssembly.allSets.allSets[kwargs[type_]]
            elif isinstance(kwargs[type_], list):
                kwargs[type_] = [mdb.models[access.modelName].rootAssembly.allSets[name] for name in kwargs[type_]]

    return kwargs


def convert_abaqus_constant(string):
    return getattr(abaqusConstants, string.upper())

def convert_abaqus_constants(**nested_dict):
    for key, value in nested_dict.items():
        if isinstance(value, dict):
            convert_abaqus_constants(**value)
        elif isinstance(value, list):
            list_ = []
            for elem in value:
                try:
                    list_.append(getattr(abaqusConstants, elem.upper()))
                except AttributeError:
                    list_.append(elem)
                except TypeError:
                    list_.append(elem)
            if key == "table":
                nested_dict[key] = [list_]
            else:
                nested_dict[key] = list_
        else:
            if value == "Initial":
                pass
            else:
                try:
                    nested_dict[key] = getattr(abaqusConstants, value.upper())
                except AttributeError:
                    pass
                except TypeError:
                    pass
    return nested_dict


def sort_dict_with_fixed_order(list_, order):
    def custom_sort_key(item):
        key = item

        try:
            level_name, level_index = key.split("::")
        except ValueError:
            level_name = key
            level_index = 0
        level_order = order.index(level_name)

        # if float(level_index) < 0:
        #     level_index = float("inf") + float(level_index)

        return float(level_index), float(level_order)

    sorted_dict = sorted(list_, key=custom_sort_key)

    return sorted_dict

def sort_dict_by_suffix(list_):
    def custom_sort_key(item):
        key = item

        try:
            level_name, level_index = key.split("::")
        except ValueError:
            level_name = key
            level_index = 0
        
        level_order = ord(level_name.lower()[0])

        return float(level_index), float(level_order)

    sorted_dict = sorted(list_, key=custom_sort_key)

    return sorted_dict


def cprint(string, prefix="info"):
    """
    Prints the given string with a specified prefix to the standard output.

    Parameters
    ----------
    string : str
        The string to be printed.
    prefix : str, optional
        The prefix to be added to the string (default is "info").

    Returns
    -------
    None

    Notes
    -----
    This function uses the standard output stream `sys.__stdout__` to print the message.

    Examples
    --------
    **python
    >>> cprint("This is a message.", "warning")
    warning This is a message.

    >>> cprint("This is another message.")
    info This is another message.
    """
    print >> sys.__stdout__, prefix + " " + str(string)  # type: ignore # noqa
