import cv2
import imageio
import os
from pathlib import Path


def convert_video(input_path, output_path):
    """Convert video using cv2 to read and imageio to write"""
    # Read video with cv2
    cap = cv2.VideoCapture(input_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video {input_path}")
        return False
    
    print(f"Processing {input_path}")
    
    # Read all frames
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Convert BGR to RGB (cv2 uses BGR, imageio expects RGB)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frames.append(frame_rgb)
    
    cap.release()
    
    if not frames:
        print(f"Error: No frames read from {input_path}")
        return False
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Write video with imageio
    print(f"  Writing to {output_path}")
    with imageio.get_writer(output_path, fps=30) as writer:
        for frame in frames:
            writer.append_data(frame)
    
    print(f"  Success: {output_path}")
    return True


def main():
    # Get the parent directory (project root)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    real_demo_path = project_root / "resources" / "real_demo"
    output_dir = real_demo_path / "converted"
    
    print("Converting videos for codec compatibility...")
    
    # Process both dp and gwm directories
    for dir_name in ["dp", "gwm"]:
        input_dir = real_demo_path / dir_name
        output_subdir = output_dir / dir_name
        
        if not input_dir.exists():
            print(f"Warning: {input_dir} does not exist, skipping...")
            continue
        
        print(f"\n=== Processing {dir_name} directory ===")
        
        # Get all mp4 files and sort them numerically
        video_files = list(input_dir.glob("*.mp4"))
        video_files.sort(key=lambda x: int(x.stem))
        
        success_count = 0
        for video_file in video_files:
            input_path = str(video_file)
            output_path = str(output_subdir / video_file.name)
            
            if convert_video(input_path, output_path):
                success_count += 1
        
        print(f"{dir_name}: {success_count}/{len(video_files)} videos converted")
    
    print("\nDone! Converted videos are in resources/real_demo/converted/")


if __name__ == "__main__":
    main()
