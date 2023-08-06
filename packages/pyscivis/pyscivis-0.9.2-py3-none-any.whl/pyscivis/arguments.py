
import argparse
import os


def parse_args() -> argparse.Namespace:
    """

    @return:
    """
    parser = argparse.ArgumentParser(description='pyscivis')
    parser.add_argument('-f', '--file', '--filename',
                        metavar='PATH',
                        type=str,
                        help='Path of file to be initially displayed')

    parser.add_argument('-n', '--noselector',
                        action='store_true',
                        help='Disable the file selector widget')

    parser.add_argument('-c', '--configfile',
                        action='store_true',
                        help='Print the path of the configuration file')

    parser.add_argument('-p', '--port',
                        type=int,
                        metavar='PORT',
                        help='The port the bokeh application should use. Bokeh-default: 5006')

    parser.add_argument('-s', '--server',
                        nargs='?',
                        default=None,  # None if no --server was entered
                        const=os.getcwd(),  # default value if --server was entered without argument
                        metavar="SHARED_DIR",
                        help='Run the application in server-mode. '
                             'The optional parameter sets the root directory containing accessible files. '
                             'Default for SHARED_DIR is the current working directory')

    parser.add_argument('-w', '--allow-websocket-origin',
                        action='append',
                        type=str,
                        metavar='HOST[:PORT]',
                        help="The bokeh server will only accept connections coming from the specified URL. "
                             "Can be specified multiple times to allow multiple origins. "
                             "Default: localhost:5006")

    return parser.parse_args()
