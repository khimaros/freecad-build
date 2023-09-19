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

- these tools have only been tested with Debian Trixie and FreeCAD version 0.20.2
- **sub**-assemblies of an assembly are not currently included diffs or exports (this is on the roadmap)
- if a part is modified but its parent assembly is not subsequently saved, the assembly diff will be skipped by git
- if you use `git difftool` on a single file (or if you use the `git diff` integration), modified files are diffed one by one, which means changes to `App::Link` parts in other files will not be reflected.

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

### diff

NOTE: the following assumes that at least one FCStd file has been mmodified, otherwise nothing will happen:

visually diff all modified FreeCAD parts and assemblies in the repository:

```shell
git difftool -d --tool=freecad
```

after a weight relative to the complexity of the exported part, a FreeCAD window will open with at least two and at most four features.

**Previous**: the exported part from HEAD

**Modified**: the exported part including modifications in your worktree

**Additions**: any geometry which was added by your modifications (green)

**Subtractions**: any geometry which was removed by your modifications (red)

NOTE: the first two features are always present, the others are present only if the diff is non-empty

### export

export STEP files for any present FCStd files:

```shell
make step
```

build a specific STEP file:

```shell
make examples/example-assembly.step
```

NOTE: as usual with `make`, target files will only be rebuilt on subsequent runs if the source file has changed.

generate 3MF or Gcode for a part:

```shell
make examples/example-assembly.3mf
make examples/example-assembly.gcode
```

other file formats are supported by `freecad-export`, but would need to be added to the `Makefile`.

here's an example using `freecad-export` directly:

```shell
freecad-export examples/example-assembly.FCStd examples/example-assembly.iges
```

## integration

these tools can be integrated into your own new or existing FreeCAD project repository.

create a repository to house your FreeCAD project files.

copy the `Makefile` from this repository into the project repository.

if you didn't configure globally, add the contents of `example-gitconfig` to `.git/config` in the project repository.

if you want to enable diffing with `git diff`, copy `.gitattributes` to the project repository and uncomment one of the filters.

NOTE: `git diff` copies and diffs a single file at a time, so if you are making use of `App::Link` in your assemblies, the diff of the assembly will not reflect changes to linked parts.

take a look at `.gitignore` and potentially copy that to your repository.

that's it!

## troubleshooting

check the log output on the console, make sure there are no `recompute` errors.

inspect the **Modified** and **Previous** features to make sure they look as expected.
