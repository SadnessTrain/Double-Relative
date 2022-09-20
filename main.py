# double relative project


#                    OBVIOUSLY ADD OSU-TRAINER STYLE MAP SELECTION
#       ADD TRY CATCH AND DELETE FILES ON ERROR SO YOU DONT LEAVE TRASH AROUND
#       ALSO ADD DOUBLE_RELATIVE TAG SO USERS CAN DELETE ALL MAPS MADE BY THIS
#
#
# pyinstaller --onefile --paths C:\Users\Myszon\PycharmProjects\a\venv\Lib\site-packages  main.py

import os
import re
import time

from pydub import AudioSegment
import tkinter as tk
from tkinter import filedialog
from pathlib import Path

startprompt=input("A window will pop up, where you will select the .osu file of the map you want.\nInput (1) to continue.\n")

root = tk.Tk()
root.withdraw()
home=Path.home()
home=str(home)
home=home.replace("\\","/")
inidir=home+"/AppData/Local/osu!/Songs"
inputpathtxt = filedialog.askopenfilename(initialdir=inidir,filetypes=[('.osu','.osu')], title='Select .osu file of the map you want')

repeats=input("how many repeats? 1 = double, 2 = triple, etc.\n")

relativepath=inputpathtxt.replace("\\","/")
relativepath=relativepath.replace("\"","")
relative=open(relativepath,"r",encoding='utf-8',errors='ignore')

temppath=[x+"/"for x in relativepath.split("/") if x]
filename=temppath[len(temppath)-1]
filename=filename.split("[")
if int(repeats) == 1:
    filename[1]="[Double Relative].osu"
elif int(repeats) == 2:
    filename[1]="[Triple Relative].osu"
elif int(repeats) == 3:
    filename[1]="[Quadruple Relative].osu"
elif int(repeats) > 3:
    filename[1]="["+repeats+" Relative].osu"
filename=filename[0]+filename[1]
temppath.remove(temppath[len(temppath)-1])
temppath.append(filename)
temppath="".join(temppath)
temppath=temppath.replace("\"","")
double=open(temppath, "w",encoding='utf-8',errors='ignore')

doubleaudioname=""
timings=[]
timingpoints=[]
objects=[]
hitobjects=[]
finishedtiming=""
finishedobject=""
audioend=-1
timeshift=-1
act1=True
act2=False
act3=False
act4=False

def timingShifter(timings, timeshift, audioend, repeats):
    for x in range(1,int(repeats)+1):
        audioendnew=audioend
        timingsnew=timings
        finishedtiming = ""
        for y in timingsnew:
            y[0]=str(int(y[0])+int(timeshift)+int(audioendnew)+1)
            for z in range(0, len(y)):
                finishedtiming = finishedtiming + y[z]
            timingpoints.append(finishedtiming)
            finishedtiming = ""
    for x in timingpoints:
        double.write(x + "\n")

def objectShifter(objects, timeshift, audioend, repeats):
    for x in range(1, int(repeats) + 1):
        audioendnew = audioend
        objectsnew = objects
        finishedobject = ""
        for y in objectsnew:
            y[4] = str(int(y[4]) + int(timeshift) + int(audioendnew) + 1)
            for z in range(0, len(y)):
                finishedobject = finishedobject + y[z]
            hitobjects.append(finishedobject)
            finishedobject = ""
    for x in hitobjects:
        double.write(x + "\n")

print("starting text editing (0%)")
print("wait warmly")

for line in relative:

    doWrite=True

    if act1:
        line=line.strip()
        line=re.split("([: ])", line)
        if len(line)>1:
            if line[0]=="AudioFilename":
                for x in range(0,len(line)):
                    if x>=4:
                        doubleaudioname=doubleaudioname+line[x]
                doubleaudioname=doubleaudioname.strip()
                doubleaudioname=doubleaudioname.split(".")
                doubleaudioextension = "." + doubleaudioname[1]
                doubleaudioname=doubleaudioname[0]

                tempaudiopath = re.split("(/)", relativepath)
                tempaudiopath.remove(tempaudiopath[len(tempaudiopath) - 1])
                tempaudiopath = "".join(tempaudiopath)
                doubleaudiopath = tempaudiopath + doubleaudioname + doubleaudioextension

                doubleaudio = AudioSegment.from_file(doubleaudiopath)
                audioend=len(doubleaudio)

                if int(repeats)==1:
                    double.write("AudioFilename: "+"double"+doubleaudioextension+"\n")
                    finishedaudioname="double"
                elif int(repeats)==2:
                    double.write("AudioFilename: " + "triple" + doubleaudioextension + "\n")
                    finishedaudioname = "triple"
                elif int(repeats)==3:
                    double.write("AudioFilename: " + "quadruple" + doubleaudioextension + "\n")
                    finishedaudioname = "quadruple"
                elif int(repeats)>3:
                    double.write("AudioFilename: " + repeats+"x" + doubleaudioextension + "\n")
                    finishedaudioname = repeats+"x"
                doWrite=False
            if line[0] == "Version":
                if int(repeats)==1:
                    double.write("Version: Double Relative"+"\n")
                elif int(repeats)==2:
                    double.write("Version: Triple Relative"+"\n")
                elif int(repeats)==3:
                    double.write("Version: Quadruple Relative"+"\n")
                elif int(repeats)>3:
                    double.write("Version: "+repeats+"x "+"Relative"+"\n")
                doWrite=False
        if line[0] == "[TimingPoints]":
            act1=False
            act2=True

    if act2:
        line="".join(line)
        line = line.strip()
        line = line.split()
        if len(line)>=1 and line[0]!="[TimingPoints]":
            timing=re.split("(,)",line[0])
            if timeshift!=-1:
                timeshift = timing[0]
                if timeshift>50:
                    timeshift=50-timeshift
            timings.append(timing)
        elif len(line)==0:
            timingShifter(timings, timeshift, audioend, repeats)
            act2 = False
            act3 = True

    if act3:
        line = "".join(line)
        line = line.strip()
        line = line.split()
        if len(line)>=1:
            if line[0] == "[HitObjects]":
                act3=False
                act4=True

    if act4:
        line = "".join(line)
        line = line.strip()
        line = line.split()
        if len(line)>=1 and line[0]!="[HitObjects]":
            Object=re.split("(,)",line[0])
            if Object[6]!="12":
                objects.append(Object)

    defaultline="".join(line)
    if doWrite:
        double.write(defaultline+"\n")

objectShifter(objects,timeshift,audioend,repeats)

relative.close()
double.close()

print("text editing done (16%)")
print("starting audio editing (18%)")
print("wait warmly, this may take a moment (23%)")


finishedaudio=doubleaudio

time.sleep(4)
print("editing... (43%)")

for x in range(0,int(repeats)):
    finishedaudio=finishedaudio+doubleaudio

time.sleep(2)
print("compiling... (78%)")

finishedaudio.export(tempaudiopath+finishedaudioname+doubleaudioextension, format=doubleaudioextension.split(".")[1])

print("exporting... (94%)")

print("done.")
os.system('pause')