class Note():
    def __init__(self,
              value,
              length,
              fingering=None,
              articulations=[],
              is_rest=False,
              octave=None,
              accidental=None):
        self.value = value
        self.length = length
        self.fingering = fingering
        self.articulations = articulations
        self.is_rest = is_rest
        self.octave = octave
        self.accidental = accidental
    
    def print(self, use_len=True):
        out = ""
        out += self.value
        if self.accidental == "#":
            out += "is"
        elif self.accidental == "b":
            out += "es"
        # pitch 
        if not self.is_rest:
            if self.octave > 3:
                for i in range(self.octave - 3):
                    out += "'"  
            elif self.octave < 3:
                for i in range(3 - self.octave):
                    out += ","  
    
        if use_len:
            out += self.length
    
        if self.fingering is not None:
            out += "^" + str(self.fingering)
            
        for art in self.articulations:
            out += "\\" + art
            
        return out

class Chord():
    def __init__(self,
               notes,
               length):

        self.notes = notes
        self.length = length
        self.value = self.get_value()

    def get_value(self):
        val = ""
        for note in self.notes:
            val += note.value + " "

        return val

    def print(self):
        out = "<"
        for note in self.notes:
            out += " " + note.print(False)
        out += " >" + str(self.length)
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

###########################################

class Score():
    def __init__(self):
        self.staves = []
        self.lyrics = ""
    
    def add_lyrics(self, lyrics):
        self.lyrics = Lyric(lyrics)

    def add_staff(self, staff):
        self.staves.append(staff)
    
    def generate_lilypond(self, filename="lilypond.ly"):
        with open(filename, "w+") as output:
            if len(self.staves) > 1:
                output.write("<<\n")
        for staff in self.staves:
            staff.print(filename = filename)
        with open(filename, "a+") as output:
            output.write(self.lyrics.print())
        with open(filename, "a+") as output:
            if len(self.staves) > 1:
                output.write("\n>>\n")

############################################
class Staff():
    def __init__(self):
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
        key_parts = key.split(" ")
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
    
    def add_notes(self, notes):
        bar_count = 0
        bar_total = (self.sigs[-1].top)/(self.sigs[-1].bot)
        for note in notes:
            # check if chord
            if type(note) == list:
                chord_len = int(note[-1].split(" ")[0])
                note_len = chord_len
                chord_notes = []
                for i in range(len(note) - 1):
                    item = note[i]
                    chord_notes.append(self.extract_note(item, chord_len))
                self.notes.append(Chord(chord_notes, chord_len))
            else:
                ret_note, note_len = self.extract_note(note)
                self.notes.append(ret_note)

            bar_count += 1/int(note_len)
            if (bar_count  >= bar_total):
                bar_count = 0
                self.bar += 1

    def extract_note(self, note, note_len=None):
        note_parts = note.split(" ")
        note_val = note_parts[0]
        ret_note_len = False    # chord
        

        is_rest = (note_val == "R")    # if note is rest
        if not is_rest:
            note_octave = int(note_parts[1])
            if note_len is None:    # not chord
                ret_note_len = True
                note_len = note_parts[2]
        else:
            note_octave = None
            if note_len is None:    # not chord
                ret_note_len = True
                note_len = note_parts[1]
        
        if len(note_val) > 1:        # check for accidental
            accidental=note_val[1]
        else:
            accidental = None
        
        if ret_note_len:
            fingart_index = 3 # not chord
        else:
            fingart_index = 2 # is chord
            
        if len(note_parts) > fingart_index: 
            # fingering
            try:
                fingering = int(note_parts[fingart_index])
                art_start_index = fingart_index + 1
            # articulation
            except:
                art_start_index = fingart_index
                
        else: 
            art_start_index = len(note_parts)
            fingering = None

        note = Note(value=note_val[0].lower(),
                             length=note_len,
                             fingering = fingering,
                             articulations = note_parts[art_start_index:],
                             is_rest=is_rest,
                             octave=note_octave,
                             accidental=accidental)

        if ret_note_len:
            return note, note_len
        else:
            return note
    
    # helper function
    def print_next_symbol(self, symbols, bar):
        if (len(symbols) > 1 and symbols[1].bar == bar):
            symbols.pop(0)
            return symbols[0].print()
        return ""
     
    def print(self, filename="lilypond.ly"):
        with open(filename, "a+") as output:
            output.write("\\new Staff {\n")
            output.write("\\absolute {\n")
            output.write(self.sigs[0].print()) # must specify initial signature, key, clef
            output.write(self.keys[0].print())
            output.write(self.clefs[0].print())
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
                output.write(note.print())
                output.write(" ")
                if m_count >= m_total:
                    # print(m_count)
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
                i += 1
            # add ending bar line
            ending_bar = "|."
            output.write("\\bar" + '"%s"' % ending_bar)
            output.write("}\n}\n") #Staff, absolute

        
score = Score()
melody = Staff()
score.add_staff(melody)
melody.add_signature("3/4")
melody.add_key("Eb major")
melody.add_clef("treble")
melody.add_notes(["Eb 4 2 4 upbow ff staccato", ["G 4", "a 1", "4 fermata downbow"], "E 4 8", "C# 4 8", "R 4", "d 7 4", ["f -1", "a 2", "2"], "R 4"])
melody.add_signature("4/8")
melody.add_key("c minor")
melody.add_clef("alto")
melody.add_notes(["Eb 4 2", "G 4 4", "E 4 8", "C# 4 8", "R 2", "d 7 4", "f# 5 4"])
score.add_lyrics("This is a test song")
score.generate_lilypond("ltest.ly")
