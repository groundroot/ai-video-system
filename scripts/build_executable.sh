#!/bin/bash
# AI Video CLI Build Script for MacOS

echo "========================================="
echo " Building AI Video System CLI Executable "
echo "========================================="

# 1. Install pyinstaller if not present
echo "[1/3] Installing dependencies..."
pip install -r requirements.txt

# 2. Run PyInstaller
echo "[2/3] Running PyInstaller..."
# --onefile: Create a single executable file
# --name: Name of the output executable
# --clean: Clean PyInstaller cache and remove temporary files before building
pyinstaller --onefile --name "ai_video_cli_mac" --clean ai_video_cli.py

echo "[3/3] Build Complete!"
echo "Your standalone executable is located at: dist/ai_video_cli_mac"
echo ""
echo "To distribute this tool to others:"
echo "1. Zip the 'dist/ai_video_cli_mac' file"
echo "2. Ask the user to run it from the root of their 'AI Video System' folder."
echo "3. Make sure they have a .env file in the root folder with their GEMINI_API_KEY."
echo "========================================="
