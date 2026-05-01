# MyTube - YouTube Clone

A simple video platform where you can upload your own videos or download videos from YouTube.

## Features

- 📹 **Upload Videos**: Upload your own video files (up to 500MB)
- 🎬 **Download from YouTube**: Paste a YouTube URL to download and save videos locally
- 🗑️ **Delete Videos**: Remove videos you no longer want
- 📱 **Responsive Design**: Works on desktop and mobile devices
- 💾 **SQLite Database**: Stores video metadata
- 🎨 **Modern UI**: Beautiful gradient design with smooth animations

## Installation

1. Navigate to the project directory:
```bash
cd youtube_clone
```

2. Activate the virtual environment:
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and go to:
```
http://localhost:5000
```

## Usage

### Uploading Your Own Video
1. Click "📹 Upload Video" button
2. Select "Upload Your Video" option
3. Choose a video file from your computer
4. Optionally add a title and description
5. Click "⬆️ Upload Video"

### Downloading from YouTube
1. Click "📹 Upload Video" button
2. Select "Download from YouTube" option
3. Paste the YouTube URL
4. Optionally customize the title and description
5. Click "📥 Download from YouTube"

### Watching Videos
- Click on any video card from the homepage
- Or click "Watch Video →" on any video

### Deleting Videos
- While watching a video, click the "🗑️ Delete Video" button
- Confirm the deletion

## Project Structure

```
youtube_clone/
├── app.py              # Main Flask application
├── videos.db           # SQLite database (created automatically)
├── static/
│   └── uploads/        # Uploaded video files and thumbnails
├── templates/
│   ├── index.html      # Homepage with video grid
│   ├── upload.html     # Upload/download form
│   └── watch.html      # Video player page
├── venv/               # Python virtual environment
└── README.md           # This file
```

## Technologies Used

- **Flask**: Web framework
- **SQLAlchemy**: Database ORM
- **yt-dlp**: YouTube video downloader
- **SQLite**: Database
- **HTML/CSS/JavaScript**: Frontend

## Notes

- Videos downloaded from YouTube are for personal use only
- Respect copyright and YouTube's Terms of Service
- Large video files may take time to upload/download
- The default secret key should be changed for production use

## License

This project is for educational purposes only.
