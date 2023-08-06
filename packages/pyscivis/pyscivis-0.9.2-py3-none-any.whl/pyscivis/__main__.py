import os
import sys
import subprocess

from pyscivis.arguments import parse_args


def main() -> None:  # entrypoint for >pyscivis
    args = parse_args()
    package_name = os.path.dirname(__file__)

    if args.configfile:
        config_path = os.path.join(package_name, "config.toml")
        print(config_path)
        sys.exit()

    optional_serve_args = []
    if args.allow_websocket_origin:
        for origin in args.allow_websocket_origin:
            optional_serve_args.append(f"--allow-websocket-origin={origin}")
    if args.port is not None:
        optional_serve_args.append(f"--port={args.port}")

    sp_call = ["bokeh", "serve", "--show", package_name, *optional_serve_args, "--args", *sys.argv[1:]]
    if args.server:
        sp_call.remove("--show")
    subprocess.call(sp_call)


if __name__ == '__main__':  # entrypoint for >python -m pyscivis
    main()

