# pylint: disable-msg=W0622
"""cubicweb-file packaging information"""

modname = "cubicweb_file"
distname = "cubicweb-file"

numversion = (4, 0, 0)
version = ".".join(str(num) for num in numversion)

license = "LGPL"
author = "Logilab"
author_email = "contact@logilab.fr"
web = f"https://forge.extranet.logilab.fr/cubicweb/cubes/{distname}"
description = "file component for the CubicWeb framework"
classifiers = [
    "Environment :: Web Environment",
    "Framework :: CubicWeb",
    "Programming Language :: Python",
    "Programming Language :: JavaScript",
]

__depends__ = {
    "cubicweb": ">= 4.0.0, < 5.0.0",
    "cubicweb-web": ">= 1.1.0, < 2.0.0",
    "Pillow": None,
}

__recommends__ = {}
