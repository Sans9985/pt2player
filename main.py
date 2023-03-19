from time import sleep
from mido import bpm2tempo, tempo2bpm
from pygame import mixer

mixer.pre_init()
mixer.init()
vol = 0.16

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

def playsounds(sounds:str, length:float) -> None:
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
                    mixer.Sound(f"sounds/{sounds[i][j]}.mp3").play().set_volume(vol)
            else:
                mixer.Sound(f"sounds/{sounds[i]}.mp3").play().set_volume(vol)

            s = False
            length -= 0.08
            sleep(0.08)

    if "@" in sounds:
        sounds = sounds.split("@")
        for i in range(len(sounds)):
            if "." in sounds[i]:
                sounds[i] = sounds[i].split(".")

            if type(sounds[i]) != list:
                mixer.Sound(f"sounds/{sounds[i]}.mp3").play().set_volume(vol)
            else:
                for j in range(len(sounds[i])):
                    mixer.Sound(f"sounds/{sounds[i][j]}.mp3").play().set_volume(vol)

            s = False
            length -= 0.06
            sleep(0.06)

    if "!" in sounds:
        sounds = sounds.split("!")
        for i in range(len(sounds)):
            if "." in sounds[i]:
                sounds[i] = sounds[i].split(".")

            if type(sounds[i]) != list:
                mixer.Sound(f"sounds/{sounds[i]}.mp3").play().set_volume(vol)
            else:
                for j in range(len(sounds[i])):
                    mixer.Sound(f"sounds/{sounds[i][j]}.mp3").play().set_volume(vol)
            s = False

            length -= 0.04
            sleep(0.04)

    if "~" in sounds:
        sounds = sounds.split("~")
        for i in range(len(sounds)):
            if "." in sounds[i]:
                sounds[i] = sounds[i].split(".")

            if type(sounds[i]) != list:
                mixer.Sound(f"sounds/{sounds[i]}.mp3").play().set_volume(vol)
            else:
                for j in range(len(sounds[i])):
                    mixer.Sound(f"sounds/{sounds[i][j]}.mp3").play().set_volume(vol)

            s = False
            sleep(length / len(sounds))

    if "." in sounds:
        sounds = sounds.split(".")
        for i in range(len(sounds)):
            mixer.Sound(f"sounds/{sounds[i]}.mp3").play().set_volume(vol)
        s = False

    if s:
        mixer.Sound(f"sounds/{sounds}.mp3").play().set_volume(vol)

    if length != 0:
        if length > 0.01:
            sleep(length - 0.01)

def playsong(song:str, tempo:float) -> None:
    if tempo < 0.001:
        raise ValueError('Tempo must be at least 0.001')
    mutes:list[str] = ["Q", "R", "S", "T", "U", "V", "W", "X", "Y"]
    lengths:list[str] = ["H", "I", "J", "K", "L", "M", "N", "O", "P"]
    tick:list[float] = [
        bpm2tempo(tempo) / 31250 * 0.25,   # H
        bpm2tempo(tempo) / 62500 * 0.25,   # I
        bpm2tempo(tempo) / 125000 * 0.25,  # J
        bpm2tempo(tempo) / 250000 * 0.25,  # K
        bpm2tempo(tempo) / 500000 * 0.25,  # L
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
            if len(song[i][0]) > 1:
                l = 0
                for j in range(len(song[i][0])):
                    n = mutes.index(song[i][0][j])
                    l += tick[n]
                print(f"{' ' * 50} {song[i][0]:16s} {str(i):5s}")
                sleep(l)
            else:
                if song[i][0] == "":
                    break
                n = mutes.index(song[i][0])
                print(f"{' ' * 50} {song[i][0]:16s} {str(i):5s}")
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

            print(f"{song[i][0]:50s} {song[i][1]:16s} {str(i):5s} {round(l*1000,1)}ms")
            playsounds(song[i][0], l)


name = input("enter the song you want to play: ")
try:
    with open(f"songs/{name}.txt") as f:
        data = f.readlines()
except:
    exit("\nfile not found; is it in the 'songs' folder?")
print(f"\nSong: {name}")
for i in range(0,len(data),2):
    h = float(data[i].strip())
    s = data[i+1].strip()
    print(f"""
 ========================= Part {(i // 2) + 1} =========================
 Tempo: {h} bpm
""")
    playsong(s,h)

print("\n ========================== end ==========================\n")