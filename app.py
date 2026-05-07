import streamlit as st
import cv2
import numpy as np
from ultralytics import YOLO
from ultralytics.utils import ops
from centroid_tracker import CentroidTracker
import tempfile
import os

# Page configuration
st.set_page_config(
    page_title="Multi Object Tracking",
    page_icon="🎯",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .title-text {
        font-size: 3em;
        font-weight: bold;
        color: #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="title-text">🎯 Multi Object Tracking</div>',
            unsafe_allow_html=True)
st.markdown("Real-time object detection and tracking using YOLOv5")
st.markdown("---")

# Default configuration
confidence_threshold = 0.45
max_disappeared = 50

# Load model


@st.cache_resource
def load_model():
    return YOLO('yolov5s.pt')


with st.spinner("Loading YOLOv5 model..."):
    model = load_model()

# Get class names and set colors
class_names = model.names if hasattr(model, 'names') else model.model.names

colors = {
    'car': (0, 255, 0),      # Green
    'person': (128, 0, 128),  # Purple
    'truck': (0, 0, 255),     # Red
    'bicycle': (255, 165, 0),
    'bus': (0, 255, 255),
}

# Generate random colors for other classes
np.random.seed(42)
for name in class_names:
    if name not in colors:
        colors[name] = tuple(np.random.randint(0, 256, 3).tolist())

if 'processing_done' not in st.session_state:
    st.session_state.processing_done = False
    st.session_state.process_requested = False
    st.session_state.output_path = ''
    st.session_state.temp_video_path = ''
    st.session_state.object_counts = {}
    st.session_state.video_info = {}
    st.session_state.uploaded_filename = ''

# File uploader
st.sidebar.title("📤 Upload Video")
uploaded_file = st.sidebar.file_uploader(
    "Choose a video file", type=['mp4', 'avi', 'mov', 'mkv'])

if uploaded_file is not None:
    # If the user uploads a new file, reset session state and save it
    if uploaded_file.name != st.session_state.uploaded_filename or not st.session_state.temp_video_path:
        st.session_state.uploaded_filename = uploaded_file.name
        st.session_state.processing_done = False
        st.session_state.process_requested = False
        st.session_state.output_path = ''
        st.session_state.object_counts = {}
        st.session_state.video_info = {}
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
            tmp_file.write(uploaded_file.read())
            st.session_state.temp_video_path = tmp_file.name

    temp_video_path = st.session_state.temp_video_path

    st.success("✅ Video uploaded successfully!")

    # Processing button
    if st.button("🚀 Process Video", key="process_btn"):
        st.session_state.process_requested = True
        st.session_state.processing_done = False

    if st.session_state.process_requested and not st.session_state.processing_done:
        st.info(
            "Processing video... This may take a few minutes depending on video length.")

        cap = cv2.VideoCapture(temp_video_path)

        if not cap.isOpened():
            st.error("❌ Error: Could not open video file")
        else:
            # Get video properties
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            # Display video info
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("FPS", fps)
            with col2:
                st.metric("Total Frames", frame_count)
            with col3:
                st.metric("Resolution", f"{width}x{height}")

            # Create progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Initialize tracker
            tracker = CentroidTracker(maxDisappeared=max_disappeared)
            video_placeholder = st.empty()
            frame_idx = 0

            output_path = os.path.splitext(temp_video_path)[0] + "_output.mp4"
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                # Detect objects
                results = model.predict(source=frame, conf=confidence_threshold, imgsz=640, verbose=False)
                if len(results) == 0 or len(results[0].boxes) == 0:
                    detections = np.empty((0, 6))
                else:
                    boxes = results[0].boxes
                    xyxy = boxes.xyxy.cpu().numpy()
                    confs = boxes.conf.cpu().numpy().reshape(-1, 1)
                    clss = boxes.cls.cpu().numpy().reshape(-1, 1)
                    detections = np.hstack((xyxy, confs, clss))

                rects = []

                for *bbox, conf, cls in detections:
                    x1, y1, x2, y2 = map(int, bbox)
                    class_name = class_names[int(cls)]
                    rects.append((x1, y1, x2, y2, class_name))

                    # Draw bounding box
                    color = colors.get(class_name, (255, 255, 255))
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

                    # Draw label with confidence
                    label = f'{class_name} {conf:.2f}'
                    cv2.putText(frame, label, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                # Update tracker
                objects = tracker.update(rects)

                # Draw tracked objects
                for (objectID, centroid) in objects.items():
                    text = f"ID {objectID}"
                    color = (255, 0, 255)  # Magenta for tracking IDs
                    cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                    cv2.circle(frame, (centroid[0], centroid[1]), 5, color, -1)

                out.write(frame)
                frame_idx += 1
                progress = frame_idx / frame_count
                progress_bar.progress(progress)
                status_text.text(f"Processing frame {frame_idx}/{frame_count}")

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                video_placeholder.image(
                    frame_rgb,
                    caption=f"Live tracking - Frame {frame_idx}/{frame_count}",
                    width=700
                )

            cap.release()
            out.release()

            st.session_state.processing_done = True
            st.session_state.output_path = output_path
            st.session_state.object_counts = {}
            for object_class in tracker.object_classes.values():
                st.session_state.object_counts[object_class] = st.session_state.object_counts.get(object_class, 0) + 1
            st.session_state.video_info = {
                'fps': fps,
                'frame_count': frame_count,
                'resolution': f"{width}x{height}"
            }

    if st.session_state.processing_done:
        st.success("✅ Processing complete!")
        st.subheader("🎬 Processed Video Preview")
        st.markdown(
            "Live tracking frames were shown during processing. Download the final processed video below."
        )

        if st.session_state.object_counts:
            st.subheader("🧮 Detected Object Counts")
            count_table = [[name, count] for name, count in st.session_state.object_counts.items()]
            st.table(count_table)

        st.subheader("💾 Download Processed Video")
        with open(st.session_state.output_path, 'rb') as f:
            st.download_button(
                label="📥 Download Processed Video",
                data=f.read(),
                file_name="output_video.mp4",
                mime="video/mp4"
            )
        # Note: keep the output file around for download without reprocessing.

else:
    # Demo section
    st.info("👆 Upload a video file to get started!")

    st.subheader("📋 Features")
    st.markdown("""
    - 🎯 Real-time object detection using YOLOv5
    - 🔍 Multi-object tracking with unique IDs
    - 💾 Download processed video
    - ⚙️ Configurable confidence threshold and tracking parameters
    """)

    st.subheader("📝 How to Use")
    st.markdown("""
    1. **Upload Video**: Click "Choose a video file" in the sidebar
    2. **Configure**: Adjust confidence threshold and tracking parameters
    3. **Process**: Click "Process Video" button
    4. **View Results**: Watch live tracking as the video processes
    5. **Download**: Download the processed video with annotations
    """)

    st.subheader("🏗️ Technology Stack")
    st.markdown("""
    - **YOLOv5**: State-of-the-art object detection
    - **OpenCV**: Video processing and frame manipulation
    - **PyTorch**: Deep learning framework
    - **Streamlit**: Web app framework
    - **Scikit-learn**: (optional analytics tools)
    """)
