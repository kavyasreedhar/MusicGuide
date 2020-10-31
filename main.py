class Note():
  def __init__(self,
              value,
              length,
              is_rest=False,
              octave=None,
              accidental=None):
  	
    self.value = value
    self.octave = octave
    self.length = length
    self.accidential = accidental
    
  def print():
    out = ""
    out += self.value
    if self.accidental == "#":
      out += "is"
    elif self.accidential == "b":
    	out += "es"
    # pitch 
    if self.octave > 4:
      for i in range(self.octave - 4):
        out += "'"  
    elif self.octave < 4:
      for i in range(4 - self.octave):
      	out += ","  
    
    out += self.length
    return out
    
class Score():
  def __init__(self):
    self.notes = []
    
  def add_notes(notes):
  	for note in notes:
      note_parts = note.split(".")
      note_val, note_len = note_parts[0], note_parts[-1]
      is_rest = (note_val == "R")
      if not is_rest:
        note_octave = int(note_parts[1])
      else:
        note_octave =  None
      if len(note_val) > 1:
        accidental=note_val[1]
      else:
        accidental = None
      self.notes.append(Note(value=note_val[0].lower(),
                             length=note_len,
                             is_rest=is_rest,
                             octave=note_octave,
                             accidential=accidental))
    
  def generate_lilypond(filename):
    with open(filename, "w+") as output:
      output.write("\relative c' {\n")
      
      for note in self.notes:
        output.write(note.print())
        output.write(" ")
      output.write("}\n")
    
s = Score()
score.add_notes(["C#.4.16", "Eb.4.2", "G.4.4", "E.4.8", "R.4"])
score.generate_lilypond("t.txt")
