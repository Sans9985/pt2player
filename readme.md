# pt2player

a script that plays piano tiles 2 songs from the raw json code (literally) and prints out some details

the details in question:
  - the note number (in the part)
  - the note(s) or chord(s)
  - the length code in json data
  - the length of the note in milliseconds

*note: some minor/major performance leaks can happen when playing heavy chords (6+ notes) or repeatedly playing chords (even 2 note ones)*

## changelog:
  * v0.2.0:
    - added a console interface with 4 commands:
      - `version` - prints the current version
      - `sound <sounds> <tempo>` - plays a short sequence of songs as if it was a whole song
      - `play <filename>` - plays a song from a file (as in previous versions)
      - `set <setting> <value>` - changes settings. there are 2 settings:
        1. `volume` - changes the volume
        2. `soundset` - switches the folder of the sounds (must be a folder in `sounds/`)

  * v0.1.2b:
    - fixed bugs with path switcher and error checker

  * v0.1.2:
    - added error checker, path changer (to file path) and more songs

  * v0.1.1:
    - added `readme.md` (this file), slightly changed output, added sample songs

  * v0.1:
    - **main release**