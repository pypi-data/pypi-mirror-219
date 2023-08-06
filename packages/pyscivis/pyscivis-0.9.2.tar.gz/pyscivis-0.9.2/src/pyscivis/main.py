import os

from bokeh.io import curdoc

from pyscivis.visualizer.dataclasses.config import load_config
from pyscivis.visualizer.standalone.standalone import MainComponent
from pyscivis.arguments import parse_args

config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.toml")  # TODO: make this nicer
config = load_config(config_path)
args = parse_args()

doc = curdoc()
doc.title = "pyscivis"
doc.add_root(MainComponent(config, **vars(args)).layout)
