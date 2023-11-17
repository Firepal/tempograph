import matplotlib.pyplot as plt 
import numpy as np

## Converts beats per minute to beat length.
## Yields length of total beats in seconds when using antidx.
def beats2sec(x):
    return 60/x

## Converts beats per minute to beats per second.
## Yields total beat count when using antidx.
def sec2beats(x):
    return x * (1.0/60.0)

def pow_series(x,p,c=1):
    return (c*(x**(p+1))) / (p+1)

def map_range(value, outMin, outMax):
    return outMin + ((outMax - outMin) * value)

def antidx_constant(x,sbpm,c=0):
    return (x * sbpm) + c

def antidx_line(x,sbpm,ebpm,c=0,p=1,length=1):
    s = (sbpm)
    e = (ebpm)
    return (s * x) + pow_series((x/length),p,e-s) + c

print(antidx_constant(1.0,sec2beats(120)))
print(antidx_line(0.5,sec2beats(120),sec2beats(140),c=0,p=1.0,length=100))

# yp = np.array([antidx_linee((i/1000)*4,1,200,p=1,length=4) for i in range(1000)])
# print(yp)
# plt.plot(yp)
# plt.show()


bpm_def = [
    { "type": "C", "bpm": 120, "sofs": "0.000000" },
    { "type": "C", "bpm": 110, "sofs": "8b" },
    { "type": "C", "bpm": 60, "sofs": "4b" },
    { "type": "C", "bpm": 110, "sofs": "8b" }
]


def get_ofs(bd,idx):
    ofs = 0.0
    d = bd[idx]
    if len(bd) > 1:
        next_d = bd[idx + 1]

        if "b" in next_d["sofs"]:
            ofs = antidx_constant(float(next_d["sofs"][:1]), beats2sec(d["bpm"]))
        else:
            ofs = float(d["sofs"])
    else:
        ofs = float(d["sofs"])
    
    return ofs
    

# def evaluate_bpm(bd,x):
    # start_bpm = float(bd[0]["bpm"])
    # last_bpm = None
    # diff = 1.0
    # print("--")
    # for i, d in enumerate(bd):
        # if "b" in d["sofs"] and start_bpm == None:
            # print("fatal error: b offset used when no bpm existed before")
            # break
        
        # bpm = float(d["bpm"])
        # print("bpm:", bpm)
        # if start_bpm == None:
            # print("first bpm found:", bpm)
            # start_bpm = bpm
        # else:
            # diff = start_bpm / bpm
        
        # print("speed scale:", diff)
        
        # ofs = get_ofs(d["sofs"],last_bpm)
        # print("beat offset:", ofs)
           
        # last_bpm = bpm
        # print("--")

def eval(d,x,ofs,func=sec2beats):
    if d["type"] == "C":
        return antidx_constant(x,func(d["bpm"]),c=ofs)
    else:
        return 0


# Returns the index to the tempo change at x seconds.
def get_idx_at_sec(bd,x):
    seconds = 0.0
    idx = 0
    
    while seconds < x:
        d = bd[idx]
        
        if "b" in d["sofs"] and idx == 0:
            print("fatal error: b offset used when no bpm existed before")
            break
        
        bpm = float(d["bpm"])
        
        ofs = get_ofs(bd,idx)
        
        
        if d["type"] == "C":
            seconds = eval(d,x=ofs,ofs=seconds,func=beats2sec)
        
        last_bpm = bpm
        
        if seconds > x: break
        if idx == len(bd)-1: break
        
        idx += 1
    
    return idx
    
# Returns the index to the tempo change at x seconds.
def get_total_beats_at_sec(bd,x):
    beats = 0.0
    seconds = 0.0
    idx = 0
    target_idx = get_idx_at_sec(bd,x)
    
    while seconds < x:
        d = bd[idx]
        
        if "b" in d["sofs"] and idx == 0:
            print("fatal error: b offset used when no bpm existed before")
            break
        
        bpm = float(d["bpm"])
        
        next_d = bd[idx+1]
        
        if "b" in next_d["sofs"]:
            # Get offset to next tempo change
            ofs = antidx_constant(float(next_d["sofs"][:1]),beats2sec(d["bpm"]))
        else:
            ofs = float(d["sofs"])
        
        if d["type"] == "C":
            sec = eval(d,x=ofs,ofs=seconds,func=beats2sec)
            print("sec", sec)
            seconds += sec
            # if seconds
            beats += eval(d,x=sec,ofs=beats,func=sec2beats)
        print(idx, beats)
        
        
        # if beats > x: break
        
        print("seconds", seconds)
        
        idx += 1
    
    return beats

# def get_total_beats_at_sec(bpm_def, x):
    # seconds = 0.0
    # total_beats = 0.0
    # idx = 0

    # while seconds < x and idx < len(bpm_def):
        # d = bpm_def[idx]

        # if "b" in d["sofs"] and idx == 0:
            # print("fatal error: b offset used when no bpm existed before")
            # break

        # bpm = float(d["bpm"])
        
        # ofs = get_ofs(bd,idx)

        # if d["type"] == "C":
            # duration = eval(d, x=ofs, ofs=seconds, func=bpm2sec)
            # if seconds + duration > x:
                # duration = x - seconds  # Adjust duration for the remaining time
            # seconds += duration
            # total_beats += eval(d, x=ofs, ofs=seconds, func=sec2beats)
        # else:
            # duration = ofs - seconds
            # if seconds + duration > x:
                # duration = x - seconds  # Adjust duration for the remaining time
            # seconds += duration
            # total_beats += eval(d, x=ofs, ofs=seconds, func=sec2beats)

        # last_bpm = bpm

        # idx += 1

    # return total_beats


print(bpm_def)
print(get_idx_at_sec(bpm_def,5.0))
print(get_total_beats_at_sec(bpm_def,8.0))
# print(antidx_constant(1.0,bpm2sec(120)))