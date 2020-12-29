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
argparser.add_argument("-a",
                       "--all",
                        action="store_true",
                        help="Specify this option to also include hidden files and directories" + 
                        " in the final output.")

def main(argv = sys.argv[1:]):
    """Runs the program."""
    args = argparser.parse_args(argv)

    show_hidden = args.all if args.all else False
    for path in args.path:
        print(create_tree(path=path, show_hidden=show_hidden))

class TreeItem(object):
    """Represents an item in the tree."""
    name = None
    isdir = False
    parent = None
    children = []
    # direct number of file and directory type
    # TreeItem children
    nfiles = ndirs = 0

    def __init__(self, name: str, isdir: bool, parent, children: List,
        nfiles: int, ndirs: int):
        self.name = name
        self.isdir = isdir
        self.parent = parent
        self.children = children
        self.nfiles = nfiles
        self.ndirs = ndirs

    def __repr__(self):
        #TODO: implement this
        pass

    def __str__(self):
        return tree_to_string(self, indent=0) + \
        "\n{} directories, {} files".format(count_dirs(self), count_files(self))


def create_tree(path: str, parent=None, show_hidden=False) -> TreeItem:
    """Creates a tree-like representation of the directory at `path`."""

    rpath = os.path.realpath(path)
    name = os.path.split(rpath)[1]

    # Base Cases: we have a file and not a directory, or we have an
    # empty directory
    if not os.path.isdir(rpath):
        ti = TreeItem(name=name, isdir=False, parent=parent, children=[],
            nfiles=0, ndirs=0)
        return ti
    elif not os.listdir(rpath):
        ti = TreeItem(name=name, isdir=True, parent=parent, children=[],
            nfiles=0, ndirs=0)
        return ti

    # Recursive case: directory with one or more children
    w = os.walk(rpath)
    children = []
    _, dirnames, filenames = get_next(w)
    
    # Form the new parent
    new_parent = TreeItem(name=name, isdir=True, parent=parent, children=[],
        nfiles=0, ndirs=0)

    # process file and directory children simultaneously
    # so output will match tree
    items = dirnames + filenames

    # count of hidden files and dirs, respectively
    fc_hidden = dc_hidden = 0
    for item in sorted(items):
        item_path = os.path.join(rpath, item)
        if os.path.isdir(item_path):
            if not show_hidden and item.startswith("."):
                dc_hidden += 1
                continue
            dc = create_tree(item_path, show_hidden=show_hidden)
            # need this to keep dc from setting it's parent field to None
            dc.parent = new_parent
            children.append(dc)
        else:
            if not show_hidden and item.startswith("."):
                fc_hidden +=1
                continue
            fc = TreeItem(name=item, isdir=False, parent=new_parent, children=[],
                nfiles=0, ndirs=0)
            children.append(fc)
   
    return TreeItem(name=name, isdir=True, children=children, parent=None,
            nfiles=len(filenames) - fc_hidden, ndirs=len(dirnames) - dc_hidden)
        

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

def count_files(ti: TreeItem) -> int:
    """Counts the number of TreeItems of file type below this one."""
    if not ti.children:
        return 0
    else:
        return ti.nfiles + sum([count_files(c) for c in ti.children])

def count_dirs(ti: TreeItem) -> int:
    """Counts the number of TreeItems of directory type below this one."""
    if not ti.children:
        return 0
    else:
        return ti.ndirs + sum([count_dirs(c) for c in ti.children])

def get_next(it: Iterator):
    """Wrapper on walk iterator __next__ method."""
    return it.__next__()
