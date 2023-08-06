# Builtin modules
import unittest, os, sys
from typing import Any
from tempfile import TemporaryFile
# Third party modules
# Local modules
from .. import dump, dumps, load, loads, UnpackingError, PackingError, ACCELERATION_IS_AVAILABLE
from ..fallback import (dump as pyDump, dumps as pyDumps, load as pyLoad, loads as pyLoads, UnpackingError as pyUnpackerError,
PackingError as pyPackerError)
# Program
def getRefs(input:Any) -> Any:
	if isinstance(input, (list, tuple)):
		return [ getRefs(i) for i in input ]
	elif isinstance(input, dict):
		return [ [getRefs(k), getRefs(v)] for k,v in input.items() ]
	return sys.getrefcount(input)

class FSPackerTest(unittest.TestCase):
	dataVer2:Any = (
		None,
		True,
		False,
		0,
		-1,
		1,
		1<<256,
		-(1<<256),
		0.0,
		0.1,
		-0.1,
		1.234e+16,
		1.234e-16,
		0.1000000000000001,
		float("inf"),
		float("-inf"),
		"",
		"test",
		"Ő",
		"\\ua4ad",
		b'\xf0\xa4\xad\xa2'.decode(),
		b"",
		b"\x00",
		b"\x00FF00",
		tuple(),
		dict(),
		{"data":"ok"},
		{None:0, 0:3, -1:4, 1:5, 255:6, -255:7, 0xFFFFFF:8, -0xFFFFFF:9, (1,2):10, 0.1:11, -0.1:12, float("inf"):13, \
		float("-inf"):14, "":15, "a":16, b"":17, b"a":18 },
		set(),
		set([1, "a", "test", "b", b"\x00"]),
		"F"*65000,
	)
	def test_acceleration(self) -> None:
		self.assertTrue(ACCELERATION_IS_AVAILABLE)
	def test_refcheck(self) -> None:
		data = [
			self.dataVer2,
			[self.dataVer2, self.dataVer2],
			(self.dataVer2, self.dataVer2),
			{False:self.dataVer2, None:self.dataVer2, True:self.dataVer2},
		]
		q = dumps(data)
		for i in range(2500):
			with self.assertRaises(UnpackingError):
				loads(q[:len(q)-1])
	def test_leakcheck(self) -> None:
		subData = os.urandom(1024*1024)
		data = [subData, [subData, subData], (subData, subData)]
		d = dumps(data)
		refDB1 = str(getRefs(data))
		with self.assertRaises(UnpackingError):
			loads(d[:len(d)-1])
		refDB2 = str(getRefs(data))
		self.assertEqual(refDB1, refDB2)
	def test_dumpsAndLoads_ver2(self) -> None:
		d:Any
		for d in self.dataVer2:
			self.assertEqual(loads(dumps( d, version=2)), (2, d))
			self.assertEqual(loads(pyDumps( d, version=2)), (2, d))
			self.assertEqual(pyLoads(pyDumps( d, version=2)), (2, d))
			self.assertEqual(pyLoads(dumps( d, version=2)), (2, d))
		self.assertTupleEqual(loads(dumps( self.dataVer2, version=2)), (2, self.dataVer2))
		self.assertTupleEqual(loads(dumps( (self.dataVer2, self.dataVer2), version=2 )), (2, (self.dataVer2, self.dataVer2)))
		self.assertTupleEqual(loads(dumps( [self.dataVer2, self.dataVer2], version=2 )), (2, (self.dataVer2, self.dataVer2)))
		self.assertTupleEqual(loads(dumps( {"data":self.dataVer2}, version=2 )), (2, {"data":self.dataVer2}))
		self.assertTupleEqual(pyLoads(pyDumps( self.dataVer2, version=2)), (2, self.dataVer2))
		self.assertTupleEqual(pyLoads(pyDumps( (self.dataVer2, self.dataVer2), version=2 )), (2, (self.dataVer2,self.dataVer2)))
		self.assertTupleEqual(pyLoads(pyDumps( [self.dataVer2, self.dataVer2], version=2 )), (2, (self.dataVer2,self.dataVer2)))
		self.assertTupleEqual(pyLoads(pyDumps( {"data":self.dataVer2}, version=2 )), (2, {"data":self.dataVer2}))
		return None
	def test_dumpAndLoad_ver2(self) -> None:
		with TemporaryFile() as fi:
			dump(self.dataVer2, fi, version=2)
			fi.flush()
			fi.seek(0)
			self.assertEqual(load(fi), (2, self.dataVer2))
			fi.seek(0)
			self.assertEqual(pyLoad(fi), (2, self.dataVer2))
			fi.seek(0)
			pyDump(self.dataVer2, fi, version=2)
			fi.flush()
			fi.seek(0)
			self.assertEqual(load(fi), (2, self.dataVer2))
			fi.seek(0)
			self.assertEqual(pyLoad(fi), (2, self.dataVer2))
		return None
	def test_packing_errors_ver2(self) -> None:
		with self.assertRaises(PackingError):
			dumps(range(2), version=2)
		with self.assertRaises(pyPackerError):
			pyDumps(range(2), version=2)
		with self.assertRaises(PackingError):
			dumps([[[1]]], version=2, recursiveLimit=2)
		with self.assertRaises(pyPackerError):
			pyDumps([[[1]]], version=2, recursiveLimit=2)
		with TemporaryFile() as fi:
			with self.assertRaises(PackingError):
				dump(range(2), fi, version=2)
			with self.assertRaises(pyPackerError):
				pyDump(range(2), fi, version=2)
			with self.assertRaises(PackingError):
				dump([[[1]]], fi, version=2, recursiveLimit=2)
			with self.assertRaises(pyPackerError):
				pyDump([[[1]]], fi, version=2, recursiveLimit=2)
		with TemporaryFile() as fi:
			with self.assertRaises(PackingError):
				dump(range(2), fi, version=2)
			with self.assertRaises(pyPackerError):
				pyDump(range(2), fi, version=2)
			with self.assertRaises(PackingError):
				dump([[[1]]], fi, version=2, recursiveLimit=2)
			with self.assertRaises(pyPackerError):
				pyDump([[[1]]], fi, version=2, recursiveLimit=2)
	def test_unpacking_errors_ver2(self) -> None:
		d:bytes = dumps(self.dataVer2, version=2)
		with self.assertRaises(UnpackingError):
			loads(d[:-1])
		with self.assertRaises(pyUnpackerError):
			pyLoads(d[:-1])
		with self.assertRaises(UnpackingError):
			loads(b"\xff" + d[1:])
		with self.assertRaises(pyUnpackerError):
			pyLoads(b"\xff" + d[1:])
		d = dumps([[[1]]], version=2)
		with self.assertRaises(UnpackingError):
			loads(d, recursiveLimit=2)
		with self.assertRaises(pyUnpackerError):
			pyLoads(d, recursiveLimit=2)
		with TemporaryFile() as fi:
			dump(self.dataVer2, fi, version=2)
			fi.flush()
			fi.seek(-1, 2)
			fi.truncate()
			fi.seek(0)
			with self.assertRaises(UnpackingError):
				load(fi)
			fi.seek(0)
			with self.assertRaises(pyUnpackerError):
				pyLoad(fi)
			dump(self.dataVer2, fi, version=2)
			fi.flush()
			fi.seek(0)
			fi.write(b"\xff")
			fi.seek(0)
			with self.assertRaises(UnpackingError):
				load(fi)
			fi.seek(0)
			with self.assertRaises(pyUnpackerError):
				pyLoad(fi)
		return None
