from main import *
# happy birthday
score = Score()
melody = Staff()
score.add_staff(melody)
melody.add_signature("4/4")
melody.add_key("c major")
melody.add_clef("treble")
melody.add_notes(["R 2", "R 4", "G 4 8 1 f", "G 4 8"])
melody.add_signature("3/4")
notes = ["A 4 4 2", "G 4 4", "C 5 4 4", "B 4 2"]
notes += ["G 4 8", "G 4 8 ", "A 4 4", "G 4 4", "D 5 4 5", "C 5 2"]
notes += ["G 4 8", "G 4 8", "G 5 4 5", "E 5 4 3", "C 5 4 1", "B 4 4 2", "A 4 4 fermata"]
notes += ["F 5 8 5", "F 5 8", "E 5 4", "C 5 4", "D 5 4", "C 5 2", "R 4"]
melody.add_notes(notes)

bass = Staff()
score.add_staff(bass)
bass.add_signature("4/4")
bass.add_key("c major")
bass.add_clef("bass")
bass.add_notes(["R 1"])
bass.add_signature("3/4")
notes = ["C 3 4", ["E 3", "G 3", "4"], ["E 3", "G 3", "4"], "G 2 4", ["D 3", "F 3", "4"], ["D 3", "F 3", "4"]]
notes += ["G 2 4", ["D 3", "F 3", "4"], ["D 3", "F 3", "4"], "C 3 4", ["E 3", "G 3", "4"], ["E 3", "G 3", "4"], "C 3 4", ["E 3", "G 3", "4"], ["E 3", "G 3", "4"]]
notes += ["F 3 4", ["A 3", "C 4", "4"], ["A 3", "C 4", "4"], "C 3 4", ["E 3", "G 3", "4"], ["F 3", "G 3", "4"], ["C 3", "E 3", "G 3", "4"], "C 2 4", "R 4"]
bass.add_notes(notes)

score.add_lyrics("Hap -- py birth -- day to you! Hap -- py birth -- day to you! Hap -- py birth -- day dear Soph -- ia, Hap -- py birth -- day to you!")
score.generate_lilypond("birthday.ly")


