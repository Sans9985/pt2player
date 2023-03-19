# pt2player

a script that plays piano tiles 2 songs from the raw json code (literally) and prints out some details

the details in question:
  - the note number (in the part)
  - the note(s) or chord(s)
  - the length code in json data
  - the length of the note in milliseconds

*note: some minor/major performance leaks can happen when playing heavy chords (6+ notes) or repeatedly playing chords (even 2 note ones)*