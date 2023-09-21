#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.state import State


class test_state(unittest.TestCase):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "State"
        self.value = State()

    def test_name3(self):
        """ """
        self.assertEqual(type(self.value.name), str)
