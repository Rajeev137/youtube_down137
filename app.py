from flask import Flask, render_template,request
import os
from pytube import YouTube
from moviepy.editor import *
import shutil
from rich.console import Console


app = Flask(__name__)
app.static_folder = 'static'
@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/results", methods = ['POST', "GET"])
def result():

    output = request.form.to_dict()
    
    global Song_url
    Song_url = output["Song_url"]
    main()
    return render_template("endpage.html")
    
    


def main():
        audio = download_vid(Song_url)
        if audio:
            os.replace(audio, f"../music/{os.path.basename(audio)}")
            console.print(
                    "[blue]______________________________________________________________________"
                )
        shutil.rmtree(f"../music/temp")
        os.chdir(f"../music")
        print(f"Download Location: {os.getcwd()}")       


def download_vid(yt_link):
    yt = YouTube(yt_link)
    yt.title = "".join([c for c in yt.title if c not in ['/', '\\', '|', '?', '*', ':', '>', '<', '"']])

    #download the music
    video = yt.streams.filter(only_audio=True).first()
    vid_file = video.download(output_path="../music/temp")
    
    #convert video to mp3
    base = os.path.splitext(vid_file)[0]
    audio_file = base + ".mp3"
    mp4_no_frame = AudioFileClip(vid_file)
    mp4_no_frame.write_audiofile(audio_file, logger = None)
    mp4_no_frame.close()
    os.remove(vid_file)
    os.replace(audio_file, f"../music/temp/{yt.title}.mp3")
    audio_file = f"../music/temp/{yt.title}.mp3"

    return audio_file

if __name__ == '__main__':
    console = Console()
    app.run(debug = True, port = 5001)