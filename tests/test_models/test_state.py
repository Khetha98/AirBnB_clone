#!/usr/bin/python3
"""Unittests for the state module.
"""
import os
import unittest
from models.engine.file_storage import FileStorage
from models.state import State
from models import storage
from datetime import datetime


class TestState(unittest.TestCase):
    """The test cases for the State class."""

    def setUp(self):
        pass

    def tearDown(self) -> None:
        """It resets FileStorage data."""
        FileStorage._FileStorage__objects = {}
        if os.path.exists(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_params(self):
        a1 = State()
        a3 = State("hello", "wait", "in")

        k = f"{type(a1).__name__}.{a1.id}"
        self.assertIsInstance(a1.name, str)
        self.assertEqual(a3.name, "")
        a1.name = "Chicago"
        self.assertEqual(a1.name, "Chicago")
        self.assertIn(k, storage.all())

    def test_init(self):
        """It a test method for public instances"""
        a1 = State()
        s2 = State(**a1.to_dict())
        self.assertIsInstance(a1.id, str)
        self.assertIsInstance(a1.created_at, datetime)
        self.assertIsInstance(a1.updated_at, datetime)
        self.assertEqual(a1.updated_at, s2.updated_at)

    def test_str(self):
        """It a test method for str representation"""
        a1 = State()
        string = f"[{type(a1).__name__}] ({a1.id}) {a1.__dict__}"
        self.assertEqual(a1.__str__(), string)

    def test_save(self):
        """It a test method for save"""
        a1 = State()
        old_update = a1.updated_at
        a1.save()
        self.assertNotEqual(a1.updated_at, old_update)

    def test_todict(self):
        """It a test method for dict"""
        a1 = State()
        s2 = State(**a1.to_dict())
        a_dict = s2.to_dict()
        self.assertIsInstance(a_dict, dict)
        self.assertEqual(a_dict['__class__'], type(s2).__name__)
        self.assertIn('created_at', a_dict.keys())
        self.assertIn('updated_at', a_dict.keys())
        self.assertNotEqual(a1, s2)


if __name__ == "__main__":
    unittest.main()
