import sys

from common import load_parts, fuse_parts, count_parts, export_parts

EXPORT_FUSED = True


def main():
    path, dest = sys.argv[1:]

    doc, parts = load_parts(path)

    if EXPORT_FUSED and len(parts) > 1 or count_parts(parts[0].Group) > 1:
        fused = fuse_parts(doc, parts)
        fused.Label = doc.Label + '-fused'
        export_parts([fused], dest)
    else:
        export_parts(parts, dest)

    #sys.exit(0)


if __name__ == 'freecad-export':
    main()
