# -*- coding: utf-8 -*-
"""
Unit tests for miscellaneous utilities
"""

import os
import pytest

from lytemaps import utils


def test_tmpname(tmp_path):
    out = utils.tmpname('.nii.gz', prefix='test', directory=tmp_path)
    assert (isinstance(out, os.PathLike) and out.name.startswith('test')
            and out.name.endswith('.nii.gz'))


@pytest.mark.xfail
def test_run():
    assert False


@pytest.mark.xfail
def test_check_fs_subjid():
    assert False
