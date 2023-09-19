# FREECAD BUILD

build tools for FreeCAD based CAD projects, including Git diff integration and headless part export

this repository contains standalone tools for converting FCStd files into a variety of formats including STEP, 3MF, and GCODE (`freecad-export`) as well as tooling to integrate mesh diffs into standard git workflows (`freecad-difftool`, `freecad-diff`).

it also serves as a sort of template repository for creating build tooling around a FreeCAD project. the included `Makefile` could be copied to another repository verbatim.

![screenshot of visual mesh diff](screenshot.png)

# quick start

install dependencies:

```shell
apt install git rsync make freecad
```

clone this repository to a known location.

make a small change to `examples/example-part.FCStd`

execute the following to see a visual diff:

```shell
git difftool -x ./freecad-difftool -d
```

## limitations

- these tools were tested with Debian Trixie and FreeCAD version 0.20.2
- **sub**-assemblies of an assembly are not currently included diffs or exports
- if a part is modified but its parent assembly is not saved, the assembly diff will be empty
- if you use `git difftool` on a single file, no other modified files will be part of the diff context

## installation

NOTE: you can continue using the `git difftool -x` method above without installing, however, the `Makefile` and further instructions assume that you have followed the steps below.

add the contents of [example-gitconfig](example-gitconfig) to `~/.gitconfig`:

```shell
cat gitconfig-example >> ~/.gitconfig
```

NOTE: alternatively, add to `.git/config` of each repo you want to enable this in.

append this directory to your `$PATH` in `~/.bashrc`

```shell
echo 'export PATH="${PATH}:'"${PWD}"'"' >> ~/.bashrc
source ~/.bashrc
```

NOTE: alternatively, symlink the tools (`freecad-diff freecad-difftool freecad-export freecad-diff.py freecad-export.py show-diff.FCMacro`) you need into an existing `$PATH` directory such as /usr/local/bin/.

## usage

build STEP files for any present FCStd files:

```shell
make step
```

build a specific STEP file:

```shell
make examples/example-assembly.step
```

NOTE: as usual with `make`, target files will only be rebuilt if the source file changes on subsequent runs.

visually diff all modified FreeCAD parts and assemblies in a repository (assumes that at least one FCStd file has been mmodified, otherwise nothing will happen):

```shell
git difftool -d --tool=freecad
```

## integration

these tools can be integrated into your own new or existing FreeCAD project repository.

create a repository to house your FreeCAD project files.

copy the `Makefile` from this repository into the project repository.

if you didn't configure globally, add the contents of `example-gitconfig` to `.git/config` in the project repository.

if you want to enable diffing with `git diff`, copy `.gitattributes` to the project repository and uncomment one of the filters.

NOTE: `git diff` copies and diffs a single file at a time, so if you are making use of `App::Link` in your assemblies, the diff of the assembly will not reflect changes to linked parts.

that's it!
