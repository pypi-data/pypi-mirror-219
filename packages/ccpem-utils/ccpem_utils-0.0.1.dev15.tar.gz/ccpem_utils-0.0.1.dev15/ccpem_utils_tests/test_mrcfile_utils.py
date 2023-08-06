#
#     Copyright (C) 2021 CCP-EM
#
#     This code is distributed under the terms and conditions of the
#     CCP-EM Program Suite Licence Agreement as a CCP-EM Application.
#     A copy of the CCP-EM licence can be obtained by writing to the
#     CCP-EM Secretary, RAL Laboratory, Harwell, OX11 0FA, UK.
#

import unittest
import os
import tempfile
import math
import shutil
from ccpem_utils_tests import test_data
from ccpem_utils.map.mrcfile_utils import (
    crop_mrc_map,
    bin_mrc_map,
    pad_mrc_map,
    calc_mrc_sigma_contour,
    save_contour_mask,
    realspace_filter_map,
    add_softedge,
)
import mrcfile
from ccpem_utils.map.parse_mrcmapobj import MapObjHandle
import numpy as np


class MapParseTests(unittest.TestCase):
    def setUp(self):
        """
        Setup test data and output directories.
        """
        self.test_data = os.path.dirname(test_data.__file__)
        self.test_dir = tempfile.mkdtemp(prefix="map_parse")
        # Change to test directory
        self._orig_dir = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self._orig_dir)
        # print(self.test_dir)
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_map_crop(self):
        # read
        map_input = os.path.join(self.test_data, "emd_3488.mrc")
        crop_mrc_map(
            map_input, new_dim=(71, 73, 58), map_output="emd_3488_cropped1.mrc"
        )
        # check1
        with mrcfile.open("emd_3488_cropped1.mrc", mode="r") as mrc:
            wrapped_mapobj1 = MapObjHandle(mrc)
            assert wrapped_mapobj1.data.shape == (58, 73, 71)

    def test_map_pad(self):
        # read
        map_input = os.path.join(self.test_data, "emd_3488.mrc")
        pad_mrc_map(map_input, ext_dim=(10, 10, 10), map_output="emd_3488_padded.mrc")
        # check1
        with mrcfile.open("emd_3488_padded.mrc", mode="r") as mrc:
            wrapped_mapobj = MapObjHandle(mrc)
            assert wrapped_mapobj.data.shape == (110, 110, 110)

    def test_downsample(self):
        map_input = os.path.join(self.test_data, "emd_3488.mrc")
        bin_mrc_map(map_input, new_dim=50, map_output="emd_3488_downsampled_dim.mrc")
        # check
        with mrcfile.open("emd_3488_downsampled_dim.mrc", mode="r") as mrc:
            downsampled_mapobj = MapObjHandle(mrc)
            assert downsampled_mapobj.data.shape == (50, 50, 50)
            assert downsampled_mapobj.origin == (0.0, 0.0, 0.0)
            assert math.isclose(
                downsampled_mapobj.apix[0],
                2.1,
                rel_tol=0.00001,
            )
        bin_mrc_map(
            map_input,
            new_spacing=(2.1, 2.1, 2.1),
            map_output="emd_3488_downsampled.mrc",
        )
        # check
        with mrcfile.open("emd_3488_downsampled.mrc", mode="r") as mrc:
            downsampled_mapobj = MapObjHandle(mrc)
            assert downsampled_mapobj.data.shape == (50, 50, 50)
            assert downsampled_mapobj.origin == (0.0, 0.0, 0.0)
            assert math.isclose(
                downsampled_mapobj.apix[0],
                2.1,
                rel_tol=0.00001,
            )

    def test_sigma_contour(self):
        map_input = os.path.join(self.test_data, "emd_3488.mrc")
        sigma_contour = calc_mrc_sigma_contour(map_input, sigma_factor=2.0)
        # sigma_contour = 0.068012
        with mrcfile.open(map_input, mode="r", permissive=True) as mrc:
            assert math.isclose(sigma_contour, 2.0 * np.std(mrc.data), rel_tol=0.09)
            mrc_array = mrc.data
        save_contour_mask(map_input, sigma_factor=2.0)
        map_output = os.path.splitext(map_input)[0] + "_contour_mask.mrc"
        assert os.path.isfile(map_output)
        with mrcfile.open(map_output, mode="r", permissive=True) as mrc:
            assert np.sum(mrc_array > sigma_contour) == np.sum(mrc.data)

    def test_real_space_filters(self):
        map_input = os.path.join(self.test_data, "emd_3488.mrc")
        # generate two filtered maps and compare
        realspace_filter_map(map_input, filter_type="gaussian")
        realspace_filter_map(map_input, filter_type="tanh")
        assert math.isclose(
            os.stat(
                os.path.join(self.test_dir, "emd_3488_gaussian_filtered.mrc")
            ).st_size,
            os.stat(os.path.join(self.test_dir, "emd_3488_tanh_filtered.mrc")).st_size,
            rel_tol=0.05,
        )

    def test_smooth_maskedge(self):
        map_input = os.path.join(self.test_data, "emd_3488_contour_mask.mrc")
        add_softedge(map_input, edgetype="cosine", edge=3)
        add_softedge(map_input, edgetype="tanh", edge=3)
        assert math.isclose(
            os.stat(
                os.path.join(self.test_dir, "emd_3488_contour_mask_cosine_softmask.mrc")
            ).st_size,
            os.stat(
                os.path.join(self.test_dir, "emd_3488_contour_mask_tanh_softmask.mrc")
            ).st_size,
            rel_tol=0.05,
        )
