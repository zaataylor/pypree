import os # listing directory contents, determining files from directories
import argparse # CLI
import sys # get command-line arguments with sys.argv
from typing import List, Iterator # type hinting

argparser = argparse.ArgumentParser(description="pypree - A Python partial tree command implementation")
argparser.add_argument("-p", 
                        "--path",
                        metavar="PATH",
                        nargs="+",
                        default=".",
                        help="Path(s) to start building the tree(s) at. Defaults to current directory.")

def main(argv = sys.argv[1:]):
    """Runs the program."""
    args = argparser.parse_args(argv)

    for path in args.path:
        print(print_tree(create_tree(path=path), indent=0))

class TreeItem(object):
    """Represents an item in the tree."""
    name = None
    isdir = False
    children = []

    def __init__(self, name: str, isdir: bool, children: List):
        self.name = name
        self.isdir = isdir
        self.children = children

    def __repr__(self):
        pass

    def __str__(self):
        return print_tree(self, indent=0)


def create_tree(path: str) -> TreeItem:
    """Creates a tree-like representation of the directory at `path`."""

    # Base Case: we have a file and not a directory, or we have an
    # empty directory
    rpath = os.path.realpath(path)
    name = os.path.split(rpath)[1]
    if not (os.path.isdir(rpath) or os.listdir(rpath)):
        ti = TreeItem(name=name, isdir=False, children=[])
        return ti

    # Recursive case: directory with one or more children
    w = os.walk(rpath)
    children = []
    _, dirnames, filenames = get_next(w)
    
    # add the file children first
    for filename in filenames:
        fc = TreeItem(name=filename, isdir=False, children=[])
        children.append(fc)

    # recursively add the directory children
    for dirname in dirnames:
        dirpath = os.path.join(rpath, dirname)
        children.append(create_tree(dirpath))

    return TreeItem(name=name, isdir=True, children=children)

def print_tree(ti: TreeItem, indent: int) -> str:
    """Prints a representation of a TreeItem."""
    indent_val = indent
    tree_string = ""
    if indent_val == 0:
        tree_string = ti.name + "\n"
        indent += 1
        tree_string += print_tree(ti=ti, indent=indent)
    elif indent_val == 1:
        indent += 1
        for index, child in enumerate(ti.children):
            # end child has "└──"
            if index == len(ti.children) - 1:
                tree_string = "└──" + child.name + "\n"
            else:
            # other children have "├──" 
                tree_string = "├──" + child.name + "\n"
            tree_string += print_tree(ti=child, indent=indent)
    else:
        while(indent_val > 1):
            tree_string += "│   "
            indent_val -= 1
        tree_string += print_tree(ti=ti, indent=indent_val)
    return tree_string

def get_next(it: Iterator):
    """Wrapper on walk iterator __next__ method."""
    return it.__next__()