#!/usr/bin/python3
"""Defines unittests for console.py.
"""
from io import StringIO
import os
import unittest
from unittest.mock import patch
from console import HBNBCommand
from models import storage
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class TestConsole(unittest.TestCase):
    """Base class for testing Console.
    """

    def setUp(self):
        pass

    def tearDown(self) -> None:
        """Resets FileStorage data."""
        storage._FileStorage__objects = {}
        if os.path.exists(storage._FileStorage__file_path):
            os.remove(storage._FileStorage__file_path)

    def test_simple(self):
        """Tests basic commands.
        """

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("quit")
            self.assertEqual(f.getvalue(), "")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("EOF")
            self.assertEqual(f.getvalue(), "\n")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("\n")
            self.assertEqual(f.getvalue(), "")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("?")
            self.assertIsInstance(f.getvalue(), str)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help")
            self.assertIsInstance(f.getvalue(), str)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("? create")
            self.assertIsInstance(f.getvalue(), str)
            self.assertEqual(f.getvalue().strip(), "It creates the new instance.")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help create")
            self.assertIsInstance(f.getvalue(), str)
            self.assertEqual(f.getvalue().strip(), "It creates the new instance.")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("? all")
            self.assertIsInstance(f.getvalue(), str)
            self.assertEqual(f.getvalue().strip(),
                             "It prints out string representation of the instances.")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help all")
            self.assertIsInstance(f.getvalue(), str)
            self.assertEqual(f.getvalue().strip(),
                             "It prints out string representation of the instances.")

        with patch('sys.stdout', new=StringIO()) as f:
            msg = "It prints the string representation of the instance."
            HBNBCommand().onecmd("? show")
            self.assertIsInstance(f.getvalue(), str)
            self.assertEqual(f.getvalue().strip(),
                             msg)

        with patch('sys.stdout', new=StringIO()) as f:
            msg = "It prints the string representation of the instance."
            HBNBCommand().onecmd("help show")
            self.assertIsInstance(f.getvalue(), str)
            self.assertEqual(f.getvalue().strip(),
                             msg)

        with patch('sys.stdout', new=StringIO()) as f:
            msg = "It updates the instance based on a class name and id."
            HBNBCommand().onecmd("? update")
            self.assertIsInstance(f.getvalue(), str)
            self.assertEqual(f.getvalue().strip(),
                             msg)

        with patch('sys.stdout', new=StringIO()) as f:
            msg = "It updates the instance based on a class name and id."
            HBNBCommand().onecmd("help update")
            self.assertIsInstance(f.getvalue(), str)
            self.assertEqual(f.getvalue().strip(),
                             msg)

        with patch('sys.stdout', new=StringIO()) as f:
            msg = "It deletes the instance based on class name and id."
            HBNBCommand().onecmd("? destroy")
            self.assertIsInstance(f.getvalue(), str)
            self.assertEqual(f.getvalue().strip(),
                             msg)

        with patch('sys.stdout', new=StringIO()) as f:
            msg = "It deletes the instance based on class name and id."
            HBNBCommand().onecmd("help destroy")
            self.assertIsInstance(f.getvalue(), str)
            self.assertEqual(f.getvalue().strip(), msg)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("? quit")
            self.assertIsInstance(f.getvalue(), str)
            self.assertEqual(f.getvalue().strip(),
                             "Quit command to exit the program.")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help quit")
            self.assertIsInstance(f.getvalue(), str)
            self.assertEqual(f.getvalue().strip(),
                             "Quit command to exit the program.")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("? help")
            self.assertIsInstance(f.getvalue(), str)
            self.assertEqual(f.getvalue().strip(),
                             "To get help on a command, type help <topic>.")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help help")
            self.assertIsInstance(f.getvalue(), str)
            self.assertEqual(f.getvalue().strip(),
                             "To get help on a command, type help <topic>.")


class TestBaseModel(unittest.TestCase):
    """For Testing the Basemodel commands.
    """

    def setUp(self):
        pass

    def tearDown(self) -> None:
        """It resets the FileStorage data."""
        storage._FileStorage__objects = {}
        if os.path.exists(storage._FileStorage__file_path):
            os.remove(storage._FileStorage__file_path)

    def test_create_basemodel(self):
        """It test the create basemodel object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create BaseModel')
            self.assertIsInstance(f.getvalue().strip(), str)
            self.assertIn("BaseModel.{}".format(
                f.getvalue().strip()), storage.all().keys())

    def test_all_basemodel(self):
        """ It test the basemodel object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('all BaseModel')
            for item in json.loads(f.getvalue()):
                self.assertEqual(item.split()[0], '[BaseModel]')

    def test_show_basemodel(self):
        """It test the show of basemodel object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            b1 = BaseModel()
            b1.eyes = "green"
            HBNBCommand().onecmd(f'show BaseModel {b1.id}')
            res = f"[{type(b1).__name__}] ({b1.id}) {b1.__dict__}"
            self.assertEqual(f.getvalue().strip(), res)

    def test_update_basemodel(self):
        """It test an update basemodel object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            b1 = BaseModel()
            b1.name = "Cecilia"
            HBNBCommand().onecmd(f'update BaseModel {b1.id} name "Ife"')
            self.assertEqual(b1.__dict__["name"], "Ife")

        with patch('sys.stdout', new=StringIO()) as f:
            b1 = BaseModel()
            b1.age = 75
            HBNBCommand().onecmd(f'update BaseModel {b1.id} age 25')
            self.assertIn("age", b1.__dict__.keys())
            self.assertEqual(b1.__dict__["age"], 25)

        with patch('sys.stdout', new=StringIO()) as f:
            b1 = BaseModel()
            b1.savings = 25.67
            HBNBCommand().onecmd(f'update BaseModel {b1.id} savings 35.89')
            self.assertIn("savings", b1.__dict__.keys())
            self.assertEqual(b1.__dict__["savings"], 35.89)

        with patch('sys.stdout', new=StringIO()) as f:
            b1 = BaseModel()
            b1.age = 60
            cmmd = f'update BaseModel {b1.id} age 10 color "green"'
            HBNBCommand().onecmd(cmmd)
            self.assertIn("age", b1.__dict__.keys())
            self.assertNotIn("color", b1.__dict__.keys())
            self.assertEqual(b1.__dict__["age"], 10)

    def test_destroy_basemodel(self):
        """It test the destroy of basemodel object.
        """
        with patch('sys.stdout', new=StringIO()):
            bm = BaseModel()
            HBNBCommand().onecmd(f'destroy BaseModel {bm.id}')
            self.assertNotIn("BaseModel.{}".format(
                bm.id), storage.all().keys())


class TestBaseModelDotNotation(unittest.TestCase):
    """For testing Basemodel commands using dot notation.
    """

    def setUp(self):
        pass

    def tearDown(self) -> None:
        """It resets FileStorage data."""
        storage._FileStorage__objects = {}
        if os.path.exists(storage._FileStorage__file_path):
            os.remove(storage._FileStorage__file_path)

    def test_create_basemodel(self):
        """It test creation of basemodel object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(HBNBCommand().precmd(
                                 'BaseModel.create()'))
            self.assertIsInstance(f.getvalue().strip(), str)
            self.assertIn("BaseModel.{}".format(
                f.getvalue().strip()), storage.all().keys())

    def test_count_basemodel(self):
        """For test count of basemodel object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(HBNBCommand().precmd('BaseModel.count()'))
            count = 0
            for i in storage.all().values():
                if type(i) == BaseModel:
                    count += 1
            self.assertEqual(int(f.getvalue()), count)

    def test_all_basemodel(self):
        """It test all the basemodel object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(HBNBCommand().precmd('BaseModel.all()'))
            for item in json.loads(f.getvalue()):
                self.assertEqual(item.split()[0], '[BaseModel]')

    def test_show_basemodel(self):
        """It test the show basemodel object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            b1 = BaseModel()
            b1.eyes = "green"
            HBNBCommand().onecmd(HBNBCommand().precmd(
                                 f'BaseModel.show({b1.id})'))
            res = f"[{type(b1).__name__}] ({b1.id}) {b1.__dict__}"
            self.assertEqual(f.getvalue().strip(), res)

    def test_update_basemodel(self):
        """It test update of basemodel object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            b1 = BaseModel()
            b1.name = "Cecilia"
            HBNBCommand().onecmd(HBNBCommand().precmd(
                                 f'BaseModel.update({b1.id}, name, "Ife")'))
            self.assertEqual(b1.__dict__["name"], "Ife")

        with patch('sys.stdout', new=StringIO()) as f:
            b1 = BaseModel()
            b1.age = 75
            HBNBCommand().onecmd(HBNBCommand().precmd(
                                 f'BaseModel.update({b1.id}, age, 25)'))
            self.assertIn("age", b1.__dict__.keys())
            self.assertEqual(b1.__dict__["age"], 25)

        with patch('sys.stdout', new=StringIO()) as f:
            b1 = BaseModel()
            b1.age = 60
            cmmd = f'BaseModel.update({b1.id}, age, 10, color, green)'
            HBNBCommand().onecmd(HBNBCommand().precmd(cmmd))
            self.assertIn("age", b1.__dict__.keys())
            self.assertNotIn("color", b1.__dict__.keys())
            self.assertEqual(b1.__dict__["age"], 10)

    def test_update_basemodel_dict(self):
        """It test update of the basemodel object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            b1 = BaseModel()
            b1.age = 75
            cmmd = f'BaseModel.update({b1.id}, {{"age": 25,"color":"black"}})'
            HBNBCommand().onecmd(HBNBCommand().precmd(cmmd))
            self.assertEqual(b1.__dict__["age"], 25)
            self.assertIsInstance(b1.__dict__["age"], int)

    def test_destroy_basemodel(self):
        """It test the destroy basemodel object.
        """
        with patch('sys.stdout', new=StringIO()):
            bm = BaseModel()
            HBNBCommand().onecmd(HBNBCommand().precmd(
                                 f'BaseModel.destroy({bm.id})'))
            self.assertNotIn("BaseModel.{}".format(
                bm.id), storage.all().keys())


class TestUser(unittest.TestCase):
    """ For testing the user commands.
    """

    def setUp(self):
        pass

    def tearDown(self) -> None:
        """It resets the FileStorage data."""
        storage._FileStorage__objects = {}
        if os.path.exists(storage._FileStorage__file_path):
            os.remove(storage._FileStorage__file_path)

    def test_create_user(self):
        """It test create user object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create User')
            self.assertIsInstance(f.getvalue().strip(), str)
            self.assertIn("User.{}".format(
                f.getvalue().strip()), storage.all().keys())

    def test_all_user(self):
        """It test all the user object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('all User')
            for item in json.loads(f.getvalue()):
                self.assertEqual(item.split()[0], '[User]')

    def test_show_user(self):
        """It test show of user object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            us = User()
            us.eyes = "green"
            HBNBCommand().onecmd(f'show User {us.id}')
            res = f"[{type(us).__name__}] ({us.id}) {us.__dict__}"
            self.assertEqual(f.getvalue().strip(), res)

    def test_update_user(self):
        """It test update of user object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            us = User()
            us.name = "Cecilia"
            HBNBCommand().onecmd(f'update User {us.id} name "Ife"')
            self.assertEqual(us.__dict__["name"], "Ife")

        with patch('sys.stdout', new=StringIO()) as f:
            us = User()
            us.age = 75
            HBNBCommand().onecmd(f'update User {us.id} age 25')
            self.assertIn("age", us.__dict__.keys())
            self.assertEqual(us.__dict__["age"], 25)

        with patch('sys.stdout', new=StringIO()) as f:
            us = User()
            us.savings = 25.67
            HBNBCommand().onecmd(f'update User {us.id} savings 35.89')
            self.assertIn("savings", us.__dict__.keys())
            self.assertEqual(us.__dict__["savings"], 35.89)

        with patch('sys.stdout', new=StringIO()) as f:
            us = User()
            us.age = 60
            cmmd = f'update User {us.id} age 10 color green'
            HBNBCommand().onecmd(cmmd)
            self.assertIn("age", us.__dict__.keys())
            self.assertNotIn("color", us.__dict__.keys())
            self.assertEqual(us.__dict__["age"], 10)

    def test_destroy_user(self):
        """It test destroy of user object.
        """
        with patch('sys.stdout', new=StringIO()):
            us = User()
            HBNBCommand().onecmd(f'destroy User {us.id}')
            self.assertNotIn("User.{}".format(
                us.id), storage.all().keys())


class TestUserDotNotation(unittest.TestCase):
    """For testing the user command's dot notation.
    """

    def setUp(self):
        pass

    def tearDown(self) -> None:
        """It resets the FileStorage data."""
        storage._FileStorage__objects = {}
        if os.path.exists(storage._FileStorage__file_path):
            os.remove(storage._FileStorage__file_path)

    def test_create_user(self):
        """It test create of user object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(HBNBCommand().precmd(
                                 'User.create()'))
            self.assertIsInstance(f.getvalue().strip(), str)
            self.assertIn("User.{}".format(
                f.getvalue().strip()), storage.all().keys())

    def test_count_user(self):
        """It test count of user object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(HBNBCommand().precmd('User.count()'))
            count = 0
            for i in storage.all().values():
                if type(i) == User:
                    count += 1
            self.assertEqual(int(f.getvalue()), count)

    def test_all_user(self):
        """It test all of user object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(HBNBCommand().precmd('User.all()'))
            for item in json.loads(f.getvalue()):
                self.assertEqual(item.split()[0], '[User]')

    def test_show_user(self):
        """It test show of user object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            us = User()
            us.eyes = "green"
            HBNBCommand().onecmd(HBNBCommand().precmd(
                                 f'User.show({us.id})'))
            res = f"[{type(us).__name__}] ({us.id}) {us.__dict__}"
            self.assertEqual(f.getvalue().strip(), res)

    def test_update_user(self):
        """It test update of user object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            us = User()
            us.name = "Cecilia"
            HBNBCommand().onecmd(HBNBCommand().precmd(
                                 f'User.update({us.id}, name, "Ife")'))
            self.assertEqual(us.__dict__["name"], "Ife")

        with patch('sys.stdout', new=StringIO()) as f:
            us = User()
            us.age = 75
            HBNBCommand().onecmd(HBNBCommand().precmd(
                                 f'User.update({us.id}, age, 25)'))
            self.assertIn("age", us.__dict__.keys())
            self.assertEqual(us.__dict__["age"], 25)

        with patch('sys.stdout', new=StringIO()) as f:
            us = User()
            us.age = 60
            cmmd = f'User.update({us.id}, age, 10, color, green)'
            HBNBCommand().onecmd(HBNBCommand().precmd(cmmd))
            self.assertIn("age", us.__dict__.keys())
            self.assertNotIn("color", us.__dict__.keys())
            self.assertEqual(us.__dict__["age"], 10)

    def test_update_user_dict(self):
        """It test update of user object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            us = User()
            us.age = 75
            cmmd = f'User.update({us.id}, {{"age": 25,"color":"black"}})'
            HBNBCommand().onecmd(HBNBCommand().precmd(cmmd))
            self.assertEqual(us.__dict__["age"], 25)
            self.assertIsInstance(us.__dict__["age"], int)

    def test_destroy_user(self):
        """It test destroy of user object.
        """
        with patch('sys.stdout', new=StringIO()):
            us = User()
            HBNBCommand().onecmd(HBNBCommand().precmd(
                                 f'User.destroy({us.id})'))
            self.assertNotIn("User.{}".format(
                us.id), storage.all().keys())


class TestState(unittest.TestCase):
    """For testing the state commands.
    """

    def setUp(self):
        pass

    def tearDown(self) -> None:
        """It resets the FileStorage data."""
        storage._FileStorage__objects = {}
        if os.path.exists(storage._FileStorage__file_path):
            os.remove(storage._FileStorage__file_path)

    def test_create_state(self):
        """It test create of state object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create State')
            self.assertIsInstance(f.getvalue().strip(), str)
            self.assertIn("State.{}".format(
                f.getvalue().strip()), storage.all().keys())

    def test_all_state(self):
        """It test all of state object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('all State')
            for item in json.loads(f.getvalue()):
                self.assertEqual(item.split()[0], '[State]')

    def test_show_state(self):
        """It test show of state object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            st = State()
            st.eyes = "green"
            HBNBCommand().onecmd(f'show State {st.id}')
            res = f"[{type(st).__name__}] ({st.id}) {st.__dict__}"
            self.assertEqual(f.getvalue().strip(), res)

    def test_update_state(self):
        """It test update of state object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            st = State()
            st.name = "Cecilia"
            HBNBCommand().onecmd(f'update State {st.id} name "Ife"')
            self.assertEqual(st.__dict__["name"], "Ife")

        with patch('sys.stdout', new=StringIO()) as f:
            st = State()
            st.age = 75
            HBNBCommand().onecmd(f'update State {st.id} age 25')
            self.assertIn("age", st.__dict__.keys())
            self.assertEqual(st.__dict__["age"], 25)

        with patch('sys.stdout', new=StringIO()) as f:
            st = State()
            st.age = 60
            cmmd = f'update State {st.id} age 10 color green'
            HBNBCommand().onecmd(cmmd)
            self.assertIn("age", st.__dict__.keys())
            self.assertNotIn("color", st.__dict__.keys())
            self.assertEqual(st.__dict__["age"], 10)

    def test_destroy_state(self):
        """It test destroy of state object.
        """
        with patch('sys.stdout', new=StringIO()):
            st = State()
            HBNBCommand().onecmd(f'destroy State {st.id}')
            self.assertNotIn("State.{}".format(
                st.id), storage.all().keys())


class TestStateDotNotation(unittest.TestCase):
    """For testing the state command's dot notation.
    """

    def setUp(self):
        pass

    def tearDown(self) -> None:
        """It resets the FileStorage data."""
        storage._FileStorage__objects = {}
        if os.path.exists(storage._FileStorage__file_path):
            os.remove(storage._FileStorage__file_path)

    def test_create_state(self):
        """It test create  of state object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(HBNBCommand().precmd(
                                 'State.create()'))
            self.assertIsInstance(f.getvalue().strip(), str)
            self.assertIn("State.{}".format(
                f.getvalue().strip()), storage.all().keys())

    def test_count_state(self):
        """It test count of state object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(HBNBCommand().precmd('State.count()'))
            count = 0
            for i in storage.all().values():
                if type(i) == State:
                    count += 1
            self.assertEqual(int(f.getvalue()), count)

    def test_all_state(self):
        """It test all of state object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(HBNBCommand().precmd('State.all()'))
            for item in json.loads(f.getvalue()):
                self.assertEqual(item.split()[0], '[State]')

    def test_show_state(self):
        """It test show of state object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            st = State()
            st.eyes = "green"
            HBNBCommand().onecmd(HBNBCommand().precmd(
                                 f'State.show({st.id})'))
            res = f"[{type(st).__name__}] ({st.id}) {st.__dict__}"
            self.assertEqual(f.getvalue().strip(), res)

    def test_update_state(self):
        """It test update of state object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            st = State()
            st.name = "Cecilia"
            HBNBCommand().onecmd(HBNBCommand().precmd(
                                 f'State.update({st.id}, name, "Ife")'))
            self.assertEqual(st.__dict__["name"], "Ife")

        with patch('sys.stdout', new=StringIO()) as f:
            st = State()
            st.age = 75
            HBNBCommand().onecmd(HBNBCommand().precmd(
                                 f'State.update({st.id}, age, 25)'))
            self.assertIn("age", st.__dict__.keys())
            self.assertEqual(st.__dict__["age"], 25)

        with patch('sys.stdout', new=StringIO()) as f:
            st = State()
            st.age = 60
            cmmd = f'State.update({st.id}, age, 10, color, green)'
            HBNBCommand().onecmd(HBNBCommand().precmd(cmmd))
            self.assertIn("age", st.__dict__.keys())
            self.assertNotIn("color", st.__dict__.keys())
            self.assertEqual(st.__dict__["age"], 10)

    def test_update_state_dict(self):
        """To test update of state object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            st = State()
            st.age = 75
            cmmd = f'State.update({st.id}, {{"age": 25,"color":"black"}})'
            HBNBCommand().onecmd(HBNBCommand().precmd(cmmd))
            self.assertEqual(st.__dict__["age"], 25)
            self.assertIsInstance(st.__dict__["age"], int)

    def test_destroy_state(self):
        """For testing destroy of state object.
        """
        with patch('sys.stdout', new=StringIO()):
            st = State()
            HBNBCommand().onecmd(HBNBCommand().precmd(
                                 f'State.destroy({st.id})'))
            self.assertNotIn("State.{}".format(
                st.id), storage.all().keys())


class TestReview(unittest.TestCase):
    """For Testing the review commands.
    """

    def setUp(self):
        pass

    def tearDown(self) -> None:
        """It resets the FileStorage data."""
        storage._FileStorage__objects = {}
        if os.path.exists(storage._FileStorage__file_path):
            os.remove(storage._FileStorage__file_path)

    def test_create_review(self):
        """It test create of review object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create Review')
            self.assertIsInstance(f.getvalue().strip(), str)
            self.assertIn("Review.{}".format(
                f.getvalue().strip()), storage.all().keys())

    def test_all_review(self):
        """It test all of review object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('all Review')
            for item in json.loads(f.getvalue()):
                self.assertEqual(item.split()[0], '[Review]')

    def test_show_review(self):
        """It test show of review object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            rv = Review()
            rv.eyes = "green"
            HBNBCommand().onecmd(f'show Review {rv.id}')
            res = f"[{type(rv).__name__}] ({rv.id}) {rv.__dict__}"
            self.assertEqual(f.getvalue().strip(), res)

    def test_update_review(self):
        """It test update of review object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            rv = Review()
            rv.name = "Cecilia"
            HBNBCommand().onecmd(f'update Review {rv.id} name "Ife"')
            self.assertEqual(rv.__dict__["name"], "Ife")

        with patch('sys.stdout', new=StringIO()) as f:
            rv = Review()
            rv.age = 75
            HBNBCommand().onecmd(f'update Review {rv.id} age 25')
            self.assertIn("age", rv.__dict__.keys())
            self.assertEqual(rv.__dict__["age"], 25)

        with patch('sys.stdout', new=StringIO()) as f:
            rv = Review()
            rv.age = 60
            cmmd = f'update Review {rv.id} age 10 color green)'
            HBNBCommand().onecmd(cmmd)
            self.assertIn("age", rv.__dict__.keys())
            self.assertNotIn("color", rv.__dict__.keys())
            self.assertEqual(rv.__dict__["age"], 10)

    def test_destroy_review(self):
        """It test destroy of review object.
        """
        with patch('sys.stdout', new=StringIO()):
            rv = Review()
            HBNBCommand().onecmd(f'destroy Review {rv.id}')
            self.assertNotIn("Review.{}".format(
                rv.id), storage.all().keys())


class TestReviewDotNotation(unittest.TestCase):
    """For testing the review command's dot notation.
    """

    def setUp(self):
        pass

    def tearDown(self) -> None:
        """It resets the FileStorage data."""
        storage._FileStorage__objects = {}
        if os.path.exists(storage._FileStorage__file_path):
            os.remove(storage._FileStorage__file_path)

    def test_create_review(self):
        """It test create of review object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(HBNBCommand().precmd(
                                 'Review.create()'))
            self.assertIsInstance(f.getvalue().strip(), str)
            self.assertIn("Review.{}".format(
                f.getvalue().strip()), storage.all().keys())

    def test_count_review(self):
        """I test count of review object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(HBNBCommand().precmd('Review.count()'))
            count = 0
            for i in storage.all().values():
                if type(i) == Review:
                    count += 1
            self.assertEqual(int(f.getvalue()), count)

    def test_all_review(self):
        """It test all of review object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(HBNBCommand().precmd('Review.all()'))
            for item in json.loads(f.getvalue()):
                self.assertEqual(item.split()[0], '[Review]')

    def test_show_review(self):
        """It test show review object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            rv = Review()
            rv.eyes = "green"
            HBNBCommand().onecmd(HBNBCommand().precmd(
                                 f'Review.show({rv.id})'))
            res = f"[{type(rv).__name__}] ({rv.id}) {rv.__dict__}"
            self.assertEqual(f.getvalue().strip(), res)

    def test_update_review(self):
        """It test update of review object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            rv = Review()
            rv.name = "Cecilia"
            HBNBCommand().onecmd(HBNBCommand().precmd(
                                 f'Review.update({rv.id}, name, "Ife")'))
            self.assertEqual(rv.__dict__["name"], "Ife")

        with patch('sys.stdout', new=StringIO()) as f:
            rv = Review()
            rv.age = 75
            HBNBCommand().onecmd(HBNBCommand().precmd(
                                 f'Review.update({rv.id}, age, 25)'))
            self.assertIn("age", rv.__dict__.keys())
            self.assertEqual(rv.__dict__["age"], 25)

        with patch('sys.stdout', new=StringIO()) as f:
            rv = Review()
            rv.age = 60
            cmmd = f'Review.update({rv.id}, age, 10, color, green)'
            HBNBCommand().onecmd(HBNBCommand().precmd(cmmd))
            self.assertIn("age", rv.__dict__.keys())
            self.assertNotIn("color", rv.__dict__.keys())
            self.assertEqual(rv.__dict__["age"], 10)

    def test_update_review_dict(self):
        """It test update of review object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            rv = Review()
            rv.age = 75
            cmmd = f'Review.update({rv.id}, {{"age": 25,"color":"black"}})'
            HBNBCommand().onecmd(HBNBCommand().precmd(cmmd))
            self.assertEqual(rv.__dict__["age"], 25)
            self.assertIsInstance(rv.__dict__["age"], int)

    def test_destroy_review(self):
        """It test destroy of review object.
        """
        with patch('sys.stdout', new=StringIO()):
            rv = Review()
            HBNBCommand().onecmd(HBNBCommand().precmd(
                                 f'Review.destroy({rv.id})'))
            self.assertNotIn("Review.{}".format(
                rv.id), storage.all().keys())


class TestPlace(unittest.TestCase):
    """For testing the place commands.
    """

    def setUp(self):
        pass

    def tearDown(self) -> None:
        """It tesets the FileStorage data."""
        storage._FileStorage__objects = {}
        if os.path.exists(storage._FileStorage__file_path):
            os.remove(storage._FileStorage__file_path)

    def test_create_place(self):
        """It test create of place object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create Place')
            self.assertIsInstance(f.getvalue().strip(), str)
            self.assertIn("Place.{}".format(
                f.getvalue().strip()), storage.all().keys())

    def test_all_place(self):
        """It test all of place object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('all Place')
            for item in json.loads(f.getvalue()):
                self.assertEqual(item.split()[0], '[Place]')

    def test_show_place(self):
        """It test show of place object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            pl = Place()
            pl.eyes = "green"
            HBNBCommand().onecmd(f'show Place {pl.id}')
            res = f"[{type(pl).__name__}] ({pl.id}) {pl.__dict__}"
            self.assertEqual(f.getvalue().strip(), res)

    def test_update_place(self):
        """It test update of place object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            pl = Place()
            pl.name = "Cecilia"
            HBNBCommand().onecmd(f'update Place {pl.id} name "Ife"')
            self.assertEqual(pl.__dict__["name"], "Ife")

        with patch('sys.stdout', new=StringIO()) as f:
            pl = Place()
            pl.age = 75
            HBNBCommand().onecmd(f'update Place {pl.id} age 25')
            self.assertIn("age", pl.__dict__.keys())
            self.assertEqual(pl.__dict__["age"], 25)

        with patch('sys.stdout', new=StringIO()) as f:
            pl = Place()
            pl.age = 60
            cmmd = f'update Place {pl.id} age 10 color green'
            HBNBCommand().onecmd(cmmd)
            self.assertIn("age", pl.__dict__.keys())
            self.assertNotIn("color", pl.__dict__.keys())
            self.assertEqual(pl.__dict__["age"], 10)

    def test_destroy_place(self):
        """It test destroy of place object.
        """
        with patch('sys.stdout', new=StringIO()):
            pl = Place()
            HBNBCommand().onecmd(f'destroy Place {pl.id}')
            self.assertNotIn("Place.{}".format(
                pl.id), storage.all().keys())


class TestPlaceDotNotation(unittest.TestCase):
    """For testing the place command's dot notation.
    """

    def setUp(self):
        pass

    def tearDown(self) -> None:
        """It resets the FileStorage data."""
        storage._FileStorage__objects = {}
        if os.path.exists(storage._FileStorage__file_path):
            os.remove(storage._FileStorage__file_path)

    def test_create_place(self):
        """It test create of place object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(HBNBCommand().precmd(
                                 'Place.create()'))
            self.assertIsInstance(f.getvalue().strip(), str)
            self.assertIn("Place.{}".format(
                f.getvalue().strip()), storage.all().keys())

    def test_count_place(self):
        """It test count of place object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(HBNBCommand().precmd('Place.count()'))
            count = 0
            for i in storage.all().values():
                if type(i) == Place:
                    count += 1
            self.assertEqual(int(f.getvalue()), count)

    def test_all_place(self):
        """It test all of place object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(HBNBCommand().precmd('Place.all()'))
            for item in json.loads(f.getvalue()):
                self.assertEqual(item.split()[0], '[Place]')

    def test_show_place(self):
        """Test show place object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            pl = Place()
            pl.eyes = "green"
            HBNBCommand().onecmd(HBNBCommand().precmd(
                                 f'Place.show({pl.id})'))
            res = f"[{type(pl).__name__}] ({pl.id}) {pl.__dict__}"
            self.assertEqual(f.getvalue().strip(), res)

    def test_update_place(self):
        """Test update place object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            pl = Place()
            pl.name = "Cecilia"
            HBNBCommand().onecmd(HBNBCommand().precmd(
                                 f'Place.update({pl.id}, name, "Ife")'))
            self.assertEqual(pl.__dict__["name"], "Ife")

        with patch('sys.stdout', new=StringIO()) as f:
            pl = Place()
            pl.age = 75
            HBNBCommand().onecmd(HBNBCommand().precmd(
                                 f'Place.update({pl.id}, age, 25)'))
            self.assertIn("age", pl.__dict__.keys())
            self.assertEqual(pl.__dict__["age"], 25)

        with patch('sys.stdout', new=StringIO()) as f:
            pl = Place()
            pl.age = 60
            cmmd = f'Place.update({pl.id}, age, 10, color, green)'
            HBNBCommand().onecmd(HBNBCommand().precmd(cmmd))
            self.assertIn("age", pl.__dict__.keys())
            self.assertNotIn("color", pl.__dict__.keys())
            self.assertEqual(pl.__dict__["age"], 10)

    def test_update_place_dict(self):
        """It test update of place object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            pl = Place()
            pl.age = 75
            cmmd = f'Place.update({pl.id}, {{"age": 25,"color":"black"}})'
            HBNBCommand().onecmd(HBNBCommand().precmd(cmmd))
            self.assertEqual(pl.__dict__["age"], 25)
            self.assertIsInstance(pl.__dict__["age"], int)

    def test_destroy_place(self):
        """It test destroy of place object.
        """
        with patch('sys.stdout', new=StringIO()):
            pl = Place()
            HBNBCommand().onecmd(HBNBCommand().precmd(
                                 f'Place.destroy({pl.id})'))
            self.assertNotIn("Place.{}".format(
                pl.id), storage.all().keys())


class TestAmenity(unittest.TestCase):
    """For testing the amenity commands.
    """

    def setUp(self):
        pass

    def tearDown(self) -> None:
        """It resets the FileStorage data."""
        storage._FileStorage__objects = {}
        if os.path.exists(storage._FileStorage__file_path):
            os.remove(storage._FileStorage__file_path)

    def test_create_amenity(self):
        """It test create of amenity object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create Amenity')
            self.assertIsInstance(f.getvalue().strip(), str)
            self.assertIn("Amenity.{}".format(
                f.getvalue().strip()), storage.all().keys())

    def test_all_amenity(self):
        """It test all of amenity object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('all Amenity')
            for item in json.loads(f.getvalue()):
                self.assertEqual(item.split()[0], '[Amenity]')

    def test_show_amenity(self):
        """It test show of amenity object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            am = Amenity()
            am.eyes = "green"
            HBNBCommand().onecmd(f'show Amenity {am.id}')
            res = f"[{type(am).__name__}] ({am.id}) {am.__dict__}"
            self.assertEqual(f.getvalue().strip(), res)

    def test_update_amenity(self):
        """It test update of amenity object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            am = Amenity()
            am.name = "Cecilia"
            HBNBCommand().onecmd(f'update Amenity {am.id} name "Ife"')
            self.assertEqual(am.__dict__["name"], "Ife")

        with patch('sys.stdout', new=StringIO()) as f:
            am = Amenity()
            am.age = 75
            HBNBCommand().onecmd(f'update Amenity {am.id} age 25')
            self.assertIn("age", am.__dict__.keys())
            self.assertEqual(am.__dict__["age"], 25)

        with patch('sys.stdout', new=StringIO()) as f:
            am = Amenity()
            am.age = 60
            cmmd = f'update Amenity {am.id} age 10 color green)'
            HBNBCommand().onecmd(cmmd)
            self.assertIn("age", am.__dict__.keys())
            self.assertNotIn("color", am.__dict__.keys())
            self.assertEqual(am.__dict__["age"], 10)

    def test_destroy_amenity(self):
        """It test destroy of amenity object.
        """
        with patch('sys.stdout', new=StringIO()):
            am = Amenity()
            HBNBCommand().onecmd(f'destroy Amenity {am.id}')
            self.assertNotIn("Amenity.{}".format(
                am.id), storage.all().keys())


class TestAmenityDotNotation(unittest.TestCase):
    """ For testing the amenity command's dot notation.
    """

    def setUp(self):
        pass

    def tearDown(self) -> None:
        """It resets the FileStorage data."""
        storage._FileStorage__objects = {}
        if os.path.exists(storage._FileStorage__file_path):
            os.remove(storage._FileStorage__file_path)

    def test_create_amenity(self):
        """It test create of amenity object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(HBNBCommand().precmd(
                                 'Amenity.create()'))
            self.assertIsInstance(f.getvalue().strip(), str)
            self.assertIn("Amenity.{}".format(
                f.getvalue().strip()), storage.all().keys())

    def test_count_amenity(self):
        """It test count of amenity object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(HBNBCommand().precmd('Amenity.count()'))
            count = 0
            for i in storage.all().values():
                if type(i) == Amenity:
                    count += 1
            self.assertEqual(int(f.getvalue()), count)

    def test_all_amenity(self):
        """It test all of amenity object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(HBNBCommand().precmd('Amenity.all()'))
            for item in json.loads(f.getvalue()):
                self.assertEqual(item.split()[0], '[Amenity]')

    def test_show_amenity(self):
        """It test show of amenity object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            am = Amenity()
            am.eyes = "green"
            HBNBCommand().onecmd(HBNBCommand().precmd(
                                 f'Amenity.show({am.id})'))
            res = f"[{type(am).__name__}] ({am.id}) {am.__dict__}"
            self.assertEqual(f.getvalue().strip(), res)

    def test_update_amenity(self):
        """It test update of amenity object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            am = Amenity()
            am.name = "Cecilia"
            HBNBCommand().onecmd(HBNBCommand().precmd(
                                 f'Amenity.update({am.id}, name, "Ife")'))
            self.assertEqual(am.__dict__["name"], "Ife")

        with patch('sys.stdout', new=StringIO()) as f:
            am = Amenity()
            am.age = 75
            HBNBCommand().onecmd(HBNBCommand().precmd(
                                 f'Amenity.update({am.id}, age, 25)'))
            self.assertIn("age", am.__dict__.keys())
            self.assertEqual(am.__dict__["age"], 25)

        with patch('sys.stdout', new=StringIO()) as f:
            am = Amenity()
            am.age = 60
            cmmd = f'Amenity.update({am.id}, age, 10, color, green)'
            HBNBCommand().onecmd(HBNBCommand().precmd(cmmd))
            self.assertIn("age", am.__dict__.keys())
            self.assertNotIn("color", am.__dict__.keys())
            self.assertEqual(am.__dict__["age"], 10)

    def test_update_amenity_dict(self):
        """It test update of amenity object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            am = Amenity()
            am.age = 75
            cmmd = f'Amenity.update({am.id}, {{"age": 25,"color":"black"}})'
            HBNBCommand().onecmd(HBNBCommand().precmd(cmmd))
            self.assertEqual(am.__dict__["age"], 25)
            self.assertIsInstance(am.__dict__["age"], int)

    def test_destroy_amenity(self):
        """It test destroy of amenity object.
        """
        with patch('sys.stdout', new=StringIO()):
            am = Amenity()
            HBNBCommand().onecmd(HBNBCommand().precmd(
                                 f'Amenity.destroy({am.id})'))
            self.assertNotIn("Amenity.{}".format(
                am.id), storage.all().keys())


class TestCity(unittest.TestCase):
    """For testing the city commands.
    """

    def setUp(self):
        pass

    def tearDown(self) -> None:
        """It resets the FileStorage data."""
        storage._FileStorage__objects = {}
        if os.path.exists(storage._FileStorage__file_path):
            os.remove(storage._FileStorage__file_path)

    def test_create_city(self):
        """It test create of city object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create City')
            self.assertIsInstance(f.getvalue().strip(), str)
            self.assertIn("City.{}".format(
                f.getvalue().strip()), storage.all().keys())

    def test_all_city(self):
        """It test all of city object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('all City')
            for item in json.loads(f.getvalue()):
                self.assertEqual(item.split()[0], '[City]')

    def test_show_city(self):
        """It test show of city object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            cty = City()
            cty.eyes = "green"
            HBNBCommand().onecmd(f'show City {cty.id}')
            res = f"[{type(cty).__name__}] ({cty.id}) {cty.__dict__}"
            self.assertEqual(f.getvalue().strip(), res)

    def test_update_city(self):
        """It test update of city object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            cty = City()
            cty.name = "Cecilia"
            HBNBCommand().onecmd(f'update City {cty.id} name "Ife"')
            self.assertEqual(cty.__dict__["name"], "Ife")

        with patch('sys.stdout', new=StringIO()) as f:
            cty = City()
            cty.age = 75
            HBNBCommand().onecmd(f'update City {cty.id} age 25')
            self.assertIn("age", cty.__dict__.keys())
            self.assertEqual(cty.__dict__["age"], 25)

        with patch('sys.stdout', new=StringIO()) as f:
            cty = City()
            cty.age = 60
            cmmd = f'update City {cty.id} age 10 color green'
            HBNBCommand().onecmd(cmmd)
            self.assertIn("age", cty.__dict__.keys())
            self.assertNotIn("color", cty.__dict__.keys())
            self.assertEqual(cty.__dict__["age"], 10)

    def test_destroy_city(self):
        """It test destroy of city object.
        """
        with patch('sys.stdout', new=StringIO()):
            cty = City()
            HBNBCommand().onecmd(f'destroy City {cty.id}')
            self.assertNotIn("City.{}".format(
                cty.id), storage.all().keys())


class TestCityDotNotation(unittest.TestCase):
    """For testing the city command's dot notation.
    """

    def setUp(self):
        pass

    def tearDown(self) -> None:
        """It resets the FileStorage data."""
        storage._FileStorage__objects = {}
        if os.path.exists(storage._FileStorage__file_path):
            os.remove(storage._FileStorage__file_path)

    def test_create_city(self):
        """It test create  of city object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(HBNBCommand().precmd(
                                 'City.create()'))
            self.assertIsInstance(f.getvalue().strip(), str)
            self.assertIn("City.{}".format(
                f.getvalue().strip()), storage.all().keys())

    def test_count_city(self):
        """It test count of city object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(HBNBCommand().precmd('City.count()'))
            count = 0
            for i in storage.all().values():
                if type(i) == City:
                    count += 1
            self.assertEqual(int(f.getvalue()), count)

    def test_all_city(self):
        """It test all of city object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(HBNBCommand().precmd('City.all()'))
            for item in json.loads(f.getvalue()):
                self.assertEqual(item.split()[0], '[City]')

    def test_show_city(self):
        """It test show of city object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            cty = City()
            cty.eyes = "green"
            HBNBCommand().onecmd(HBNBCommand().precmd(
                                 f'City.show({cty.id})'))
            res = f"[{type(cty).__name__}] ({cty.id}) {cty.__dict__}"
            self.assertEqual(f.getvalue().strip(), res)

    def test_update_city(self):
        """It test update of city object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            cty = City()
            cty.name = "Cecilia"
            HBNBCommand().onecmd(HBNBCommand().precmd(
                                 f'City.update({cty.id}, name, "Ife")'))
            self.assertEqual(cty.__dict__["name"], "Ife")

        with patch('sys.stdout', new=StringIO()) as f:
            cty = City()
            cty.age = 75
            HBNBCommand().onecmd(HBNBCommand().precmd(
                                 f'City.update({cty.id}, age, 25)'))
            self.assertIn("age", cty.__dict__.keys())
            self.assertEqual(cty.__dict__["age"], 25)

        with patch('sys.stdout', new=StringIO()) as f:
            cty = City()
            cty.age = 60
            cmmd = f'City.update({cty.id}, age, 10, color, green)'
            HBNBCommand().onecmd(HBNBCommand().precmd(cmmd))
            self.assertIn("age", cty.__dict__.keys())
            self.assertNotIn("color", cty.__dict__.keys())
            self.assertEqual(cty.__dict__["age"], 10)

    def test_update_city_dict(self):
        """It test update of city object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            cty = City()
            cty.age = 75
            cmmd = f'City.update({cty.id}, {{"age": 25,"color":"black"}})'
            HBNBCommand().onecmd(HBNBCommand().precmd(cmmd))
            self.assertEqual(cty.__dict__["age"], 25)
            self.assertIsInstance(cty.__dict__["age"], int)

    def test_destroy_city(self):
        """It test destroy of city object.
        """
        with patch('sys.stdout', new=StringIO()):
            cty = City()
            HBNBCommand().onecmd(HBNBCommand().precmd(
                                 f'City.destroy({cty.id})'))
            self.assertNotIn("City.{}".format(
                cty.id), storage.all().keys())
