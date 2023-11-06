import matplotlib.pyplot as plt 
import numpy as np

## Converts beats per minute to beat length.
## Yields length of total beats in seconds when using antidx.
def bpm2blen(x):
    return 60/x

## Converts beats per minute to beats per second.
## Yields total beat count when using antidx.
def bpm2bps(x):
    return x/60

def pow_series(x,p,c=1):
    return (c*(x**(p+1))) / (p+1)

def map_range(value, outMin, outMax):
    return outMin + ((outMax - outMin) * value)

def antidx_constant(x,sbpm,c=0):
    return (x * sbpm) + c

def antidx_linee(x,sbpm,ebpm,c=0,p=1,length=1):
    s = (sbpm)
    e = (ebpm)
    return (s * x) + pow_series((x/length),p,e-s) + c

print(antidx_constant(1.0,bpm2bps(120)))
print(antidx_linee(0.5,bpm2bps(120),bpm2bps(140),c=0,p=1.0,length=100))

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


def get_ofs(ofs_string,bpm):
    num = float(ofs_string.replace('b',''))
    
    if "b" in ofs_string: num *= 60 / bpm
    
    return num
    

def evaluate_bpm(bd,x):
    start_bpm = float(bd[0]["bpm"])
    last_bpm = None
    diff = 1.0
    print("--")
    for i, d in enumerate(bd):
        if "b" in d["sofs"] and start_bpm == None:
            print("fatal error: b offset used when no bpm existed before")
            break
        
        bpm = float(d["bpm"])
        print("bpm:", bpm)
        if start_bpm == None:
            print("first bpm found:", bpm)
            start_bpm = bpm
        else:
            diff = start_bpm / bpm
        
        print("speed scale:", diff)
        
        ofs = get_ofs(d["sofs"],last_bpm)
        print("beat offset:", ofs)
           
        last_bpm = bpm
        print("--")

def get_totalbeats_at_sec(bd,x):
    last_bpm = None
    print("--")
    seconds = 0.0
    for i, d in enumerate(bd):
        if "b" in d["sofs"] and last_bpm == None:
            print("fatal error: b offset used when no bpm existed before")
            break
        
        bpm = float(d["bpm"])
        
        
        if "b" in d["sofs"]:
            # Get offset from last tempo change
            ofs = antidx_constant(float(d["sofs"][:1]),bpm2blen(bd[i-1]["bpm"]))
        else:
            ofs = float(d["sofs"])
        
        
        print("bpm:", bpm)
        print("beat offset:", ofs)
        
        if d["type"] == "C":
            seconds += antidx_constant(1.0,bpm2bps(bpm),c=ofs)
            print(seconds)
        last_bpm = bpm
        print("--")
    
    return seconds
    

get_totalbeats_at_sec(bpm_def,1.0)