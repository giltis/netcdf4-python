import sys
import unittest
import os
import tempfile
import numpy as NP
from numpy.testing import assert_almost_equal
import netCDF4
import math

VAR_NAME='temp'
VAR_TYPE='f4'
VAR_VAL=math.pi
FILE_NAME = tempfile.mktemp(".nc")
GROUP_NAME = 'subgroup'

# test scalar variable creation and retrieval.

class ScalarVariableTestCase(unittest.TestCase):

    def setUp(self):
        self.file = FILE_NAME
        rootgrp = netCDF4.Dataset(self.file, 'w')
        # scalar variable.
        temp = rootgrp.createVariable(VAR_NAME,VAR_TYPE)
        #temp[:] = VAR_VAL
        temp.assignValue(VAR_VAL)
        subgroup = rootgrp.createGroup(GROUP_NAME)
        tempg = subgroup.createVariable(VAR_NAME,VAR_TYPE)
        tempg[:] = VAR_VAL
        #tempg.assignValue(VAR_VAL)
        rootgrp.close()

    def tearDown(self):
        # Remove the temporary file
        os.remove(self.file)

    def runTest(self):
        """testing dimensions"""
        # check dimensions in root group.
        f  = netCDF4.Dataset(self.file, 'r+')
        v = f.variables[VAR_NAME]
        # dimensions and shape should be empty tuples
        self.assert_(v.dimensions == ())
        self.assert_(v.shape == ())
        # check result of getValue and slice
        assert_almost_equal(v.getValue(), VAR_VAL, decimal=6)
        assert_almost_equal(v[:], VAR_VAL, decimal=6)
        g = f.groups[GROUP_NAME]
        vg = g.variables[VAR_NAME]
        # dimensions and shape should be empty tuples
        self.assert_(vg.dimensions == ())
        self.assert_(vg.shape == ())
        # check result of getValue and slice
        assert_almost_equal(vg.getValue(), VAR_VAL, decimal=6)
        assert_almost_equal(vg[:], VAR_VAL, decimal=6)
        f.close()

if __name__ == '__main__':
    unittest.main()