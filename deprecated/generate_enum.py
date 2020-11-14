print("class NoteValue(IntEnum):")
i = 0
for letter in ["A", "B", "C", "D", "E", "F", "G", "a", "b", "c", "d", "e", "f", "g"]:
    for accidential in ["s", "f", ""]:
        for octave in range(8):
            print("  " + letter + accidential + str(octave) + " = " + str(i))
            i += 1

