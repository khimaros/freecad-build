PARTS := $(wildcard **/*.FCStd)

PARTS_STEP := $(addsuffix .step, $(basename $(PARTS)))
PARTS_DXF := $(addsuffix .dxf, $(basename $(PARTS)))
PARTS_3MF := $(addsuffix .3mf, $(basename $(PARTS)))
PARTS_GCODE := $(addsuffix .gcode, $(basename $(PARTS)))

PARTS_CLEAN := $(wildcard **/*.step **/*.dxf **/*.3mf **/*.gcode **/*.FCBak)

all: step 3mf gcode
.PHONY: all

step: $(PARTS_STEP)
.PHONY: step

dxf: $(PARTS_DXF)
.PHONY: dxf

3mf: $(PARTS_3MF)
.PHONY: 3mf

gcode: $(PARTS_GCODE)
.PHONY: gcode

%.step: %.FCStd
	freecad-export "$<" "$@"

%.dxf: %.FCStd
	freecad-export "$<" "$@"

%.3mf: %.FCStd
	freecad-export "$<" "$@"

%.gcode: %.3mf
	#prusa-slicer --export-gcode "$<"
	#slic3r --no-gui --duplicate 6 "$<"
	slic3r --no-gui "$<"

clean:
	rm -f $(PARTS_CLEAN)
.PHONY: clean
