import yaml
import click
from pandas import DataFrame
from subprocess import run as prun
from pathlib import Path
from rich.console import Console
from abml_cli.abml_yamler import generate_abml_file
from abml_cli.abml_grids import get_parameters_list, generate_param_grid,flatten_dict
import glob
from os import remove, rename
from os.path import isfile
from yaml import safe_load
import logging
import sys
import time

c = Console()

parser_path = (Path(__file__).parents[0] / "abml_parser.py").resolve()

logger = logging.getLogger(__name__)
logFormatter = logging.Formatter("%(asctime)s [%(name)s] [%(levelname)s]  %(message)s")
streamhandler = logging.StreamHandler(logging.StreamHandler())
streamhandler.setFormatter(logFormatter)
logger.addHandler(streamhandler)

@click.command()
@click.option("--file", "-f", help="abml-files", required=False, multiple=False)
@click.option("--debug", "-d", is_flag=True, show_default=True, default=False, help="debug mode")
def run(file, debug):

    if debug is True:
        logger.setLevel(logging.DEBUG)
        debug_flag = "--debug"
    else:
        logger.setLevel(logging.INFO)
        debug_flag = ""
    
    if file is None:
        files = glob.glob("*.abml")
    else:
        files = [file]

    params={}
    if Path("_env.abml").is_file():
        with open("_env.abml", mode="r", encoding="utf-8") as f:
            env = safe_load(f)
    
        params = env.get("parameters", {})
        
    for f in files:
        if not f.startswith("_"):
            generate_abml_file(f, **params)
            rendered = f'_{f.replace(".abml", "")}.render.abml'
            cwd = Path().cwd()
            cmd = f'abaqus cae nogui="{parser_path}" -- --yml "{cwd / rendered}" {debug_flag}'
            prun(cmd, shell=True, check=True)

    rpys = glob.glob("*.rpy*")
    recs = glob.glob("*.rec*")

    for file in rpys+recs:
        try:
            remove(file)
        except PermissionError:
            pass
            

@click.command()
@click.option("--file", "-f", help="abml-files", required=True, multiple=False)
def run_grid(file):
    params={}
    grids = {}
    if Path("_env.abml").is_file():
        with open("_env.abml", mode="r", encoding="utf-8") as f:
            env = safe_load(f)
    
        params = env.get("parameters", {})
        grids = env.get("grids", {})

    input_folder = grids.pop("input_folder", None)
    
    
    root = Path("grids")
    root.mkdir(exist_ok=True)

    for grid_name in grids:
        grid_path = root / Path(grid_name)
        grid_path.mkdir(exist_ok=True)
        
        params_list = get_parameters_list(params, grids[grid_name])
        df = DataFrame(map(flatten_dict, params_list))
        names = []
        for i, params_grid in enumerate(params_list):
            timestr = time.strftime("%Y%m%d-%H%M%S")
            names.append(timestr)
            path = grid_path / Path(f"{timestr}")
            path.mkdir(exist_ok=True)
            
            filename = f'{file.split(".abml")[0]}.{path.name}'
            generate_abml_file(file, path=path, filename=filename, **params_grid)
            rendered = f"_{filename}.render.abml"
            cwd = Path().cwd()
            cmd = f'abaqus cae nogui="{parser_path}" -- --yml "{cwd / path / rendered}" --path "{cwd / path}"'
            prun(cmd, shell=True, check=True)

            cae =  cwd / path / Path(file).with_suffix(".cae")
            cae_new = Path(cwd / path / f"{i+1}.cae")
            if cae_new.is_file():
                cae_new.unlink()
            cae.rename(cae_new)

            jnl =  cwd / path / Path(file).with_suffix(".jnl")
            jnl_new = Path(cwd / path / f"{i+1}.jnl")
            if jnl_new.is_file():
                jnl_new.unlink()
            jnl.rename(jnl_new)

            inp =  cwd / path / Path(file).with_suffix(".inp")
            inp_new = Path(cwd / path / f"{i+1}.inp")
            if inp_new.is_file():
                inp_new.unlink()
            inp.rename(inp_new)

            if input_folder is not None:
                Path(cwd / grid_path / input_folder).mkdir(exist_ok=True)
                Path(cwd / grid_path / input_folder / f"{i+1}.inp").write_bytes(inp_new.read_bytes())
        df["name"] = names
        df.set_index("name", inplace=True)
        df.to_csv(grid_path / "env.csv", sep=",")

    rpys = glob.glob("*.rpy*")
    recs = glob.glob("*.rec*")

    for file in rpys+recs:
        try:
            remove(file)
        except PermissionError:
            pass

