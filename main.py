import os, subprocess, base64, zlib, tempfile
from tkinter import Tk
from tkinter import Label
from tkinter import Entry
from tkinter import Scrollbar
from tkinter import Frame
from tkinter import Canvas
from tkinter import filedialog
from pymediainfo import MediaInfo

def getLength(filename):
    media_info = MediaInfo.parse(filename)
    duration_in_ms = media_info.tracks[0].duration
    return duration_in_ms

def time(ms):
    ms = int(ms)
    seconds=(ms/1000)%60
    seconds = int(seconds)
    minutes=(ms/(1000*60))%60
    minutes = int(minutes)
    hours=int((ms/(1000*60*60))%24)
    output = ""
    strHours = ''
    strMinutes = ''
    strSeconds = ''
    if hours < 10:
        strHours += '0'
    if minutes < 10:
        strMinutes = '0'
    if seconds < 10:
        strSeconds = '0'
    strHours += str(hours)
    strMinutes += str(minutes)
    strSeconds += str(seconds)
    if hours > 0:
        output += strHours + ":"
    output += strMinutes + ":" + strSeconds
    return output

root = Tk()
root.iconbitmap(default='./icon.ico')
root.title("RUNTIME")
root.directory = filedialog.askdirectory()

rframe = Frame(root)
rframe.grid(row=0, column=0, pady=(5, 0), sticky='nw')
rframe.grid_rowconfigure(0, weight=1)
rframe.grid_columnconfigure(0, weight=1)
rframe.grid_propagate(False)

rcanvas = Canvas(rframe)
rcanvas.grid(row=0, column=0, sticky='news')

scrollbar = Scrollbar(rframe, orient='vertical', command=rcanvas.yview)
scrollbar.grid(row=0,column=1,sticky='ns')
rcanvas.configure(yscrollcommand=scrollbar.set)

frame_text = Frame(rcanvas)

print(root.directory)

output = ''
totalTime = 0
count = 0
fileArray = []
durArray = []

for filename in os.listdir(root.directory):
    if filename.endswith(('.mkv','.mp4','.m4v','.wmv')):
        count+=1
        print(filename)
        fileTime = getLength(root.directory + "/" + filename)
        duration = str(time(fileTime))
        output += filename + "\t" + duration + "\n"
        fileArray.append(filename)
        fileArray.append(duration)
        totalTime += fileTime

fileArray.append("Total runtime: ")
fileArray.append(time(totalTime))

height = int(len(fileArray) / 2)
width = 2
count = 0
ew = True
print(fileArray)
fileArray.reverse()
b = [[Label() for j in range(width)] for i in range(height)]
for i in range(height): #Rows
    for j in range(width): #Columns
        q = i+j
        if i+j >= height:
            q = i
        fi = fileArray.pop()
        print(fi)
        if ew:
            b[i][0] = Label(frame_text, text=fi, anchor="e")
            b[i][0].grid(row=i, column=j, sticky='news')
            ew = False
        else:
            b[i][1] = Label(frame_text, text=fi, anchor="e")
            b[i][1].grid(row=i, column=j, sticky='news')
            ew = True
        count += 1

minHeight = 10
if height < 10:
    minHeight = height

rcanvas.create_window((0, 0), window=frame_text, anchor='nw')
frame_text.update_idletasks()
first5columns_width = sum([b[0][j].winfo_width() for j in range(0, 2)])
first5rows_height = sum([b[i][0].winfo_height() for i in range(0, minHeight)])
rcanvas.config(scrollregion=rcanvas.bbox('all'), width = first5columns_width,height = first5rows_height)

rframe.config(width=first5columns_width + scrollbar.winfo_width(),height=first5rows_height)

root.mainloop()