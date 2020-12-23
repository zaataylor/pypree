<a href="https://project-types.github.io/#toy">
  <img src="https://img.shields.io/badge/project%20type-toy-blue" alt="Toy Badge"/>
</a>

# Description

From the `man` page:
> Tree is a recursive directory listing program that produces a depth indented listing of files, which is colorized ala dircolors if the LS_COLORS environment variable is set and output is to tty. With no arguments, tree lists the files in the current directory. When directory arguments are given, tree lists all the files and/or directories found in the given directories each in turn.  Upon completion of listing all files/directories found, tree returns the total number of files and/or directories listed.

I was curious about how `tree` works, so I decided to implement a very scoped-down version of it in Python. `pypree` stands for "partial Python implementation of `tree`". I know the word order doesn't exactly match up, but I like the sound of this better. It's _not_ currently optimized for speed, or anything else for that matter. I was just having fun. :)

# Using the Code:

## Prerequisites
- Python 3.7+

## Running the Code:
1. Clone the repository and visit the directory:
```bash
git clone https://github.com/zaataylor/pypree
cd pypree
```

2. Make sure that `pypree` is executable:
```bash
chmod +x pypree
```

3. Run the code on a directory of your choosing using the following semantics, where _PATH_ is the absolute or relative path to the directory.
```bash
./pypree -p {PATH}
```
The full usage information is here:
```bash
usage: pypree [-h] [-p PATH [PATH ...]]

pypree - A partial Python tree command implementation

optional arguments:
  -h, --help            show this help message and exit
  -p PATH [PATH ...], --path PATH [PATH ...]
                        Path(s) to one or more directories to build the
                        tree(s) at. Defaults to current directory.
```