#!/usr/bin/python3
"""Unittests for the city module.
"""
import os
import unittest
from models.engine.file_storage import FileStorage
from models import storage
from models.city import City
from datetime import datetime

b1 = City()
b2 = City(**b1.to_dict())
b3 = City("hello", "wait", "in")


class TestCity(unittest.TestCase):
    """The test cases for the City class."""

    def setUp(self):
        pass

    def tearDown(self) -> None:
        """It resets the FileStorage data."""
        FileStorage._FileStorage__objects = {}
        if os.path.exists(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_params(self):
        """It test method for class attributes"""
        k = f"{type(b1).__name__}.{b1.id}"
        self.assertIsInstance(b1.name, str)
        self.assertEqual(b3.name, "")
        b1.name = "Durban"
        self.assertEqual(b1.name, "Durban")

    def test_init(self):
        """It test method for public instances"""
        self.assertIsInstance(b1.id, str)
        self.assertIsInstance(b1.created_at, datetime)
        self.assertIsInstance(b1.updated_at, datetime)
        self.assertEqual(b1.updated_at, b2.updated_at)

    def test_save(self):
        """It test method for save"""
        old_update = b1.updated_at
        b1.save()
        self.assertNotEqual(b1.updated_at, old_update)

    def test_todict(self):
        """It test method for dict"""
        a_dict = b2.to_dict()
        self.assertIsInstance(a_dict, dict)
        self.assertEqual(a_dict['__class__'], type(b2).__name__)
        self.assertIn('created_at', a_dict.keys())
        self.assertIn('updated_at', a_dict.keys())
        self.assertNotEqual(b1, b2)


if __name__ == "__main__":
    unittest.main()
