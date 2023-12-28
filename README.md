# tempograph

**Note:** this software suite is in the conception stage. Contributions welcome.

`tempograph` comes in parts:

- a dense text notation based on ffmpeg's filtergraph (`name=value:any_key=value`) to describe the tempo of a song (constant or variable)

- a software library which can query information about notated tempo (x beat's time, total beat count at x time, total time at x beats...) using analytical evaluation of the notation as an integral

- a graphical interface to make tempo notation easy


[Read more.](HOW.md)

# Prior work

- [Force Dynamics of Tempo Change in Music, 1992](https://continuum-hypothesis.com/music/feldman.pdf) (Jacob Feldman, David Epstein and Whitman Richards) is a covered application of manual tempo notation and analysis