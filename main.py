import customtkinter
import pystray
from pystray import MenuItem as item
from PIL import Image
import vlc
from yt_dlp import YoutubeDL
from threading import Thread

url = "https://www.youtube.com/watch?v=jfKfPfyJRdk"

song_info = None
customtkinter.set_appearance_mode("dark")

app = customtkinter.CTk()
app.resizable(False, False)
app.title('lofi player')
x = (app.winfo_screenwidth() - app.winfo_reqwidth()) // 2 - (400 // 4)
y = (app.winfo_screenheight() - app.winfo_reqheight()) // 2 - (240 // 4)
app.wm_geometry(f"+{x}+{y}")
app.geometry("400x240")

def play():
    global song_info, media_player
    if song_info == None:
        label.configure(text="connecting...")
        label.update()
        with YoutubeDL({'format': 'bestaudio'}) as ydl:
            song_info = ydl.extract_info(url, download=False)
        
        media_player = vlc.MediaPlayer()
        media = vlc.Media(song_info['url'])
        media_player.set_media(media)
    
    media_player.play()
    label.configure(text="playing...")

def on_play():
    t = Thread(target=play, daemon=True)
    t.start()

def stop():
    media_player.stop()
    label.configure(text="none")

app.grid_columnconfigure(0, weight=1)
button1 = customtkinter.CTkButton(app, text="play", width=200, command=on_play)
button1.grid(row=0, column=0, pady=20)
button2 = customtkinter.CTkButton(app, text="stop", width=200, command=stop)
button2.grid(row=2, column=0)
label = customtkinter.CTkLabel(app, text="none")
label.grid(row=3, column=0, pady=20)

def quit_window(icon):
    icon.stop()
    app.destroy()

def show_window(icon):
    icon.stop()
    app.after(0,app.deiconify)

def withdraw_window():  
    app.withdraw()
    image = Image.open('img\logo.ico')
    menu = (item('Выйти', quit_window), item('Развернуть', show_window))
    icon = pystray.Icon("player", image, "lofi player", menu)
    icon.run()

app.protocol('WM_DELETE_WINDOW', withdraw_window)
app.mainloop()