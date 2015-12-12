#!/usr/bin/python

import os
import sys


class Category:
    """

    """

    def __init__(self, name, abspath_dir):
        self.name = name
        self.abspath_dir = abspath_dir
        self.examples = []

    def add_example(self, example):
        self.examples.append(example)

    def emit(self):
        print("CATEGORY: " + self.name + ", " + self.abspath_dir)
        for example in self.examples:
            example.emit()


class Example:
    """

    """

    def __init__(self, name, abspath_dir, category):
        self.name = name
        self.abspath_dir = abspath_dir
        self.category = category

    def emit(self):
        print("    EXAMPLE: " + self.category + ", " + self.name + ", " + self.abspath_dir)


class Manager:
    """

    """

    def __init__(self):
        self.categories = []
        self.examples = []
        pass

    @staticmethod
    def error(message):
        print("")
        print("ERROR: " + message)
        print("")
        sys.exit(1)

    def parse_category(self, abspath_dir, category_description_file):
        f = open(category_description_file)
        line = f.readline().rstrip()
        f.close()
        category_name = line
        if '/' in category_name:
            self.error("Directory " + abspath_dir + " has / character in Category name (" + line + ")")
        if len(category_name) == 0:
            self.error("Directory " + abspath_dir + " has empty Category name")
        category = Category(category_name, abspath_dir)
        return category

    def parse_example(self, abspath_dir, example_description_file, category):
        f = open(example_description_file)
        line = f.readline().rstrip()
        f.close()
        example_name = line
        if '/' in example_name:
            self.error("Directory " + abspath_dir + " has / character in Example name (" + line + ")")
        if len(example_name) == 0:
            self.error("Directory " + abspath_dir + " has empty Example name")
        example = Example(example_name, abspath_dir, category)
        return example

    def build(self, abspath_dir, current_category):
        used_this_dir = None

        # Check to see if this directory contains a category.
        category_description_file = os.path.join(abspath_dir, "cat.txt")
        if os.path.exists(category_description_file):
            if used_this_dir is not None:
                self.error("Directory " + abspath_dir +
                           " has Category metadata but is already used as a " + used_this_dir)
            current_category = self.parse_category(abspath_dir, category_description_file)
            self.categories.append(current_category)
            used_this_dir = "Category"

        # Check to see if this directory contains an example.
        example_description_file = os.path.join(abspath_dir, "ex.txt")
        if os.path.exists(example_description_file):
            if used_this_dir is not None:
                self.error("Directory " + abspath_dir +
                           " has Example metadata but is already used as a " + used_this_dir)
            example = self.parse_example(abspath_dir, example_description_file, current_category)
            self.examples.append(example)
            current_category.add_exmaple(example)
            used_this_dir = "Example"

        if used_this_dir is None:
            self.error("Directory " + abspath_dir + " has neither Category nor Example metadata")

        # Search subdirectories for more content.
        entries = sorted(os.listdir(abspath_dir))
        for entry in entries:
            if os.path.isdir(entry):
                if entry == ".git":
                    continue
                if entry == ".idea":
                    continue
                if entry == "examples":
                    continue
                abspath_entry = os.path.join(abspath_dir, entry)
                self.build(abspath_entry, current_category)

    def emit(self):
        for category in self.categories:
            category.emit()


def main(argv):
    """
    Main program.

    @return: none
    """

    script_dir = os.path.realpath(os.path.dirname(argv[0]))
    os.chdir(script_dir)

    m = Manager()
    root = os.path.abspath(os.path.join(os.getcwd(), "h2o"))
    m.build(root, None)
    m.emit()


if __name__ == "__main__":
    main(sys.argv)
