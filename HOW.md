# Types used for simplicity

## OffsetUnit
a number with at most 6 decimals that can represent either seconds or beats.
This is denoted using a suffix.

Example:
`0.166666` means 1/60th of a second.

`0.1b` means 1/10 of a beat. Can only be used if tempo was previously declared.


# Tempo declaration

## CONSTANT
Describes a constant tempo that will simply be `bpm` until another declaration is found.

- beatsperminute (bpm): `float`
- start_offset (sofs): `OffsetUnit`

## POWER
Describes a tempo that changes from `start_bpm` to `end_bpm`
during `length` with a non-linearity of `power`.

- start_bpm (sbpm): `float`
- end_bpm (ebpm): `float`
- length: `float`
- power (p): `float`
- start_offset (sofs): `OffsetUnit`

## POLYNOMIAL
Describes a tempo that changes from `start_bpm` to `end_bpm` during `length`
with respect to the [0,1] bound of the xnd-degree polynomial function defined in `p`.

- start_bpm (sbpm): `float`
- end_bpm (ebpm): `float`
- length: `float`
- orders (p): `list(float)`
- start_offset (sofs): `OffsetUnit`

