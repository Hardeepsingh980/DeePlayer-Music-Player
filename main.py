## Importing all the neccesary modules.
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox as mb
import os
from PIL import ImageTk, Image
from pygame import mixer
from tkinter import ttk
from ttkthemes import themed_tk as tk
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
import threading
import time
import random
import _thread




mixer.init()

playing = False
paused = False
mute = False
cur_playing = ''
con_style = 'rep_one'
to_break = False
current_time = 0


## Main Class 
class Main_class():

    songs = []
    play_thread = None

    def about(self):
        mb.showinfo('About','This is an exclusive distribution of DeePlayer.\n Creator of this apllication is Hardeep Singh.\nThis was completed on 23/6/2019.\n Thanks For Using The Application.')


    def start_count(self,t):        
        # mixer.music.get_busy(): - Returns FALSE when we press the stop button (music stop playing)
        # Continue - Ignores all of the statements below it. We check if music is paused or not.
        global current_time
        while current_time <= t and mixer.music.get_busy():
            global paused
            global dur_start
            global progress_bar
            global total_length
            global con_style
            global to_break

            if paused:
                continue
            elif to_break:
                break
            else:                
                mins, secs = divmod(current_time, 60)
                mins = round(mins)
                secs = round(secs)
                timeformat = '{:02d}:{:02d}'.format(mins, secs)
                dur_start['text'] = timeformat
                time.sleep(1)
                current_time += 1
                progress_bar['value'] = current_time
                progress_bar.update()
        if to_break:
            to_break = False
            current_time=0
            return None
        else:         
            try:
                self.con_func(con_style)            
            except:
                pass
                
                



    def show_details(self,play_song):
        global dur_end
        global progress_bar
        global total_length
        # global th
        file_data = os.path.splitext(play_song)

        if file_data[1] == '.mp3':
            audio = MP3(play_song)
            total_length = audio.info.length

            # try:    
            with open('temp.jpg', 'wb') as img:
                a = ID3(play_song)
                img.write(a.getall('APIC')[0].data)
                image = self.makeAlbumArtImage('temp.jpg')
                self.album_art_label.configure(image=image)
                self.album_art_label.image = image
            # except:
            #     pass

        else:
            a = mixer.Sound(play_song)
            total_length = a.get_length()

        progress_bar['maximum'] = total_length
        # div - total_length/60, mod - total_length % 60
        mins, secs = divmod(total_length, 60)
        mins = round(mins)
        secs = round(secs)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        dur_end['text'] = timeformat


        self.play_thread = _thread.start_new_thread(self.start_count,(total_length,))

        #t1 = threading.Thread(target=self.start_count, args=(total_length,))
        #t1.start()


    ## Add songs to the playlist.
    def set_playlist(self):
        music_ex = ['mp3','wav','mpeg','m4a','wma','ogg']
        dir_ =  filedialog.askdirectory(initialdir='D:\\',title='Select Directory')
        os.chdir(dir_)
        status_bar['text'] = 'Playlist Updated.'
        dir_files = os.listdir(dir_)
        self.songs = []
        for file in dir_files:
            exten = file.split('.')[-1]
            for ex in music_ex:
                if exten == ex:
                    play_list.insert(END,file)
                    self.songs.append(file)


    def con_func(self,con):
        global cur_playing
        global current_time
        current_time=0
        if con == 'rand':
            try:
                in_ = random.randint(0,len(self.songs))
                next_play = self.songs[in_]
                self.play_next(next_play)
            except:
                self.play_music()
        elif con == 'rep_all':
            try:
                in_ = self.songs.index(cur_playing)
                next_play = self.songs[in_+1]
                self.play_next(next_play)
            except:
                self.play_music()
        else:
            self.play_next(cur_playing)
                    


    def play_next(self,song):
        global playing
        global cur_playing
        global file
        file = song
        cur_playing = file
        mixer.music.load(file)
        mixer.music.play()
        status_bar['text'] = 'Playing - '+file
        play_button['image'] = pause_img
        playing = True
        self.show_details(file)


    def playSongInitial(self, *args):
        self.stop()
        self.play_music()
                

    def play_music(self):
        global playing
        global cur_playing
        try:
            if playing == False:
                global file
                file = play_list.get(ACTIVE)
                cur_playing = file
                mixer.music.load(file)
                mixer.music.play()
                status_bar['text'] = 'Playing - '+file
                play_button['image'] = pause_img
                playing = True
                self.show_details(file)
            else:
                global paused
                if paused == True:
                    mixer.music.unpause()
                    paused = False
                    status_bar['text'] = 'Playing - '+file
                    play_button['image'] = pause_img
                else:
                    mixer.music.pause()
                    paused = True
                    play_button['image'] = play_img
                    status_bar['text'] = 'Music Paused'
        except:
                mb.showerror('error','No file found to play.')
                



    def stop(self):
        mixer.music.stop()
        global playing
        global paused
        global dur_start
        global progress_bar
        global cur_playing
        global current_time
        global to_break
        to_break = True
        current_time=0
        cur_playing = ''
        playing = False
        paused = False
        dur_start['text'] = '--:--'
        dur_end['text'] = '--:--'
        progress_bar['value'] = 0.0
        progress_bar.update()

        self.album_art_label.configure(image=None)
        self.album_art_label.image = None

        
        play_button['image'] = play_img
        status_bar['text'] = 'Music Stopped'
        to_break = False

        return None
        
        



    def next_prev(self,num):
        global file
        global playing
        global to_break
        global dur_start
        to_break = True
        dur_start['text'] = '00:00'
        try:
            if num == 1:
                index = self.songs.index(file) - 1
                file = self.songs[index]
                mixer.music.load(file)
                mixer.music.play()
                status_bar['text'] = 'Playing - '+file
                play_button['image'] = pause_img
                playing = True
                self.show_details(file)
            else:
                index = self.songs.index(file) + 1
                file = self.songs[index]
                mixer.music.load(file)
                mixer.music.play()
                status_bar['text'] = 'Playing - '+file
                play_button['image'] = pause_img
                playing = True
                self.show_details(file)
        except IndexError:
            self.play_music()
        except ValueError:
            global paused
            playing = False
            paused = False
            self.play_music()




    def open_file(self):
        dir_ = filedialog.askopenfilename(initialdir='D:/',title='Select File')
        cng_dir = dir_.split('/')[0:-1]
        cng_dir = ''.join(cng_dir)
        os.chdir(cng_dir)
        self.songs.append(dir_)
        filename = os.path.basename(dir_)
        play_list.insert(END,filename)
        global playing
        playing = False


    def set_con(self,num):
        global con_style
        if num == 1:
            con_style = 'rand'
        elif num == 2:
            con_style = 'rep_all'
        else:
            con_style = 'rep_one'



    def speaker_func(self):
        global mute
        global status_bar
        if mute == False:
            speaker['image'] = mute_img
            mixer.music.set_volume(0.0)
            mute = True            
        else:
            speaker['image'] = speaker_img
            num = scale.get()
            mixer.music.set_volume(float(num) /100)
            mute = False




    def set_vol(self,num):
        global mute
        global status_bar
        if num == float(0):
            speaker['image'] = mute_img
            mixer.music.set_volume(0.0)
            mute = True
        elif mute == True:
            speaker['image'] = speaker_img
            num = scale.get()
            mixer.music.set_volume(float(num) /100)
            mute = False
        else:
            volume = float(num) / 100
            mixer.music.set_volume(volume)




    def exit(self):
        self.stop()
        win.destroy()
        sys.exit()


    def coming_soon(self):
        mb.showinfo('Coming Soon','The Feature You Clicked Will Be Coming Soon.\n Please Wait For An Update. Stay Tuned')


    def makeAlbumArtImage(self, image_path):
        image = Image.open(image_path)
        image = image.resize((350, 350), Image.ANTIALIAS)
        return ImageTk.PhotoImage(image)


    


    ## Constructer Method -  Main method For GUI.
    def __init__(self):
        

        ## Making Tkinter Window.
        global win
        win = Tk()
        win.geometry('800x520')
        win.resizable(0,0)
        win.title('DeePlayer')
        win.wm_attributes('-alpha',0.95)
        win.iconbitmap('icon.ico')


        ## Menu bar - all the menu_cascades and menu_commands.
        main_menu = Menu(win,tearoff=0)
        win.configure(menu=main_menu)
        
        file = Menu(main_menu,tearoff=0)
        main_menu.add_cascade(label='Media',menu=file)
        
        file.add_command(label='Open',command=self.open_file)
        file.add_command(label='Open Folder',command=self.set_playlist)
        file.add_command(label='Save Playlist',command=self.coming_soon)
        file.add_command(label='Open Muliple Files',command=self.coming_soon)
        file.add_command(label='Open Disk',command=self.coming_soon)
        file.add_command(label='Open Network Stream',command=self.coming_soon)
        file.add_separator()
        file.add_command(label='Open Recent Media',command=self.coming_soon)
        file.add_command(label='Add Inteface',command=self.coming_soon)
        file.add_command(label='Fullscreen',command=self.coming_soon)
        file.add_separator()
        file.add_command(label='Exit',command=self.exit)

        about = Menu(main_menu,tearoff=0)
        main_menu.add_cascade(label='About',menu=about)

        about.add_command(label='About Us',command=self.about)


        #Album Art Part
        # album_art_photo = self.makeAlbumArtImage('temp.jpg')
        self.album_art_label = Label(win)
        self.album_art_label.place(x=85, y=20)


        #Playlist Frame
        Label(win,text='', bg='White',height=19,width=35,relief_='ridge').place(x=543,y=0)
        
        Button(win, text='Add a Folder.',bd=2,font=('arialblack',13),width=25,command=self.set_playlist).place(x=552,y=10)

        global play_list
        play_list = Listbox(win,height=21,width=41)
        play_list.place(x=544,y=50)
        play_list.bind('<Double-Button>', self.playSongInitial)



        ## Bottom Control Center
        Label(win, text='',height=5,relief_='groove',width=200).place(x=0,y=395)

        global play_img 
        play_img = PhotoImage(file='resources/play.png')

        def on_enter_play(event):
            play_des.place(x=25,y=460)

        def on_leave_play(event):
            play_des.place(x=1000,y=1000)

        global play_button
        play_button = Button(win, image=play_img,bd=0,command=self.play_music)
        play_button.place(x=10,y=440)        
        play_button.bind('<Enter>',on_enter_play)
        play_button.bind('<Leave>',on_leave_play)


        def on_enter_prev(event):
            prev_des.place(x=45,y=460)

        def on_leave_prev(event):
            prev_des.place(x=1000,y=1000)
        

        prev_img = PhotoImage(file='resources/prev.png')
        prev_button = Button(win, image=prev_img,bd=0,command=lambda:self.next_prev(1))
        prev_button.place(x=50,y=433)
        prev_button.bind('<Enter>',on_enter_prev)
        prev_button.bind('<Leave>',on_leave_prev)



        def on_enter_stop(event):
            stop_des.place(x=70,y=460)

        def on_leave_stop(event):
            stop_des.place(x=1000,y=1000)

        stop_img = PhotoImage(file='resources/stop.png')
        stop_button = Button(win,image=stop_img,bd=0,command=self.stop)
        stop_button.place(x=85,y=438)
        stop_button.bind('<Enter>',on_enter_stop)
        stop_button.bind('<Leave>',on_leave_stop)


        def on_enter_next(event):
            next_des.place(x=100,y=460)

        def on_leave_next(event):
            next_des.place(x=1000,y=1000)

        next_img = PhotoImage(file='resources/next.png')
        next_button = Button(win, image=next_img,bd=0,command=lambda:self.next_prev(2))
        next_button.place(x=113,y=433)
        next_button.bind('<Enter>',on_enter_next)
        next_button.bind('<Leave>',on_leave_next)

        global pause_img
        pause_img = PhotoImage(file='resources/pause.png')


        global speaker_img
        speaker_img = PhotoImage(file='resources/vol.png')

        global mute_img
        mute_img = PhotoImage(file='resources/mute.png')


        def on_enter_vol(event):
            vol_des.place(x=560,y=450)

        def on_leave_vol(event):
            vol_des.place(x=1000,y=1000)

        global speaker
        speaker = Button(win,image=speaker_img,bd=0,command=self.speaker_func)
        speaker.place(x=650,y=442)
        speaker.bind('<Enter>',on_enter_vol)
        speaker.bind('<Leave>',on_leave_vol)


        def on_enter_shuffle(event):
            shuffle_des.place(x=180,y=460)

        def on_leave_shuffle(event):
            shuffle_des.place(x=1000,y=1000)

        shuffle_img = PhotoImage(file='resources/shuffle.png')
        shuffle_button = Button(win, image=shuffle_img,bd=0,command=lambda:self.set_con(1))
        shuffle_button.place(x=170,y=440)
        shuffle_button.bind('<Enter>',on_enter_shuffle)
        shuffle_button.bind('<Leave>',on_leave_shuffle)


        def on_enter_rep_all(event):
            rep_all_des.place(x=220,y=460)

        def on_leave_rep_all(event):
            rep_all_des.place(x=1000,y=1000)

        

        repeat_img = PhotoImage(file='resources/repeat.png')
        repeat_button = Button(win, image=repeat_img,bd=0,command=lambda:self.set_con(2))
        repeat_button.place(x=200,y=440)
        repeat_button.bind('<Enter>',on_enter_rep_all)
        repeat_button.bind('<Leave>',on_leave_rep_all)


        def on_enter_rep_one(event):
            rep_one_des.place(x=250,y=460)

        def on_leave_rep_one(event):
            rep_one_des.place(x=1000,y=1000)

        rep_one_img = PhotoImage(file='resources/rep_one.png')
        rep_one_button = Button(win, image=rep_one_img,bd=0,command=lambda:self.set_con(3))
        rep_one_button.place(x=230,y=437)
        rep_one_button.bind('<Enter>',on_enter_rep_one)
        rep_one_button.bind('<Leave>',on_leave_rep_one)




        play_des = Label(win, text='Play/Pause',relief='groove')
        prev_des = Label(win, text='Previous Track',relief='groove')
        stop_des = Label(win, text='Stop Music',relief='groove')
        next_des = Label(win, text='Next Track',relief='groove')
        shuffle_des = Label(win, text='Shuffle All',relief='groove')
        rep_all_des = Label(win, text='Repeat All',relief='groove')
        rep_one_des = Label(win, text='Repeat One',relief='groove')
        vol_des = Label(win, text='Adjust Volume',relief='groove')

        


        ## Volume Scale - adjust volume
        global scale
        scale = ttk.Scale(win, from_=0, to=100, orient=HORIZONTAL,command=self.set_vol)
        scale.set(70)  # implement the default value of scale when music player starts
        mixer.music.set_volume(0.7)
        scale.place(x=680,y=440)


        ## Time Durations
        global dur_start, dur_end
        dur_start = Label(win, text='--:--',font=('Calibri',10,'bold'))
        dur_start.place(x=5,y=400)
        dur_end = Label(win, text='--:--',font=('Calibri',10,'bold'))
        dur_end.place(x=750,y=400)



        ## Progress Bar - The progress bar which indicates the running music
        global progress_bar
        progress_bar = ttk.Progressbar(win, orient='horizontal',length=705)
        progress_bar.place(x=42,y=400)

        

        ## Status Bar - at the bottom of window
        global status_bar
        status_bar = Label(win,text='Welcome to DeePlayer',relief_='sunken',anchor=W)
        status_bar.pack(side=BOTTOM,fill=X)

        

        win.protocol("WM_DELETE_WINDOW", self.exit)
        win.mainloop()





music_player = Main_class()
