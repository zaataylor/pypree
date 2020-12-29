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
    fullpath = None
    isdir = False
    parent = None
    children = []
    # direct number of file and directory type
    # TreeItem children
    nfiles = ndirs = 0

    def __init__(self, name: str, fullpath: str, isdir: bool, parent, children: List,
        nfiles: int, ndirs: int):
        self.name = name
        self.fullpath = fullpath
        self.isdir = isdir
        self.parent = parent
        self.children = children
        self.nfiles = nfiles
        self.ndirs = ndirs

    def __repr__(self):
        #TODO: implement this
        pass

    def __str__(self):
        dir_count = count_dirs(self)
        file_count = count_files(self)
        dir_string = "directory"
        if dir_count > 1:
            dir_string = "directories"
        return tree_to_string(self, indent=0) + \
        "\n{} {}, {} files".format(dir_count, dir_string, file_count)


def create_tree(path: str, parent=None, show_hidden=False) -> TreeItem:
    """Creates a tree-like representation of the directory at `path`."""

    rpath = os.path.realpath(path)
    name = os.path.split(rpath)[1]
    # root Tree item
    if parent == None:
        if path == ".":
            rpath = path

    # Base Cases: we have a file and not a directory, or we have an
    # empty directory
    if not os.path.isdir(rpath):
        ti = TreeItem(name=name, fullpath=rpath, isdir=False, parent=parent, children=[],
            nfiles=0, ndirs=0)
        return ti
    elif not os.listdir(rpath):
        ti = TreeItem(name=name, fullpath=rpath, isdir=True, parent=parent, children=[],
            nfiles=0, ndirs=0)
        return ti

    # Recursive case: directory with one or more children
    w = os.walk(rpath)
    # children = []
    _, dirnames, filenames = get_next(w)
    
    # Form the new parent
    new_parent = TreeItem(name=name, fullpath=rpath, isdir=True, parent=parent, children=[],
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
            new_parent.children.append(dc)
        else:
            if not show_hidden and item.startswith("."):
                fc_hidden +=1
                continue
            fc = TreeItem(name=item, fullpath = item_path, isdir=False, parent=new_parent, children=[],
                nfiles=0, ndirs=0)
            new_parent.children.append(fc)

    new_parent.nfiles = len(filenames) - fc_hidden
    new_parent.ndirs = len(dirnames) - dc_hidden
    return new_parent
        

def tree_to_string(ti: TreeItem, indent: int) -> str:
    """Creates a string representation of a TreeItem."""
    tree_string = ""
    indent_val = indent

    # Case: I am the root/start TreeItem. I'll use my
    # real path name
    if indent_val == 0:
        tree_string += ti.fullpath + "\n"
        tree_string += tree_to_string(ti, indent=indent + 1)
    # Case: also the root/start TreeItem. Here, I iterate
    # over my children by adding their string representations
    # to mine
    elif indent_val == 1:
        for _, child in enumerate(ti.children):
            tree_string += tree_to_string(ti=child, indent=indent + 1)
    else:
        # Case: I am not a direct child of the root TreeItem. I need
        # to traverse upwards in my lineage to determine how many of
        # my parents are the last children of their parents.
        skip_lines = []
        saved_ti = ti
        # go all the way back up to the root
        while(ti.parent is not None):
            if ti.parent.parent is not None:
                ti_gp = ti.parent.parent
                names = [c.name for c in ti_gp.children]
                # Idea: the child's parent is the last child of grandparent,
                # so we skip the line that would be directly under the
                # grandparent. Since we're traversing upwards (i.e. right
                # to left in final output), we insert bars or spaces in
                # reverse order (i.e. insert at index 0)
                if sorted(names)[-1] == ti.parent.name:
                    skip_lines.insert(0, "  ")
                else:
                    skip_lines.insert(0, "│   ")

            # go up one level for the next iteration
            ti = ti.parent
        
        # restore original TreeItem after iteration completes
        ti = saved_ti
        bars = "".join(skip_lines)
        names = [c.name for c in ti.parent.children]
        # last child has "└──"
        if sorted(names)[-1] == ti.name:
            # TODO: fix this problematic section
            ts = bars + "└── " + ti.name + "\n"
            ts = ts.replace("   ", " \uc2a0\uc2a0")
            tree_string += ts
        else:
            # other children have "├──" 
            tree_string += bars + "├── " + ti.name + "\n"
    
        # I recurse on my children so they can do the same
        # thing as me
        for _, child in enumerate(ti.children):
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
