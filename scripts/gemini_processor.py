import os
import re
import time
from pathlib import Path
from dotenv import load_dotenv

# Try to import google-genai
try:
    from google import genai
    from google.genai import types
except ImportError:
    print("google-genai library is not installed. Please run: pip install -r requirements.txt")
    exit(1)

# Load environment variables (for GEMINI_API_KEY)
load_dotenv()

# --- Configurations ---
BASE_DIR = Path(__file__).resolve().parent.parent
IMAGE_PROMPTS_FILE = BASE_DIR / "02_preproduction" / "image_prompts" / "hanroro_0plus0_image_prompts_v2.md"
ACTION_PROMPTS_FILE = BASE_DIR / "03_production" / "action_prompts" / "hanroro_0plus0_action_prompts_v3.md"

IMAGE_OUTPUT_DIR = BASE_DIR / "assets" / "exports" / "images"
VIDEO_OUTPUT_DIR = BASE_DIR / "assets" / "exports" / "takes"

# Ensure output directories exist
IMAGE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
VIDEO_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Initialize Gemini Client
client = genai.Client()

def parse_markdown_prompts(filepath: Path) -> dict:
    """
    Parses a markdown file and extracts code blocks for each Shot.
    Returns a dict: {'Shot 01': 'prompt text...', 'Shot 02': ...}
    """
    if not filepath.exists():
        print(f"Warning: File not found - {filepath}")
        return {}

    content = filepath.read_text(encoding='utf-8')
    
    # Match headers like `### Shot 01 — ...`
    shot_blocks = re.split(r'(###\s+Shot\s+\d+.*?)\n', content)
    
    prompts = {}
    current_shot = None
    
    for block in shot_blocks:
        shot_match = re.match(r'###\s+(Shot\s+\d+)', block)
        if shot_match:
            current_shot = shot_match.group(1)
        elif current_shot:
            # Extract the content inside the first ``` block
            code_match = re.search(r'```(.*?)```', block, re.DOTALL)
            if code_match:
                prompt_text = code_match.group(1).strip()
                prompts[current_shot] = prompt_text
            current_shot = None
            
    return prompts

def generate_image(shot_id: str, prompt: str) -> Path:
    """
    Generates an image using Gemini Imagen 3 and saves it.
    Returns the Path to the saved image.
    """
    output_path = IMAGE_OUTPUT_DIR / f"{shot_id.replace(' ', '_').lower()}.png"
    if output_path.exists():
        print(f"[{shot_id}] Image already exists. Skipping image generation.")
        return output_path

    print(f"[{shot_id}] Generating image via Imagen 3...")
    try:
        result = client.models.generate_images(
            model='imagen-3.0-generate-001',
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="16:9",
                output_mime_type="image/png"
            )
        )
        
        for generated_image in result.generated_images:
            with open(output_path, "wb") as f:
                f.write(generated_image.image.image_bytes)
            print(f"[{shot_id}] Image saved to {output_path}")
            return output_path
            
    except Exception as e:
        print(f"[{shot_id}] Error generating image: {e}")
        
    return None

def generate_video(shot_id: str, image_path: Path, action_prompt: str) -> Path:
    """
    Generates a video using Gemini Veo (Image-to-Video).
    Returns the Path to the saved video.
    """
    output_path = VIDEO_OUTPUT_DIR / f"{shot_id.replace(' ', '_').lower()}.mp4"
    if output_path.exists():
        print(f"[{shot_id}] Video already exists. Skipping video generation.")
        return output_path

    print(f"[{shot_id}] Uploading image for Veo...")
    try:
        # Upload the image to the Gemini file API for video generation
        uploaded_image = client.files.upload(file=str(image_path))
        
        print(f"[{shot_id}] Generating video via Veo...")
        # Note: 'veo-2.0-generate-001' is an example endpoint. Adjust if necessary for your Google Cloud/GenAI setup.
        operation = client.models.generate_videos(
            model='veo-2.0-generate-001',
            prompt=[uploaded_image, action_prompt],
            config=types.GenerateVideosConfig(
                person_generation="ALLOW_ADULT",
            )
        )
        
        print(f"[{shot_id}] Video generation started. Waiting for completion...")
        # Polling for completion
        while not operation.done:
            print(f"[{shot_id}] Still generating... (sleeping 15s)")
            time.sleep(15)
            # Re-fetch the operation status
            operation = client.operations.get_operation(operation.name)
            
        if operation.error:
            print(f"[{shot_id}] Video generation failed: {operation.error}")
            return None
            
        # Download the resulting video
        if operation.response and hasattr(operation.response, 'generated_videos'):
            for video in operation.response.generated_videos:
                with open(output_path, "wb") as f:
                    f.write(video.video.video_bytes)
                print(f"[{shot_id}] Video saved to {output_path}")
                return output_path
                
        # If the API returns a URI instead of bytes
        elif operation.response and hasattr(operation.response, 'uri'):
            import requests
            resp = requests.get(operation.response.uri)
            with open(output_path, "wb") as f:
                f.write(resp.content)
            print(f"[{shot_id}] Video downloaded and saved to {output_path}")
            return output_path
            
    except Exception as e:
        print(f"[{shot_id}] Error generating video: {e}")
        
    return None

def main():
    print("=== Gemini API Image & Veo Video Processor ===")
    
    # 1. Parse Prompts
    print("\n1. Parsing markdown files...")
    image_prompts = parse_markdown_prompts(IMAGE_PROMPTS_FILE)
    action_prompts = parse_markdown_prompts(ACTION_PROMPTS_FILE)
    
    print(f"Found {len(image_prompts)} image prompts.")
    print(f"Found {len(action_prompts)} action prompts.")
    
    # Get common shots
    shots = sorted(list(set(image_prompts.keys()) & set(action_prompts.keys())))
    
    if not shots:
        print("No matching shots found between image and action prompts. Exiting.")
        return

    print(f"Processing {len(shots)} matched shots...\n")
    
    # 2. Process each shot
    for shot in shots:
        print(f"\n--- Processing {shot} ---")
        img_prompt = image_prompts[shot]
        act_prompt = action_prompts[shot]
        
        # Step A: Generate Image
        image_path = generate_image(shot, img_prompt)
        
        if image_path and image_path.exists():
            # Step B: Generate Video
            generate_video(shot, image_path, act_prompt)
        else:
            print(f"[{shot}] Skipping video generation due to missing image.")

    print("\n=== Processing Complete ===")

if __name__ == "__main__":
    main()
