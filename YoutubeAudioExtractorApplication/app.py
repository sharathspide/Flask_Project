import os
from flask import Flask, render_template, request, send_from_directory, redirect, url_for, flash
from pytube import YouTube
from flask_mail import Mail, Message
from authenticationdetails import password, userName, appSecret
app = Flask(__name__)
app.secret_key = appSecret

# Configuration for Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = userName
app.config['MAIL_PASSWORD'] = password
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = userName

mail = Mail(app)

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
        audioFileName = "".join(["Audio", ".mp3"])
        audio_stream.download(output_path=DOWNLOAD_AUDIO_FOLDER, filename=audioFileName)
        audio_file_path = os.path.join(DOWNLOAD_AUDIO_FOLDER, audioFileName)
        delete_file(video_file_path)
        return render_template('result.html', audio_file=os.path.basename(audio_file_path))
    
    except FileNotFoundError:
        return str(f"File '{videoFileName} or {audioFileName}' not found.")
    
    except Exception as e:
        return str(e)
    

@app.route('/downloads/<filename>')
def download_file(filename):
    try: 
        return send_from_directory('..\YoutubeAudioExtractorApplication\AUDIO', filename, as_attachment=True)
    except Exception as e:
        return str(e)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        # Here you can add code to save the data to a database or send an email
        try:
            msg = Message("Contact Form Submission",recipients=[email])
            msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
            mail.send(msg)
            flash('Your message has been sent successfully!', 'success')
        except Exception as e:
            flash(f'An error occurred while sending your message: {str(e)}', 'danger')
        
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
