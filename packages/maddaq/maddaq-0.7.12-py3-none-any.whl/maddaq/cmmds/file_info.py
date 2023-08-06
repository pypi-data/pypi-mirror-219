#!/usr/bin/env python3
"""Python script to show the data in a file."""

import sys
from pathlib import Path
from maddaq import MadDAQData


def getFileInfo():
    """Main entry."""
    try:
        # We open here the file with MadDAQData
        ifile = Path(sys.argv[1])
        maddaq = MadDAQData(ifile)

        print("\n++ {}".format(ifile))
        maddaq.show_info(True)

        for m in maddaq.modules.values():
            m.save_pedestals("module_{}.ped".format(m.id))

    except KeyError:
        print("I need an input file")


if __name__ == "__main__":
    getFileInfo()