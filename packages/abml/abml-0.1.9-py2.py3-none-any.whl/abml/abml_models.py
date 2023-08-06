from abaqus import mdb, openMdb
from abml.abml_helpers import cprint, sort_dict_with_fixed_order
from abml.abml_sketches import Abml_Sketch
from abml.abml_materials import Abml_Material
from abml.abml_sections import Abml_Section
from abml.abml_assembly import Abml_Assembly
from abml.abml_steps import Abml_Step
from abml.abml_parts import Abml_Part
from abml.abml_interaction import Abml_Interaction
from abml.abml_constraint import Abml_Constraint
from abml.abml_bc import Abml_Bc 
from abml.abml_loads import Abml_Load 
from abml.abml_interaction_property import Abml_Interaction_Property
import logging
from collections import OrderedDict

logger = logging.getLogger(__name__)


class Abml_Model:
    def __init__(self, **data):
        self.name = next(iter(data))
        self.description = data[self.name].pop("description", "")
        self.modules = data[self.name].pop("modules", [])

        for module in self.modules:
            data[self.name].update(module)

        self.members = data[self.name]

        self.execution_map = {
            "sketches": self.create_sketches,
            "materials": self.create_materials,
            "sections": self.create_sections,
            "parts": self.create_parts,
            "assembly": self.create_assembly,
            "interaction_properties": self.create_interactions_props,
            "interactions": self.create_interactions,
            "constraints": self.create_constraints,
            "steps": self.create_steps,
            "bcs": self.create_bcs,
            "loads": self.create_loads,
            "jobs": self.create_jobs,
        }

        execution_order = [
            "sketches",
            "materials",
            "sections",
            "parts",
            "assembly",
            "steps",
            "interaction_properties",
            "interactions",
            "constraints",
            "bcs",
            "loads",
            "jobs",
        ]

        self.create()
        self.order = sort_dict_with_fixed_order(self.members.keys(), execution_order)
        self.create_instances()

    def create(self):
        mdb.Model(name=self.name, description=self.description)

    def create_instances(self):
        for instance in self.order:
            try:
                instance_name, _ = instance.split("::")
            except ValueError:
                instance_name = instance

            self.execution_map[instance_name](self.members[instance])

    def create_sketches(self, data):
        for sketch_name in data:
            Abml_Sketch(name=sketch_name, model_name=self.name, cmds=data[sketch_name])

    def create_materials(self, data):
        for material in data:
            Abml_Material(name=material, model=self.name, members=data[material])

    def create_sections(self, data):
        for section in data:
            Abml_Section(name=section, model=self.name, **data[section])

    def create_parts(self, data):
        for part in data:
            Abml_Part(name=part, model=self.name, **data[part])

    def create_assembly(self, data):
        Abml_Assembly(model=self.name, **data)

    def create_steps(self, data):
        data = OrderedDict(sorted(data.items()))
        for step in data:
            Abml_Step(model=self.name, name=step, **data[step])

    def create_interactions_props(self, data):
        for prop in data:
            Abml_Interaction_Property(model=self.name, name=prop, **data[prop])

    def create_interactions(self, data):
        for interaction in data:
            Abml_Interaction(model=self.name, name=interaction, **data[interaction])

    def create_constraints(self, data):
        for interaction in data:
            Abml_Constraint(model=self.name, name=interaction, **data[interaction])

    def create_bcs(self, data):
        for bc in data:
            Abml_Bc(model=self.name, name=bc, **data[bc])

    def create_loads(self, data):
        for load in data:
            Abml_Load(model=self.name, name=load, **data[load])

    def create_jobs(self, data):
        pass
