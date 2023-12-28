import matplotlib.pyplot as plt 
import numpy as np

## Converts beats per minute to beat length.
## Yields length of total beats in seconds when using antidx.
def beats2sec(x):
    return 60/x

## Converts beats per minute to beats per second.
## Yields total beat count when using antidx.
def sec2beats(x):
    if x == 0: return x
    return x / 60.0

def pow_series(x,p,c=1):
    return (c*(x**(p+1))) / (p+1)

def map_range(value, outMin, outMax):
    return outMin + ((outMax - outMin) * value)

def antidx_constant(t,sbpm):
    return (t * sbpm)

def antidx_line(t,sbpm,ebpm,p=1,length=1):
    s = (sbpm)
    e = (ebpm)
    if s == e: return antidx_constant(t,s)
    return (s * t) + pow_series(t/length,p,e-s)


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


def get_sec_at_beatcount(graph,time):
    seconds = 0.0
    beats = 0.0
    
    for d in graph:
        max_time = 1e20
        if "b" in d["sofs"]:
            max_time = antidx_constant(float(d["sofs"][:1]), beats2sec(d["bpm"]))
        
        if d["type"] == "C":
            t = min(time,max_time)
            t_seconds = antidx_constant(t,beats2sec(d["bpm"]))
            t_beats = antidx_constant(t_seconds,sec2beats(d["bpm"]))
            
            beats += t_beats
            seconds += t_seconds
        if time < max_time: break
    
    return seconds
    

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

def validate(bd):
    if "b" in bd[0]["sofs"]:
        print("fatal error: b offset used when no bpm existed before")
        return False
    return True


# Returns the index to the tempo change at x seconds.
def get_idx_at_sec(bd,x):
    seconds = 0.0
    beats = 0.0
    idx = 0
    ofs = 0.0
    
    if not validate(bd): raise Exception()
    
    while seconds < x:
        d = bd[idx]
        
        bpm = float(d["bpm"])
        
        d = bd[idx]
        if len(bd) > 1 and idx != len(bd)-1:
            next_d = bd[idx + 1]
            
            if "b" in next_d["sofs"]:
                ofs = antidx_constant(float(next_d["sofs"][:1]), beats2sec(d["bpm"]))
            else:
                ofs = float(d["sofs"])
        else:
            ofs = 100.0
        
        print(bpm, ofs)
        
        temp_ofs = min(ofs,x)
        
        if d["type"] == "C":
            sec = antidx_constant(temp_ofs,beats2sec(bpm),seconds)
            if sec > x:
                print("overshoot")
                temp_ofs = x
                sec = antidx_constant(temp_ofs,beats2sec(bpm),seconds)
            print("report:", seconds, sec)
            
            seconds = sec
            beats = antidx_constant(temp_ofs,sec2beats(bpm),beats)
        
        last_bpm = bpm
        
        if seconds >= x: break
        if idx == len(bd)-1: break
        
        idx += 1
    
    return {
        "idx": idx,
        "seconds": seconds,
        "beats": beats
    }

