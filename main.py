  
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
               bot=4, 
               bar=0):
    # default time signature
    self.top = top
    self.bot = bot
    self.bar = bar
    
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
               key_m="major",
               bar=0):

    # default key note
    self.key_note = key_note
    self.key_m = key_m
    self.bar = bar
    
  def print(self):
    out = "\\key " + self.key_note.print() + " \\" + self.key_m + "\n"
    return out 

class Clef():
  def __init__(self, clef="treble", bar=0):
    self.clef = clef
    self.bar = bar

  def print(self):
    out = "\\clef " + self.clef + "\n"
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
    self.sigs = []
    self.keys = []
    self.clefs = []
    self.lyrics = ""
    self.bar = 0
  
  def add_signature(self, sig): # sig 4/3
    sig_parts = sig.replace(" ", "").split("/")
    sig_top = int(sig_parts[0])
    sig_bot = int(sig_parts[1])

    self.sigs.append(Signature(sig_top, sig_bot, self.bar))
    
  def add_key(self, key): # todo: changing key and sig 
    key_parts = key.split(".")
    if (len(key_parts[0]) > 1):
        accidental = key_parts[0][1]
    else:
        accidental = None

    key_note = Note(value = key_parts[0][0].lower(), 
                         length = "",
                         is_rest = False,
                         octave = 4,
                         accidental = accidental)
    key_m = key_parts[1]
    self.keys.append(Key(key_note, key_m, self.bar))

  def add_clef(self, clef): 
    self.clefs.append(Clef(clef, self.bar))
                         
  def add_lyrics(self, lyrics):
    self.lyrics = Lyric(lyrics)
    
  def add_notes(self, notes):
    bar_count = 0
    bar_total = (self.sigs[-1].top)/(self.sigs[-1].bot)
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
      bar_count += 1/int(note_len)
      if (bar_count  >= bar_total):
          bar_count = 0
          self.bar += 1
 
  # helper function
  def print_next_symbol(self, symbols, bar):
    if (len(symbols) > 1 and symbols[1].bar == bar):
      symbols.pop(0)
      return symbols[0].print()
    return ""
     
  def generate_lilypond(self, filename="lilypond.ly"):
    with open(filename, "w+") as output:
      output.write("\\relative c' {\n")
      output.write(self.sigs[0].print()) # must specify initial signature, key, clef
      output.write(self.keys[0].print())
      output.write(self.clefs[0].print())
      print(self.sigs[1].bar)
      print(self.sigs[0].bar)
      print(self.clefs[1].bar)
      m_count = 0
      bar_num = 0
      curr_notes, curr_index = [], []
      i = 0
      for note in self.notes:
        curr_notes.append(note.value)
        curr_index.append(i)
        m_count += 1 / int(note.length)
        # end measure
        m_total = self.sigs[0].top / self.sigs[0].bot
        curr, index = "", ""
        if m_count >= m_total:
          print(m_count)
          for curr_note in curr_notes:
              curr += " " + curr_note
          for j in curr_index:
              index += " " + str(j)

          curr, index = curr[1:], index[1:]
          assert_print = "Notes in this measure ("+curr+") corresponding to these indices ("+index+") do not match time signature."
          assert m_count == m_total, assert_print
          m_count = 0 
          bar_num += 1
          output.write(self.print_next_symbol(self.sigs, bar_num))
          output.write(self.print_next_symbol(self.keys, bar_num))
          output.write(self.print_next_symbol(self.clefs, bar_num))
          curr_notes = []
          curr_index = []
        output.write(note.print())
        output.write(" ")
        i += 1
      # add ending bar line
      ending_bar = "|."
      output.write("\\bar" + '"%s"' % ending_bar)
      output.write("}\n")
      
      output.write(self.lyrics.print())

   

score = Score()
score.add_signature("3/4")
score.add_key("Eb.major")
score.add_clef("treble")
score.add_notes(["Eb.4.2", "G.4.4", "E.4.8", "C#.4.8", "R.4", "d.7.4", "f.-1.2", "R.4"])
score.add_signature("4/8")
score.add_key("c.minor")
score.add_clef("alto")
score.add_notes(["Eb.4.2", "G.4.4", "E.4.8", "C#.4.8", "R.2", "d.7.4", "f#.5.4"])
score.add_lyrics("This is a test song")
score.generate_lilypond("ltest.ly")
