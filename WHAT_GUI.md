# GUI
ideas for the GUI



## Layout
Tempo changes are shown as color-coded "blocks" with names on the inside top-left.<br><br>
At all zoom levels, we show the line going from the minimum BPM to the maximum BPM going through all blocks.
At a low-enough zoom level, we also show markers at each beat inside all blocks.<br>

We show the waveform of the loaded audio.

In the same way that Audacity has the "Label Track" separate from the music,
we should show our tempo changes below the waveform.

We should have an option that makes "beat markers" show on top of the waveform as well for easier alignment.

## "Freeform" block
I'm thinking there should be this virtual tempo change type, 
where the user can place a marker on each beat. 

This can then be converted into standard "polynomial" blocks by applying polynomial regression. We'll have several (likely one for every 4 or 8 beats) because polynomials don't accurately fit at high point counts.