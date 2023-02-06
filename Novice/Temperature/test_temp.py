from contextlib import redirect_stdout, redirect_stderr
import gc
from pathlib import Path
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from io import StringIO
import sys
import unittest
import warnings


class TempTests(unittest.TestCase):

    """
    Tests for temp.py.

    Print out feedback on the given temperature.
    """

    def test_72_degrees(self):
        output = run_program('temp.py', ['72'])
        self.assertEqual(output, "Quite nice\n")

    def test_85_degrees(self):
        output = run_program('temp.py', ['85'])
        self.assertEqual(output, "Too hot\n")

    def test_60_degrees(self):
        output = run_program('temp.py', ['60'])
        self.assertEqual(output, "Too cold\n")

    def test_65_degrees(self):
        output = run_program('temp.py', ['66'])
        self.assertEqual(output, "Quite nice\n")

    def test_80_degrees(self):
        output = run_program('temp.py', ['80'])
        self.assertEqual(output, "Quite nice\n")


class DummyException(Exception):
    """No code will ever raise this exception."""


try:
    DIRECTORY = Path(__file__).resolve().parent
except NameError:
    DIRECTORY = Path.cwd()


def run_program(path, args=[], raises=DummyException, stderr=False):
    """
    Run program at given path with given arguments.
    If raises is specified, ensure the given exception is raised.
    """
    path = str(DIRECTORY / path)
    old_args = sys.argv
    assert all(isinstance(a, str) for a in args)
    warnings.simplefilter("ignore", ResourceWarning)
    try:
        sys.argv = [path] + args
        with redirect_stdout(StringIO()) as output:
            error = StringIO() if stderr else output
            with redirect_stderr(error):
                try:
                    if '__main__' in sys.modules:
                        del sys.modules['__main__']
                    loader = SourceFileLoader('__main__', path)
                    spec = spec_from_loader(loader.name, loader)
                    module = module_from_spec(spec)
                    sys.modules['__main__'] = module
                    loader.exec_module(module)
                except raises:
                    pass
                except SystemExit as e:
                    if e.args != (0,):
                        raise SystemExit(output.getvalue()) from e
                else:
                    if raises is not DummyException:
                        raise AssertionError("{} not raised".format(raises))
                if stderr:
                    return output.getvalue(), error.getvalue()
                else:
                    return output.getvalue()
    finally:
        sys.argv = old_args
        # The next 3 lines seem to fix weird cyclic-reference issues
        if '__main__' in sys.modules:
            sys.modules['__main__'].__dict__.clear()
            sys.modules.pop('__main__', None)
        gc.collect()


if __name__ == "__main__":
    from platform import python_version
    if sys.version_info < (3, 6):
        sys.exit("Running {}.  Python 3.6 required.".format(python_version()))
    unittest.main(verbosity=2)
