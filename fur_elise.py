# fur elise

from main import *
# happy birthday
score = Score()
melody = Staff()
score.add_staff(melody)
melody.add_signature("3/8")
melody.add_key("c major")
melody.add_clef("treble")
notes = ["R 4", "E 5 16", "D# 5 16", "E 5 16", "D# 5 16", "E 5 16", "B 4 16", "D 5 16", "C 5 16"]
notes += ["A 4 8", "R 16", "C 4 16", "E 4 16", "A 4 16"]
notes += ["B 4 8", "R 16", "E 4 16", "G# 4 16", "B 4 16"]
notes += ["C 5 8", "R 16", "E 4 16", "E 5 16", "D# 5 16", "E 5 16", "D# 5 16", "E 5 16", "B 4 16", "D 5 16", "C 5 16"]
notes += ["A 4 8", "R 16", "C 4 16", "E 4 16", "A 4 16", "B 4 8", "R 16", "E 4 16", "C 5 16", "B 4 16", "A 4 8", "R 16", "B 4 16", "C 5 16", "D 5 16"]
melody.add_notes(notes)

bass = Staff()
score.add_staff(bass)
bass.add_signature("3/8")
bass.add_key("c major")
bass.add_clef("bass")
notes = ["R 8", "R 8", "R 8", "R 8", "R 8", "R 8"]
notes += ["A 2 16", "E 3 16", "A 3 16", "R 16", "R 8"]
notes += ["E 2 16", "E 3 16", "G# 3 16", "R 16", "R 8"]
notes += ["A 2 16", "E 3 16", "A 3 16", "R 16", "R 8"]
notes += ["R 8", "R 8", "R 8"]
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

