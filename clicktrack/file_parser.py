from functions import ConstantFunction, LinearFunction, OffsetUnit, TimePoint
from clicktrack import make_click_track


def arden_parser(lines_in):
    # Remove comment lines
    # TODO: remove parts of lines that are commented
    lines = [l for l in lines_in if not l.startswith("#")]

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

def pal_preparse(line_in):
    result = []
    tokens = line_in.split(',')

    for token in tokens:
        defdict = {}
        key_value_pair = token.split('=')
        key = key_value_pair[0]
        value_str = '='.join(key_value_pair[1:])

        def isdigitorfloat(s):
            return s.replace('.','',1).isdigit()

        def get_num(s):
            if '.' in s: return float(s)
            else: return int(s)

        def get_num_or_str(s):
            if isdigitorfloat(s): return get_num(s)
            else: return s
        
        if ':' in value_str:
            # TBD:
            # both key-value pairs and unlabeled values (key determined via hardcoded order) are legal.
            # can we safely extrapolate what the user meant
            # if they mix and match the systems?
            # need to find inspiration from ffmpeg or something
            split_col = value_str.split(':')
            keyvals = [val.split('=') for val in split_col]

            values = [{val[0]: get_num_or_str(val[1])} if len(val) == 2 else get_num_or_str(val[0]) for val in keyvals]
        else:
            kv = value_str.split('=')

            val = kv[0]
            if len(kv) == 2: val = kv[1]

            values = [float(val) if isdigitorfloat(val) else val]

        # hmm this looks odd, chatgpt or did i have brainfart?
        if key not in defdict: defdict[key] = []

        defdict[key] = values
        
        result.append(defdict)

    return result

def pal_parser(lines_in):
    raw_parse = pal_preparse(lines_in[0])
    
    
    if start_offset.mode == start_offset.BEATS:
        pos = TimePoint(start_offset.val,0)
    else:
        pos = TimePoint(0, start_offset.val)
    
    for change in raw_parse:
        c_type = list(change.keys())[0]
        c_vals = list(change.values())[0]
        
        # it's 4AM and I realize I've envisioned the format
        # to store start-offsets, not ends.
        # and i just remembered that this implementation
        # is designed to have defined ends.
        
        # I guess we can add an arbitrary "end gap"
        # after the last tempo change if we don't know the audio length.
        # I would like to tackle this... gotta sleep first.
        
        # TODO: implement key-value order as a dictionary with int keys and str values???
        
        if c_type == 'C':
            end = OffsetUnit(c_vals[1])
            # end.shift(pos)
            bpm = float(parts[1])
            functions.append(ConstantFunction(pos.copy(), bpm, end))
        elif c_type == 'L':
            end = OffsetUnit(parts[5])
            # end.shift(pos)
            start_bpm = float(parts[1])
            end_bpm = float(parts[2])
            power = 1 # TODO
            functions.append(LinearFunction(None, start_bpm, end_bpm, power, end))
            
    

def parse_file(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
    
    is_arden = not ('=' in lines[0])
    
    functions = None
    if is_arden:
        functions = arden_parser(lines)
    else:
        functions = pal_parser(lines)

    return functions

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2: quit()
    target = sys.argv[1]
    print(parse_file(target))
    