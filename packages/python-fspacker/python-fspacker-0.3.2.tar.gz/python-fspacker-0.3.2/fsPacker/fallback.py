# Builtin modules
from __future__ import annotations
import struct
from io import BytesIO
from math import ceil
from typing import Dict, Any, List, Tuple, IO, Union
# Third party modules
# Local modules
# Program
HIGHEST_VERSION:int = 2

class PackerError(Exception): pass
class PackingError(PackerError): pass
class UnpackingError(PackerError): pass

class _OP_CODES_ver2:
	VINT_2BYTES           = b"\xE5"
	VINT_3BYTES           = b"\xE6"
	VINT_4BYTES           = b"\xE7"
	OP_NONE               = b"\xE8"
	OP_BOOL_FALSE         = b"\xE9"
	OP_BOOL_TRUE          = b"\xEA"
	OP_INTERGER           = b"\xEB"
	OP_NEG_INTERGER       = b"\xEC"
	OP_ZERO_INTERGER      = b"\xED"
	OP_CHAR_INTERGER      = b"\xEE"
	OP_NEG_CHAR_INTERGER  = b"\xEF"
	OP_SHORT_INTERGER     = b"\xF0"
	OP_NEG_SHORT_INTERGER = b"\xF1"
	OP_FLOAT              = b"\xF2"
	OP_ZERO_FLOAT         = b"\xF3"
	OP_INF_FLOAT          = b"\xF4"
	OP_NEG_INF_FLOAT      = b"\xF5"
	OP_UNICODE            = b"\xF6"
	OP_ZERO_UNICODE       = b"\xF7"
	OP_BYTES              = b"\xF8"
	OP_ZERO_BYTES         = b"\xF9"
	OP_LIST               = b"\xFA"
	OP_ZERO_LIST          = b"\xFB"
	OP_DICT               = b"\xFC"
	OP_ZERO_DICT          = b"\xFD"
	OP_SET                = b"\xFE"
	OP_ZERO_SET           = b"\xFF"

class Packer_ver2(_OP_CODES_ver2):
	recursiveLimit:int
	stack:int
	buffer:Union[BytesIO, IO[bytes]]
	index:Dict[Any, int]
	indexCounter:int
	def __init__(self, recursiveLimit:int=512) -> None:
		self.recursiveLimit = recursiveLimit
		self.buffer         = BytesIO()
		self.index          = {}
		self.indexCounter   = 0
		self.stack          = 0
	def _create_indexNr(self, d:int) -> bytes:
		if d < self.VINT_2BYTES[0]:
			return d.to_bytes(1, "little")
		elif d <= 0xFFFF:
			return self.VINT_2BYTES + d.to_bytes(2, "little")
		elif d <= 0xFFFFFF:
			return self.VINT_3BYTES + d.to_bytes(3, "little")
		elif d <= 0xFFFFFFFF:
			return self.VINT_4BYTES + d.to_bytes(4, "little")
		else:
			raise PackingError("Too big number")
	def _create_vint(self, d:int) -> bytes:
		if d < 0xFD:
			return d.to_bytes(1, "little")
		elif d <= 0xFFFF:
			return b"\xFD" + d.to_bytes(2, "little")
		elif d <= 0xFFFFFF:
			return b"\xFE" + d.to_bytes(3, "little")
		elif d <= 0xFFFFFFFF:
			return b"\xFF" + d.to_bytes(4, "little")
		else:
			raise PackingError("Too big number")
	def dump(self, data:Any, file:IO[bytes]) -> None:
		self.buffer = file
		self.buffer.write(b"\x02")
		self._dump(data)
	def dumps(self, data:Any) -> bytes:
		self._dump(data)
		assert isinstance(self.buffer, BytesIO)
		return b"\x02" + self.buffer.getbuffer()
	def _dump(self, d:Any) -> None:
		if self.stack == self.recursiveLimit:
			raise PackingError("Recusive limit reached")
		dt = type(d)
		if d is None:
			self.buffer.write(self.OP_NONE)
		elif d is False:
			self.buffer.write(self.OP_BOOL_FALSE)
		elif d is True:
			self.buffer.write(self.OP_BOOL_TRUE)
		elif dt is int:
			if d == 0:
				self.buffer.write(self.OP_ZERO_INTERGER)
			elif d in self.index:
				self.buffer.write( self._create_indexNr( self.index[d] ) )
			else:
				isNeg = d < 0
				nd = abs(d) if isNeg else d
				nl = ceil(nd.bit_length() / 8)
				if nl == 1:
					self.buffer.write(self.OP_NEG_CHAR_INTERGER if isNeg else self.OP_CHAR_INTERGER)
				elif nl == 2:
					self.buffer.write(self.OP_NEG_SHORT_INTERGER if isNeg else self.OP_SHORT_INTERGER)
				else:
					self.buffer.write((self.OP_NEG_INTERGER if isNeg else self.OP_INTERGER) + self._create_vint(nl))
				self.buffer.write(nd.to_bytes(nl, "little"))
				self.index[d] = self.indexCounter
				self.indexCounter += 1
		elif dt is float:
			if d == 0.0:
				self.buffer.write(self.OP_ZERO_FLOAT)
			elif d == float("inf"):
				self.buffer.write(self.OP_INF_FLOAT)
			elif d == float("-inf"):
				self.buffer.write(self.OP_NEG_INF_FLOAT)
			elif d in self.index:
				self.buffer.write( self._create_indexNr( self.index[d] ) )
			else:
				self.buffer.write(self.OP_FLOAT)
				self.buffer.write(struct.pack("d", d))
				self.index[d] = self.indexCounter
				self.indexCounter += 1
		elif dt is str:
			if d == "":
				self.buffer.write(self.OP_ZERO_UNICODE)
			elif d in self.index:
				self.buffer.write( self._create_indexNr( self.index[d] ) )
			else:
				s = d.encode()
				self.buffer.write(self.OP_UNICODE + self._create_vint(len(s)) + s)
				self.index[d] = self.indexCounter
				self.indexCounter += 1
		elif dt in (bytes, bytearray):
			if d == b"":
				self.buffer.write(self.OP_ZERO_BYTES)
			elif d in self.index:
				self.buffer.write( self._create_indexNr( self.index[d] ) )
			else:
				self.buffer.write(self.OP_BYTES + self._create_vint(len(d)) + d)
				self.index[d] = self.indexCounter
				self.indexCounter += 1
		elif dt in (tuple, list):
			if len(d):
				self.buffer.write(self.OP_LIST + self._create_vint(len(d)))
				self.stack += 1
				for sd in d:
					self._dump(sd)
				self.stack -= 1
			else:
				self.buffer.write(self.OP_ZERO_LIST)
		elif dt is dict:
			if len(d):
				self.buffer.write(self.OP_DICT + self._create_vint(len(d)))
				self.stack += 1
				for k, v in d.items():
					self._dump(k)
					self._dump(v)
				self.stack -= 1
			else:
				self.buffer.write(self.OP_ZERO_DICT)
		elif dt is set:
			if len(d):
				self.buffer.write(self.OP_SET + self._create_vint(len(d)))
				self.stack += 1
				for sd in d:
					self._dump(sd)
				self.stack -= 1
			else:
				self.buffer.write(self.OP_ZERO_SET)
		else:
			raise PackingError("Packing {} type is not supported".format(dt))

def dumps(data:Any, *, version:int=HIGHEST_VERSION, recursiveLimit:int=512) -> bytes:
	if version == 2:
		return Packer_ver2(recursiveLimit=recursiveLimit).dumps(data)
	raise PackingError("Unsupported packer version: {}".format(version))

def dump(data:Any, file:IO[bytes], *, version:int=HIGHEST_VERSION, recursiveLimit:int=512) -> None:
	if not hasattr(file, "write"):
		raise PackingError("Stream does not have write method")
	if version == 2:
		return Packer_ver2(recursiveLimit=recursiveLimit).dump(data, file)
	raise PackingError("Unsupported packer version: {}".format(version))

class Unpacker_ver2(_OP_CODES_ver2):
	maxIndexSize:int
	recursiveLimit:int
	buffer:Union[BytesIO, IO[bytes]]
	index:List[Any]
	stack:int
	OPs:Dict[bytes, Any]
	def __init__(self, maxIndexSize:int=0, recursiveLimit:int=512):
		self.maxIndexSize   = maxIndexSize
		self.recursiveLimit = recursiveLimit
		self.index          = []
		self.stack          = 0
		self.OPs            = {
			self.OP_NONE:         None,
			self.OP_BOOL_FALSE:   False,
			self.OP_BOOL_TRUE:    True,
			self.OP_ZERO_INTERGER:0,
			self.OP_ZERO_FLOAT:   0.0,
			self.OP_ZERO_UNICODE: "",
			self.OP_ZERO_BYTES:   b"",
			self.OP_INF_FLOAT:    float("inf"),
			self.OP_NEG_INF_FLOAT:float("-inf"),
		}
	def load(self, file:IO[bytes]) -> Any:
		self.buffer = file
		return self._parse()
	def loads(self, data:bytes) -> Any:
		self.buffer = BytesIO(data)
		return self._parse()
	def _read_vint(self) -> int:
		d = self._read(1)
		if d[0] < 0xFD:
			return d[0]
		elif d[0] == 0xFD:
			return int.from_bytes(self._read(2), "little")
		elif d[0] == 0xFE:
			return int.from_bytes(self._read(3), "little")
		return int.from_bytes(self._read(4), "little")
	def _read(self, size:int) -> bytes:
		b = self.buffer.read(size)
		if len(b) != size:
			raise UnpackingError("End of buffer/Not enough data")
		return b
	def _parse(self) -> Any:
		r:Any = None
		if self.stack == self.recursiveLimit:
			raise UnpackingError("Recusive limit reached")
		op = self._read(1)
		if op[0] < self.OP_NONE[0]:
			if op[0] < self.VINT_2BYTES[0]:
				return self.index[ op[0] ]
			elif op[0] == self.VINT_2BYTES[0]:
				return self.index[ int.from_bytes(self._read(2), "little") ]
			elif op[0] == self.VINT_3BYTES[0]:
				return self.index[ int.from_bytes(self._read(3), "little") ]
			return self.index[ int.from_bytes(self._read(4), "little") ]
		elif op in self.OPs:
			return self.OPs[op]
		elif op == self.OP_ZERO_LIST:
			return tuple()
		elif op == self.OP_ZERO_DICT:
			return dict()
		elif op == self.OP_ZERO_SET:
			return set()
		elif op == self.OP_CHAR_INTERGER:
			r = int.from_bytes(self._read(1), "little")
		elif op == self.OP_NEG_CHAR_INTERGER:
			r = -int.from_bytes(self._read(1), "little")
		elif op == self.OP_SHORT_INTERGER:
			r = int.from_bytes(self._read(2), "little")
		elif op == self.OP_NEG_SHORT_INTERGER:
			r = -int.from_bytes(self._read(2), "little")
		elif op == self.OP_INTERGER:
			l = self._read_vint()
			r = int.from_bytes(self._read(l), "little")
		elif op == self.OP_NEG_INTERGER:
			l = self._read_vint()
			r = -int.from_bytes(self._read(l), "little")
		elif op == self.OP_FLOAT:
			r = struct.unpack("d", self._read(8))[0]
		elif op == self.OP_UNICODE:
			l = self._read_vint()
			r = self._read(l).decode()
		elif op == self.OP_BYTES:
			l = self._read_vint()
			r = self._read(l)
		if r is not None:
			self.index.append(r)
			if len(self.index) == self.maxIndexSize:
				raise UnpackingError("Max index size reached")
			return r
		self.stack += 1
		if op == self.OP_LIST:
			r = tuple(( self._parse() for i in range(self._read_vint()) ))
		elif op == self.OP_DICT:
			r = dict(( (self._parse(), self._parse())  for i in range(self._read_vint()) ))
		elif op == self.OP_SET:
			r = set([ self._parse() for i in range(self._read_vint()) ])
		else:
			raise UnpackingError("Unknown OP code: {}".format(op[0]))
		self.stack -= 1
		return r

def loads(data:bytes, maxIndexSize:int=0, recursiveLimit:int=512) -> Tuple[int, Any]:
	if type(data) is not bytes:
		raise UnpackingError("Only bytes can be unpacked, not {}".format(type(data)))
	if len(data) == 0:
		raise UnpackingError("Nothing to unpack")
	if data[0] == 2:
		return 2, Unpacker_ver2(maxIndexSize, recursiveLimit).loads(data[1:])
	raise UnpackingError("Unsupported packer version: {}".format(data[0]))

def load(file:IO[bytes], maxIndexSize:int=0, recursiveLimit:int=512) -> Tuple[int, Any]:
	if not hasattr(file, "read"):
		raise UnpackingError("Stream does not have read method")
	version = file.read(1)
	if len(version) == 0:
		raise UnpackingError("Nothing to unpack")
	if version[0] == 2:
		return 2, Unpacker_ver2(maxIndexSize, recursiveLimit).load(file)
	raise UnpackingError("Unsupported packer version: {}".format(version[0]))

