#!/usr/bin/env python
# ------------------------------------------------------------------------------
# This file is part of PyTango (http://pytango.rtfd.io)
#
# Copyright 2006-2012 CELLS / ALBA Synchrotron, Bellaterra, Spain
# Copyright 2013-2014 European Synchrotron Radiation Facility, Grenoble, France
#
# Distributed under the terms of the GNU Lesser General Public License,
# either version 3 of the License, or (at your option) any later version.
# See LICENSE.txt for more info.
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# WARNING: This script should only be executed as a Post-Build Event from inside
#          Microsoft Visual Studio and not from the command line
# ------------------------------------------------------------------------------

import os
import sys
import traceback


def main():
    print("winsetup: invoked with: " + " ".join(sys.argv))
    if len(sys.argv) < 6:
        print(
            "winsetup: need to supply build directory, distribution directory, "
            "temporary binary install directory, configuration name and platform name"
        )
        return 1

    build_dir, dist_dir, bdist_dir = map(os.path.abspath, sys.argv[1:4])
    config_name, plat_name = sys.argv[4:6]
    # Pypi is picky about platform name. Make sure we obey his/her majesty
    plat_name = plat_name.lower()
    if plat_name == "x64":
        plat_name = "win-amd64"

    executable = sys.executable
    setup_name = "setup.py"
    curr_dir = os.getcwd()
    winsetup_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(winsetup_dir)
    try:
        cmd_line = (
            f"{executable} {setup_name} "
            f"build_py --force --no-compile --build-lib={build_dir} "
            f"build_scripts --force "
            f"install_lib --skip-build --no-compile --build-dir={build_dir} "
            f"bdist_wheel --skip-build "
            f"--bdist-dir={bdist_dir} "
            f"--dist-dir={dist_dir} "
            f"--plat-name={plat_name} "
        )
        os.system(cmd_line)
    except Exception:
        print("Failed:")
        traceback.print_exc()
        return 2
    finally:
        os.chdir(curr_dir)

    return 0


if __name__ == "__main__":
    ret = main()
    sys.exit(ret)
