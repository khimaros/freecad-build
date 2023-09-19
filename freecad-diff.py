#!/usr/bin/env freecadcmd

import sys

from common import load_parts, export_parts, find_labeled_part

import FreeCAD


def main():
    if len(sys.argv) != 4:
        print('usage: freecad-diff <part1> <part2> <output>')
        sys.exit(1)

    path1, path2, path3 = sys.argv[1:]

    doc1, parts1 = load_parts(path1)
    part1 = parts1[0]
    part1.Visibility = False
    part1.Label = 'Modified'

    doc2, parts2 = load_parts(path2)
    part2 = parts2[0]
    part2.Visibility = False
    part2.Label = 'Previous'

    print('### creating diff document')
    FreeCAD.newDocument()
    doc3 = FreeCAD.ActiveDocument

    print('### copying objects to diff document')
    doc3.copyObject(part1, True)
    doc3.copyObject(part2, True)

    part1_copy = find_labeled_part(doc3, 'Modified')
    part2_copy = find_labeled_part(doc3, 'Previous')

    exports = []

    print('### creating additions cut')
    doc3.addObject("Part::Cut", "Additions")
    doc3.Additions.Base = part1_copy
    doc3.Additions.Tool = part2_copy
    doc3.Additions.Label = 'Additions'
    cut1 = doc3.Additions

    print('### creating subtractions cut')
    doc3.addObject("Part::Cut", "Subtractions")
    doc3.Subtractions.Base = part2_copy
    doc3.Subtractions.Tool = part1_copy
    doc3.Subtractions.Label = 'Subtractions'
    cut2 = doc3.Subtractions

    doc3.recompute()

    exports.append(part1_copy)
    exports.append(part2_copy)
    exports.append(cut1)
    exports.append(cut2)

    export_parts(exports, path3)

    #sys.exit(0)


if __name__ == 'freecad-diff':
    main()
