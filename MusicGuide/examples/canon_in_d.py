from MusicGuide.src.main import *

score = Score()
melody = Staff()
score.add_staff(melody)
melody.add_signature("4/4")
melody.add_key("d major")
melody.add_clef("treble")
notes = ["R 1", "R 1", "R 1", "R 1"]
notes += ["f# 5 2", "e 5 2", "d 5 2", "c# 5 2", "b 4 2", "a 4 2", "b 4 2", "c# 4 2"]
melody.add_notes(notes)

bass = Staff()
score.add_staff(bass)
bass.add_signature("4/4")
bass.add_key("d major")
bass.add_clef("bass")
notes = ["d 3 8", "a 3 8", "d 4 8", "f 4 8", "a 2 8", "e 3 8", "a 3 8", "c 4 8"]
notes += ["b 2 8", "f 3 8", "b 3 8", "d 4 8", "f 2 8", "c 3 8", "f 3 8", "a 3 8"]
#score.change_instrumentation(["violin", "violin"])

#score.add_intervals_harmony(melody, "violin")
# score.add_intervals_harmony(melody, "cello")
#score.add_intervals_harmony(melody, "viola")
# score.add_intervals_harmony(melody, "violin")
# score.add_chord_harmony(melody)
score.add_header("Canon in D", "Johann Pachelbel")
score.generate_lilypond("canon_in_d.ly")
