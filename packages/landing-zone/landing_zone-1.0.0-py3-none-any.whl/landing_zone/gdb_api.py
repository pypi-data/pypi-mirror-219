import logging
import time

from pygdbmi.gdbcontroller import GdbController

logging.basicConfig(level=logging.INFO)


class GdbAPI:
    def __init__(self):
        self.gdbmi = GdbController()
        self.args = ""

    def set_target(self, target):
        logging.debug(f"setting target to '{target}'")
        self.gdbmi.write(f"-file-exec-and-symbols {target}")

    def set_arguments(self, args):
        self.args = args
        logging.debug(f"setting target arguments to '{self.args}'")
        self.gdbmi.write(f"-exec-arguments {self.args}")

    def set_breakpoint(self, function_name):
        logging.debug(f"setting breakpoint on function: '{function_name}'")
        self.gdbmi.write(f"-break-insert {function_name}")

    def run_target(self):
        logging.debug("running target...")

        out = self.gdbmi.write(f"-exec-run")

        for each_msg in out:
            if each_msg['message'] == "stopped" and each_msg['payload']['reason'] == "breakpoint-hit":
                out = self.gdbmi.write("-stack-list-frames")
                self.print_alert(out)
                self.gdbmi.write("-exec-continue")

    def print_alert(self, msg):
        logging.warning(f"Landed in target function with arguments: '{self.args}'")
        line_number = ""
        func = ""
        file = ""

        print("---------------------------")
        for each_obj in msg:
            stacks = each_obj['payload']
            stack = stacks['stack']
            for element in stack:
                line_number = element['line']
                func = element['func']
                file = element['file']
                print(f"{file}:{line_number}:{func}")
            print()

    def quit_gdb(self):
        logging.debug("exiting program")
        self.gdbmi.exit()
