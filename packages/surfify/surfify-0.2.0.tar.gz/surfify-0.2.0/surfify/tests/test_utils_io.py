# -*- coding: utf-8 -*-
##########################################################################
# NSAp - Copyright (C) CEA, 2021
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# Imports
import os
import sys
import unittest
import tempfile
import numpy as np
from time import time
from io import StringIO
from surfify.utils.io import HidePrints, compute_and_store


class TestUtilsSampling(unittest.TestCase):
    """ Test spherical sampling.
    """
    def setUp(self):
        """ Setup test.
        """
        pass

    def tearDown(self):
        """ Run after each test.
        """
        pass

    def test_hideprints(self):
        """ Test HidePrints class.
        """
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()

        with HidePrints():
            print("hey")
        sys.stdout = old_stdout
        self.assertTrue(mystdout.getvalue() == "")

        old_stderr = sys.stderr
        sys.stderr = mystderr = StringIO()

        with HidePrints():
            print("hey", file=sys.stderr)
        sys.stderr = old_stderr
        self.assertTrue(mystderr.getvalue() == "hey\n")

        old_stderr = sys.stderr
        sys.stderr = mystderr = StringIO()

        with HidePrints(hide_err=True):
            print("hey", file=sys.stderr)
        sys.stderr = old_stderr
        self.assertTrue(mystderr.getvalue() == "")

    def test_compute_and_store(self):
        """ Test compute and store decorator
        """
        def multiplication(a, b):
            for idx in range(b):
                a += a
            return {"ab": a}

        def fast_function(a, b, c, ab=None):
            if ab is None:
                ab = a * b
            return ab * c

        with tempfile.TemporaryDirectory() as tmpdirname:
            cached_fast_function = compute_and_store(
                multiplication, tmpdirname)(fast_function)
            a = np.random.randint(1000, 5000)
            start = time()
            res_1 = cached_fast_function(a, 1000, 5)
            first_time = time() - start
            start = time()
            res_2 = cached_fast_function(a, 1000, 5)
            second_time = time() - start

        # self.assertTrue(second_time < first_time)
        self.assertTrue(res_1 == res_2)


if __name__ == "__main__":
    from surfify.utils import setup_logging

    setup_logging(level="debug")
    unittest.main()
