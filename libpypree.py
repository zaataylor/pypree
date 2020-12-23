import os # listing directory contents, determining files from directories
import argparse # CLI
import sys # get command-line arguments with sys.argv
from typing import List, Iterator # type hinting

argparser = argparse.ArgumentParser(description="pypree - A partial Python tree command implementation")
argparser.add_argument("-p", 
                        "--path",
                        metavar="PATH",
                        nargs="+",
                        default=".",
                        help="Path(s) to one or more directories to build the tree(s) at." +
                        " Defaults to current directory.")

def main(argv = sys.argv[1:]):
    """Runs the program."""
    args = argparser.parse_args(argv)

    for path in args.path:
        print(create_tree(path=path))

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
        #TODO: implement this
        pass

    def __str__(self):
        return tree_to_string(self, indent=0)


def create_tree(path: str) -> TreeItem:
    """Creates a tree-like representation of the directory at `path`."""

    # Base Case: we have a file and not a directory, or we have an
    # empty directory
    rpath = os.path.realpath(path)
    name = os.path.split(rpath)[1]
    if not os.path.isdir(rpath) or not os.listdir(rpath):
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

def tree_to_string(ti: TreeItem, indent: int) -> str:
    """Creates a string representation of a TreeItem."""
    indent_val = indent
    tree_string = ""
    # Case: root TreeItem
    if indent_val == 0:
        tree_string += ti.name + "\n"
        tree_string += tree_to_string(ti=ti, indent=indent + 1)
    else:
        # use one less than the total number of indents, so that
        # the special "└──" or "├── " will fill the last spot
        vert_bars = "│   " * (indent_val - 1)
        for index, child in enumerate(ti.children):
            # end child has "└──" if it lacks children
            if index == len(ti.children) - 1 and not child.children:
                tree_string += vert_bars + "└── " + child.name + "\n"
            else:
            # other children have "├──" 
                tree_string += vert_bars + "├── " + child.name + "\n"

            tree_string += tree_to_string(ti=child, indent=indent + 1)

    return tree_string

def get_next(it: Iterator):
    """Wrapper on walk iterator __next__ method."""
    return it.__next__()