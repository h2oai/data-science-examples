#!/usr/bin/python

import os
import sys


class Category:
    """

    """

    def __init__(self, name, abspath_dir, parent_category, index_in_parent_category):
        self.name = name
        self.abspath_dir = abspath_dir
        self.parent_category = parent_category
        self.index_in_parent_category = index_in_parent_category
        self.examples = []

    def add_example(self, example):
        self.examples.append(example)

    def full_name(self):
        if self.parent_category is None:
            return self.name

        parent_full_name = self.parent_category.full_name()
        if parent_full_name == "":
            return self.name

        return parent_full_name + "/" + self.name

    def full_number(self):
        if self.index_in_parent_category is None:
            return ""

        parent_full_number = self.parent_category.full_number()
        if parent_full_number == "":
            return str(self.index_in_parent_category)

        return parent_full_number + "." + str(self.index_in_parent_category)

    def emit(self):
        if len(self.examples) > 0:
            print("CATEGORY:  " + self.full_number() + "  " + self.full_name() + "  " + self.abspath_dir)
        for example in self.examples:
            example.emit()


class Example:
    """

    """

    def __init__(self, name, abspath_dir, parent_category, index_in_parent_category):
        self.name = name
        self.abspath_dir = abspath_dir
        self.parent_category = parent_category
        self.index_in_parent_category = index_in_parent_category

    def full_number(self):
        return self.parent_category.full_number() + "." + str(self.index_in_parent_category)

    def emit(self):
        print("    EXAMPLE:  " + self.full_number() + "  " + self.name + "  " + self.abspath_dir)


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

    def parse_category(self, abspath_dir, category_description_file, parent_category, index_in_parent_category):
        f = open(category_description_file)
        line = f.readline().rstrip()
        f.close()
        category_name = line
        if '/' in category_name:
            self.error("Directory " + abspath_dir + " has / character in Category name (" + line + ")")
        if len(category_name) == 0:
            self.error("Directory " + abspath_dir + " has empty Category name")
        category = Category(category_name, abspath_dir, parent_category, index_in_parent_category)
        return category

    def parse_example(self, abspath_dir, example_description_file, parent_category, index_in_parent_category):
        f = open(example_description_file)
        line = f.readline().rstrip()
        f.close()
        example_name = line
        if '/' in example_name:
            self.error("Directory " + abspath_dir + " has / character in Example name (" + line + ")")
        if len(example_name) == 0:
            self.error("Directory " + abspath_dir + " has empty Example name")
        example = Example(example_name, abspath_dir, parent_category, index_in_parent_category)
        return example

    def build(self, abspath_dir, parent_category, index_in_parent_category):
        used_this_dir = None

        if not os.path.exists(abspath_dir):
            self.error("Directory " + abspath_dir + " does not exist")

        # Check to see if this directory contains a category.
        category_description_file = os.path.join(abspath_dir, "cat.txt")
        if os.path.exists(category_description_file):
            if used_this_dir is not None:
                self.error("Directory " + abspath_dir +
                           " has Category metadata but is already used as a " + used_this_dir)
            parent_category = self.parse_category(abspath_dir, category_description_file,
                                                  parent_category, index_in_parent_category)
            self.categories.append(parent_category)
            used_this_dir = "Category"

        # Check to see if this directory contains an example.
        example_description_file = os.path.join(abspath_dir, "ex.txt")
        if os.path.exists(example_description_file):
            if used_this_dir is not None:
                self.error("Directory " + abspath_dir +
                           " has Example metadata but is already used as a " + used_this_dir)
            example = self.parse_example(abspath_dir, example_description_file,
                                         parent_category, index_in_parent_category)
            self.examples.append(example)
            parent_category.add_example(example)
            used_this_dir = "Example"

        if used_this_dir is None:
            self.error("Directory " + abspath_dir + " has neither Category nor Example metadata")

        # Search subdirectories for more content.
        abspath_idx = os.path.join(abspath_dir, "idx")
        if os.path.exists(abspath_idx):
            if used_this_dir == "Example":
                self.error("Directory " + abspath_dir + " is an Example but has a category index")
            with open(abspath_idx) as f:
                index_in_parent_category = 0
                for line in f:
                    index_in_parent_category += 1
                    entry = line.strip()
                    abspath_entry = os.path.join(abspath_dir, entry)
                    self.build(abspath_entry, parent_category, index_in_parent_category)

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
    root = os.path.abspath(os.path.join(os.getcwd(), "examples"))
    m.build(root, None, None)
    m.emit()


if __name__ == "__main__":
    main(sys.argv)
