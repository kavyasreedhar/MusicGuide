from MusicGuide.src.main import *

score = Score()
melody = Staff()
score.add_staff(melody)
melody.add_signature("3/8")
melody.add_key("C major")
melody.add_clef("treble")
notes = ["R 4", "E 5 16", "D# 5 16", "E 5 16", "D# 5 16", "E 5 16", "B 4 16", "D 5 16", "C 5 16"]
notes += ["A 4 8", "R 16", "C 4 16", "E 4 16", "A 4 16"]
notes += ["B 4 8", "R 16", "E 4 16", "G# 4 16", "B 4 16"]
notes += ["C 5 8", "R 16", "E 4 16", "E 5 16", "D# 5 16", "E 5 16", "D# 5 16", "E 5 16", "B 4 16", "D 5 16", "C 5 16"]
notes += ["A 4 8", "R 16", "C 4 16", "E 4 16", "A 4 16", "B 4 8", "R 16", "E 4 16", "C 5 16", "B 4 16", "A 4 8"]

notes2 = ["R 16", "B 4 16", "C 5 16", "D 5 16"] # 1st repeat here
notes2 += ["E 5 8.", "G 4 16", "F 5 16", "E 5 16"] 
notes2 += ["D 5 8.", "F 4 16", "E 5 16", "D 5 16"] 
notes2 += ["C 5 8.", "E 4 16", "D 5 16", "C 5 16"] 
notes2 += ["B 4 8", "R 16", "E 4 16", "E 5 16", "R 16"]
notes2 += ["R 16", "E 5 16", "E 6 16", "R 16", "R 16", "D# 5 16"]
notes2 += ["E 5 8", "R 16", "D# 4 16", "E 5 16", "D# 5 16", "E 5 16", "D# 5 16", "E 5 16", "B 4 16", "D 5 16", "C 5 16"]

noteend = ["R 4"]

melody.add_notes(notes)
melody.add_notes(notes2)
melody.add_notes(notes)
melody.add_notes(noteend)

bass = Staff()
score.add_staff(bass)
bass.add_signature("3/8")
bass.add_key("C major")
bass.add_clef("bass")
notes = ["R 8", "R 8", "R 8", "R 8", "R 8", "R 8"]
notes += ["A 2 16", "E 3 16", "A 3 16", "R 16", "R 8"]
notes += ["E 2 16", "E 3 16", "G# 3 16", "R 16", "R 8"]
notes += ["A 2 16", "E 3 16", "A 3 16", "R 16", "R 8"]
notes += ["R 8", "R 8", "R 8"]
notes += ["A 2 16", "E 3 16", "A 3 16", "R 16", "R 8"]
notes += ["E 2 16", "E 3 16", "G# 3 16", "R 16", "R 8"]
notes += ["A 2 16", "E 3 16", "A 3 16", "R 16", "R 8"]
notes += ["C 3 16", "G 3 16", "C 4 16", "R 16", "R 8"]
notes += ["G 2 16", "G 3 16", "B 3 16", "R 16", "R 8"]
notes += ["A 2 16", "E 3 16", "A 3 16", "R 16", "R 8"]
notes += ["A 2 16", "E 3 16", "E 4 16", "R 16", "R 16", "E 4 16"]
bass.add_notes(notes)
bass.add_clef("treble")
notes = ["E 5 16", "R 16", "R 16", "D# 5 16", "E 5 16", "R 16"]
notes += ["R 16", "D# 5 16", "E 5 16", "R 16", "R 8", "R 1"]
bass.add_notes(notes)
bass.add_clef("bass")
notes = ["A 2 16", "E 3 16", "A 3 16", "R 16", "R 8"]
notes += ["E 2 16", "E 3 16", "G# 3 16", "R 16", "R 8"]
notes += ["A 2 16", "E 3 16", "A 3 16", "R 16", "R 8", "R 1"]
notes += ["A 2 16", "E 3 16", "A 3 16", "R 16", "R 8"]
notes += ["E 2 16", "E 3 16", "G# 3 16", "R 16", "R 8"]
notes += ["A 2 16", "E 3 16", "A 3 16", "R 16", "R 8", "R1"]
notes += ["A 2 16", "E 3 16", "A 3 16", "R 16", "R 8"]
notes += ["E 2 16", "E 3 16", "G# 3 16", "R 16", "R 8"]
notes += ["A 2 16", "E 3 16", "A 3 16", "R 16", "R 8"]
bass.add_notes(notes)

# score.change_instrumentation(["piano", "cello"])

#score.add_intervals_harmony(melody, "violin")
#score.add_intervals_harmony(melody, "cello")
score.add_intervals_harmony(melody, intervals =[5])
#score.add_intervals_harmony(melody, "violin")
score.generate_lilypond("fur_elise.ly", 60)
