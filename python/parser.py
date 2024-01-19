import sys

def parse_input(input_str):
    result = {}
    tokens = input_str.split(',')

    for token in tokens:
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
            split_col = value_str.split(':')
            keyvals = [val.split('=') for val in split_col]

            values = [{val[0]: get_num_or_str(val[1])} if len(val) == 2 else get_num_or_str(val[0]) for val in keyvals]
        else:
            kv = value_str.split('=')

            val = kv[0]
            if len(kv) == 2: val = kv[1]


            values = [float(val) if isdigitorfloat(val) else val]

        if key not in result:
            result[key] = []

        result[key] = values

    return result

def serialize(d):
    result = ""

    for i, key in enumerate(d.keys()):
        result += key + "="
        val = d[key]

        for j, v in enumerate(val):
            s = ""
            if isinstance(v,dict):
                s += list(v.keys())[0] + "="
                s += str(list(v.values())[0])
            else:
                s += str(v)


            result += s
            if j < len(val)-1:
                result += ":"

        if i < len(d.keys())-1:
            result += ","

    return result


if not len(sys.argv) < 2:
    inp = sys.argv[1]

    print("input:", inp)
    parsed = parse_input(inp)
    print("parsed:", parsed)
    print("output:", serialize(parsed))
