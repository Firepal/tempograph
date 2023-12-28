# The idea
Let's represent tempo as a list of functions. These functions return tempo as BPM. 

With this representation, you can get tempo at any time in a song.<br>
You can also get the passed beats at any real time in the song,
or real time at any beat in the song, via analytical integration of each function in sequence.

- This representation makes it possible to transform between two tempo representations.

  This allows one to, for example, take a song with variable tempo and transform it to constant tempo (and vice-versa).

- Another application allows rhythm game chart makers to map songs with variable tempo easily.<br>
  Should be easy enough to just transform discrete note values of their map format between tempo representations.

- A graphical editor for "tempo graphs" is considered. Could make this very accessible.

- A long-term goal would be to have a database of "tempo graphs" 
  to allow anyone to contribute or download them, like MusicBrainz for music information.

# Types used for simplicity

## OffsetUnit
a number with at most 6 decimals(?) that can represent either seconds or beats.
This is denoted using a suffix.

Example:
`0.166666` means 1/60th of a second.

`0.1b` means 1/10 of a beat. Can only be used if tempo was previously declared.


# Tempo methods

## CONSTANT
Describes a constant tempo `bpm` until the next tempo change.

- beatsperminute (bpm): `float`
- start_offset (sofs): `OffsetUnit`

## LINE
Describes a tempo that changes from `start_bpm` to `end_bpm`
during `length` with a non-linearity of `power`.
If `length` is left undefined, it will last until the next tempo change.
If this is the last tempo change, `length` field *must* be set.

- start_bpm (sbpm): `float`
- end_bpm (ebpm): `float`
- length (l): `float`
- power (p): `float`
- start_offset (sofs): `OffsetUnit`

## POLYNOMIAL
Describes a tempo that changes from `start_bpm` to `end_bpm` during `length`
with respect to the [0,1] XY-axis range of the xnd-degree polynomial function defined in `p`.
If `length` is left undefined, it will last until the next tempo change.
If this is the last tempo change, `length` field *must* be set.

tempograph shall remap the X-axis from [0,1] to [0,length] (stretch) and the Y-axis from [0,1] to [s,e] automatically.

Polynomials are curves that can go up and down over time. They should be pretty performant, as they're
[easy to calculate integrals for.](en.wikipedia.org/wiki/Polynomial#Calculus)

This is intended for tempo changes where you think `LINE` might still be too linear and not flexible enough. 
Musicians using DAWs may use "smooth"-type interpolation for tempo changes, 
and this intends to be a catch-all solution to that.

Users are not expected to manually create the polynomial;
they're expected to make CONSTANT tempo changes representing one beat each,
and use 
[polynomial regression](https://en.wikipedia.org/wiki/Curve_fitting#Fitting_lines_and_polynomial_functions_to_data_points)
on them.
The graphical editor should have this functionality.

- start_bpm (s): `float`
- end_bpm (e): `float`
- length(l): `float`
- terms: list of `float`
- start_offset (sofs): `OffsetUnit`

