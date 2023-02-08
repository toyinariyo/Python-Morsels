from contextlib import redirect_stdout
from io import StringIO
import unittest


from earliest import get_earliest


class GetEarliestTests(unittest.TestCase):

    """Tests for get_earliest."""

    def test_zreturn_instead_of_print(self):
        with redirect_stdout(StringIO()) as stdout:
            actual = get_earliest("01/25/2024", "01/25/2025")
        output = stdout.getvalue().strip()
        if actual is None and output:
            self.fail(
                "\n\nUh oh!\n"
                "It looks like you may have printed instead of returning.\n"
                f"None was returned but this was printed:\n{output}"
            )

    def test_same_month_and_day(self):
        newer = "01/27/1832"
        older = "01/27/1756"
        self.assertEqual(get_earliest(newer, older), older)

    def test_february_29th(self):
        newer = "02/29/1972"
        older = "12/21/1946"
        self.assertEqual(get_earliest(newer, older), older)

    def test_smaller_month_bigger_day(self):
        newer = "03/21/1946"
        older = "02/24/1946"
        self.assertEqual(get_earliest(older, newer), older)

    def test_same_month_and_year(self):
        newer = "06/24/1958"
        older = "06/21/1958"
        self.assertEqual(get_earliest(older, newer), older)

    def test_invalid_date_allowed(self):
        newer = "02/29/2006"
        older = "02/28/2006"
        self.assertEqual(get_earliest(older, newer), older)

    def test_two_invalid_dates(self):
        newer = "02/30/2006"
        older = "02/29/2006"
        self.assertEqual(get_earliest(newer, older), older)

    def test_invalid_date_with_earlier_month_but_more_days(self):
        newer = "02/01/0000"
        older = "01/99/0000"
        self.assertEqual(get_earliest(newer, older), older)

    # To test bonus 1, comment out the next line
    @unittest.expectedFailure
    def test_many_dates(self):
        d1 = "01/24/2007"
        d2 = "01/21/2008"
        d3 = "02/29/2009"
        d4 = "02/30/2006"
        d5 = "02/28/2006"
        d6 = "02/29/2006"
        self.assertEqual(get_earliest(d1, d2, d3), d1)
        self.assertEqual(get_earliest(d1, d2, d3, d4), d4)
        self.assertEqual(get_earliest(d1, d2, d3, d4, d5, d6), d5)


class AllowUnexpectedSuccessRunner(unittest.TextTestRunner):
    """Custom test runner to avoid FAILED message on unexpected successes."""
    class resultclass(unittest.TextTestResult):
        def wasSuccessful(self):
            return not (self.failures or self.errors)


if __name__ == "__main__":
    from platform import python_version
    import sys
    if sys.version_info < (3, 6):
        sys.exit("Running {}.  Python 3.6 required.".format(python_version()))
    unittest.main(verbosity=2, testRunner=AllowUnexpectedSuccessRunner)
