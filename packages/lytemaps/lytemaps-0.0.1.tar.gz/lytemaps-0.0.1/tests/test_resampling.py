# -*- coding: utf-8 -*-
"""
Unit tests for resampling operations
"""

import pytest

from lytemaps import resampling


@pytest.mark.xfail
def test__estimate_density():
    assert False


@pytest.mark.xfail
def test_mni_transform():
    assert False


def test__check_altspec():
    spec = ('fsaverage', '10k')
    assert resampling._check_altspec(spec) == spec

    for spec in (None, ('fsaverage',), ('fsaverage', '100k')):
        with pytest.raises(ValueError):
            resampling._check_altspec(spec)
