import sys
import copy 
import random as rand

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
              num_dots=0,
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
        self.num_dots = num_dots
    
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
            
        for i in range(self.num_dots):
            out += "."
            
        if self.fingering is not None:
            out += "^" + str(self.fingering)
            
        for art in self.articulations:
            out += "\\" + art
            
        return out

class Chord():
    def __init__(self,
               notes,
               length,
               num_dots=0,
               fingering=None,
               articulations=[]):

        self.notes = notes
        self.length = length
        self.value = self.get_value()
        self.fingering = fingering
        self.articulations = articulations
        self.num_dots = num_dots

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
        
        for i in range(self.num_dots):
            out += "."
        
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
    orig_octave = note.octave
    # check if note is in range of instrument
    if note.octave < min_octave:
        legal = False
        note.octave = min_octave + 1
    elif note.octave == min_octave and NoteVal[note.value.lower()] < NoteVal[min_note.lower()]:
        legal = False
        note.octave += 1

    if note.octave > max_octave:
        legal = False
        note.octave = max_octave - 1
    elif note.octave == max_octave and NoteVal[note.value.lower()] > NoteVal[max_note.lower()]:
        legal = False
        note.octave -= 1

    #if not legal:
    #    print("Note " + note.value + " in octave " + str(orig_octave) +  " is not within range of instrument " + staff.instrument + "...not expected? Note moved to octave" + str(note.octave))
        
        
class Score():
    def __init__(self):
        self.staves = []
        self.lyrics = ""
        self.title = ""
        self.composer = ""
        note_vals = ["a", "b", "c", "d", "e", "f", "g"]
        note_keys = []
        for i in note_vals:
            note_keys.append(i)
            note_keys.append(i+"#")
            note_keys.append(i+"b")
            
        note_keys.append("r")
        
        inter = {}
        for key in note_keys:
            inter[key] = 0
            
        self.transition_matrix = {}
        for key in note_keys:
            self.transition_matrix[key] = copy.deepcopy(inter)
        
    def add_lyrics(self, lyrics):
        self.lyrics = Lyric(lyrics)

    def add_staff(self, staff):
        self.staves.append(staff)
    
    def add_header(self, title="", composer=""):
        self.title = title
        self.composer = composer
    
    def create_transition_matrix(self):
        for staff in self.staves:
            for i in range(len(staff.notes) - 1):
                note, next_note = staff.notes[i], staff.notes[i + 1]
                if type(note) == Chord:
                    note_comp = note.notes[0]
                else:
                    note_comp = note
                    
                if type(next_note) == Chord:
                    next_note_comp = next_note.notes[0]
                else:
                    next_note_comp = next_note
            
                real_note = note_comp.value
                if note_comp.accidental is not None:
                    real_note += note_comp.accidental
                
                next_real_note = next_note_comp.value
                if next_note_comp.accidental is not None:
                    next_real_note += next_note_comp.accidental
            
                self.transition_matrix[real_note][next_real_note] += 1
                # print(real_note, " ", next_real_note)
            
        
        for note in self.transition_matrix.keys():
            total = 0
            for next_note in self.transition_matrix[note].keys():
                
                total += self.transition_matrix[note][next_note]
                
            for next_note in self.transition_matrix[note].keys():
                if (total != 0):
                    # print(total)
                    self.transition_matrix[note][next_note] /= total
        # print(self.transition_matrix)
        
        
    def transition_get_next_note(self, note, melody_note):
        if melody_note.is_rest:
            return melody_note

        num = rand.random()
        real_note = note.value
        if note.accidental is not None:
            real_note += note.accidental
            
        probs = self.transition_matrix[real_note]
        
        prob_sum = 0
        for prob in probs.keys():
            p = probs[prob]
            prob_sum += p
            if prob_sum >= num:
                next_note = prob
                if next_note == "r":
                    return melody_note
                note.value = next_note[0]
                if len(next_note) > 1:
                    note.accidental = next_note[1]
                else:
                    note.accidental = None
                return note
                
        return melody_note
            
            
    def transition_harmony(self, melody_staff, instrument):
        self.create_transition_matrix()
        
        if type(melody_staff.notes[0]) is Chord:
            start_note = melody_staff.notes[0].notes[0]
        else:
            start_note = melody_staff.notes[0]
            
        new_staff = copy.deepcopy(melody_staff)
        new_staff.notes[0] = start_note
        
        for i in range(1, len(melody_staff.notes)):
            note = new_staff.notes[i]
            if not note.is_rest:
                new_staff.notes[i] = self.transition_get_next_note(note, melody_staff.notes[i])
                
        self.add_basic_harmony(new_staff, new_staff.notes)
        
        
    def generate_lilypond(self, filename = "lilypond.ly", tempo = 120, tempo_note = 4):
        with open(filename, "w+") as output:
            output.write('\\header { \n title = "' + self.title + '"\n' 
                         + 'composer = "' + self.composer + '"\n }\n')
            
            output.write("\\score { \n")
            if len(self.staves) > 1:
                output.write("<<\n")
        for staff in self.staves:
            staff.print(filename = filename)
        with open(filename, "a+") as output:
            if self.lyrics != "":
                output.write(self.lyrics.print())
        with open(filename, "a+") as output:
            if len(self.staves) > 1:
                output.write("\n>>\n")
            output.write("\\layout{} \n") # print out sheet music
            output.write("\\midi{ \n") #  output midi 
            output.write("\\tempo " + str(tempo_note) + " = " + str(tempo) + " \n")
            output.write("}}") # end midi and score   

    # change all staves to a list of instruments
    def change_instrumentation(self, instruments):
        for i in range(len(self.staves)):
            staff = self.staves[i]
            self.change_one_instrument(instruments[i], staff)
                        
    # change one staff to a different instrument
    def change_one_instrument(self, instrument, staff):
        staff.instrument = instrument
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
        
    # return (notes + interval) one octave lower
    # helper function
    def create_harmony_notes(self, staff, interval):
        intnotes = []
        for note in staff.notes:
            if type(note) is Note:
                if not note.is_rest:
                    inote = self.harmony_note(interval, note)
                    intnotes.append(inote)
                else:
                    intnotes.append(note)
                    
            elif type(note) is Chord:
                chord_notes = []
                for chord_note in note.notes:
                    chord_notes.append(self.harmony_note(interval, chord_note))
                
                third_chord = Chord(chord_notes,
                                    note.length,
                                    note.num_dots,
                                    note.fingering,
                                    note.articulation)
                intnotes.append(third_chord)
                
            else:
                print("Unexcepted note type...exiting")
                sys.exit()
                
        return intnotes
        
    # add harmony object to staff
    # helper function
    def add_basic_harmony(self, staff, notes):
        harmony = copy.deepcopy(staff)
        self.add_staff(harmony)
        harmony.notes = notes
        return harmony
        
    # add random harmony from given interval list
    def add_intervals_harmony(self, staff, instrument=None, intervals=[3, 4, 6]):
        
        intnotes = []
        for interval in intervals:
            intnotes.append(self.create_harmony_notes(staff, interval))
            
        new_notes = []
        for i in range(len(staff.notes)):
            randinterval = rand.randrange(len(intervals))
            new_note = intnotes[randinterval][i]
            new_notes.append(new_note)
        
        harmony = self.add_basic_harmony(staff, new_notes)
        
        if instrument is not None:
            self.change_one_instrument(instrument, harmony)
        
                
    def harmony_note(self, interval, note):
        abs_val = NoteVal[note.value] + interval # move up by interval
        if abs_val > 6: # check if moved to higher octave
            octave = note.octave
        else:
            octave = note.octave - 1 # and move down an octave

        value = abs_val % 7
        
        return Note(value = list(NoteVal.keys())[value],
                    length = note.length,
                    is_rest = note.is_rest,
                    num_dots = note.num_dots,
                    articulations = note.articulations,
                    octave = octave,
                    accidental = note.accidental)
    
    def add_chord_harmony(self, staff, instrument=None):
        bar_count = 0
        bar_num = 0
        bar_total = (staff.sigs[-1].top)/(staff.sigs[-1].bot)
        new_notes = []
        
        for note in staff.notes:
            
            if bar_count == 0:
                if not note.is_rest:
                    chord_start_note = note
                    chord_start_note.octave -= 1

                    chord_second_note = copy.deepcopy(chord_start_note)
                    chord_second_note.value = list(NoteVal.keys())[(NoteVal[note.value] + 3) % 7]

                    chord_third_note = copy.deepcopy(chord_start_note)
                    chord_third_note.value = list(NoteVal.keys())[(NoteVal[note.value] + 5) % 7]

                    chord = Chord([chord_start_note, chord_second_note, chord_third_note],
                        length = str(1/bar_total),
                        num_dots=0,
                        fingering=None,
                        articulations=[])

                    new_notes.append(chord)
                else:
                    new_notes.append(note)
            
                note_len = note.length
                one_div_note_len = 1/int(note_len)
                for i in range(staff.notes[-1].num_dots):
                    one_div_note_len += 1/(2**(i+1) * int(note_len))

                bar_count += one_div_note_len
                if (bar_count  >= bar_total):
                    bar_count = 0
                    bar_num += 1
                    
        self.add_basic_harmony(staff, new_notes)

        
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
                
                chord_len, chord_num_dots = self.get_dots(misc[0])
                
                fingering, articulation = get_fing_art(1, misc)
                
                note_len = chord_len
                chord_notes = []
                for i in range(len(note) - 1):
                    item = note[i]
                    chord_notes.append(self.extract_note(item, chord_len, chord_num_dots))
                
                self.notes.append(Chord(chord_notes, chord_len, chord_num_dots, fingering, articulation))
            else:
                ret_note, note_len = self.extract_note(note)
                self.notes.append(ret_note)
            
            one_div_note_len = 1/int(note_len)
            for i in range(self.notes[-1].num_dots):
                one_div_note_len += 1/(2**(i+1) * int(note_len))
                
            bar_count += one_div_note_len
            if (bar_count  >= bar_total):
                bar_count = 0
                self.bar += 1

    def get_dots(self, input_list):
        dot_start_index = input_list.find(".")
        if dot_start_index == -1:
            length = input_list
            num_dots = 0
        else:
            length = input_list[0:dot_start_index]
            num_dots = len(input_list) - dot_start_index
        
        return length, num_dots
                
    def extract_note(self, note, note_len=None, note_num_dots=None):
        note_parts = note.split(" ")
        note_val = note_parts[0]
        ret_note_len = False    # chord
        

        is_rest = (note_val == "R")    # if note is rest
        if not is_rest:
            note_octave = int(note_parts[1])
            if note_len is None:    # not chord
                ret_note_len = True
                note_len, note_num_dots = self.get_dots(note_parts[2])
        else:
            note_octave = None
            if note_len is None:    # not chord
                ret_note_len = True
                note_len, note_num_dots = self.get_dots(note_parts[1])
        
        if len(note_val) > 1:        # check for accidental
            accidental=note_val[1]
        else:
            accidental = None
        
        fingering, articulations = get_fing_art(3, note_parts)

        note = Note(value=note_val[0].lower(),
                     length=note_len,
                     num_dots=note_num_dots,
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
            output.write("\\new Staff \n")
            if self.instrument is not None:
                output.write('\\with {\n instrumentName = #"' + self.instrument +'"\n}') #+ '"\n midiInstrument = #"' + self.instrument +'"\n }')
            output.write("{\\absolute {\n")
            output.write("\\override Score.BarNumber.break-visibility = ##(#t #t #t)")
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
                
                one_div_note_len = 1/int(note.length)
                for j in range(note.num_dots):
                    one_div_note_len += 1/(2**(j+1) * int(note.length))
                
                m_count += one_div_note_len
                # end measure
                m_total = self.sigs[0].top / self.sigs[0].bot
                curr, index = "", ""
                output.write(note.print())
                output.write(" ")
                if m_count >= m_total:
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
