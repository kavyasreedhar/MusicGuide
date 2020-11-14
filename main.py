import sys

Instruments = {
    "piano RHS": ["treble", "A 0", "C 8"],
    "piano LHS": ["bass", "A 0", "C 8"],
    "viola": ["alto", "C 3","E 6"],
    "violin": ["treble", "G 3", "A 7"],
    "cello": ["bass", "C 2", "C 6"],
    "double bass": ["bass", "C 2", "C 5"]
}    
    
#    "oboe": "treble",
#    "flute": "treble",
#    "clarinet": "treble",
#    "alto sax": "treble",
#    "tenor sax": "treble",
#    "baritone sax": "treble",
#    "french horn": "treble",
#    "trombone": "bass",
#    "bassoon" "bass",
#    "guitar": "treble",
#    "timpani": "bass",
#    "drums": "percussion",
#    "trumpet": "treble",
#    "tuba": "bass"
#}

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
               length,
               fingering=None,
               articulations=[]):

        self.notes = notes
        self.length = length
        self.value = self.get_value()
        self.fingering = fingering
        self.articulations = articulations

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
        
        if self.fingering is not None:
            out += "^" + str(self.fingering)
            
        for art in self.articulations:
            out += "\\" + art
            
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
NoteVal = {"c": 0, "d": 1, "e": 2, "f": 3, "g": 4, "a": 5, "b": 6}

def check_legal_note(note, min_octave, max_octave, min_note, max_note, staff, min_, max_):
    legal = True
    # check if note is in range of instrument
    if note.octave < min_octave:
        legal = False
    elif note.octave == min_octave and NoteVal[note.value.lower()] < NoteVal[min_note.lower()]:
        legal = False

    if note.octave > max_octave:
        legal = False
    elif note.octave == max_octave and NoteVal[note.value.lower()] > NoteVal[max_note.lower()]:
        legal = False

    if not legal:
        print("Note " + note.value + " in octave " + str(note.octave) +  " is not within range of instrument " + staff.instrument)

        sys.exit()
        
        
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
                
    def change_instrumentation(self, instruments):
        for i in range(len(self.staves)):
            staff = self.staves[i]
            staff.instrument = instruments[i]
            staff.clefs = [Clef(clef = Instruments[staff.instrument][0])]
            # get min and max note and octave range for instrument
            min_ = Instruments[staff.instrument][1].split(" ")
            min_note, min_octave = min_[0], int(min_[1])
            
            max_ = Instruments[staff.instrument][2].split(" ")
            max_note, max_octave = max_[0], int(max_[1])
            
            for note in staff.notes:
                if type(note) is Note and not note.is_rest:
                    check_legal_note(note, min_octave, max_octave, min_note, max_note, staff, min_, max_)
                elif type(note) is Chord:
                    for chord_note in note.notes:
                        check_legal_note(chord_note, min_octave, max_octave, min_note, max_note, staff, min_, max_)
                    
            
############################################

def get_fing_art(fingart_index, note_parts):
            
    fingering = None
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
        
    return fingering, note_parts[art_start_index:]

        
class Staff():
    def __init__(self):
        self.notes = []
        self.sigs = []
        self.keys = []
        self.clefs = []
        self.instrument = None
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
                misc = note[-1].split(" ")
                chord_len = int(misc[0])
                
                fingering, articulation = get_fing_art(1, misc)
                
                note_len = chord_len
                chord_notes = []
                for i in range(len(note) - 1):
                    item = note[i]
                    chord_notes.append(self.extract_note(item, chord_len))
                
                self.notes.append(Chord(chord_notes, chord_len, fingering, articulation))
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
        
        fingering, articulations = get_fing_art(3, note_parts)

        note = Note(value=note_val[0].lower(),
                             length=note_len,
                             fingering = fingering,
                             articulations = articulations,
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
            if self.instrument is not None:
                output.write('\\with {\n instrumentName = #"' + self.instrument + '"\n }')
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

