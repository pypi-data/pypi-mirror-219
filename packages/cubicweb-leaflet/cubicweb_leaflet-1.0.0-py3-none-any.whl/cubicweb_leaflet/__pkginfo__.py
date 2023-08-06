# pylint: disable=W0622
"""cubicweb-leaflet application packaging information"""

modname = "leaflet"
distname = "cubicweb-leaflet"

numversion = (1, 0, 0)
version = ".".join(str(num) for num in numversion)

license = "LGPL"
author = "LOGILAB S.A. (Paris, FRANCE)"
author_email = "contact@logilab.fr"
description = "Cube for leaflet map, see http://leafletjs.com/"
web = f"https://forge.extranet.logilab.fr/cubicweb/cubes/{distname}"

__depends__ = {"cubicweb": ">= 4.0.0, < 5.0.0", "cubicweb-web": ">= 1.0.0, < 2.0.0"}
__recommends__ = {}

classifiers = [
    "Environment :: Web Environment",
    "Framework :: CubicWeb",
    "Programming Language :: Python",
    "Programming Language :: JavaScript",
]
