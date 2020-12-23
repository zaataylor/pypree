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

    print(args)

class TreeItem(object):
    name = None
    isdir = False
    children = []

    def __init__(self, name: str, isdir: bool, children: List):
        self.name = name
        self.isdir = isdir
        self.children = children

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

def print_tree(tree_root: TreeItem):
    """Prints a representation of a TreeItem."""
    pass

def get_next(it: Iterator):
    """Wrapper on walk iterator __next__ method."""
    return it.__next__()