import os
from flask import Flask, render_template, request, send_from_directory, redirect, url_for, flash
from pytube import YouTube
from moviepy.editor import VideoFileClip

app = Flask(__name__)
app.secret_key = 'spide4evr'  # Replace with your own secret key

DOWNLOAD_VIDEO_FOLDER = 'YoutubeAudioExtractorApplication/VIDEO'
DOWNLOAD_AUDIO_FOLDER = 'YoutubeAudioExtractorApplication/AUDIO'
if not os.path.exists(DOWNLOAD_VIDEO_FOLDER):
    os.makedirs(DOWNLOAD_VIDEO_FOLDER)
if not os.path.exists(DOWNLOAD_AUDIO_FOLDER):
    os.makedirs(DOWNLOAD_AUDIO_FOLDER)

def delete_file(file_path):
    try:
        os.remove(file_path)
        flash(f"File '{file_path}' has been deleted successfully.", 'success')
        print(f"File '{file_path}' has been deleted successfully.")
    except FileNotFoundError:
        flash(f"File '{file_path}' was not found.", 'Not Found')
        print(f"File '{file_path}' not found.")
    except PermissionError:
        flash(f"File '{file_path}' has no permission.", 'Failed')
        print(f"Permission denied to delete '{file_path}'.")
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'danger')
        print(f"Error occurred while deleting file '{file_path}': {e}")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download_audio', methods=['POST'])
def download_audio():
    url = request.form['url']
    try:
        yt = YouTube(url)
        video_stream = yt.streams.filter(only_audio=True).first()
        videoFileName = video_stream.default_filename
        video_file_path = os.path.join(DOWNLOAD_VIDEO_FOLDER, videoFileName)
        video_stream.download(output_path=DOWNLOAD_VIDEO_FOLDER)

        audio_stream = yt.streams.filter(only_audio=True).first()
        #audio_file_path = os.path.join(DOWNLOAD_AUDIO_FOLDER, "Audio" + '.mp3')
        audioFileName = "".join(["Audio", ".mp3"])
        audio_stream.download(output_path=DOWNLOAD_AUDIO_FOLDER, filename=audioFileName)
        audio_file_path = os.path.join(DOWNLOAD_AUDIO_FOLDER, audioFileName)
        #video_clip = VideoFileClip(video_file_path)
        #video_clip.audio.write_audiofile(audio_file_path)
        #print(video_file_path)
        # Removing the downloaded video file after extracting audio
        #os.path.join(video_file_path).remove(videoFileName)
        delete_file(video_file_path)
        return render_template('result.html', audio_file=os.path.basename(audio_file_path))
    except FileNotFoundError:
        return str(f"File '{videoFileName} or {audioFileName}' not found.")
    except Exception as e:
        return str(e)
@app.route('/downloads/<filename>')
def download_file(filename):
    #return send_from_directory(os.path.join(DOWNLOAD_AUDIO_FOLDER), filename)
    try:
        return send_from_directory('E:\Flask_Project\Flask_Project\YoutubeAudioExtractorApplication\AUDIO', filename, as_attachment=True)
        #return render_template('index.html')
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
