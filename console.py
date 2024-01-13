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


current_cls = {'BaseModel': BaseModel}


class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "
    valid_classes = ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]
    # display_help = True



    def do_quit(self, arg):
        """
        Quits/Exits the program.
        """
        return True

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
        if not line.strip():
            return '\n'

        parts = line.split()
        if len(parts) >= 3 and parts[1] in ["all", "count"]:
            return "{} {}".format(parts[1], parts[0])

        return super().precmd(line)

    # def postcmd(self, stop, line):
    #     """
    #     Override postcmd to reset display_help flag after each command.
    #     """
    #     HBNBCommand.display_help = True
    #     return super().postcmd(stop, line)

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
        elif len(args) == 3:
            print("** attribute name missing **")
            return
        elif len(args) == 4:
            print("** value missing **")
            return

        obj_key = args[0] + "." + args[1]
        if obj_key in storage.all():
            obj = storage.all()[obj_key]
            setattr(obj, args[2], args[3].strip('"'))
            storage.save()
        else:
            print("** no instance found **")
        


if __name__ == '__main__':
    HBNBCommand().cmdloop()