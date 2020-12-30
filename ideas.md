# Ideas
- Use [rich](https://github.com/willmcgugan/rich/) for coloring the output
- Add other CLI options to make `pypree` even more `tree`-like

# Remaining Things To Do:
- [&check;] `TreeItem` class
    - Plan: make a `TreeItem` class that'll recursively hold the values of the files and directories below it in the form of `TreeItem`s. Then, print out this tree recursively with some nice-looking formatting, maybe using `pprint`?
    - `TreeItem` has:
        - Name
        - IsDir
        - Children (which are `TreeItem`s)
- [&check;] Function to print out the contents of a `TreeItem`
- [&check;] Function to create the Tree
    - Strategy here is to recurse down until we get a regular file (or an empty directory), then we construct a basic `TreeItem` and return it. This will be appended to the children member of the `TreeItem` corresponding to the parent of that `TreeItem`.
- [&check;] Function(s) to calculate total count of directories and files
- [&check;] Resolve issue with output using parent references to make output more tree-like
    - [&check;] Implement parent refernces
    - [&check;] Use parent references in `tree_string` to control number of vertical bars on a given line