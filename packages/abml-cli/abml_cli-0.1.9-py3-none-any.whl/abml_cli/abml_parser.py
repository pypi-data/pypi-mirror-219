from abaqus import mdb
from yaml import load, Loader
from abml.abml_cae import Abml_Cae
from abml.abml_helpers import cprint
from abml.abml_logger import Logger
from io import open
import argparse
from os import path, getcwd, chdir
import logging
import traceback

parser = argparse.ArgumentParser()
parser.add_argument("--yml")
parser.add_argument("--path", default=None)
parser.add_argument('-d', '--debug', action='store_true')

args, _ = parser.parse_known_args()

if args.debug is True:
    logging.root.setLevel(logging.DEBUG)
else:
    logging.root.setLevel(logging.INFO)

if __name__ == "__main__":
    with open(args.yml, mode="r", encoding="utf-8") as f:
        data = load(f, Loader=Loader)
        models = data.get("models", {})
        if args.path == None:
            args.path = getcwd()

        if args.debug is True:
            try:
                cae = Abml_Cae(analysis=data.get("analysis"), session=data.get("session"), models=models, cae=data.get("cae"), cwd=args.path)
            except Exception as e:
                mdb.saveAs("{}.debug.cae".format(args.yml.split(".")[0]).strip("_"))
                raise Exception(traceback.format_exc())
        else:
            cae = Abml_Cae(analysis=data.get("analysis"), session=data.get("session"), models=models, cae=data.get("cae"), cwd=args.path)
        
        filename = path.basename(args.yml.split(".")[0]).strip("_")
        
        if models != {}:
            cae.save_cae(path.join(args.path, "{}.cae").format(filename))
