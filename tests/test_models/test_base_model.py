"""The testing of the base_model module"""
import unittest
from models.engine.file_storage import FileStorage
import os
from models.base_model import BaseModel
from datetime import datetime
import uuid


class TestBase(unittest.TestCase):
    """These are test cases for the Base class"""
    
    def setUp(self):
        pass


    def tearDown(self) -> None:
        """It resets te file storage data"""
        FileStorage._FileStorage__objects = {}
        if os.path.exists(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_initialization_positive(self):
        """Test the cases BaseModel initialization"""
        b1 = BaseModel()
        b2_uuid = str(uuid.uuid4())
        b2 = BaseModel(id=b2_uuid, name="The weeknd", album="Trilogy")
        self.assertIsInstance(b1.id, str)
        self.assertIsInstance(b2.id, str)
        self.assertEqual(b2_uuid, b2.id)
        self.assertEqual(b2.album, "Trilogy")
        self.assertEqual(b2.name, "The weeknd")
        self.assertIsInstance(b1.created_at, datetime)
        self.assertIsInstance(b1.created_at, datetime)
        self.assertEqual(str(type(b1)),
                         "<class 'models.base_model.BaseModel'>")
        
