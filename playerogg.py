# This is a program to play ogg files. I'm following the Codemy.com Videos done by John Elder
# The first bunch are on his website, but I think he further enhanced the ogg player in the
# Youtube videos on his channel.

# Get tkinter modules - best practice might be to just import the modules you're going to actually use.
from tkinter import *
# Have to import file dialog separately
from tkinter import filedialog
# Need pygame to play the music
import pygame
import time
from mutagen.oggvorbis import OggVorbis
import tkinter.ttk as ttk
import glob
from tinytag import TinyTag
import random
import sys

# Set the main window of our ogg player
# root = Tk()

# Give the main window a title and make it 500x400 pixels
# root.title("OGG Player")
# root.geometry("800x480")

# Initialize Pygame mixer
pygame.mixer.init()

class make_ogg_objects:
    def __init__(self,file_name):
        # print(f"File Name: {file_name}")
        ogg_metadata = TinyTag.get(file_name)
        self.filename = file_name
        self.genre = ogg_metadata.genre
        self.album = ogg_metadata.album
        self.artist = ogg_metadata.artist
        self.title = ogg_metadata.title



def build_initial_file_list():

    # folder = '/home/terry/Music'
    folder = '/home/terry/Dropbox/MusicAllOgg'

    files = glob.glob(folder+"/**/*.ogg", recursive=True)
    if len(files) == 0:
        print ("No ogg files in directory.", folder,"..exiting")
        sys.exit(1)
    root.lift()
    num_files_label.configure(text=f"Processing File # of {len(files)}")
    num_files_label.pack()
    root.update()

    file_count = 0
    for ogg_file in files:
        ogg_file_list.append(make_ogg_objects(ogg_file))
        # print(ogg_file_list[-1])
        # print (file_count)
        # print (ogg_file_list[file_count].title, ogg_file_list[file_count].artist, ogg_file_list[file_count].album, ogg_file_list[file_count].genre)
        # print (ogg_file_list[file_count].filename)
        # print (ogg_file_list[file_count].genre, type(ogg_file_list[file_count].genre))
        # if type(ogg_file_list[file_count].genre) != str:
        #     input()
        
        file_count += 1
        
        if file_count % 100 == 0:
            num_files_label.configure(text=f"Processing File # {file_count} of {len(files)}")
            num_files_label.pack()
            root.update()


# Create function to deal with time
def play_time():
    global playlist_box, song_slider, status_bar, volume_slider, codemy_player, final_playlist
    # Check to see if song is stopped
    if stopped:
        return

    # returns how far into the song you are in milliseconds
    current_time = pygame.mixer.music.get_pos()/1000
    # convert time to time format
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))

    # Get song to play - ACTIVE means selected song.
    index_tuple = playlist_box.curselection()
    index = index_tuple[0]
    song = final_playlist[index].filename

    # Find Current Song Length
    song_mut = OggVorbis(song)
    
    global song_length
    song_length = song_mut.info.length

    # Convert song_length to time format
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))
    
    # check to see if we're at the end of the song
    if int(song_slider.get()) == int(song_length):
        # stop()

        # Call the next song
        next_song()
     

    # Paused variable set by the pause function. If paused don't update the slider
    elif paused:
        pass
        # song_slider.config(value=current_time)
    else:
        # Move slider along 1 second at at time. This works because the play_time function runs every second.
        next_time = int(song_slider.get()) + 1
        # Output new time value to slider. Also set the to property to the length of the song.
        song_slider.config(value=next_time, to=song_length)

        # convert slider position to time format
        converted_current_time = time.strftime('%M:%S', time.gmtime(int(song_slider.get())))
        


    if current_time >= 1:
        # Put the time into the status_bar
        status_bar.config(text='Time Elapsed: ' + converted_current_time + ' of ' + converted_song_length + '  ')

    # After 1000 milliseconds, call this function again - keep updating the time.
    status_bar.after(1000, play_time)

# Create play song function
def play():
    global playlist_box, song_slider, status_bar, volume_slider, codemy_player, final_playlist
    global stopped
    # Set stopped to false since a song is now playing
    stopped = False

    # Get song to play - ACTIVE means selected song.
    index_tuple = playlist_box.curselection()
    index = index_tuple[0]
    print(index, len(final_playlist))
    song = final_playlist[index].filename

    # Load song with pygame mixer
    pygame.mixer.music.load(song)
    # Play song with pygame mixer and don't loop. Play the song just once.
    pygame.mixer.music.play(loops=0)

    # Get Song Time
    play_time()



# Created stopped boolean variable
global stopped
stopped = False

# Create stop function
def stop():
    global playlist_box, song_slider, status_bar, volume_slider, codemy_player
    # Stop the song
    pygame.mixer.music.stop()
    # Clear playlist selected bar
    playlist_box.selection_clear(ACTIVE)
    # Clear status bar
    status_bar.config(text='')

    # Set our slider to zero when we stop the song
    song_slider.config(value=0)

    # Set Stopped variable to True
    global stopped
    stopped = True

# Create paused variable so when we get to the pause routine we know if we're pausing a song,
# or if we're restarting a paused song.
global paused
paused = False

# Create pause function
def pause(is_paused):
    global playlist_box, song_slider, status_bar, volume_slider, codemy_player
    global paused
    paused = is_paused

    if paused:
        # Unpause
        pygame.mixer.music.unpause()
        paused = False
    else:
        # Pause
        pygame.mixer.music.pause()
        paused = True

# Create function to play the next song
def next_song():
    global playlist_box, song_slider, status_bar, volume_slider, codemy_player, final_playlist
    # Reset Slider Position and Status Bar
    status_bar.config(text='')
    song_slider.config(value=0)

    # Get current song number - actually returns a python tuple (x,) 
    next_one = playlist_box.curselection()
    # my_label.config(text=next_one)
    # add one to the current song number tuple.
    next_one = next_one[0] + 1

    # print(f"Next one: {next_one}, Length of final_playlist: {len(final_playlist)} ")

    if next_one == len(final_playlist):
        stop()
    else:

        # Grab song title from playlist
        # index_tuple = playlist_box.curselection()
        # index = index_tuple[0] + 1
        song = final_playlist[next_one].filename

        # Load song with pygame mixer
        pygame.mixer.music.load(song)
        # Play song with pygame mixer and don't loop. Play the song just once.
        pygame.mixer.music.play(loops=0)

        # Clear Active Bar in Playlist
        playlist_box.selection_clear(0, END)

        # Move active bar to next song
        playlist_box.activate(next_one)

        # Set active bar to next song
        playlist_box.selection_set(next_one, last=None)
        
# Create function to play previous song.
def previous_song():
    global playlist_box, song_slider, status_bar, volume_slider, codemy_player
    # Reset Slider Position and Status Bar
    status_bar.config(text='')
    song_slider.config(value=0)
    
    # Get current song number - actually returns a python tuple (x,) 
    next_one = playlist_box.curselection()
    # my_label.config(text=next_one)
    # add one to the current song number tuple.
    next_one = next_one[0] - 1
    if next_one < 0:
        stop()
    else:
        # Grab song title from playlist
        song = final_playlist[next_one].filename

        # Load song with pygame mixer
        pygame.mixer.music.load(song)
        # Play song with pygame mixer and don't loop. Play the song just once.
        pygame.mixer.music.play(loops=0)

        # Clear Active Bar in Playlist
        playlist_box.selection_clear(0, END)

        # Move active bar to next song
        playlist_box.activate(next_one)

        # Set active bar to next song
        playlist_box.selection_set(next_one, last=None)

#Create Volume function sliders need a variable even though we won't use it.
def volume(x):
    global playlist_box, song_slider, status_bar, volume_slider, codemy_player
    # my_label.config(text=volume_slider.get())     
    pygame.mixer.music.set_volume(volume_slider.get())


# Create slide function for song positioning, sliders need a variable even though we won't use it.
def slide(x):
    global playlist_box, song_slider, status_bar, volume_slider, codemy_player, final_playlist
    # Get song to play - ACTIVE means selected song.
    # song = playlist_box.get(ACTIVE)
    index_tuple = playlist_box.curselection()
    index = index_tuple[0]
    song = final_playlist[index].filename

    # Load song with pygame mixer
    pygame.mixer.music.load(song)
    # Play song with pygame mixer and don't loop. Play the song just once.
    pygame.mixer.music.play(loops=0, start=song_slider.get())

def ogg_player(playlist):
    # Set the main window of our ogg player

    global playlist_box, song_slider, status_bar, volume_slider, codemy_player, pick_genre, pick_artist, final_playlist

    if (pick_genre is not None):
        if pick_genre.winfo_exists():
            pick_genre.destroy()
    if pick_artist is not None:        
        if pick_artist.winfo_exists():
            pick_artist.destroy()
    codemy_player = Toplevel()

    # Give the main window a title and make it 500x400 pixels
    codemy_player.title("OGG Player")
    codemy_player.geometry("800x480")

    # Create main Frame
    main_frame = Frame(codemy_player)
    main_frame.pack(pady=20)
    
    random.shuffle(playlist)
    # Listbox to show our playlist
    # I think width is in characters
    playlist_box = Listbox(main_frame, bg="black", fg="#98fb98", width=75, height=13, font=('Times', 14), selectbackground="#98fb98", selectforeground="black")
    playlist_box.grid(row=0, column=0)
    # print(type(playlist_box))
    # create volume slider frame
    volume_frame = LabelFrame(main_frame, text="Volume")
    volume_frame.grid(row=0, column=1, padx=20)

    # Create volume slider, from_ because from is already a python keyword and tkinter can't use it.
    volume_slider = ttk.Scale(volume_frame, from_=1, to=0, value=0.5, orient=VERTICAL, length=125, command=volume)
    volume_slider.pack(pady=10)

    # Create Song Slider
    song_slider = ttk.Scale(main_frame, from_=0, to=100, value=0, orient=HORIZONTAL, length=480, command=slide)
    song_slider.grid(row=2, column=0, pady=20)

    # Define Button Images for Control Buttons
    back_btn_img = PhotoImage(file='images/back50.png')
    forward_btn_img = PhotoImage(file='images/forward50.png')
    play_btn_img = PhotoImage(file='images/play50.png')
    pause_btn_img = PhotoImage(file='images/pause50.png')
    stop_btn_img = PhotoImage(file='images/stop50.png')

    # Create Button Frame
    control_frame = Frame(main_frame)
    control_frame.grid(row=1, column=0, pady=20)

    # Create Play/Stop/Pause/Back/Forward Buttons
    back_button = Button(control_frame, image=back_btn_img, borderwidth=0,command=previous_song) 
    forward_button = Button(control_frame, image=forward_btn_img, borderwidth=0, command=next_song) 
    play_button = Button(control_frame, image=play_btn_img, borderwidth=0, command=play) 
    pause_button = Button(control_frame, image=pause_btn_img, borderwidth=0, command=lambda: pause(paused)) 
    stop_button = Button(control_frame, image=stop_btn_img, borderwidth=0, command=stop) 

    # Put the buttons on the screen
    back_button.grid(row=0, column=0, padx=10)
    forward_button.grid(row=0, column=1, padx=10)
    play_button.grid(row=0, column=2, padx=10)
    pause_button.grid(row=0, column=3, padx=10)
    stop_button.grid(row=0, column=4, padx=10)

    # quit_button = Button(control_frame, text="Quit", font="Verdana 30 bold", command=sys.exit)
    # quit_button.grid(row=0, column=5, padx=15)
    quit_button = Button(volume_frame, text="Quit", font="Verdana 15 bold", command=sys.exit)
    quit_button.pack()
# button = tk.Button(frame, text="Click me!", font="Verdana 19 bold")

    # Create Menu
    # my_menu = Menu(root)
    # root.config(menu=my_menu)

    # Create Add Song Menu Dropdowns
    # Don't show the tearoff dotted line
    # add_song_menu = Menu(my_menu, tearoff=0)
    # my_menu.add_cascade(label="Add Songs", menu=add_song_menu)

    # add one and many songs to playlist menu entries
    # add_song_menu.add_command(label="Add One Song To Playlist", command=add_song)
    # add_song_menu.add_command(label="Add Many Songs To Playlist", command=add_many_songs)
    # add quit option to add_song_menu
    # add_song_menu.add_command(label="Quit Music Player", command=root.quit)

    # Create Delete Song Menu Dropdowns
    # remove_song_menu = Menu(my_menu, tearoff=0)
    # my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
    # remove_song_menu.add_command(label="Delete a Song From Playlist", command=delete_song)
    # remove_song_menu.add_command(label="Delete all Songs From Playlist", command=delete_all_songs)

    # Create Status bar
    status_bar = Label(main_frame, text='xxxxx', bd=1, relief=GROOVE, anchor=E)
    # Fill along x axis, and place at the bottom, internal pad of 2
    status_bar.grid(row=20, column=0)

    # We've Created the gui, now put the songs in the file list into the listbox

    for song in playlist:
        # print (song.filename)
        # print (song.artist, song.title)
        playlist_box.insert(END, song.artist + " - " + song.title)

    playlist_box.select_set(0)
    playlist_box.activate(0)
    # input("Should be activated")
    playlist_box.see(0)
    play()

    # Temporary Label
    my_label = Label(root, text="")
    my_label.pack(pady=20)
    root.mainloop()

# OK, going to call the ogg_player function with a filelist that it can then play. 
# First let's read the ogg files in and put them in our list of objects.

def play_all():
    # in each of these functions all we're going to do is update the playlist, close the pick_songs_window
    # and then call a play the playlist function.
    global final_playlist
    final_playlist = ogg_file_list
    pick_songs.destroy()
    ogg_player(final_playlist)

def genre_selected():
    global final_playlist, pick_genre
    genre_to_play = genres[genrelist_box.curselection()[0]]
    # print(f"Genre: {genre_to_play}")
    # Now go through the ogg file list and copy anything with this genre to final_playlist
    for song in ogg_file_list:
        if song.genre == genre_to_play:
            final_playlist.append(song)
            # print(final_playlist[-1])
    ogg_player(final_playlist)

def play_by_genre():
    global final_playlist, genres, genrelist_box, pick_genre
    close_pick_songs_window()
    print(ogg_file_list)
    # OK first loop through the list of files and find all the genres:
    genres = []
    for song in ogg_file_list:
        print (song)
        if song.genre not in genres:
            genres.append(song.genre)
            # input (f"Added Genre: {song.genre}")
    genres.sort()
    pick_genre = Toplevel()
    pick_genre.geometry("800x480")
    pick_genre.title("Picking Genre To Play")
    genrelist_box = Listbox(pick_genre, bg="black", fg="#98fb98", width=80, height=13, font=('Times', 14), selectbackground="#98fb98", selectforeground="black")
    genrelist_box.grid(row=0, column=0)
    select_genre_button = Button(pick_genre, text="Pick a Genre", command=genre_selected).grid(row=1, column=0)
    # print(type(genrelist_box))
    # genre_count = 0
    for genre in genres:
        genrelist_box.insert(END, genre)
        
def artist_selected():
    global final_playlist
    artist_to_play = artists[artistlist_box.curselection()[0]]
    # print(f"Artist: {artist_to_play}")
    # Now go through the ogg file list and copy anything with this genre to final_playlist
    for song in ogg_file_list:
        if song.artist == artist_to_play:
            final_playlist.append(song)
            # print(final_playlist[-1])
    
    ogg_player(final_playlist)

def play_by_artist():
    global final_playlist, artists, artistlist_box, pick_artist
    # OK first loop through the list of files and find all the genres:
    close_pick_songs_window()
    artists = []
    for song in ogg_file_list:
        if song.artist not in artists:
            artists.append(song.artist)
            # input (f"Added Genre: {song.genre}")
    artists.sort()
    pick_artist = Toplevel()
    pick_artist.geometry("800x480")
    pick_artist.title("Picking Artist To Play")
    artistlist_box = Listbox(pick_artist, bg="black", fg="#98fb98", width=80, height=13, font=('Times', 14), selectbackground="#98fb98", selectforeground="black")
    artistlist_box.grid(row=0, column=0)
    select_artist_button = Button(pick_artist, text="Pick an Artist", command=artist_selected).grid(row=1, column=0)
    # print(type(artistlist_box))
    for artist in artists:
        artistlist_box.insert(END, artist)

def close_pick_songs_window():
    pick_songs.destroy()
    root.deiconify()

global final_playlist
ogg_file_list = []
final_playlist = []

root = Tk()
root.title("Better OGG Player")
root.geometry("800x480")

building_db_label = Label(root, text = "Building Initial File List")
building_db_label.pack()
num_files_label = Label(root, text = f"Processing File #  of Files.")
num_files_label.pack()

build_initial_file_list()

pick_artist = None
pick_genre = None

root.withdraw()
pick_songs = Toplevel()
pick_songs.geometry("800x480")
pick_songs.title("Picking Songs To Play")
play_all_button = Button(pick_songs, text="Play All Non Played Songs in Random Order", command=play_all).pack()
play_by_genre_button = Button(pick_songs, text="Play By Genre", command=play_by_genre).pack()
play_by_artist_button = Button(pick_songs, text="Play By Artist", command=play_by_artist).pack()
close_window_button = Button(pick_songs, text="close window", command=close_pick_songs_window).pack()


pick_songs.mainloop()

ogg_player(final_playlist)