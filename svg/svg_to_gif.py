import os
from PIL import Image
import cairosvg
import io
import time
from pathlib import Path

def extract_animation_duration(svg_content):
    """Extract animation duration from SVG content"""
    # Default duration if not found
    default_duration = 2000  # 2 seconds in milliseconds
    
    # Look for dur attribute in the SVG
    if 'dur="' in svg_content:
        dur_start = svg_content.find('dur="') + 5
        dur_end = svg_content.find('"', dur_start)
        dur_str = svg_content[dur_start:dur_end]
        
        # Convert duration string to milliseconds
        if 's"' in dur_str:
            return float(dur_str.replace('s', '')) * 1000
    
    return default_duration

def create_frame(svg_content, frame_num, total_frames):
    """Create a single frame by modifying the SVG content"""
    # This is a simple way to create frames - you might need to adjust this
    # based on your specific animation needs
    modified_svg = svg_content
    
    # Convert SVG to PNG bytes
    png_bytes = cairosvg.svg2png(bytestring=modified_svg.encode('utf-8'))
    
    # Convert PNG bytes to PIL Image
    return Image.open(io.BytesIO(png_bytes))

def svg_to_gif(svg_path, output_path=None, frames=10, duration=100):
    """Convert SVG to animated GIF"""
    # Read SVG file
    with open(svg_path, 'r') as f:
        svg_content = f.read()
    
    # If no output path specified, use same directory as SVG
    if output_path is None:
        output_path = Path(svg_path).with_suffix('.gif')
    
    # Extract animation duration from SVG
    anim_duration = extract_animation_duration(svg_content)
    frame_duration = int(anim_duration / frames)
    
    # Create frames
    print(f"Creating {frames} frames...")
    frames_list = []
    for i in range(frames):
        frame = create_frame(svg_content, i, frames)
        frames_list.append(frame)
        print(f"Frame {i+1}/{frames} created")
    
    # Save as GIF
    print(f"Saving GIF to {output_path}...")
    frames_list[0].save(
        output_path,
        save_all=True,
        append_images=frames_list[1:],
        duration=frame_duration,
        loop=0,
        optimize=True
    )
    
    print("Conversion complete!")
    return output_path

# Example usage
if __name__ == "__main__":
    # Get current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Look for SVG files in current directory
    svg_files = [f for f in os.listdir(current_dir) if f.endswith('.svg')]
    
    if not svg_files:
        print("No SVG files found in current directory!")
    else:
        for svg_file in svg_files:
            print(f"Converting {svg_file}...")
            svg_path = os.path.join(current_dir, svg_file)
            svg_to_gif(svg_path)