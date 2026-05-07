# Multi Object Tracking with YOLOv5

Real-time object detection and tracking using YOLOv5 and Streamlit.

## 🎯 Features

- **Real-time Detection**: YOLOv5 for object detection
- **Multi-object Tracking**: Unique ID assignment with centroid tracking
- **Live Processing Preview**: Watch tracked frames as the video processes
- **Detected Object Counts**: Summary of unique objects by class
- **Download Results**: Save processed videos with annotations
- **Web-based**: Runs in the browser with Streamlit

## 🚀 Quick Start

### Live Demo

Try the live application: [Multi Object Tracking App](https://KashyapFadadu-multi-object-tracking.streamlit.app)

### Local Installation

```bash
# Clone the repository
git clone https://github.com/KashyapFadadu/Multi-Object-Tracking.git
cd Multi-Object-Tracking

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## 📖 How to Use

1. **Upload Video**: Click the file uploader in the sidebar and select a video (MP4, AVI, MOV, MKV)
2. **Configure Parameters**:
   - Adjust confidence threshold (0.0-1.0)
   - Set max disappeared frames for tracking
3. **Process**: Click "Process Video" button
4. **View Results**: Watch the live tracking preview and object counts
5. **Download**: Download the processed video with bounding boxes and tracking IDs

## 🏗️ Technology Stack

- **YOLOv5**: Object detection model
- **OpenCV**: Video processing and annotations
- **PyTorch**: Deep learning backend
- **Streamlit**: Web application framework
- **NumPy**: Numerical computing

## 📊 Project Structure

```
Multi-Object-Tracking/
├── app.py                      # Main Streamlit application
├── centroid_tracker.py         # Tracking algorithm
├── requirements.txt            # Dependencies
├── .streamlit/config.toml      # Streamlit configuration
├── README.md                   # This file
├── .gitignore                  # Files to ignore in Git
└── yolov5s.pt                  # YOLOv5 weights file
```

## 🔧 Configuration

Edit `.streamlit/config.toml` to customize:

- Theme colors
- Maximum upload size
- Server settings

## 📈 Performance Notes

- If `yolov5s.pt` is not present locally, YOLOv5 may download weights on first run
- Processing time depends on:
  - Video length
  - Video resolution
  - Server resources
- Free tier on Streamlit Cloud: shorter videos perform better

## 🐛 Troubleshooting

**Video Upload Fails**: Compress video or try shorter clips
**Out of Memory**: Use lower resolution videos
**Slow Processing**: Streamlit Cloud free tier has limited CPU
**Model Download Error**: Check internet connection

## 📚 References

- [YOLOv5 Documentation](https://github.com/ultralytics/yolov5)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [OpenCV Documentation](https://docs.opencv.org/)

## 🤝 Contributing

Feel free to fork this repository and submit pull requests!

---

**Live App**: [https://KashyapFadadu-multi-object-tracking.streamlit.app](https://KashyapFadadu-multi-object-tracking.streamlit.app)

**GitHub**: [https://github.com/KashyapFadadu/Multi-Object-Tracking](https://github.com/KashyapFadadu/Multi-Object-Tracking)
