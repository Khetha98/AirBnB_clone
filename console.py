#!/usr/bin/python3

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


current_cls = {'BaseModel': BaseModel}


class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "
    valid_classes = ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]



    def do_quit(self, arg):
        """
        Quit command to exit the program.
        """
        raise SystemExit

    def do_EOF(self, arg):
        """
        Exits the program on EOF (Ctrl+D).
        """
        print("")
        return True

    def do_emptyline(self):
        """
        Do nothing on an empty line
        """
        pass


    def do_help(self, arg):
        """
        Displays help information about the available commands.
        """
        super().do_help(arg)


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

    def do_create(self, arg):
        """
        Creates a new instance of BaseModel, saves it, and prints the id.
        Usage: create <class name>
        """
        if not arg:
            print("** class name missing **")
            return

        if arg not in self.valid_classes:
            print("** class doesn't exist **")
            return

        new_instance = eval(arg)()
        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """
        Prints the string representation of an instance based on class name and id.
        Usage: show <class name> <id>
        """
        args = arg.split()
        if not args or len(args) == 1:
            print("** class name missing **")
            return
        elif args[0] not in self.valid_classes:
            print("** class doesn't exist **")
            return
        elif len(args) == 2:
            print("** instance id missing **")
            return

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
        if not args or len(args) == 1:
            print("** class name missing **")
            return
        elif args[0] not in self.valid_classes:
            print("** class doesn't exist **")
            return
        elif len(args) == 2:
            print("** instance id missing **")
            return

        obj_key = args[0] + "." + args[1]
        if obj_key in storage.all():
            del storage.all()[obj_key]
            storage.save()
        else:
            print("** no instance found **")


    def do_all(self, arg):
        """
        Prints all string representation of all instances based or not on the class name.
        Usage: all [optional: <class name>]
        """
        objects = storage.all()
        if arg and arg not in self.valid_classes:
            print("** class doesn't exist **")
            return

        result = []
        for key, value in objects.items():
            if not arg or key.split(".")[0] == arg:
                result.append(value)
        print(result)

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

def is_a_float(x):
    """Checks if parameter is float.
    """
    try:
        a = float(x)
    except (TypeError, ValueError):
        return False
    else:
        return True   

def is_int(x):
    """Checks if parameter is an int.
    """
    try:
        a = float(x)
        b = int(a)
    except (TypeError, ValueError):
        return False
    else:
        return a == b


if __name__ == '__main__':
    HBNBCommand().cmdloop()