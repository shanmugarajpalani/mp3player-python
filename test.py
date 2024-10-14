from tkinter import *
import pygame
from tkinter import filedialog
import os

# Initialize Pygame
pygame.init()  # Initialize all Pygame modules
pygame.mixer.init()  # Initialize the mixer for audio playback

root = Tk()
root.title("MP3 Player")
root.iconbitmap(r"D:\software projects\mp3 player\app_icon.ico")

# Add song

def add_song():
    song = filedialog.askopenfilename(initialdir="D:\software projects\mp3 player\songs",
                                       title="Choose a file", filetypes=(("MP3 files", "*.mp3"),))
    if song:  # Check if a song was selected
        song_name = os.path.basename(song)  # Get the file name
        song_box.insert(END, song_name[:-4])  # Remove the .mp3 extension

# Add many songs
def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir="D:\software projects\mp3 player\songs",
                                         title="Choose files", filetypes=(("MP3 files", "*.mp3"),))
    for song in songs:
        song_name = os.path.basename(song)  # Get the file name
        song_box.insert(END, song_name[:-4])  # Remove the .mp3 extension
    
def play_song():
    song = song_box.get(ACTIVE)
    song_path = f"D:\\software projects\\mp3 player\\songs\\{song}.mp3"
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play(loops=0)

def on_song_end():
    next_one = song_box.curselection()
    if next_one:  # Check if there's a song selected
        next_one = next_one[0] + 1
        if next_one < song_box.size():  # Check bounds
            song_box.selection_clear(0, END)
            song_box.activate(next_one)
            song_box.selection_set(next_one)
            play_song()
        else:
            song_box.selection_clear(0, END)  # Clear selection if at the end

def forward():
    next_one = song_box.curselection()
    if next_one:  # Check if there's a song selected
        next_one = next_one[0] + 1
        if next_one < song_box.size():  # Check bounds
            song_box.selection_clear(0, END)
            song_box.activate(next_one)
            song_box.selection_set(next_one)
            play_song()

def reverse():
    prev_one = song_box.curselection()
    if prev_one:  # Check if there's a song selected
        prev_one = prev_one[0] - 1
        if prev_one >= 0:  # Check bounds
            song_box.selection_clear(0, END)
            song_box.activate(prev_one)
            song_box.selection_set(prev_one)
            play_song()

global paused
paused = False

def pause():
    global paused
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True

# Create list box
song_box = Listbox(root, background="black", fg="white", width=60, height=30,
                   selectbackground="gray", selectforeground="black")
song_box.pack(pady=20, padx=20)

# Create buttons
play_btn_img = PhotoImage(file="D:\software projects\mp3 player\play.png")
pause_btn_img = PhotoImage(file="D:\software projects\mp3 player\pause.png")
forward_btn_img = PhotoImage(file="D:\software projects\mp3 player\joker.png")
reverse_btn_img = PhotoImage(file="D:\software projects\mp3 player\left.png")

control_frame = Frame(root)
control_frame.pack()

play_btn = Button(control_frame, image=play_btn_img, borderwidth=0, command=play_song)
pause_btn = Button(control_frame, image=pause_btn_img, borderwidth=0, command=pause)
forward_btn = Button(control_frame, image=forward_btn_img, borderwidth=0, command=forward)
reverse_btn = Button(control_frame, image=reverse_btn_img, borderwidth=0, command=reverse)

reverse_btn.grid(row=0, column=0)
play_btn.grid(row=0, column=1)
pause_btn.grid(row=0, column=2)
forward_btn.grid(row=0, column=3)

# Add menu
my_menu = Menu(root)
root.config(menu=my_menu)

add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add Song to Playlist", command=add_song)
add_song_menu.add_command(label="Add Many Songs", command=add_many_songs)



# Bind the end of the song to the on_song_end function
def check_music_status():
    if pygame.mixer.music.get_busy() == 0:  # Check if music is not playing
        on_song_end()
    root.after(100, check_music_status)  # Check the music status every 100 ms

check_music_status()  # Start checking music status

root.mainloop()

# Quit Pygame when done
pygame.quit()
