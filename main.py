from time import sleep
from pygame import mixer, version as pygver
from os import chdir

try:
    from mido import bpm2tempo
except ImportError:
    exit("use `pip install mido` before running this file")

def checkerrors(song:str) -> None:
    song = song.replace(";", ",")
    song = song.split(",")

    for i in range(len(song)):
        if " " in song[i]:
            print(f"syntax error: there is a missing comma somewhere at around note {i+1}")
            return -1

        notebrackets = (song[i].count("["), song[i].count("]"))
        if notebrackets[0] != notebrackets[1]:
            print(f"syntax error: missing '[' or ']' at note {i+1}")
            return -1

        brackets = (song[i].count("("), song[i].count(")"))

        if ((brackets[0] != brackets[1]) and ("." or "@" or "~" or "!" or "%" in song[i])):
            print(f"syntax error: missing '(' or ')' at note {i+1}")
            return -1

    return 0


def playsounds(sounds:str, length:float) -> None:
    c = 0.02
    if sounds == '':
        return

    s = True
    sounds = sounds.replace("(","")
    sounds = sounds.replace(")","")

    if "%" in sounds:
        sounds = sounds.split("%")
        for i in range(len(sounds)):
            if "." in sounds[i]:
                sounds[i] = sounds[i].split(".")

            if type(sounds[i]) == list:
                for j in range(len(sounds[i])):
                    mixer.Sound(f"{soundpath}/{sounds[i][j]}.mp3").play().set_volume(vol)
            else:
                mixer.Sound(f"{soundpath}/{sounds[i]}.mp3").play().set_volume(vol)

            s = False
            length -= c * 4
            sleep(c * 4)

    if "@" in sounds:
        sounds = sounds.split("@")
        for i in range(len(sounds)):
            if "." in sounds[i]:
                sounds[i] = sounds[i].split(".")

            if type(sounds[i]) != list:
                mixer.Sound(f"{soundpath}/{sounds[i]}.mp3").play().set_volume(vol)
            else:
                for j in range(len(sounds[i])):
                    mixer.Sound(f"{soundpath}/{sounds[i][j]}.mp3").play().set_volume(vol)

            s = False
            length -= c * 3
            sleep(c * 3)

    if "!" in sounds:
        sounds = sounds.split("!")
        for i in range(len(sounds)):
            if "." in sounds[i]:
                sounds[i] = sounds[i].split(".")

            if type(sounds[i]) != list:
                mixer.Sound(f"{soundpath}/{sounds[i]}.mp3").play().set_volume(vol)
            else:
                for j in range(len(sounds[i])):
                    mixer.Sound(f"{soundpath}/{sounds[i][j]}.mp3").play().set_volume(vol)
            s = False

            length -= c * 2
            sleep(c * 2)

    if "~" in sounds:
        sounds = sounds.split("~")
        for i in range(len(sounds)):
            if "." in sounds[i]:
                sounds[i] = sounds[i].split(".")

            if type(sounds[i]) != list:
                mixer.Sound(f"{soundpath}/{sounds[i]}.mp3").play().set_volume(vol)
            else:
                for j in range(len(sounds[i])):
                    mixer.Sound(f"{soundpath}/{sounds[i][j]}.mp3").play().set_volume(vol)

            s = False
            sleep(length / len(sounds))

    if "." in sounds:
        sounds = sounds.split(".")
        for i in range(len(sounds)):
            mixer.Sound(f"{soundpath}/{sounds[i]}.mp3").play().set_volume(vol)
        s = False

    if s:
        mixer.Sound(f"{soundpath}/{sounds}.mp3").play().set_volume(vol)

    if length != 0:
        if length > 0.01:
            sleep(length - 0.01)

def playsong(song:str, tempo:float) -> None:
    if tempo < 0.001:
        print('tempo must be at least 0.001')
        return

    s = checkerrors(song)
    if s == 0:
        mutes:list[str] = ["Q", "R", "S", "T", "U", "V", "W", "X", "Y"]
        lengths:list[str] = ["H", "I", "J", "K", "L", "M", "N", "O", "P"]
        tick:list[float] = [
            bpm2tempo(tempo) /   31250 * 0.25, # H
            bpm2tempo(tempo) /   62500 * 0.25, # I
            bpm2tempo(tempo) /  125000 * 0.25, # J
            bpm2tempo(tempo) /  250000 * 0.25, # K
            bpm2tempo(tempo) /  500000 * 0.25, # L
            bpm2tempo(tempo) / 1000000 * 0.25, # M
            bpm2tempo(tempo) / 2000000 * 0.25, # N
            bpm2tempo(tempo) / 4000000 * 0.25, # O
            bpm2tempo(tempo) / 8000000 * 0.25  # P
        ]

        rep = ["2<", "3<", "5<", "6<", "7<", "8<", "9<", "10<", ">"]
        for ss in rep:
            song = song.replace(ss, "")

        song = song.replace(";", ",")
        song = song.split(",")
        if song[-1] == '':
            del song[-1]

        for i in range(len(song)):
            song[i] = song[i].replace("]", "")
            song[i] = song[i].split("[")

        for i in range(len(song)):
            if len(song[i]) == 1:
                l = 0
                if len(song[i][0]) > 1:
                    for j in range(len(song[i][0])):
                        n = mutes.index(song[i][0][j])
                        l += tick[n]
                    print(f"{str(i+1):>5} {' ' * 50} {song[i][0]:50s} {round(l*1000,3)}ms")
                    sleep(l)
                else:
                    if song[i][0] == "":
                        break
                    n = mutes.index(song[i][0])
                    print(f"{str(i+1):>5} {' ' * 50} {song[i][0]:50s} {round(tick[n]*1000,3)}ms")
                    sleep(tick[n])
            else:
                if len(song[i][1]) > 1:
                    l = 0
                    for j in range(len(song[i][1])):
                        n = lengths.index(song[i][1][j])
                        l += tick[n]
                else:
                    n = lengths.index(song[i][1])
                    l = tick[n]

                print(f"{str(i+1):>5} {song[i][0]:50s} {song[i][1]:50s} {round(l*1000,3)}ms")

                playsounds(song[i][0], l)

if __name__ == '__main__':
    loc = __file__.split("\\")[:-1]

    path = ""
    for i in range(len(loc)):
        if path != "":
            path = path + "/" + loc[i]
        else:
            path = loc[i]

    chdir(path)
    print(f"current directory: {path}")
    del chdir

    mixer.pre_init()
    mixer.init()

    soundpath = "sounds/1"
    version = "0.2.1c"
    vol = 0.15

    def setchannels(c: int) -> None:
        mixer.set_num_channels(c)

    setchannels(500)

    bBeats:list[float | int] = [0.03125, 0.0625, 0.125, 0.1875, 0.25, 0.375, 0.5, 0.75, 1, 1.5, 2, 2.5, 3, 4, 5, 6, 8]
    class Calculator:
        def BpmToTps(bpm:float, bb:float, FPS:int = 60) -> float:
            if bb in bBeats and bpm >= 0:
                return round(bpm / FPS / bb,3)
            else:
                return -1.0

        def TpsToBpm(tps:float, bb:float, FPS:int = 60) -> float:
            if bb in bBeats and tps >= 0:
                return round(tps * FPS * bb,3)
            else:
                return -1.0

    st = True
    print("\nyou can change the soundset by typing 'set soundset <value>' according to the folders in sounds/\n(by default, this is 1)")

    if pygver.ver < "2.4.0":
        print(f"pygame {pygver.ver} was found; update to 2.4.0 or newer for best performance\n")
    else:
        print()

    while st:
        name = input("> ").strip()
        if name == "exit":
            st = False

        elif name.startswith("set"):
            try:
                name: str = name.split(" ",1)[1]
                (name, option) = name.split(" ", 1)
                # option = name.split(" ",1)[1].split()
            except IndexError:
                print("set <option> <value>")
                continue

            if name == "soundset":
                soundpath = f"sounds/{option}"
                print(f"using sounds from sounds/{option}")

            elif name == "volume":
                if option == "default":
                    vol = 0.15
                    print("volume has been set to default value (15%)")
                else:
                    vol = float(option) / 100.0
                    print(f"volume has been set to {option}%")

            else:
                print("option doesn't exist; options are:\n - soundset\n - volume")

        elif name.startswith("play"):
            f: int = 0
            try:
                name: str = name.split(" ",1)[1]
            except IndexError:
                print("play <filename>")
                continue

            try:
                with open(f"songs/{name}.pt2") as f:
                    data: list[str] = f.readlines()
                d: int = 1
            except:
                print(f"\nfile (songs/{name}.pt2) not found")
                d: int = 0

            if d == 1:
                print(f"\nsong: {name} (from file: songs/{name}.pt2)")

                i = 0
                while i < len(data):
                    if data[i].startswith(":"):
                        del data[i]
                        i = -1
                    i += 1

                i: int = 0
                while i < len(data):
                    if len(data) >= 2:
                        tempo: float = float(data[i].strip())
                        songdata: str = data[i+1].strip()

                        if ";;" in songdata or ",," in songdata:
                            songdata = songdata.split(";;")[0]
                            f = 1
                    else:
                        print("empty song")

                    print(f"""
========================= Part {(i // 2) + 1} =========================
Tempo: {tempo} bpm
""")
                    playsong(songdata,tempo)
                    i += 2

                    if f == 1:
                        break

                print("\n ========================== end ==========================\n")

        elif name.startswith("sound"):
            try:
                s = name.split(" ",1)[1]
            except IndexError:
                print("sound <json code> <tempo>")
                continue

            if not " " in name:
                print("sound <json code> <tempo>")

            else:
                s = s.split()

                if len(s) != 2:
                    print("sound command must have 2 arguments: 'sound' and 'bpm'")
                else:
                    playsong(s[0],float(s[1]))

        elif name == "version":
            print(f"\npt2player ver. {version}\n")

        elif name == "help":
            print(f"""
COMMANDS:

set             sets values
syntax: set <option> <value>
-> soundset    changes the soundset (from ./sounds/ folder; currently {soundpath})
-> volume      sets master volume of the app (currently {vol*100}%)

play            reads a file then plays the notes from it
syntax: play <filename>

sound           plays notes from an input
syntax: sound <json code> <tempo>
""", flush=True)