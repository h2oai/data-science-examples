#!/usr/bin/python

import os
import sys
import subprocess


def find_markdown():
    p = "/usr/local/bin/markdown"
    if os.path.exists(p):
        return p

    print("")
    print("ERROR: markdown binary not found")
    print("")
    sys.exit(1)


def relative_hyperlink(name):
    rh = ""
    for c in name:
        if ('a' <= c <= 'z') or ('A' <= c <= 'Z') or ('0' <= c <= '9'):
            rh += c
        else:
            rh += "_"
    return rh.lower()


class Category:
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
            return ""

        parent_full_name = self.parent_category.full_name()
        if parent_full_name == "":
            return self.name

        return parent_full_name + " / " + self.name

    def relative_hyperlink(self):
        return relative_hyperlink(self.full_name())

    def full_number(self):
        if self.index_in_parent_category is None:
            return ""

        parent_full_number = self.parent_category.full_number()
        if parent_full_number == "":
            return str(self.index_in_parent_category)

        return parent_full_number + "." + str(self.index_in_parent_category)

    def emit_toc(self):
        if self.index_in_parent_category is None:
            return
        print("")
        print("    <h2>" + "Section " + self.full_number() + ".  " + self.name + "</h2>")
        print("    <ul>")
        for example in self.examples:
            example.emit_toc()
        print("    </ul>")

    def emit_examples(self):
        for example in self.examples:
            example.emit_example()

    def debug(self):
        if len(self.examples) > 0:
            print("CATEGORY:  " + self.full_number() + "  " + self.full_name() + "  " + self.abspath_dir)
        for example in self.examples:
            example.debug()


class Example:
    def __init__(self, name, abspath_dir, parent_category, index_in_parent_category):
        self.name = name
        self.abspath_dir = abspath_dir
        self.parent_category = parent_category
        self.index_in_parent_category = index_in_parent_category
        self.tags = []

    def full_number(self):
        return self.parent_category.full_number() + "." + str(self.index_in_parent_category)

    def full_name(self):
        return self.parent_category.full_name() + " / " + self.name

    def relative_hyperlink(self):
        return relative_hyperlink(self.name)

    def emit_toc(self):
        print("        <li><a href=\"#" +
              self.relative_hyperlink() +
              "\">" +
              self.full_number() +
              "  " +
              self.name +
              "</a>" +
              "</li>")

    def emit_example(self):
        print("    <div id=\"" + self.relative_hyperlink() + "\">")
        self._emit_nav_tabs()
        self._emit_tab_content()
        print("    </div>")

    def debug(self):
        print("    EXAMPLE")
        print("        " + self.full_number() + " " + self.name)
        print("        " + self.abspath_dir)
        print("        " + self.relative_hyperlink())

    # ---------------------------------------------------------------
    # Private methods below this line.
    # ---------------------------------------------------------------

    _lang__________ = ["lang-r", "lang-r",      "lang-python"]
    _tabs_to_check_ = ["R",      "h2o-R",       "h2o-python"]
    _files_to_check = ["ex-R.R", "ex-h2o.R",    "ex-h2o.py"]

    def _emit_nav_tabs(self):
        print("        <h3>" +
              self.full_number() + ". " +
              self.full_name() +
              "<a href=\"#" +
              self.relative_hyperlink() +
              "\"> <em>[link]</em></a></h3>")

        ref_prefix = self.full_number().replace(".", "_")
        print("        <ul class=\"nav nav-tabs\">")
        print("            <li class=\"active\"><a data-toggle=\"tab\" href=\"#" +
              ref_prefix + "_description" +
              "\">" +
              "Description</a></li>")

        i = 0
        while i < len(self._files_to_check):
            fn = self._files_to_check[i]
            abspath_fn = os.path.join(self.abspath_dir, fn)
            if os.path.exists(abspath_fn):
                tab_name = self._tabs_to_check_[i]
                print("            <li><a data-toggle=\"tab\" href=\"#" +
                      ref_prefix + "_" + tab_name +
                      "\">" +
                      tab_name +
                      "</a></li>")
            i += 1

        print("        </ul>")

    @staticmethod
    def _emit_markdown_as_html(abspath_filename):
        sys.stdout.flush()
        abspath_markdown = find_markdown()
        subprocess.check_call(["node", abspath_markdown, abspath_filename])

    @staticmethod
    def _emit_file(abspath_filename):
        f = open(abspath_filename, 'r')
        lines = f.readlines()
        for line in lines:
            print line.rstrip()
        f.close()

    def _emit_tab_content(self):
        ref_prefix = self.full_number().replace(".", "_")
        print("        <div class=\"tab-content\">")
        print("            <div id=\"" +
              ref_prefix + "_description" +
              "\" class=\"tab-pane fade in active\">"
              )
        print("<div class=\"well\">")
        example_description_file = os.path.join(self.abspath_dir, "ex.md")
        self._emit_markdown_as_html(example_description_file)
        print("</div>")
        print("            </div>")

        i = 0
        while i < len(self._files_to_check):
            fn = self._files_to_check[i]
            abspath_fn = os.path.join(self.abspath_dir, fn)
            if os.path.exists(abspath_fn):
                tab_name = self._tabs_to_check_[i]
                print("            <div id=\"" +
                      ref_prefix + "_" + tab_name +
                      "\" class=\"tab-pane fade\">")
                print("<pre>")
                print("<code class=\"" + self._lang__________[i] + "\">")
                self._emit_file(abspath_fn)
                print("</code>")
                print("</pre>")
                print("            </div>")
            i += 1

        print("        </div>")


class Manager:
    def __init__(self):
        self.categories = []
        self.examples = []
        self.tags = {}
        self.duplicate_checker = {}
        pass

    @staticmethod
    def error(message):
        print("")
        print("ERROR: " + message)
        print("")
        sys.exit(1)

    def parse_category(self, abspath_dir, category_name_file, parent_category, index_in_parent_category):
        f = open(category_name_file)
        line = f.readline().rstrip()
        f.close()
        category_name = line
        if '/' in category_name:
            self.error("Directory " + abspath_dir + " has / character in Category name (" + line + ")")
        if len(category_name) == 0:
            self.error("Directory " + abspath_dir + " has empty Category name")
        category = Category(category_name, abspath_dir, parent_category, index_in_parent_category)
        self._check_unique(category)
        return category

    def parse_example(self, abspath_dir, example_name_file, parent_category, index_in_parent_category):
        f = open(example_name_file)
        line = f.readline().rstrip()
        f.close()
        example_name = line
        if '/' in example_name:
            self.error("Directory " + abspath_dir + " has / character in Example name (" + line + ")")
        if len(example_name) == 0:
            self.error("Directory " + abspath_dir + " has empty Example name")
        example = Example(example_name, abspath_dir, parent_category, index_in_parent_category)
        self._check_unique(example)
        example_tags_file = os.path.join(abspath_dir, "ex.tags")
        if os.path.exists(example_tags_file):
            f = open(example_tags_file)
            for line in f:
                tag = line.strip()
                self._check_legal_tag(tag, example)
                if len(tag) > 0:
                    example.tags.append(tag)
            f.close()
        return example

    def build(self, abspath_dir, parent_category, index_in_parent_category):
        used_this_dir = None

        if not os.path.exists(abspath_dir):
            self.error("Directory " + abspath_dir + " does not exist")

        # Check to see if this directory contains a category.
        category_name_file = os.path.join(abspath_dir, "cat.txt")
        if os.path.exists(category_name_file):
            if used_this_dir is not None:
                self.error("Directory " + abspath_dir +
                           " has Category metadata but is already used as a " + used_this_dir)
            parent_category = self.parse_category(abspath_dir, category_name_file,
                                                  parent_category, index_in_parent_category)
            self.categories.append(parent_category)
            used_this_dir = "Category"

        # Check to see if this directory contains an example.
        example_name_file = os.path.join(abspath_dir, "ex.txt")
        if os.path.exists(example_name_file):
            if used_this_dir is not None:
                self.error("Directory " + abspath_dir +
                           " has Example metadata but is already used as a " + used_this_dir)
            example_description_file = os.path.join(abspath_dir, "ex.md")
            if not os.path.exists(example_description_file):
                self.error("Directory " + abspath_dir + " does not have description file ex.md")
            example = self.parse_example(abspath_dir, example_name_file,
                                         parent_category, index_in_parent_category)
            self.examples.append(example)
            parent_category.add_example(example)
            self._add_tags(example)
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
        self._emit_doctype()
        self._emit_html_start()
        self._emit_head()
        self._emit_body_start()
        self._emit_container_start()
        self._emit_jumbotron()
        self._emit_toc()
        self._emit_tags()
        self._emit_examples()
        self._emit_container_end()
        self._emit_body_end()
        self._emit_html_end()

    def debug(self):
        for category in self.categories:
            category.debug()

    # ---------------------------------------------------------------
    # Private methods below this line.
    # ---------------------------------------------------------------

    def _check_unique(self, item):
        rh = item.relative_hyperlink()
        if rh in self.duplicate_checker:
            self.error("Directory " + item.abspath_dir + " has a conflict with " + self.duplicate_checker[rh])
        else:
            self.duplicate_checker[rh] = item.abspath_dir

    def _check_legal_tag(self, tag, item):
        for c in tag:
            if not(('a' <= c <= 'z') or ('0' <= c <= '9') or c == "_" or c == " "):
                self.error("Directory " + item.abspath_dir + " has an invalid tag " + tag +
                           " (characters must be a-z 0-9 _ and space)")

    def _add_tags(self, example):
        for tag in example.tags:
            if tag not in self.tags:
                self.tags[tag] = []
            list_of_examples_for_tag = self.tags[tag]
            list_of_examples_for_tag.append(example)

    @staticmethod
    def _emit_doctype():
        print("<!DOCTYPE html>")

    @staticmethod
    def _emit_html_start():
        print("""
<html lang=\"en\">
""")

    @staticmethod
    def _emit_html_end():
        print("""
</html>
""")

    @staticmethod
    def _emit_head():
        print("""
<head>
    <title>Data Science Examples</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <script src="static/jquery/jquery-1.11.3.min.js"></script>

    <link rel="stylesheet" href="static/bootstrap/3.3.6/css/bootstrap.min.css">
    <script src="static/bootstrap/3.3.6/js/bootstrap.min.js"></script>

    <link rel="stylesheet" href="static/highlight/styles/default.css">
    <script src="static/highlight/highlight.pack.js"></script>
    <script>hljs.initHighlightingOnLoad();</script>
</head>
""")

    @staticmethod
    def _emit_body_start():
        print("""
<body>""")

    @staticmethod
    def _emit_body_end():
        print("""
</body>
""")

    @staticmethod
    def _emit_container_start():
        print("""
<div class="container">
""")

    @staticmethod
    def _emit_container_end():
        print("""
</div>
""")

    @staticmethod
    def _emit_jumbotron():
        print("""
    <div class="jumbotron text-center">
        <h1>Data Science Examples</h1>
        <em>A collection of data science examples implemented across a variety of languages and libraries.</em>
        <hr>
        <h3>
            <a href="https://github.com/h2oai/data-science-examples/blob/gh-pages/README.md">
            [How to contribute]</a>
            <a href="https://github.com/h2oai/data-science-examples/graphs/contributors">
            [List of contributors]</a>
            <a href="report_an_issue.html">
            [Report an issue]</a>
        </h3>
    </div>
""")

    def _emit_toc(self):
        print("""
    <div class="bg-primary">
        <h1>Table of Contents</h1>
    </div>
""")
        for category in self.categories:
            category.emit_toc()

    def _emit_tags(self):
        print("""
    <div class="bg-primary">
        <h1>Tags</h1>
    </div>
""")
        print("    <table class=\"table table-bordered\">")
        print("        <thead>")
        print("            <tr>")
        print("                <th>Tag</th>")
        print("                <th>Related Examples</th>")
        print("            </tr>")
        print("        </thead>")
        print("        <tbody>")
        for tag in sorted(self.tags.keys()):
            print("            <tr>")
            print("                <td>" + tag + "</td>")
            list_of_examples_for_tag = self.tags[tag]
            print("                <td>")
            i = 0
            while i < len(list_of_examples_for_tag):
                example = list_of_examples_for_tag[i]
                if (i + 1) < len(list_of_examples_for_tag):
                    maybe_comma = ","
                else:
                    maybe_comma = ""
                print("                    <a href=#" +
                      example.relative_hyperlink() + ">" +
                      example.name +
                      maybe_comma +
                      "</a>")
                i += 1
            print("                </td>")
            print("            </tr>")
        print("        </tbody>")
        print("    </table>")

    def _emit_examples(self):
        print("""
    <div class="bg-primary">
        <h1>The Examples</h1>
    </div>
""")
        for category in self.categories:
            category.emit_examples()


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
