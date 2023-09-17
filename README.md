# FREECAD BUILD

build tools for FreeCAD based CAD projects, including Git diff integration and headless part export

this repository contains standalone tools for converting FCStd files into a variety of formats including STEP, 3MF, and GCODE (`freecad-export`) as well as tooling to integrate mesh diffs into standard git workflows (`freecad-difftool`, `freecad-diff`).

it also serves as a sort of template repository for creating build tooling around a FreeCAD project. the included `Makefile` could be copied to another repository verbatim.

## usage

build STEP files for all FCStd files in a repository:

```shell
make step
```

build a specific step file:

```shell
make examples/example-assembly.step
```

visually diff all modified FreeCAD parts and assemblies in a repository (assumes that at least one FCStd file has been mmodified, otherwise nothing will happen):

```shell
git difftool -d --tool=freecad
```

## prepare

install dependencies:

```shell
apt install git make freecad
```

clone this repository to a known location.

add the contents of [example-gitconfig](example-gitconfig) to `.git/config` in your FreeCAD project repo or to `~/.gitconfig` for global:

```shell
cat example-gitconfig >> ~/.gitconfig
```

append this directory to your `$PATH` in `~/.bashrc` or symlink the tools you need into an existing `$PATH` directory.

```shell
echo 'PATH="${PATH}:${PWD}"' >> ~/.bashrc
```

## integrate

these tools can be integrated into your own new or existing FreeCAD project repository.

create a repository to house your FreeCAD project files.

copy the `Makefile` from this repository into the project repository.

copy `.gitattributes` to the project repository.

add the contents of `example-gitconfig` to `.git/config` in the project repository (if you didn't do so globally before).

that's it!

## limitations

- these tools were tested with Debian Trixie and FreeCAD version 0.20.2
- if a part is modified but its parent assembly is not saved, the assembly diff will be empty
- if you use `git difftool` on a single file, no other modified files will be part of the diff context
