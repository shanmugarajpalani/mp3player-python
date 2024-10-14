from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
root=Tk()
root.title("mp3_player")
root.iconbitmap(r"D:\software projects\mp3 player\app_icon.ico")
#root.geometry("5000x700")

def play_time():
    current_time=pygame.mixer.music.get_pos()/1000
    current_time_converter=time.strftime("%H:%M:%S",time.gmtime(current_time))
    
    #current_song=song_box.curselection
    song=song_box.get(ACTIVE)
    song=f"D:\software projects\mp3 player\songs\{song}.mp3"
    song_mut=MP3(song)
    global song_lenght_converted, song_lenght
    song_lenght=song_mut.info.length
    
    song_lenght_converted=time.strftime("%H:%M:%S",time.gmtime(song_lenght))
    
    status_bar.config(text=f"time eclippsed{current_time_converter}/{song_lenght_converted}")
    #song_slider.config(value=0)
    status_bar.after(1000,play_time)




#add song
def add_song():
    song=filedialog.askopenfilename(initialdir="D:\software projects\mp3 player\songs",title="choose a file",filetypes=(("mp3 files","*.mp3"),))
    
    song=song.replace("D:/software projects/mp3 player/songs/","")
    song=song.replace("-.mp3","")

    song_box.insert(END,song)


#add many songs
def add_many_songs():
    songs=filedialog.askopenfilenames(initialdir="D:\software projects\mp3 player\songs",title="choose a file",filetypes=(("mp3 files","*.mp3"),))
    for song in songs:
        song=song.replace("D:/software projects/mp3 player/songs/","")
        song=song.replace(".mp3","")

        song_box.insert(END,song)


def on_song_end():
    next_one = song_box.curselection()
    if next_one:  # Check if there's a song selected
        next_one = next_one[0] + 1
        if next_one < song_box.size():  # Check bounds
            song_box.selection_clear(0, END)
            song_box.activate(next_one)
            song_box.selection_set(next_one)
            play()
        else:
            song_box.selection_clear(0, END)

    
def play():
    global a
    a=2
    song=song_box.get(ACTIVE)
    song=f"D:\software projects\mp3 player\songs\{song}.mp3"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    play_time()
    #song_pos=int(song_lenght)
    #song_slider.config(to=song_pos)
    #slide()

def forward():
    next_one=song_box.curselection()
    next_one=next_one[0]+1
    song=song_box.get(next_one)
    song=f"D:\software projects\mp3 player\songs\{song}.mp3"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    song_box.selection_clear(0,END)
    song_box.activate(next_one)
    song_box.selection_set(next_one,last=None)
    


def reverse():
    next_one=song_box.curselection()
    next_one=next_one[0]-1
    song=song_box.get(next_one)
    song=f"D:\software projects\mp3 player\songs\{song}.mp3"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    song_box.selection_clear(0,END)
    song_box.activate(next_one)
    song_box.selection_set(next_one,last=None)
    

global paused
paused=False
def pause(is_paused):
    
    global paused
    paused=is_paused
    if paused:
        pygame.mixer.music.unpause()
        paused=False
    else:
        pygame.mixer.music.pause()
        paused=True
'''def slide(x):
    
    
    slider_label.config(text=f'{(song_slider.get())}to{int(song_lenght)}')'''

#create list box
pygame.mixer.init()
song_box= Listbox(root,background="black",fg="white",width=60,height=30,selectbackground="gray",selectforeground="black")
song_box.pack(pady=20,padx=20)


#create buttons
play_btn_img=PhotoImage(file="D:\software projects\mp3 player\play.png")
pause_btn_img=PhotoImage(file="D:\software projects\mp3 player\pause.png")
forward_btn_img=PhotoImage(file="D:\software projects\mp3 player\joker.png")
reverse_btn_img=PhotoImage(file="D:\software projects\mp3 player\left.png")

controframe=Frame(root)
controframe.pack()

play_btn=Button(controframe,image=play_btn_img,borderwidth=0,command=play)
pause_btn=Button(controframe,image=pause_btn_img,borderwidth=0,command= lambda: pause(paused))
forward_btn=Button(controframe,image=forward_btn_img,borderwidth=0,command=forward)
reverse_btn=Button(controframe,image=reverse_btn_img,borderwidth=0,command=reverse)

reverse_btn.grid(row=0,column=0)
play_btn.grid(row=0,column=1)
pause_btn.grid(row=0,column=2)
forward_btn.grid(row=0,column=3)

#add menu
my_menu=Menu(root)
root.config(menu=my_menu)

add_song_menu=Menu(my_menu)
my_menu.add_cascade(label="add songs",menu=add_song_menu)
add_song_menu.add_command(label="add song to the playlist",command=add_song)
add_song_menu.add_command(label="add many songs",command=add_many_songs)
status_bar=Label(root,text="",bd=1,relief=GROOVE,anchor=E)
status_bar.pack(fill=X,side=BOTTOM,ipady=2)

#song_slider=Scale(root,from_=0,to=100,orient=HORIZONTAL,command=slide,length=360,width=10)
#song_slider.pack(pady=20)

#slider_label=Label(root,text="0")
#slider_label.pack()

global a
a=1


def check_music_status():

    if paused==False and a!=1:
        if pygame.mixer.music.get_busy() == 0:  # Check if music is not playing
            on_song_end()
    root.after(100, check_music_status)  # Check the music status every 100 ms

check_music_status()


root.mainloop()