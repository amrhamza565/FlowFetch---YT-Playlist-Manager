import customtkinter as ctk
from tkinter import filedialog
import threading
import yt_dlp


ctk.set_appearance_mode("dark")


app = ctk.CTk()
app.title("YT Playlist Manager")
app.geometry("500x420")
app.resizable(False, False)


folder = ""


def choose_folder():
    global folder
    folder = filedialog.askdirectory()
    folder_label.configure(text=folder)


def download():

    url = url_entry.get()
    quality = quality_menu.get()

    def worker():

        options = {
            "format": f"bestvideo[height<={quality[:-1]}]+bestaudio/best",
            "merge_output_format": "mp4",
            "outtmpl": f"{folder}/%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s",
            "noplaylist": False,
            "ignoreerrors": True
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])

        status.configure(text="Finished")


    status.configure(text="Downloading...")

    threading.Thread(
        target=worker,
        daemon=True
    ).start()



title = ctk.CTkLabel(
    app,
    text="YT Playlist Manager",
    font=("Arial",20)
)
title.pack(pady=15)


url_entry = ctk.CTkEntry(
    app,
    width=400,
    placeholder_text="Paste YouTube URL"
)
url_entry.pack(pady=15)


quality_menu = ctk.CTkOptionMenu(
    app,
    values=["1080p","720p","480p"]
)

quality_menu.set("1080p")
quality_menu.pack(pady=10)


folder_btn = ctk.CTkButton(
    app,
    text="Choose Folder",
    command=choose_folder
)

folder_btn.pack(pady=10)


folder_label = ctk.CTkLabel(
    app,
    text="No folder selected"
)

folder_label.pack()


start_btn = ctk.CTkButton(
    app,
    text="Start Download",
    command=download
)

start_btn.pack(pady=20)


status = ctk.CTkLabel(
    app,
    text="Ready"
)

status.pack()


app.mainloop()
