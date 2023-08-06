# pyscivis
![build-status](https://gitlab.com/chi-imrt/pyscivis/pyscivis/badges/main/pipeline.svg) ![coverage](https://gitlab.com/chi-imrt/pyscivis/pyscivis/badges/main/coverage.svg?job=unit-test)

pyscivis is a Python package for visualizing ismrmrd/mrd-files. You can run it as both a standalone application or embed it into  a jupyter notebook.

Note that this package is still under heavy development.
If you encounter any bugs please open an issue where you include the exception, the steps to reproduce the bug and (if possible) the data you tried to visualize!

If you do not have ismrmrd-files but still want to play around with this application, I suggest using ismrmrd-files (.h5) from this repo: [ismrmrdviewer](https://github.com/ismrmrd/ismrmrdviewer/tree/master/res/data).

# Note
- If selecting the BoxEditTool (to draw ROIs) you need to hold shift while dragging OR double click, then drag to draw the box: [Demo](https://docs.bokeh.org/en/latest/docs/user_guide/tools.html#boxedittool)

# Table of contents
1. [Installation](#Installation)
    1. [Production](#Production)
    2. [Development](#Development)
2. [Usage](#Usage)
    1. [Standalone](#Standalone)
    2. [Notebook](#Notebook)
    3. [Server](#Server)
3. [Configuration](#Configuration)
4. [Writing Extensions](#Extensions)
5. [Creating and Compiling custom models](#Models)
    1. [Difference between "start up" and pre-compiled models](#Difference)
6. [Building the documentation](#Documentation)

<a name="Installation"></a>
## Installation

<a name="Production"></a>
### Production

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pyscivis.

```bash
> pip install pyscivis
```

<a name="Development"></a>
### Development

Clone this repository

```bash
> git clone https://gitlab.com/chi-imrt/pyscivis/pyscivis.git
```

and install dev-dependencies

```bash
> pip install -r requirements/test.txt
```

or to run setup.py locally

```bash
> pip install -e .[testing]
```

<a name="Usage"></a>
## Usage

<a name="Standalone"></a>
### Standalone

After installation simply run this in your terminal:

```bash
> pyscivis
```

This will show you possible command-line arguments:
```bash
> pyscivis --help

usage: pyscivis [-h] [-f FILE] [-n] [-c]

pyscivis

optional arguments:
  -h, --help            show this help message and exit
  -f PATH, --file PATH, --filename PATH
                        Path of file to be initially displayed
  -n, --noselector      Disable the file selector widget
  -c, --configfile      Print the path of the configuration file
  -p PORT, --port PORT  The port the bokeh application should use. Bokeh-default: 5006
  -s [SHARED_DIR], --server [SHARED_DIR]
                        Run the application in server-mode. The optional parameter sets the root directory containing
                        accessible files. Default for SHARED_DIR is the current working directory
  -w HOST[:PORT], --allow-websocket-origin HOST[:PORT]
                        The bokeh server will only accept connections coming from the specified URL. Can be specified
                        multiple times to allow multiple origins. Default: localhost:5006
```

<a name="Notebook"></a>
### Notebook

Please check the [notebook-example](https://gitlab.com/chi-imrt/pyscivis/pyscivis/-/tree/main/examples/pyscivis-demo.ipynb) in the examples folder for an introduction on how to use pyscivis in conjunction with jupyter notebook.

Be aware that if you use the Notebook in a dockerized environment you will need to make sure the bokeh-server ports (as specified in the config) are forwarded and you call `nb.enable` with the docker keyword, i.e., `nb.enable(docker=True)`


<a name="Server"></a>
### Server

It is possible to deploy this application using web frameworks like `flask`.
An example snippet to run a flask server is located <a href="src/pyscivis/flask_deploy.py" target="_blank">here</a>.

This script will fetch a session from the currently running pyscivis at the specified port.
To run pyscivis in server-mode use
```bash
> pyscivis --server SHARED_DIR --allow-websocket-origin=URL_OF_SERVING_WEBSITE:PORT
``` 

Note that, if the optional argument `SHARED_DIR` is omitted, the current working directory will be browsable by the user.
If the bokeh-application should run on a different port, specify `--port YOUR_PORT`.

If reverse proxies are used certain modifications like using [relative URLs](https://docs.bokeh.org/en/latest/docs/reference/embed.html#bokeh.embed.server_document) might be necessary.
Check [the bokeh docs](https://docs.bokeh.org/en/latest/docs/user_guide/server.html#embedding-bokeh-server-as-a-library) for further information on how to set up a server with a bokeh-app.

<a name="Configuration"></a>
## Configuration

There are a few parameters that you can tune to your liking.
The configuration file is located in "src/pyscivis".

If you have trouble finding it, consider using

```bash
> pyscivis --configfile
```

which will print a path to your configuration file.

<a name="Extensions"></a>
## Writing Extensions for other files

Currently only ismrmrd-files and (some) types of images are supported.
If you wish to support other files you will have to implement a custom extension.

The procedere is described <a href="src/pyscivis/visualizer/extensions/README.md" target="_blank">here</a>.


<a name="Models"></a>
## Creating and Compiling custom models

Bokeh supports the usage of [custom models](https://docs.bokeh.org/en/latest/docs/user_guide/extensions.html#extending-bokeh).
This allows the usage of more specialized HTML+JS constructs in a bokeh-supported way.

However, these models have to be compiled on every start of the bokeh server (be it standalone or in the notebook), which can introduce huge delays.
To avoid this, `pyscivis` ships with all custom models pre-compiled.

If you wish to modify existing models or create new ones, study `pyscivis`'s models and read the docs.
To manually re-compile them, go to `src/pyscivis` and run `> bokeh build` which will require external dependencies like npm.
See [this manual](https://docs.bokeh.org/en/latest/docs/user_guide/extensions.html#pre-built-extensions) for further explanation.

Note: 
Models that get compiled on every startup have a different structure compared to the ones that you pre-compile.
For the first, simply read the docs linked above. For the latter, look at `pyscivis`'s models AND read [this awesome tutorial from Marc Skov Madsen](https://awesome-panel.readthedocs.io/en/latest/guides/awesome-panel-extensions-guide/bokeh-extensions.html#prebuilt-bokeh-extensions) AND specifically [this minimal example](https://github.com/golmschenk/bokeh_prebuilt_extension_example) carefully. Even though it's written for the higher-level bokeh wrapper [Awesome Panel](https://awesome-panel.org/), it holds true for pre-compiling bokeh models.

### Difference between "start up" and pre-compiled models.
The following table shows all structural differences between "start up" and pre-compiled files to allow an easier entry point to writing models and pre-compiling them.
**TS** means it's related to the typescript-files, **PY** to python files.

|  | start up | pre-compiled |
| ------ | ------ | ------ |
| "library import" **(TS)** | plain "bokeh" | "@bokehjs"* |
| \_\_implementation\_\_-dunder **(PY)** | necessary | forbidden |
|static \_\_module\_\_ = "pyscivis.visualizer.models.mymodel" **(TS)** | forbidden | necessary|

Note: All other things have been explained in great detail in the documentation above (including the links).

\* Name can vary depending on what you write into your `tsconfig.json`.
<a name="Documentation"></a>
## Building the documentation

The documentation is written with [Google-style docstrings](https://google.github.io/styleguide/pyguide.html#382-modules).
This allows the documentation to be build using either doxygen+doxypypy or sphinx.

To build the documentation using doxygen follow these steps:

0. Installing dependencies

    0. Install doxygen from the [doxygen website](https://www.doxygen.nl/download.html), make sure it's in your path if you are using windows
    1. Install doxypypy from the repo (not pypi as it's outdated)
    ```bash
    > pip install git+https://github.com/Feneric/doxypypy
    ```
1. Navigate to the `doxygen` folder of this repo
    ```bash
    > cd doxygen
    ```
2. Run the script appropriate for your OS, e.g. for Unix systems do:
    ```bash
    > doxygen Doxyfile_unix
    ```
3. Done. Check the directory `html` for the output

Note: Depending on your Python version the 2nd step might fail (errors in output log), in this case add [this snippet](https://github.com/Feneric/doxypypy/issues/70#issuecomment-583398545) to your local doxypypy version.
