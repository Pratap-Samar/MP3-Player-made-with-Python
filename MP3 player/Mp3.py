from tkinter import *
from pygame import mixer, time
from tkinter import filedialog
from tkinter import ttk


root = Tk()
root.title("MP3 Player")
root.geometry("600x400")


mixer.init()

#Function to add song
def add_song():
    songs= filedialog.askopenfilenames(initialdir="songs/",title="select the song", filetypes=(("mp3 Files","*.mp3"),))
    for song in songs:
        song_list.insert(END, song)

#delete one song
def delete_song():
    song_list.delete(ANCHOR)
    mixer.music.stop()

#delete all song
def delete_all():
    song_list.delete(0,END)
    mixer.music.stop()

def volume(x):
    mixer.music.set_volume(volume_slider.get())


#Global variable for Pause and Stop
global paused
global stopped
paused = False
stopped = False


#function to play song
def play():
    global stopped
    stopped = False
    song= song_list.get(ACTIVE)
    mixer.music.load(song)
    mixer.music.play(loops=0)
    check_music()

#to automatically move to next song
def check_music():
    if not mixer.music.get_busy() and not stopped:
        next_song()
    # check again after 1000ms
    root.after(1000, check_music)

#function to stop song
def stop():
    global stopped
    stopped = True
    song= song_list.get(ACTIVE)
    mixer.music.load(song)
    mixer.music.stop()

#function for next song
def next_song():
    next_one= song_list.curselection()
    next_one=next_one[0]+1
    song=  song_list.get(next_one)
    mixer.music.load(song)
    mixer.music.play(loops=0)

    #move active selection 
    song_list.select_clear(0, END)
    song_list.activate(next_one)
    song_list.selection_set(next_one,last=None)

#function for previous song

def previous_song():
    next_one= song_list.curselection()
    next_one=next_one[0]-1
    song=  song_list.get(next_one)
    mixer.music.load(song)
    mixer.music.play(loops=0)

    #move active selection 
    song_list.select_clear(0, END)
    song_list.activate(next_one)
    song_list.selection_set(next_one,last=None)


#Pause function
def pause(is_paused):
    global paused
    paused= is_paused

    if paused:
        mixer.music.unpause()
        paused= False
    else:
        mixer.music.pause()
        paused= True


#main Frame
main_frame= Frame(root)
main_frame.pack(pady=20)

song_list = Listbox(main_frame,bg='black',fg='white',width=90, selectbackground="green",selectforeground="black")
song_list.grid(row=0,column=0)

#volume frame
volume_frame= LabelFrame(main_frame, text="Volume")
volume_frame.grid(row=2,column=0)

#volume slider
volume_slider=ttk.Scale(volume_frame,from_= 0, to=1, orient=HORIZONTAL,value=0.5,command=volume, length=300)
volume_slider.pack(pady=10)

#MP3 button images
play_img= PhotoImage(file='images/play.png')
stop_img= PhotoImage(file='images/stop.png')
previous_img= PhotoImage(file='images/prev.png')
next_img= PhotoImage(file='images/next.png')

control= Frame(main_frame)
control.grid(row=1,column=0,pady=20)

#MP3 control buttons
play_button= Button(control, image=play_img, borderwidth=0, command=play)
stop_button= Button(control, image=stop_img, borderwidth=0, command=stop)
previous_button= Button(control, image=previous_img, borderwidth=0, command=previous_song)
next_button= Button(control, image=next_img, borderwidth=0, command= next_song)

play_button.grid(row=0, column=2, padx=10)
stop_button.grid(row=0, column=3, padx=10)
previous_button.grid(row=0, column=1, padx=10)
next_button.grid(row=0, column=5, padx=10)

#Menu for song
song_menu= Menu(root)
root.config(menu=song_menu)

#add songs
add_song_menu=Menu(song_menu)
song_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add songs to playlist", command=add_song)

#delete songs
remove_song_menu= Menu(song_menu)
song_menu.add_cascade(label="Remove Songs",menu=remove_song_menu)
remove_song_menu.add_command(label="Delete the selected song", command= delete_song)
remove_song_menu.add_command(label="Delete all songs from Playlist", command= delete_all)


root.mainloop()
