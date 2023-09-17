import os.path
import sys

import FreeCAD
import Import
import Part

INCLUDE_SUBASSEMBLIES = False

PART_TYPEIDS = ('PartDesign::Body', 'App::Part', 'Part::Feature')


def auto_part_label(dest):
    return '.'.join(os.path.basename(dest).split('.')[0:-1])


def has_part(o):
    if o.TypeId == 'App::Link' and o.LinkedObject.TypeId in PART_TYPEIDS:
        return True

    if not o.Visibility:
        return False

    if o.TypeId in PART_TYPEIDS:
        return True

    return False


def find_labeled_part(doc, label):
    print('### finding part with label', label)
    found = doc.findObjects(Label=label)
    if found:
        print('### found labeled part')
        return found[0]

    return None


def find_parts(doc, label=None, max_parts=0):
    parts = []

    if label:
        part = find_labeled_part(doc, label)
        if part:
            parts.append(part)

    if not max_parts or len(parts) < max_parts:
        print('### searching for usable parts...')
        for o in doc.Objects:
            #print('### checking', o.FullName, type(o), o.TypeId, o.Visibility)

            #if hasattr(o, 'LinkedObject'):
            if o.TypeId == 'App::Link':
                print('### linked object', o.LinkedObject.FullName, type(o.LinkedObject),
                      o.LinkedObject.TypeId, o.LinkedObject.Visibility)

                if o.LinkedObject.Name == 'Assembly':
                    print('### subassembly', o.LinkedObject.FullName)
                    if INCLUDE_SUBASSEMBLIES:
                        o.LinkedObject.Document.recompute()
                        parts.extend(find_parts(o.LinkedObject.Document))

            if has_part(o):
                parts.append(o)

            if max_parts and len(parts) >= max_parts:
                break

    for part in parts:
        print('### found usable part', part.FullName, part.TypeId)

    if not parts:
        print('### could not any usable parts in', path)
        sys.exit(1)

    return parts


def load_parts(path):
    fmt = path.rpartition('.')[-1]

    print('### loading document', path, fmt)

    FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Import/hSTEP").SetBool("ReadShapeCompoundMode", True)
    FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Import").SetInt("ImportMode", 0)
    FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Import").SetBool("ImportHiddenObject", False)
    FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Import").SetBool("ExpandCompound", False)
    FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Import").SetBool("UseBaseName", False)
    FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Import").SetBool("UseLinkGroup", False)
    FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Import").SetBool("ShowProgress", False)

    if fmt == 'step':
        Import.open(path)
    else:
        FreeCAD.openDocument(path)

    doc = FreeCAD.ActiveDocument

    print('### active document', doc.FileName)

    doc.recompute()

    label = auto_part_label(path)

    max_parts = 1
    if hasattr(doc, 'Assembly'):
        max_parts = 0

    parts = find_parts(doc, label, max_parts)

    return doc, parts


def export_parts(parts, dest):
    fmt = dest.rpartition('.')[-1]

    print('### exporting', fmt, dest)

    FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Import").SetBool("ExportHiddenObject", False)
    FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Import").SetBool("ReduceObjects", False)
    FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Import").SetBool("UseLinkGroup", False)
    FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Import").SetBool("ShowProgress", False)

    if fmt in ('3mf', 'stl', 'wrl', 'obj'):
        import Mesh
        Mesh.export(parts, dest)
    elif fmt == 'dxf':
        import Draft
        views = []
        for part in parts:
            view = Draft.make_shape2dview(part, FreeCAD.Vector(-0.0, -0.0, 1.0))
            views.append(view)
        doc.recompute()
        import importDXF
        importDXF.export(views, dest)
    else:
        import Import
        Import.export(parts, dest)

    print('### export successful')


def fuse_parts(doc, parts):
    print('### fusing parts:', [o.FullName for o in parts])

    doc.addObject("Part::MultiFuse","Fusion")
    doc.Fusion.Shapes = parts
    doc.recompute()

    return doc.Fusion


def count_parts(objects):
    count = 0
    for o in objects:
        if has_part(o):
            count += 1
    return count

