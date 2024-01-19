from main import *
import math
import sys

def equal_approx(a,b):
    return abs(a-b) < 1e-20

def t_basic():
    # Getting the length of 8 beats at 120 BPM in seconds
    assert equal_approx(antidx_constant(8.0,beats2sec(120)), 4.0)
    return True

def t_beatcount():
    # Running the output of a function into itself with inverse BPM yields the beat count during that time.
    _bpm = 160
    beatcount = 2
    prelen_sec = antidx_constant(2,         beats2sec(_bpm))
    beatcount = antidx_constant(prelen_sec, sec2beats(_bpm)) # This should always return 2
    assert beatcount == 2
    return True

def antidx_any(t,d,func):
    if d["type"].upper() in ["C","CONSTANT"]:
        return(antidx_constant(t,func(d["bpm"])))


def get_beatcount_at_sec(graph,time):
    seconds = 0.0
    beats = 0.0
    
    for i, d in enumerate(graph):
        max_time = 1e20
        if i < len(graph)-1:
            next_d = graph[i+1]["sofs"]
            print(next_d)
            if "b" in next_d:
                max_time = antidx_any(float(next_d[:1]),d,beats2sec)
        
        t = min(time,max_time)
        print("mt:",max_time)
        print("time:",time)
        print("t:",t)
        
        if d["type"] == "C":
            t_beats = antidx_any(t,d,sec2beats)
            t_seconds = antidx_any(t_beats,d,beats2sec)
            
            beats += t_beats
            seconds += t_seconds
        print("sec:", seconds)
        if time > max_time or seconds >= time: break
    
    return beats

def t_beatcount_fn():
    g_test = [
        { "type": "C", "bpm": 120, "sofs": "0.000000" },
    ]
    
    beatcount = get_beatcount_at_sec(g_test,1.0)
    print(1.0, "sec ->", beatcount, "beats")
    assert beatcount == 2
    return True

def t_beatcount_fn2():
    g_test = [
        { "type": "C", "bpm": 120, "sofs": "0.000000" },
        { "type": "C", "bpm": 160, "sofs": "8b" },
    ]
    
    beatcount = get_beatcount_at_sec(g_test,5.0)
    print(4.0, "sec ->", beatcount, "beats")
    assert beatcount == 8
    return True

# def t_timeatbeat_fn():
    # g_test = [
        # { "type": "C", "bpm": 120, "sofs": "0.000000" },
        # { "type": "C", "bpm": 60, "sofs": "8b" },
    # ]
    
    # time = get_sec_at_beatcount(g_test,1.0)
    # print(time)
    
    # # assert time == 0.5
    # return True


if __name__ == '__main__':
    this_mod = sys.modules[__name__]
    
    for func in [getattr(this_mod,f) for f in dir(this_mod) if f.startswith("t_")]:
        if func():
            print(func.__name__, "passed")
        else:
            print(func.__name__, "had an unhandled error")
        print("---")