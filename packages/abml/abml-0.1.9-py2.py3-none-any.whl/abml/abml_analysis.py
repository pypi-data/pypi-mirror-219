from abaqus import mdb
from abml.abml_helpers import convert_abaqus_constants, cprint
import logging
from os import rename, listdir, getcwd, path

class Abml_Analysis():
    def __init__(self, **data):
        self.data = data
        self.jobs = self.data.get("jobs", {})
    
        self.create_jobs()
    
    def create_jobs(self):
        for job in self.jobs:
            Abml_Job(name=job, **self.jobs[job])



class Abml_Job():
    def __init__(self, name, **kwargs):
        self.name = name
        self.kwargs = convert_abaqus_constants(**kwargs)
        self.commands = self.kwargs.pop("commands", [])

        self.create()

        self.access = mdb.jobs[self.name]
        self.command_map = { 
            "writeInput": self.write_input,
            "submit": self.access.submit,
            "waitForCompletion": self.access.waitForCompletion,
            "kill": self.access.kill, 
            "clearMessages": self.access.clearMessages,
            "setValues": self.access.setValues,
        }

        self.command_map = {k.lower():v for k,v in self.command_map.items()}

        self.call_commands()

    def create(self):
        mdb.Job(name=self.name, **self.kwargs)

    def call_commands(self):
        for command in self.commands:
            type_ = next(iter(command))
            self.command_map[type_.lower()](**command[type_])


    def write_input(self, **kwargs):
        name = None
        if "name" in kwargs:
            name = kwargs.pop("name")

        mdb.jobs[self.name].writeInput(**kwargs)

        if name is not None:
            src = path.join(getcwd(), "{}.inp".format(self.name))
            dest = path.join(getcwd(), name)
            
            rename(src, dest)
    
    def submit(self):
        mdb.jobs[self.name].submit(**self.submit_kwargs)

    def waitForCompletion(self):
        mdb.jobs[self.name].waitForCompletion()