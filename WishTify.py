# Realization : DELZENNE 'OniX' Gauthier & GRAVEL 'AssA' Téo

# Prerequisite :
# - Install PyGame : pip install pygame
# - Install Mutagen : pip install mutagen


# Setup Import :
import os
import json
from tkinter import *
from tkinter import filedialog
import pygame
import time
from mutagen.mp3 import MP3

# Creation "Music" class
class Music :
    # Executed when an instance is created
    # Takes the location of the file as a setting
    # Sets <Instance>.store as the location and <Instance>.name as the name, the name being after the last / in the location
    def __init__(self, store : str):
        # We test if the location ends with .mp3
        if not store.endswith(".mp3") :
            raise ValueError("`store` devrait se terminer par .mp3")
        self.store = store
        self.name = store.split("/")[-1].replace(".mp3", "", 1)

    # Method to obtain a music instance by knowing its name
    @staticmethod
    def nameToInstance(song_name) :
        global songs
        for song in songs :
            if song.name == song_name :
                return song

    # Method to obtain a music instance knowing its location
    @staticmethod
    def storeToInstance(store) :
        global songs
        for song in songs :
            if song.store == store :
                return song

# Setup Window :
window = Tk()
window.title("WishTify - MP3 Player")
window.geometry("375x800")
window.resizable(False, False)
window.iconbitmap("img/wishtify_logo.ico")
window.config(background="#222")

# Initialisation Pygame :
pygame.mixer.init()

# Variables
pause = False
playing = False
songs = []

# Methods :
def play_action() :
    global playing
    playing = True
    song = song_box.get(ACTIVE)
    song = Music.nameToInstance(song).store
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()
    song_duration()

    # Timeline Refresh :
    slider_position = int(song_length)
    timeline_slider.config(to=slider_position)
    timeline_slider.set(0)

def pause_action(pause_on) :
    global pause
    pause = pause_on
    if pause :
        pygame.mixer.music.unpause()
        pause = False
    else :
        pygame.mixer.music.pause()
        pause = not pause

def stop_action() :
    global playing
    playing = False
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)
    current_time_label.config(text="Waiting for music")

def next_song_action() :
    try:
        next_song = song_box.curselection()[0] + 1
        song = song_box.get(next_song)

        if song != "" or song != None :
            song = Music.nameToInstance(song).store
            pygame.mixer.music.load(song)
            pygame.mixer.music.play()

            song_box.selection_clear(0, END)
            song_box.activate(next_song)
            song_box.selection_set(next_song, last=None)
        else :
            stop_action()
    except FileNotFoundError :
        stop_action()
    except IndexError :
        stop_action()

def previous_song_action() :
    try:
        previous_song = song_box.curselection()[0] - 1
        song = song_box.get(previous_song)

        if song != "" or song != None :
            song = Music.nameToInstance(song).store
            pygame.mixer.music.load(song)
            pygame.mixer.music.play()

            song_box.selection_clear(0, END)
            song_box.activate(previous_song)
            song_box.selection_set(previous_song, last=None)
        else :
            stop_action()
    except FileNotFoundError :
        stop_action()
    except IndexError :
        stop_action()
    
def song_duration() :
    current_time = pygame.mixer.music.get_pos() / 1000
    converted_current_time = time.strftime("%M:%S", time.gmtime(current_time))

    # Sound duration :
    act_liste = list(song_box.get(0, END))
    if act_liste != [] :
        song = song_box.get(ACTIVE)
        song = Music.nameToInstance(song).store
    
        # Use of Mutagen :
        song_mutagen = MP3(song)
        global song_length
        song_length = song_mutagen.info.length
        converted_song_length = time.strftime("%M:%S", time.gmtime(song_length))

        if converted_current_time == converted_song_length :
            next_song_action()

        # Display Duration :
        global playing
        if playing :
            current_time_label.config(text=f"{converted_current_time}    -    {converted_song_length}")
        else :
            current_time_label.config(text="Waiting for music")

        # Timeline position :
        slider_position = int(song_length)
        timeline_slider.config(to=slider_position)
        timeline_slider.set(int(current_time))

        # Refreshing the Timer :
        current_time_label.after(1000, song_duration)
    else :
        current_time_label.config(text="Waiting for music")

# Volume :
def volume_control(x) :
    pygame.mixer.music.set_volume(volume_cursor.get())

# Songs Methods :
# Add :
def add_song() :
    asong = filedialog.askopenfilename(initialdir="song/", title="Choose a music :", filetypes=(("MP3 File", "*.mp3"), ))
    if asong == '' :
        return
    # Name change (Music)
    music = Music(asong)
    songs.append(music)
    song_box.insert(0, music.name)

# Add Multiples :
def add_many_songs() :
    asongs = filedialog.askopenfilenames(initialdir="song/", title="Choose several musics :", filetypes=(("MP3 Files", "*.mp3"), ))
    for song in asongs :
        if song == '' :
            return
        music = Music(song)
        songs.append(music)
        song_box.insert(0, music.name)

# Remove :
def remove_song() :
    song_box.delete(ANCHOR)
    stop_action()

# Remove Multiples :
def remove_many_songs() :
    song_box.delete(0, END)
    stop_action()

# Playlist Methods :
# Read :
def playlist_lire() :
    playlist_loc = filedialog.askopenfilename(initialdir="playlist/", title="Choose a playlist :", filetypes=(("JSON File", "*.json"), ))
    if playlist_loc == '' :
        return
    playlist_file = open(playlist_loc, "r")
    playlist_read = playlist_file.read()
    playlist_file.close()
    playlist = json.loads(playlist_read)['list']
    
    remove_many_songs()
    for song in playlist:
        music = Music(song)
        songs.append(music)
        song_box.insert(END, music.name)

# Read Multiples :
def playlist_lire_multiples() :
    playlists_locs = filedialog.askopenfilenames(initialdir="playlist/", title="Choose several playlists :", filetypes=(("JSON Files", "*.json"), ))
    for playlist_loc in playlists_locs :
        if playlist_loc == '' :
            return
        playlist_file = open(playlist_loc, "r")
        playlist_read = playlist_file.read()
        playlist_file.close()
        playlist = json.loads(playlist_read)['list']
        
        remove_many_songs()
        for song in playlist:
            music = Music(song)
            songs.append(music)
            song_box.insert(END, music.name)

# Add :
def playlist_ajouter() :
    playlist_loc = filedialog.askopenfilename(initialdir="playlist/", title="Choose a playlist :", filetypes=(("JSON File", "*.json"), ))
    if playlist_loc == '' :
        return 
    playlist_file = open(playlist_loc, "r")
    playlist_read = playlist_file.read()
    playlist_file.close()
    playlist = json.loads(playlist_read)['list']
    
    for song in playlist:
        music = Music(song)
        songs.append(music)
        song_box.insert(END, music.name)

# Add Multiples :
def playlist_ajouter_multiple() :
    playlists_locs = filedialog.askopenfilenames(initialdir="playlist/", title="Choose several playlists :", filetypes=(("JSON Files", "*.json"), ))
    for playlist_loc in playlists_locs :
        if playlist_loc == '' :
            return
        playlist_file = open(playlist_loc, "r")
        playlist_read = playlist_file.read()
        playlist_file.close()
        playlist = json.loads(playlist_read)['list']
        
        for song in playlist:
            music = Music(song)
            songs.append(music)
            song_box.insert(END, music.name)

# Save :
def playlist_enregistrer() :
    act_liste = list(song_box.get(0, END))
    if act_liste == [] :
        return
    l = { 'list' : [] }
    for song in act_liste :
        music = Music.nameToInstance(song)
        l['list'].append(music.store)
    json_liste = json.dumps(l)
    json_loc = filedialog.asksaveasfilename(initialdir="playlist/", title="Save playlist :", defaultextension=".json", filetype=(("JSON File", "*.json"), ))
    if json_loc == '':
        return
    json_file = open(json_loc, "w")
    json_file.write(json_liste)
    json_file.close()

# Interface :
# Menu TopBar :
menu_topbar = Menu(window)
window.config(menu=menu_topbar)

# Menu TopBar - Music :
song_menu = Menu(menu_topbar, tearoff=0)

song_menu.add_command(label="Add a music", command=add_song)
song_menu.add_command(label="Add several musics", command=add_many_songs)
song_menu.add_separator()
song_menu.add_command(label="Remove the selected music", command=remove_song)
song_menu.add_command(label="Remove all music", command=remove_many_songs)

menu_topbar.add_cascade(label="Music", menu=song_menu)

# Menu TopBar - Playlist :
playlist_menu = Menu(menu_topbar, tearoff=0)

playlist_menu.add_command(label="Read a playlist", command=playlist_lire)
playlist_menu.add_command(label="Read several playlists", command=playlist_lire_multiples)
playlist_menu.add_separator()
playlist_menu.add_command(label="Add a playlist to the current list", command=playlist_ajouter)
playlist_menu.add_command(label="Add playlists to the current list", command=playlist_ajouter_multiple)
playlist_menu.add_separator()
playlist_menu.add_command(label="Save the current list", command=playlist_enregistrer)

menu_topbar.add_cascade(label="Playlist", menu=playlist_menu)

# Menu TopBar - Control Button :
control_btn_menu = Menu(menu_topbar, tearoff=0)

# The command cannot provide an argument
# Create a function that does not require an argument.
# And calls the basic function with the right argument
def pause_action_cmd() :
    global pause
    pause_action(pause)

control_btn_menu.add_command(label="Play", command=play_action)
control_btn_menu.add_command(label="Pause", command=pause_action_cmd)
control_btn_menu.add_command(label="Stop", command=stop_action)
control_btn_menu.add_separator()
control_btn_menu.add_command(label="Previous", command=previous_song_action)
control_btn_menu.add_command(label="Next", command=next_song_action)

menu_topbar.add_cascade(label="Control", menu=control_btn_menu)

# Interface :
# Title :
title_wishtify = Label(window, text="WishTify", font=("Montserrat", 24), bg="#222", fg="#1ED760")
title_wishtify.pack(pady=10)

# Playlist :
playlist_frame = Frame(window, bg="#222")

song_boxtitle = Label(playlist_frame, text="Choose your music", font=("Montserrat", 18), bg="#222", fg="#FFF")
song_boxtitle.pack()
song_box = Listbox(playlist_frame, bg="#111", font=("Montserrat", 14), fg="#FFF", borderwidth="0", selectbackground="#1ED760", selectforeground="#222", width=26)
song_box.pack()

playlist_frame.pack(pady=20)

# TimeLine :
timeline_frame = Frame(window, bg="#222")

current_time_label = Label(timeline_frame, text="Waiting for music", font=("Montserrat", 18), bg="#222", fg="#FFF")
current_time_label.pack()

timeline_slider = Scale(timeline_frame, orient="horizontal", from_=0, to=100, showvalue=0, font=("Montserrat", 18), bg="#222", fg="#FFF", troughcolor='#000', highlightthickness=0, sliderrelief='flat', length=285, activebackground="#1ED760", borderwidth=0)
timeline_slider.pack(pady=15)

timeline_frame.pack()

# Control Bouton :
control_btn_frame = Frame(window, bg="#222")

previous_img = PhotoImage(file="img/btn_previous.png")
next_img = PhotoImage(file="img/btn_next.png")
pause_img = PhotoImage(file="img/btn_pause.png")
play_img = PhotoImage(file="img/btn_play.png")
stop_img = PhotoImage(file="img/btn_stop.png")

previous_btn = Button(control_btn_frame, image=previous_img, borderwidth=0, bg="#222", activebackground="#222", command=previous_song_action)
next_btn = Button(control_btn_frame, image=next_img, borderwidth=0, bg="#222", activebackground="#222", command=next_song_action)
pause_btn = Button(control_btn_frame, image=pause_img, borderwidth=0, bg="#222", activebackground="#222", command=lambda: pause_action(pause))
play_btn = Button(control_btn_frame, image=play_img, borderwidth=0, bg="#222", activebackground="#222", command=play_action)
stop_btn = Button(window, image=stop_img, borderwidth=0, bg="#222", activebackground="#222", command=stop_action)

previous_btn.grid(row=0, column=0)
next_btn.grid(row=0, column=3)
pause_btn.grid(row=0, column=2, padx=15)
play_btn.grid(row=0, column=1, padx=15)

control_btn_frame.pack(pady=20)
stop_btn.pack()

# Volume :
volume_frame = Frame(window, bg="#222")

volume_label = Label(volume_frame, text="Volume", font=("Montserrat", 20), bg="#222", fg="#FFF")
volume_label.pack()

volume_cursor = Scale(volume_frame, orient="horizontal", from_=0, to=1, font=("Montserrat", 18), bg="#222", fg="#FFF", troughcolor='#000', highlightthickness=0, sliderrelief='flat', length=250, activebackground="#1ED760", borderwidth=0, resolution=0.1, command=volume_control)
volume_cursor.set(0.5)
volume_cursor.pack(side=BOTTOM)

volume_frame.pack(pady=25)

# Open Window :
window.mainloop()