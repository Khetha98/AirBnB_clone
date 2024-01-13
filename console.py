#!/usr/bin/python3
"""This module console.py is an entry point"""
import cmd
import re
import json
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

model_classes = {'BaseModel': BaseModel, 'User': User,
                   'Amenity': Amenity, 'City': City, 'State': State,
                   'Place': Place, 'Review': Review}



class HBNBCommand(cmd.Cmd):
    
    """This is command interpreter class"""
    
    prompt = "(hbnb) "
    
    def precmd(self, line):
        """
        Override precmd to always display the help message before each command.
        """
        if not line:
            return '\n'

        pattern = re.compile(r"(\w+)\.(\w+)\((.*)\)")
        match_list = pattern.findall(line)
        if not match_list:
            return super().precmd(line)

        match_tuple = match_list[0]
        if not match_tuple[2]:
            if match_tuple[1] == "count":
                instance_objs = storage.all()
                print(len([
                    v for _, v in instance_objs.items()
                    if type(v).__name__ == match_tuple[0]]))
                return "\n"
            return "{} {}".format(match_tuple[1], match_tuple[0])
        else:
            args = match_tuple[2].split(", ")
            if len(args) == 1:
                return "{} {} {}".format(
                    match_tuple[1], match_tuple[0],
                    re.sub("[\"\']", "", match_tuple[2]))
            else:
                match_json = re.findall(r"{.*}", match_tuple[2])
                if (match_json):
                    return "{} {} {} {}".format(
                        match_tuple[1], match_tuple[0],
                        re.sub("[\"\']", "", args[0]),
                        re.sub("\'", "\"", match_json[0]))
                return "{} {} {} {} {}".format(
                    match_tuple[1], match_tuple[0],
                    re.sub("[\"\']", "", args[0]),
                    re.sub("[\"\']", "", args[1]), args[2])


    def do_quit(self, arg):
        """
        Quit command to exit the program.
        """
        return True

    def do_EOF(self, arg):
        """
        Exits the program on EOF (Ctrl+D).
        """
        print("")
        return True

    def emptyline(self):
        """
        Do nothing on an empty line
        """
        pass


    def do_help(self, arg):
        """
        Displays help information about the available commands.
        """
        return super().do_help(arg)



    def do_create(self, arg):
        """
        Creates a new instance of BaseModel, saves it, and prints the id.
        Usage: create <class name>
        """
        args = arg.split()
        if not validate_the_classname(args):
            return

        new_obj = model_classes[args[0]]()
        new_obj.save()
        print(new_obj.id)

    def do_show(self, arg):
        """
        Prints the string representation of an instance based on class name and id.
        Usage: show <class name> <id>
        """
        args = arg.split()
        if not validate_the_classname(args, check_id=True):
            return

        instance_objs = storage.all()
        key = "{}.{}".format(args[0], args[1])
        req_instance = instance_objs.get(key, None)
        if req_instance is None:
            print("** no instance found **")
            return
        print(req_instance)

        obj_key = args[0] + "." + args[1]
        if obj_key in storage.all():
            print(storage.all()[obj_key])
        else:
            print("** no instance found **")


    def do_destroy(self, arg):
        """
        Deletes an instance based on class name and id.
        Usage: destroy <class name> <id>
        """
        args = arg.split()
        if not validate_the_classname(args, check_id=True):
            return

        instance_objs = storage.all()
        key = "{}.{}".format(args[0], args[1])
        req_instance = instance_objs.get(key, None)
        if req_instance is None:
            print("** no instance found **")
            return

        del instance_objs[key]
        storage.save()


    def do_all(self, arg):
        """
        Prints all string representation of all instances based or not on the class name.
        Usage: all [optional: <class name>]
        """
        args = arg.split()
        all_objs = storage.all()

        if len(args) < 1:
            print(["{}".format(str(v)) for _, v in all_objs.items()])
            return
        if args[0] not in model_classes.keys():
            print("** class doesn't exist **")
            return
        else:
            print(["{}".format(str(v))
                  for _, v in all_objs.items() if type(v).__name__ == args[0]])
            return

    def do_update(self, arg):
        """
        Updates an instance based on class name and id by adding or updating an attribute.
        Usage: update <class name> <id> <attribute name> "<attribute value>"
        """
        args = arg.split(maxsplit=3)
        if not validate_the_classname(args, check_id=True):
            return

        instance_objs = storage.all()
        key = "{}.{}".format(args[0], args[1])
        req_instance = instance_objs.get(key, None)
        if req_instance is None:
            print("** no instance found **")
            return

        match_json = re.findall(r"{.*}", arg)
        if match_json:
            payload = None
            try:
                payload: dict = json.loads(match_json[0])
            except Exception:
                print("** invalid syntax")
                return
            for k, v in payload.items():
                setattr(req_instance, k, v)
            storage.save()
            return
        if not valid_attrs(args):
            return
        first_attr = re.findall(r"^[\"\'](.*?)[\"\']", args[3])
        if first_attr:
            setattr(req_instance, args[2], first_attr[0])
        else:
            value_list = args[3].split()
            setattr(req_instance, args[2], parsed_str(value_list[0]))
        storage.save()

def validate_the_classname(args, check_id=False):
    """Checks args for validation of classname."""
    if len(args) < 1:
        print("** class name missing **")
        return False
    if args[0] not in model_classes.keys():
        print("** class doesn't exist **")
        return False
    if len(args) < 2 and check_id:
        print("** instance id missing **")
        return False
    return True

def valid_attrs(args):
    """Checks the args to validate classname attributes and values.
    """
    if len(args) < 3:
        print("** attribute name missing **")
        return False
    if len(args) < 4:
        print("** value missing **")
        return False
    return True


def is_a_float(x):
    """Checks if parameter is float.
    """
    try:
        a = float(x)
    except (TypeError, ValueError):
        return False
    else:
        return True   

def is_an_int(x):
    """Checks if parameter is an int.
    """
    try:
        a = float(x)
        b = int(a)
    except (TypeError, ValueError):
        return False
    else:
        return a == b

def parsed_str(arg):
    """Parse `arg` to an `int`, `float` or `string`.
    """
    parsed = re.sub("\"", "", arg)

    if is_an_int(parsed):
        return int(parsed)
    elif is_a_float(parsed):
        return float(parsed)
    else:
        return arg


if __name__ == '__main__':
    HBNBCommand().cmdloop()
