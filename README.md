# tempotools

a command-line thing which can play with a song's tempo, using special tempo metadata

# goals
allow one to:
- define the full tempo of a song, with skips and non-linear tempo changes, using a GUI
- remap the tempo using this detailed representation, in a GUI or on the command-line


# [how](HOW.md)
the idea is to have a metadata field for audio files (maybe called BPM_EXTENDED)
which will store characteristics of the tempo such as simple "jump" tempo changes, linear tempo changes and non-linear tempo changes

the software will be able to recognise (or be given) this metadata and allow the user
to do various things with the song, including cutting every x beats, linearizing the whole song to one constant tempo
