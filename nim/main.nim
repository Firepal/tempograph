import streams
import std/[sequtils,os]
import asyncdispatch
import typetraits

echo "ah yes"

let fname = "Mare Nova_126bpm.wav"

var strm = openFileStream(fname,fmRead)

type SoundFileData* [T = SomeNumber] = 
    object
        data_sample*: seq[T]


proc readWAV*(wavfile: FileStream) {.async.} =
    
    var header = newSeq[int8](44)
    discard wavfile.readData(addr(header[0]),44)
    wavfile.setPosition(44)
    

var fsize = os.getFileSize(fname)
var snddata = newSeq[int16](fsize div sizeof(int16))
var hdrdata = newSeq[int8](44)

echo name(type(snddata))

discard strm.readData(addr(hdrdata[0]),44)
strm.setPosition(44)
discard strm.readData(addr(snddata[0]),fsize-44)


echo "beeg array"
echo $snddata.len

proc calcBeatSize(bpm: int, smprate: int): int =
    return ((60/bpm) * smprate.float).int

let smp = 44100

let fineness = 1.0

proc evenify(x: Natural): int =
    return x + int(x mod 2 == 1)

var srcBS = (calcBeatSize(126,smp).float / fineness).int
var dstBS = (calcBeatSize(120,smp).float / fineness).int


let diffBS = srcBS-dstBS
echo "src:", srcBS
echo "dst:", dstBS
echo "diffBS: ", diffBS

proc lerp*(a: float, b: float, c: float): float =
    result = (a * (1.0 - c)) + (b * c)

proc smoothstep(x: float): float =
    return x * x * (3.0 - 2.0 * x)


var slices = newSeq[seq[int16]]()
var sliceinterp = newSeq[int16]()
var i: int64 = 0

while i < snddata.len:
    var ns = snddata[i..min(i+dstBS,snddata.len-1)]
    # if i > 0:
        # var mix = newSeq[int16]()
        # if ns.len > sliceinterp.len:           
            # let silen = ((min(min(sliceinterp.len,ns.len),20))-1) div 2
            # echo silen
            
            # let rcpt = 1.0/silen.float
            # for j in 0..silen:
                # let y = j*2
                # let fac = smoothstep(j.float*rcpt)
                # ns[y] =   lerp(sliceinterp[y].float, ns[y].float, fac).int16
                # ns[y+1] = lerp(sliceinterp[y+1].float, ns[y+1].float, fac).int16
        # else:
            # echo "fuck"
    slices.add(ns)
    
    # if ns.len > sliceinterp.len:    
        # sliceinterp = snddata[i+dstBS..evenify(i+srcBS)]
    i += srcBS
    

echo "processing complete"

proc flattenSeq[T](inputSeq: seq[seq[T]]): seq[T] =
  var resultSeq: seq[T] = @[]
  for seqItem in inputSeq:
    for item in seqItem:
      resultSeq.add(item)
  return resultSeq

echo "flattening"
var slicesdata = flattenSeq(slices)
echo slicesdata.len


var wStrm = openFileStream("yes.wav",fmWrite)
wStrm.writeData(addr(hdrdata[0]),hdrdata.len)
wStrm.writeData(addr(slicesdata[0]),slicesdata.len*sizeof(int16))

wStrm.close()