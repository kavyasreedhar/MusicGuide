  
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
    
class Signature():
  def __init__(self,
               top=4,
               bot=4):
    # default time signature
    self.top = top
    self.bot = bot
    
  def print(self):
    out = "\\time " + str(self.top) + "/" + str(self.bot) + "\n"
    return out
    
class Key():
  def __init__(self, 
               key_note=Note(value="c",
                             length="",
                             is_rest=False,
                             octave=4,
                             accidental=""),
               key_m="major"):

    # default key note
    self.key_note = key_note
    self.key_m = key_m
    
  def print(self):
    out = "\\key " + self.key_note.print() + " \\" + self.key_m + "\n"
    return out 

class Lyric():
  def __init__(self,
               lyrics=None):
    
    self.lyrics = lyrics
    
  def print(self):
    if self.lyrics is not None:
      out = "\\addlyrics {\n"
      out += self.lyrics
      out += "}"
      return out
    else:
      return ""
    
class Score():
  def __init__(self,
               S=Signature()):
    self.notes = []
    self.sig = Signature()
    self.key = Key()
    self.lyrics = ""
  
  def add_signature(self, sig): # sig 4/3
    sig_parts = sig.replace(" ", "").split("/")
    sig_top = int(sig_parts[0])
    sig_bot = int(sig_parts[1])

    self.sig = Signature(sig_top, sig_bot)
    
  def add_key(self, key): # todo: changing key and sig 
    key_parts = key.split(".")
    key_note = Note(value = key_parts[0][0].lower(), 
                         length = "",
                         is_rest = False,
                         octave = 4,
                         accidental = key_parts[0][1])
    key_m = key_parts[1]
    self.key = Key(key_note, key_m)
                         
  def add_lyrics(self, lyrics):
    self.lyrics = Lyric(lyrics)
    
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
      output.write(self.sig.print())
      output.write(self.key.print())     
      m_count = 0
      for note in self.notes:
        m_count += 1 / int(note.length)
        # end measure
        if m_count > self.sig.top / 4:
          output.write(" | \n")
          m_count = 1 / int(note.length)
        output.write(note.print())
        output.write(" ")

      # add ending bar line
      ending_bar = "|."
      output.write("\\bar" + '"%s"' % ending_bar)
      output.write("}\n")
      
      output.write(self.lyrics.print())
    
      
score = Score()
score.add_signature("3/4")
score.add_key("Eb.major")
score.add_notes(["C#.4.8", "Eb.4.2", "G.4.4", "E.4.8", "R.4", "d.7.2"])
score.add_lyrics("This is a test song")
score.generate_lilypond("ltest.ly")
