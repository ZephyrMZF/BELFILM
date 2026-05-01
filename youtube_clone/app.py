from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import yt_dlp
import os
import uuid

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max upload

# Database setup
engine = create_engine('sqlite:///videos.db', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Video(Base):
    __tablename__ = 'videos'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    video_path = Column(String(500))  # Path to local file or YouTube URL
    thumbnail = Column(String(500))
    source_type = Column(String(20))  # 'youtube' or 'upload'
    youtube_url = Column(String(500))  # Original YouTube URL if downloaded
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(engine)

def download_youtube_video(url):
    """Download video from YouTube"""
    output_dir = app.config['UPLOAD_FOLDER']
    unique_id = str(uuid.uuid4())[:8]
    
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': os.path.join(output_dir, f'{unique_id}.%(ext)s'),
        'writesubtitles': False,
        'writethumbnail': True,
        'thumbnail_format': 'jpg',
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        video_file = ydl.prepare_filename(info)
        thumbnail_file = os.path.splitext(video_file)[0] + '.jpg'
        
        # Rename to mp4 if needed
        if not video_file.endswith('.mp4'):
            new_video_file = os.path.splitext(video_file)[0] + '.mp4'
            if os.path.exists(video_file):
                os.rename(video_file, new_video_file)
                video_file = new_video_file
        
        return {
            'video_path': os.path.basename(video_file),
            'thumbnail': os.path.basename(thumbnail_file) if os.path.exists(thumbnail_file) else None,
            'title': info.get('title', 'Unknown Title'),
            'description': info.get('description', '')
        }

@app.route('/')
def index():
    session = Session()
    videos = session.query(Video).order_by(Video.created_at.desc()).all()
    session.close()
    return render_template('index.html', videos=videos)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        source_type = request.form.get('source_type')
        title = request.form.get('title')
        description = request.form.get('description', '')
        
        session = Session()
        
        try:
            if source_type == 'youtube':
                youtube_url = request.form.get('youtube_url')
                if not youtube_url:
                    flash('Please provide a YouTube URL', 'error')
                    return redirect(url_for('upload'))
                
                # Download YouTube video
                result = download_youtube_video(youtube_url)
                
                video = Video(
                    title=result['title'] if not title else title,
                    description=result['description'] if not description else description,
                    video_path=result['video_path'],
                    thumbnail=result['thumbnail'],
                    source_type='youtube',
                    youtube_url=youtube_url
                )
                
            elif source_type == 'upload':
                if 'video_file' not in request.files:
                    flash('No video file selected', 'error')
                    return redirect(url_for('upload'))
                
                file = request.files['video_file']
                if file.filename == '':
                    flash('No video file selected', 'error')
                    return redirect(url_for('upload'))
                
                if file:
                    unique_id = str(uuid.uuid4())[:8]
                    ext = os.path.splitext(file.filename)[1]
                    filename = f"{unique_id}{ext}"
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    
                    video = Video(
                        title=title if title else file.filename,
                        description=description,
                        video_path=filename,
                        thumbnail=None,
                        source_type='upload'
                    )
            else:
                flash('Invalid source type', 'error')
                return redirect(url_for('upload'))
            
            session.add(video)
            session.commit()
            flash('Video added successfully!', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('upload'))
        finally:
            session.close()
    
    return render_template('upload.html')

@app.route('/watch/<int:video_id>')
def watch(video_id):
    session = Session()
    video = session.query(Video).filter_by(id=video_id).first_or_404()
    session.close()
    return render_template('watch.html', video=video)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete/<int:video_id>', methods=['POST'])
def delete(video_id):
    session = Session()
    video = session.query(Video).filter_by(id=video_id).first_or_404()
    
    try:
        # Delete file if it's an upload
        if video.source_type == 'upload' and video.video_path:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], video.video_path)
            if os.path.exists(filepath):
                os.remove(filepath)
        
        session.delete(video)
        session.commit()
        flash('Video deleted successfully!', 'success')
    except Exception as e:
        session.rollback()
        flash(f'Error deleting video: {str(e)}', 'error')
    finally:
        session.close()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
