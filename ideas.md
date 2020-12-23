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
    - Strategy here is to recurse down until we get a regular file, then we construct a basic `TreeItem` that is not a directory (or an empty directory) and return it. This will be appended to the children member of the `TreeItem` corresponding to the parent of that `TreeItem`.
- [**TODO**] Function to calculate total count of directories and files