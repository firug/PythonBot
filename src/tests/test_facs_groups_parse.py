import pytest


import sys
sys.path.append('../')
from facs_groups_parse import get_facs

class TestGetFaculties:
    faculties = get_facs()
    def test_not_empty(self):
        assert self.faculties.keys() != 0
    def test_check_format(self):
        for i in self.faculties.keys():
            assert type(i) == str

