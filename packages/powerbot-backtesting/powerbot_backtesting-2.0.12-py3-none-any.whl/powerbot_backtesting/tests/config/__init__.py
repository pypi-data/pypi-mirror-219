import yaml
from pathlib import Path

with open(Path(__file__).resolve().parent.joinpath("config.yml"), "r") as configfile:
    config = yaml.full_load(configfile)
