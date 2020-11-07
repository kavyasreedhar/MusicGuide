class Note():
  def __init__(self,
              value,
              length,
              is_rest=False,
              octave=None,
              accidental=None):
  	
    self.value = value
    self.length = length
    self.is_rest = is_rest
    self.octave = octave
    self.accidental = accidental
    
  def print(self):
    out = ""
    out += self.value
    if self.accidental == "#":
      out += "is"
    elif self.accidental == "b":
    	out += "es"
    # pitch 
    if not self.is_rest:
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
    self.signature_top = 4
    self.signature_bot = 4
    
    
  def add_notes(self, notes):
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
                             accidental=accidental))
    
  def generate_lilypond(self, filename="lilypond.ly"):
    with open(filename, "w+") as output:
      output.write("\\relative c' {\n")
      
      m_count = 0
      for note in self.notes:
        m_count += 1 / int(note.length)
        # end measure
        if m_count > self.signature_top / 4:
          output.write(" | \n")
          m_count = 1 / int(note.length)
        output.write(note.print())
        output.write(" ")

      # add ending bar line
      ending_bar = "|."
      output.write("\\bar" + '"%s"' % ending_bar)
      output.write("}\n")
    
score = Score()
score.add_notes(["C#.4.8", "Eb.4.2", "G.4.4", "E.4.8", "R.4"])
score.generate_lilypond("ltest.ly")
