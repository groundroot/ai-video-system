import os
import sys
import re
import time
from pathlib import Path
from dotenv import load_dotenv

# Optional dependencies based on engine
try:
    from google import genai
    from google.genai import types
    has_genai = True
except ImportError:
    has_genai = False

# Load env variables
if getattr(sys, 'frozen', False):
    # If the application is run as a bundle (via PyInstaller)
    application_path = Path(sys._MEIPASS)
    # The actual executing directory where user ran the binary
    execution_dir = Path(os.getcwd())
else:
    application_path = Path(__file__).parent
    execution_dir = application_path

env_path = execution_dir / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv() # Fallback

# --- System Paths ---
# If frozen, we need to locate the project folders relative to the execution directory
# Assuming the user runs this in the 'AI Video System' root, or we look for it.
BASE_DIR = execution_dir.resolve()
if BASE_DIR.name == "scripts":
    BASE_DIR = BASE_DIR.parent

IMAGE_PROMPTS_FILE = BASE_DIR / "02_preproduction" / "image_prompts" / "hanroro_0plus0_image_prompts_v2.md"
ACTION_PROMPTS_FILE = BASE_DIR / "03_production" / "action_prompts" / "hanroro_0plus0_action_prompts_v3.md"

IMAGE_OUTPUT_DIR = BASE_DIR / "assets" / "exports" / "images"
VIDEO_OUTPUT_DIR = BASE_DIR / "assets" / "exports" / "takes"

# Ensure output directories exist
IMAGE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
VIDEO_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# --- Core Parser ---
def parse_markdown_prompts(filepath: Path) -> dict:
    if not filepath.exists():
        print(f"Warning: File not found - {filepath}")
        return {}

    content = filepath.read_text(encoding='utf-8')
    shot_blocks = re.split(r'(###\s+Shot\s+\d+.*?)\n', content)
    
    prompts = {}
    current_shot = None
    
    for block in shot_blocks:
        shot_match = re.match(r'###\s+(Shot\s+\d+)', block)
        if shot_match:
            current_shot = shot_match.group(1)
        elif current_shot:
            code_match = re.search(r'```(.*?)```', block, re.DOTALL)
            if code_match:
                prompts[current_shot] = code_match.group(1).strip()
            current_shot = None
    return prompts


# --- Image Engines ---
def generate_image_gemini(shot_id: str, prompt: str) -> Path:
    output_path = IMAGE_OUTPUT_DIR / f"{shot_id.replace(' ', '_').lower()}.png"
    if output_path.exists():
        print(f"[{shot_id}] Image exists. Skipping.")
        return output_path
        
    if not has_genai:
        print("Error: google-genai is not installed.")
        return None

    try:
        client = genai.Client()
        print(f"[{shot_id}] Generating image (Gemini Imagen 3)...")
        result = client.models.generate_images(
            model='imagen-3.0-generate-001',
            prompt=prompt,
            config=types.GenerateImagesConfig(number_of_images=1, aspect_ratio="16:9", output_mime_type="image/png")
        )
        for img in result.generated_images:
            with open(output_path, "wb") as f:
                f.write(img.image.image_bytes)
            print(f"[{shot_id}] Saved to {output_path}")
            return output_path
    except Exception as e:
        print(f"[{shot_id}] Gemini Image Error: {e}")
    return None

def generate_image_qwen(shot_id: str, prompt: str) -> Path:
    print(f"[{shot_id}] Qwen Studio API is not yet configured. Mocking image generation.")
    output_path = IMAGE_OUTPUT_DIR / f"{shot_id.replace(' ', '_').lower()}_qwen_mock.png"
    # Create empty file as mock
    with open(output_path, "w") as f:
        f.write("Mock Qwen Image")
    return output_path


# --- Video Engines ---
def generate_video_gemini(shot_id: str, image_path: Path, action_prompt: str) -> Path:
    output_path = VIDEO_OUTPUT_DIR / f"{shot_id.replace(' ', '_').lower()}.mp4"
    if output_path.exists():
        print(f"[{shot_id}] Video exists. Skipping.")
        return output_path
        
    if not has_genai:
        print("Error: google-genai is not installed.")
        return None

    try:
        client = genai.Client()
        print(f"[{shot_id}] Uploading image for Veo...")
        uploaded_image = client.files.upload(file=str(image_path))
        
        print(f"[{shot_id}] Generating video (Gemini Veo)...")
        operation = client.models.generate_videos(
            model='veo-2.0-generate-001',
            prompt=[uploaded_image, action_prompt],
            config=types.GenerateVideosConfig(person_generation="ALLOW_ADULT")
        )
        while not operation.done:
            print(f"[{shot_id}] Generating... (sleeping 15s)")
            time.sleep(15)
            operation = client.operations.get_operation(operation.name)
            
        if operation.error:
            print(f"[{shot_id}] Video failed: {operation.error}")
            return None
            
        if operation.response and hasattr(operation.response, 'generated_videos'):
            for video in operation.response.generated_videos:
                with open(output_path, "wb") as f:
                    f.write(video.video.video_bytes)
                print(f"[{shot_id}] Saved to {output_path}")
                return output_path
        elif operation.response and hasattr(operation.response, 'uri'):
            import requests
            resp = requests.get(operation.response.uri)
            with open(output_path, "wb") as f:
                f.write(resp.content)
            print(f"[{shot_id}] Saved to {output_path}")
            return output_path
    except Exception as e:
        print(f"[{shot_id}] Gemini Video Error: {e}")
    return None

def generate_video_wan(shot_id: str, image_path: Path, action_prompt: str) -> Path:
    print(f"[{shot_id}] Wan Video API is not yet configured. Mocking video generation.")
    output_path = VIDEO_OUTPUT_DIR / f"{shot_id.replace(' ', '_').lower()}_wan_mock.mp4"
    with open(output_path, "w") as f:
        f.write("Mock Wan Video")
    return output_path

def generate_video_hunyuan(shot_id: str, image_path: Path, action_prompt: str) -> Path:
    print(f"[{shot_id}] Hunyuan Video API is not yet configured. Mocking video generation.")
    output_path = VIDEO_OUTPUT_DIR / f"{shot_id.replace(' ', '_').lower()}_hunyuan_mock.mp4"
    with open(output_path, "w") as f:
        f.write("Mock Hunyuan Video")
    return output_path


# --- CLI Interface ---
def main():
    print("========================================")
    print("    AI Video System - Pipeline CLI")
    print("========================================")
    
    # Check execution path
    if not IMAGE_PROMPTS_FILE.exists():
        print(f"Warning: Prompt files not found at {IMAGE_PROMPTS_FILE.parent.parent.parent}.")
        print("Please run this executable from the root of your 'AI Video System' project directory.")
        input("Press Enter to exit...")
        return

    # Select Image Engine
    print("\n[ Select Image Generation Engine ]")
    print("1. Google Gemini (Imagen 3)")
    print("2. Qwen Studio (Mock)")
    while True:
        img_choice = input("Enter number (1-2): ").strip()
        if img_choice in ['1', '2']: break
    
    img_engine = generate_image_gemini if img_choice == '1' else generate_image_qwen

    # Select Video Engine
    print("\n[ Select Video Generation Engine ]")
    print("1. Google Gemini (Veo)")
    print("2. Wan (Mock)")
    print("3. Hunyuan (Mock)")
    while True:
        vid_choice = input("Enter number (1-3): ").strip()
        if vid_choice in ['1', '2', '3']: break
        
    if vid_choice == '1':
        vid_engine = generate_video_gemini
    elif vid_choice == '2':
        vid_engine = generate_video_wan
    else:
        vid_engine = generate_video_hunyuan

    print("\n========================================")
    print("Parsing Markdown Prompts...")
    image_prompts = parse_markdown_prompts(IMAGE_PROMPTS_FILE)
    action_prompts = parse_markdown_prompts(ACTION_PROMPTS_FILE)
    shots = sorted(list(set(image_prompts.keys()) & set(action_prompts.keys())))
    
    if not shots:
        print("No matching shots found. Please check your markdown files.")
        input("Press Enter to exit...")
        return
        
    print(f"Found {len(shots)} matched shots to process.")
    print("========================================\n")
    
    # Process
    for shot in shots:
        print(f"--- Processing {shot} ---")
        img_prompt = image_prompts[shot]
        act_prompt = action_prompts[shot]
        
        # 1. Image
        img_path = img_engine(shot, img_prompt)
        
        # 2. Video
        if img_path and img_path.exists():
            vid_engine(shot, img_path, act_prompt)
        else:
            print(f"[{shot}] Skipped video due to missing image.")

    print("\nAll tasks completed successfully!")
    input("Press Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProcess canceled by user.")
        sys.exit(0)
