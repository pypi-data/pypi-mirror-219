#!/usr/bin/env python3

import argparse
import logging

from landing_zone.conf import *
from landing_zone.gdb_api import *


def main():
    parser = argparse.ArgumentParser(prog="Landing Zone",
                                     description="Checks if a user input reaches a specified function")

    parser.add_argument("--conf", help="path to a Landing Zone config file")

    args = parser.parse_args()

    logging.info(f"reading config file: '{args.conf}'")
    exe, args, funcs = get_target_conf(args.conf)

    logging.info(f"examining target application: '{exe}'\n")
    for each_arg in args:
        for each_func in funcs:
            debugger = GdbAPI()
            debugger.set_target(exe)
            debugger.set_arguments(each_arg)
            debugger.set_breakpoint(each_func)
            debugger.run_target()
            debugger.quit_gdb()


if __name__ == "__main__":
    main()
