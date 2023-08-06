import unittest
from subprocess import CompletedProcess
import sys
from pathlib import Path
import os
from unittest.mock import patch, MagicMock
from os.path import dirname, abspath

MFROOT = str(dirname(dirname(abspath(__file__))))
if MFROOT not in sys.path:
    sys.path.insert(0, MFROOT)

from myfuncs import runcmd, ObjInfo  # noqa


class TestRunCmd(unittest.TestCase):
    def test_runcmd_with_output(self):
        # Mock the subprocess.run() function to return a CompletedProcess object
        mock_completed_process = CompletedProcess(
            args=['echo', 'Hello, World!'],
            returncode=0,
            stdout='Hello, World!\n',
            stderr='',
        )
        with patch('subprocess.run', return_value=mock_completed_process):
            result = runcmd('echo Hello, World!')

        self.assertEqual(result, ['Hello, World!'])

    def test_runcmd_without_output(self):
        # Mock the subprocess.run() function to return None
        with patch('subprocess.run'):
            result = runcmd('echo Hello, World!', output=False)

        self.assertIsNone(result)


class TestObjInfo(unittest.TestCase):
    def test_print_info(self):
        obj = TestObj()
        oinfo = ObjInfo(obj)
        with patch("builtins.print") as mock_print:
            oinfo.print_info()

        mock_print.assert_called()

    def test_obj_info_attributes(self):
        obj = TestObj()
        oinfo = ObjInfo(obj)
        self.assertEqual(oinfo.obj_name, 'objname')
        self.assertEqual(oinfo.obj_type, type(obj))
        for attstr in ["attr1", "attr2"]:
            self.assertTrue(attstr in oinfo.obj_attrs)
        for mstr in ["method1", "method2"]:
            self.assertTrue(mstr in oinfo.obj_methods)
        self.assertEqual(oinfo.obj_doc, "This is the documentation for TestObj")
        self.assertEqual(oinfo.obj_scope, "Local")
        self.assertEqual(oinfo.obj_mutability, "Mutable")
        self.assertEqual(oinfo.obj_identity, id(obj))


class TestObj:
    attr1 = "Attribute 1"
    attr2 = "Attribute 2"

    def method1(self):
        pass

    def method2(self):
        pass

    __doc__ = "This is the documentation for TestObj"
    __name__ = 'objname'


if __name__ == '__main__':
    unittest.main()
