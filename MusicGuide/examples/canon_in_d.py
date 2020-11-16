from MusicGuide.src.main import *

            
score = Score()
melody = Staff()
score.add_staff(melody)
melody.add_signature("4/4")
melody.add_key("d major")
melody.add_clef("treble")
notes = ["R 1", "R 1", "R 1", "R 1"]

#line 5
notes += ["f# 5 2", "e 5 2", "d 5 2", "c# 5 2", "b 4 2", "a 4 2", "b 4 2", "c# 5 2"]

#line 13
notes += ["d 5 4", "f# 5 4", "a 5 4", "g 5 4", "f# 5 4", "d 5 4", "f# 5 4.", "e 4 8"]
notes += ["d 5 4", "b 4 4", "d 5 4", "f# 5 4", "g 5 4", "b 5 4", "a 5 4.", "g 5 8"]

# line 21
notes += ["d 5 8", "c# 5 8", "d 5 8", "a 4 8", "a 4 4", "c# 5 4"]
notes += ["d 5 4", "f# 5 4", "b 5 4.", "c# 6 8"]
notes += ["g 4 8", "f# 4 8", "e 4 8", "g 4 8", "f# 4 8", "e 4 8", "d 4 8", "c# 4 8"]
notes += ["b 3 8", "a 3 8", "d 4 4", "d 4 4.", "c# 4 8"]

# line 29
notes += ["d 5 8", "c# 5 8", "d 5 8", "a 4 8", "c# 5 8", "a 4 8", "e 5 8", "f# 5 8"]
notes += ["d 5 8",  "d 5 8", "c# 5 8", "b 4 8", "c# 5 8", "f# 5 8", "a 5 8", "b 5 8"]
notes += ["g 5 8", "f# 5 8", "e 5 8", "g 5 8", "f# 5 8", "e 5 8", "d 5 8", "c# 5 8"]
notes += ["b 4 8", "a 4 8", "g 4 8", "f# 4 8", "e 4 8", "g 4 8", "f# 4 8", "e 4 8"]

# line 37
notes += ["a 5 8", "f# 5 16", "g 5 16"]
notes += ["a 5 8", "f# 5 16", "g 5 16"]
notes += ["a 5 16", "a 4 16", "b 4 16", "c# 5 16", "d 5 16", "e 5 16", "f# 5 16", "g 5 16"]
          
notes += ["f# 5 8", "d 5 16", "e 5 16"]
notes += ["f# 5 8", "f 4 16", "g 4 16"]
notes += ["a 4 16", "b 4 16", "a 4 16", "g 4 16", "a 4 16", "f# 4 16", "g 4 16", "a 4 16"]
          
notes += ["g 4 8", "b 4 16", "a 4 16"]
notes += ["g 4 8", "f# 4 16", "e 4 16"]
notes += ["f# 4 16", "e 4 16","d 4 16", "e 4 16", "f# 4 16", "g 4 16", "a 4 16", "b 4 16"]

# measure 40
notes += ["g 4 8", "b 4 16", "a 4 16"]
notes += ["b 4 8", "c# 5 16", "d 5 16"]
notes += ["a 4 16", "b 4 16", "c# 5 16", "d 5 16", "e 5 16", "f# 5 16", "g 5 16", "a 5 16"]

notes += ["a 5 8", "f# 5 16", "g 5 16"]
notes += ["a 5 8", "f# 5 16", "g 5 16"]
notes += ["a 5 8", "a 4 16", "b 4 16", "c# 5 16", "d 5 16", "e 5 16", "f# 5 16", "g 5 16"]

notes += ["f# 5 8", "d 5 16", "e 5 16"]
notes += ["f# 5 8", "f 4 16", "g 4 16"]
notes += ["a 4 16", "b 4 16", "a 4 16", "g 4 16", "a 4 16", "f# 4 16", "g 4 16", "a 4 16"]

melody.add_notes(notes)

bass = Staff()
score.add_staff(bass)
bass.add_signature("4/4")
bass.add_key("d major")
bass.add_clef("bass")
notes_base = ["d 3 8", "a 3 8", "d 4 8", "f# 4 8", "a 2 8", "e 3 8", "a 3 8", "c# 4 8"]
notes_base += ["b 2 8", "f# 3 8", "b 3 8", "d 4 8", "f# 2 8", "c# 3 8", "f# 3 8", "a 3 8"]
notes_base += ["g 2 8", "d 3 8", "g 3 8", "b 3 8", "d 2 8", "a 2 8", "d 3 8", "f# 3 8"]
notes_base += ["g 2 8", "d 3 8", "g 3 8", "b 3 8", "a 2 8", "e 3 8", "a 3 8", "c# 4 8"]
          
notes = []
for i in range(6):
    notes += notes_base

bass.add_notes(notes)
#score.change_instrumentation(["violin", "violin"])

#score.add_intervals_harmony(melody, "violin")
# score.add_intervals_harmony(melody, "cello")
#score.add_intervals_harmony(melody, "viola")
# score.add_intervals_harmony(melody, "violin")
# score.add_chord_harmony(melody)
score.add_header("Canon in D", "Johann Pachelbel")
score.generate_lilypond("canon_in_d.ly")
