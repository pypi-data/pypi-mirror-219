# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides a palet entry point
===========================

Todo:
-----

Links:
------

"""


# =============================================================================
# Import
# =============================================================================

# Import | Futures
from __future__ import print_function

# Import | Standard Library
import platform
try:
    import pkg_resources
except ImportError:
    pkg_resources = None

# Import | Libraries
import palet

# Import | Local Modules


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":

    print()
    print("palet is set!")
    print()
    print("tite: {}".format(palet.__version__))
    print(
        "Python: {} ({})".format(
            platform.python_version(), platform.python_implementation()
        )
    )

    if pkg_resources:
        working_set = pkg_resources.working_set
        packages = set([p.project_name for p in working_set]) - set(["palet"])
        palet_pkgs = [p for p in packages if p.lower().startswith("palet")]

        if palet_pkgs:
            print("Extensions: {}".format([p for p in palet_pkgs]))
