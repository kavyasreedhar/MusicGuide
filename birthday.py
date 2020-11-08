from main import *

# happy birthday
score = Score()
score.add_signature("4/4")
score.add_key("c.major")
score.add_clef("treble")
score.add_notes(["R.2", "R.4", "G.4.8", "G.4.8"])
score.add_lyrics("Hap -- py")
score.add_signature("3/4")
notes = ["A.4.4", "G.4.4", "C.5.4", "B.4.2"]
notes += ["G.4.8", "G.4.8", "A.4.4", "G.4.4", "D.5.4", "C.5.2"]
notes += ["G.4.8", "G.4.8", "G.5.4", "E.5.4", "C.5.4", "B.4.4", "A.4.4"]
notes += ["F.5.8", "F.5.8", "E.5.4", "C.5.4", "D.5.4", "C.5.2", "R.4"]
score.add_notes(notes)
score.add_lyrics("birth -- day to you! Hap -- py birth -- day to you! Hap -- py birth -- day dear Soph -- ia, Hap -- py birth -- day to you!")
score.generate_lilypond("birthday.ly")


