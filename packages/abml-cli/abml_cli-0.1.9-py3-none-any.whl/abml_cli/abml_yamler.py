from yaml import load, load_all, safe_load_all, safe_load, dump, SafeLoader, FullLoader, nodes, Loader
from rich.console import Console
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os 
from yaml import load
import importlib.util
from inspect import getmembers, isfunction
from importlib import import_module
from abml_cli import abml_filters
c = Console()
import sys

class Include_Loader(SafeLoader):

    def __init__(self, stream):
        # self._root = os.path.split(stream.name)[0]
        super().__init__(stream)
    
    @classmethod
    def set_params(cls, params):
        cls.params = params

    def include(self, node):
        args = []
        kwargs = {}
        if isinstance(node, nodes.ScalarNode):  # type: ignore
            return render_yaml_file(self.construct_scalar(node), **Include_Loader.params)
        if isinstance(node, nodes.SequenceNode):  # type: ignore
            args = self.construct_sequence(node)
            result = {}
            for arg in args:
                result.update(render_yaml_file(arg, **Include_Loader.params))
            return result
        if isinstance(node, nodes.MappingNode):  # type: ignore
            kwargs = self.construct_mapping(node)
            filename = kwargs.pop("filename")
            filter_module = kwargs.pop("filter") if "filter" in kwargs else None
            result = render_yaml_file(filename, filter_module=filter_module, **{**kwargs, **Include_Loader.params})
            return result


Loader.add_constructor('!include', Include_Loader.include)

class Env(Environment):
    def load_filters(self, module):
        for filter_func in getmembers(module, isfunction):
            self.filters[filter_func[0]] = filter_func[1]

    def load_filters_local(self, module_path):
        spec = importlib.util.spec_from_file_location("custom_filters", module_path)
        if spec is not None:
            module = importlib.util.module_from_spec(spec)
            for filter_func in getmembers(module, isfunction):
                self.filters[filter_func[0]] = filter_func[1]


def render_yaml_file(filename, filter_module=None, **params):
    cwd = Path().cwd()

    env = Env(loader=FileSystemLoader(cwd), autoescape=select_autoescape())
    env.load_filters(abml_filters)

    filters = ["_filters.py"] 
    if filter_module is not None:
        filters.append(filter_module)

    for filter_ in filters:
        try:
            name = filter_.removesuffix(".py")
            path = (Path().cwd() / filename).parent / filter_
            spec = importlib.util.spec_from_file_location(name=name, location=path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            env.load_filters(module)
        except ImportError:
            pass
        except FileNotFoundError:
            pass

    template = env.get_template(filename)
    return load(template.render(**params), Loader=Loader)


def generate_abml_file(file, path=Path(), filename=None, **params):
    if filename is None:
        filename = f'{file.split(".abml")[0]}'

    Include_Loader.set_params(params)
    output = render_yaml_file(file, __file__=filename.split(".")[0], **params)
    
    with open(path / f"_{filename}.render.abml", mode="w", encoding="utf-8") as f:
        dump(output, f)