# tempograph

**Note:** this software suite is in the conception stage. Contributions welcome.

`tempograph` comes in parts:

- a dense text notation based on ffmpeg's filtergraph (`constant=120:start=1.0,linear=120:140:start=4b`) to describe the tempo of a song ([read more](HOW.md))

- a software library which can query information about notated tempo (x beat's time, total beat count at x time, total time at x beats...) using analytical evaluation of the notation as an integral

- a graphical interface to make tempo notation easy ([ideas](WHAT_GUI.md))




# Prior work

- [Force Dynamics of Tempo Change in Music, 1992](https://continuum-hypothesis.com/music/feldman.pdf) (Jacob Feldman, David Epstein and Whitman Richards) is a covered application of manual tempo notation and analysis