BINARY := freecad-export freecad-diff freecad-difftool freecad-export.py freecad-diff.py
COMMON := freecad_build.py
MACROS := show-diff.FCMacro

all:
	@echo "run 'sudo make install' to install system wide"
.PHONY: all

install:
	mkdir -p /usr/local/bin/
	cp -v $(BINARY) /usr/local/bin/
	mkdir -p /usr/share/freecad/Ext/freecad_build/
	cp -v $(COMMON) /usr/share/freecad/Ext/freecad_build/__init__.py
	mkdir -p /usr/share/freecad/Macro/
	cp -v $(MACROS) /usr/share/freecad/Macro/
.PHONY: install

uninstall:
	cd /usr/local/bin/ && rm -v $(BINARY)
	rm -rfv /usr/share/freecad/Ext/freecad_build/
	cd /usr/share/freecad/Macro/ && rm -v $(MACROS)
.PHONY: uninstall
