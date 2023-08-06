__version__ = "0.3.2"
__doc__ = """
FS Message Packer v{}
Copyright (C) 2021 Fusion Solutions KFT <contact@fusionsolutions.io>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/lgpl.txt>.
""".format(__version__)
try:
	ACCELERATION_IS_AVAILABLE = True
	from ._fspacker import load, loads, dump, dumps, PackerError, PackingError, UnpackingError
except ImportError:
	ACCELERATION_IS_AVAILABLE = False
	from .fallback import load, loads, dump, dumps, PackerError, PackingError, UnpackingError # type: ignore

from .fallback import HIGHEST_VERSION

__all__ = ("dump", "dumps", "load", "loads", "PackerError", "PackingError", "UnpackingError", "HIGHEST_VERSION",
"ACCELERATION_IS_AVAILABLE")