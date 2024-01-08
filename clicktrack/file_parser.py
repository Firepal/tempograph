from functions import ConstantFunction, LinearFunction, OffsetUnit, TimePoint
from clicktrack import make_click_track


def parse_file(filename):
    with open(filename) as f:
        lines = f.read().splitlines()

    # Remove comment lines
    # TODO: remove parts of lines that are commented
    lines = [l for l in lines if not l.startswith("#")]

    functions = []
    start_offset = OffsetUnit(lines[0])
    if start_offset.mode == start_offset.BEATS:
        pos = TimePoint(start_offset.val,0)
    else:
        pos = TimePoint(0, start_offset.val)

    for l in lines[1:]:
        parts = l.split()
        if parts[0] == 'C':
            end = OffsetUnit(parts[2])
            end.shift(pos)
            bpm = float(parts[1])
            functions.append(ConstantFunction(pos.copy(), bpm, end))
        elif parts[0] == 'L':
            end = OffsetUnit(parts[5])
            end.shift(pos)
            start_bpm = float(parts[1])
            end_bpm = float(parts[2])
            power = 1 # TODO
            functions.append(LinearFunction(pos.copy(), start_bpm, end_bpm, power, end))
        pos = functions[-1].end.copy()
    return functions