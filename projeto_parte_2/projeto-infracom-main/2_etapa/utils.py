from enum import StrEnum


def pretty_print(msg, gutter="|", roof="-", floor="-"):
    msg = gutter + " " + msg + " " + gutter
    printc(len(msg) * roof, bcolors.HEADER)
    printc(msg, bcolors.HEADER)
    printc(len(msg) * floor, bcolors.HEADER)

def print_elapsed(tic, toc, id=""):
    printc(f"# [{id}]: {toc - tic}s", bcolors.OKCYAN)

def printc(msg, color=None):
    if color:
        print(f"{color}{msg}{bcolors.ENDC}")
    else:
        print(msg)

class bcolors(StrEnum):
    HEADER = '\033[95m',
    OKBLUE = '\033[94m',
    OKCYAN = '\033[96m',
    OKGREEN = '\033[92m',
    WARNING = '\033[93m',
    FAIL = '\033[91m',
    ENDC = '\033[0m',
    BOLD = '\033[1m',
    UNDERLINE = '\033[4m'