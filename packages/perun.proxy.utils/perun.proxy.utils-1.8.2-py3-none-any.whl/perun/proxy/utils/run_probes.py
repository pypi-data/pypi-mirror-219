#!/usr/bin/python3
import re
import subprocess
import sys
from threading import Thread

import yaml


def open_file(filepath):
    try:
        with open(filepath) as f:
            return f.read()
    except OSError as e:
        print(
            f"Cannot open config with path: {filepath}, error: {e.strerror}",
            file=sys.stderr,
        )
        sys.exit(2)


def run_probe(probe_name, command):
    result = subprocess.run(
        command, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    output = re.sub("[ \t\n]+", " ", result.stdout)
    search = re.search(r" - .*", output)
    if search:
        print(f"{result.returncode} {probe_name} {search.group()}")
    else:
        print(f"{result.returncode} {probe_name} - {output}")
    return result.returncode


def main():
    config_filepath = "/etc/run_probes_cfg.yaml"
    config = yaml.safe_load(open_file(config_filepath))
    if not config:
        return

    for _, options in config.items():
        module = options["module"]
        for name, args in options.get("runs").items():
            command = ["python3", "-m", module]
            for arg_name, arg_val in args.items():
                if len(arg_name) == 1:
                    arg_name = "-" + arg_name
                else:
                    arg_name = "--" + arg_name
                if arg_val is True:
                    arg_val = "true"
                elif arg_val is False:
                    arg_val = "false"
                command.append(arg_name)
                if arg_val is not None:
                    command.append(str(arg_val))
            Thread(target=run_probe, args=[name, command]).start()


if __name__ == "__main__":
    main()
