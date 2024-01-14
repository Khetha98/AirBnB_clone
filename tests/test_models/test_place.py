#!/usr/bin/python3
"""Unittests for the city module.
"""
import os
import unittest
from models.engine.file_storage import FileStorage
from models.place import Place
from models import storage
from datetime import datetime


class TestPlace(unittest.TestCase):
    """The test cases for the Place class."""

    def setUp(self):
        pass

    def tearDown(self) -> None:
        """It resets FileStorage data."""
        FileStorage._FileStorage__objects = {}
        if os.path.exists(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_params(self):
        """It a test method for class attributes"""

        b1 = Place()
        b3 = Place("hello", "wait", "in")
        k = f"{type(b1).__name__}.{b1.id}"
        self.assertIsInstance(b1.name, str)
        self.assertIn(k, storage.all())
        self.assertEqual(b3.name, "")

        self.assertIsInstance(b1.name, str)
        self.assertIsInstance(b1.user_id, str)
        self.assertIsInstance(b1.city_id, str)
        self.assertIsInstance(b1.description, str)
        self.assertIsInstance(b1.number_bathrooms, int)
        self.assertIsInstance(b1.number_rooms, int)
        self.assertIsInstance(b1.price_by_night, int)
        self.assertIsInstance(b1.max_guest, int)
        self.assertIsInstance(b1.longitude, float)
        self.assertIsInstance(b1.latitude, float)
        self.assertIsInstance(b1.amenity_ids, list)

    def test_init(self):
        """It a test method for public instances"""

        b1 = Place()
        p2 = Place(**b1.to_dict())
        self.assertIsInstance(b1.id, str)
        self.assertIsInstance(b1.created_at, datetime)
        self.assertIsInstance(b1.updated_at, datetime)
        self.assertEqual(b1.updated_at, p2.updated_at)

    def test_str(self):
        """It a test method for str representation"""
        b1 = Place()
        string = f"[{type(b1).__name__}] ({b1.id}) {b1.__dict__}"
        self.assertEqual(b1.__str__(), string)

    def test_save(self):
        """It a test method for save"""
        b1 = Place()
        old_update = b1.updated_at
        b1.save()
        self.assertNotEqual(b1.updated_at, old_update)

    def test_todict(self):
        """It a test method for dict"""
        b1 = Place()
        p2 = Place(**b1.to_dict())
        a_dict = p2.to_dict()
        self.assertIsInstance(a_dict, dict)
        self.assertEqual(a_dict['__class__'], type(p2).__name__)
        self.assertIn('created_at', a_dict.keys())
        self.assertIn('updated_at', a_dict.keys())
        self.assertNotEqual(b1, p2)


if __name__ == "__main__":
    unittest.main()
