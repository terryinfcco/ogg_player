# Python program to play ogg files. Select them by genre, artist, or everything
# that hasn't been played before.

# Do the imports we need.
import glob
import sys
import vlc
import time
import random

ogg_file_list = []

# def build_initial_file_list():

folder = '/home/terry/Dropbox/MusicAllOgg'
files = glob.glob(folder+"/**/*.ogg", recursive=True)
if len(files) == 0:
    print ("No ogg files in directory.", folder,"..exiting")
    sys.exit(1)
print(f"Found {len(files)} ogg files.")

# At this point I've got the songs all in the list called files.
# Ask if we're playing everything, a particular genre, or a particular genre

print("Make a selection: ")
print("1. Play all songs randomly")
print("2. Play songs of a particular genre randomly")
print("3. Play songs of a particular artist randomly")

play_type = input("Enter the number of your selection: ")

if play_type == "1":
    # At this point we're playing everything.
    final_playlist = files[:]



# At this point we've created the final_playlist and can just play it.
# set up vlc

random.shuffle(final_playlist)
player = vlc.MediaPlayer()
medialist = vlc.MediaList(final_playlist)
mlplayer = vlc.MediaListPlayer()
mlplayer.set_media_player(player)
mlplayer.set_media_list(medialist)

# print(files[0])
print(final_playlist[0])
mlplayer.play()
time.sleep(10)
