import os
import whisper
import subprocess
import sys

def check_ffmpeg():
    """Check if ffmpeg is installed and accessible"""
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def list_audio_files(directory, extensions=None):
    if extensions is None:
        extensions = ['.mp3', '.wav', '.m4a', '.flac', '.mp4', '.mkv', '.aac', '.ogg']
    files = []
    for filename in os.listdir(directory):
        if any(filename.lower().endswith(ext) for ext in extensions):
            files.append(filename)
    return files

def main():
    print("Batch audio files transcription to subtitle files using Whisper")
    
    # Check for ffmpeg dependency
    print("Checking for required dependencies...")
    if not check_ffmpeg():
        print("ERROR: ffmpeg is not installed or not found in PATH.")
        print("Please install ffmpeg and add it to your system PATH.")
        print("")
        print("Instructions:")
        print("1. Download ffmpeg from https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl-shared.zip")
        print("2. Extract the archive")
        print("3. Add the path to the 'bin' folder (e.g., C:\\ffmpeg\\bin) to your system PATH environment variable")
        print("4. Restart your command prompt/terminal")
        print("")
        print("Alternatively, run the setup.py script which will automatically download and configure ffmpeg.")
        return

    input_dir = None
    while not input_dir or not os.path.isdir(input_dir):
        input_dir = input("Enter the path to the directory containing audio files: ").strip()
        if not os.path.isdir(input_dir):
            print("Invalid directory path. Please try again.")

    model_options = {
        "1": "tiny",
        "2": "base",
        "3": "small",
        "4": "medium",
        "5": "large"
    }
    print("Select Whisper model:")
    for key, value in model_options.items():
        print(f"{key}: {value}")
    model_choice = input("Enter the number corresponding to the model (1-5): ").strip()
    model_name = model_options.get(model_choice, "medium")

    # Remove language selection, always use auto-detect
    language = None

    output_format_options = {
        "1": "srt",
        "2": "vtt",
        "3": "txt"
    }
    print("Select output file format:")
    for key, value in output_format_options.items():
        print(f"{key}: {value}")
    output_format_choice = None
    while output_format_choice not in output_format_options:
        output_format_choice = input("Enter the number corresponding to the format (1-3), required: ").strip()
    output_format = output_format_options[output_format_choice]

    output_dir = None
    while not output_dir or not os.path.isdir(output_dir):
        output_dir = input("Enter the path to the output directory for subtitle files: ").strip()
        if not os.path.isdir(output_dir):
            create_dir = input(f"Directory '{output_dir}' does not exist. Create it? (y/n): ").strip().lower()
            if create_dir == 'y':
                os.makedirs(output_dir)
            else:
                output_dir = None

    audio_files = list_audio_files(input_dir)
    if not audio_files:
        print("No audio files found in the input directory.")
        return

    print(f"Loading Whisper model '{model_name}'...")
    model = whisper.load_model(model_name)

    for audio_file in audio_files:
        print(f"Processing file: {audio_file} ...")
        options = {}
        if language:
            options["language"] = language
        # transcribe returns a dict with 'segments' and 'text'
        audio_path = os.path.join(input_dir, audio_file)
        try:
            result = model.transcribe(audio_path, **options)
        except Exception as e:
            print(f"Error processing file {audio_file}: {str(e)}")
            print("This might be due to a missing or incompatible ffmpeg installation.")
            continue

        base_name = os.path.splitext(audio_file)[0]
        out_base = os.path.join(output_dir, os.path.basename(base_name))
        if output_format == "srt":
            out_path = out_base + ".srt"
            with open(out_path, "w", encoding="utf-8") as out_file:
                for i, segment in enumerate(result["segments"], start=1):
                    start = segment["start"]
                    end = segment["end"]
                    text = segment["text"].strip()
                    out_file.write(f"{i}\n")
                    out_file.write(f"{format_timestamp(start)} --> {format_timestamp(end)}\n")
                    out_file.write(f"{text}\n\n")
        elif output_format == "vtt":
            out_path = out_base + ".vtt"
            with open(out_path, "w", encoding="utf-8") as out_file:
                out_file.write("WEBVTT\n\n")
                for segment in result["segments"]:
                    start = segment["start"]
                    end = segment["end"]
                    text = segment["text"].strip()
                    out_file.write(f"{format_timestamp_vtt(start)} --> {format_timestamp_vtt(end)}\n")
                    out_file.write(f"{text}\n\n")
        elif output_format == "txt":
            out_path = out_base + ".txt"
            with open(out_path, "w", encoding="utf-8") as out_file:
                out_file.write(result["text"].strip() + "\n")
        else:
            # fallback to srt
            out_path = out_base + ".srt"
            with open(out_path, "w", encoding="utf-8") as out_file:
                for i, segment in enumerate(result["segments"], start=1):
                    start = segment["start"]
                    end = segment["end"]
                    text = segment["text"].strip()
                    out_file.write(f"{i}\n")
                    out_file.write(f"{format_timestamp(start)} --> {format_timestamp(end)}\n")
                    out_file.write(f"{text}\n\n")

        print(f"Saved subtitle file: {out_path}")

def format_timestamp(seconds):
    # Chuyển giây sang định dạng hh:mm:ss,ms
    ms = int((seconds - int(seconds)) * 1000)
    s = int(seconds) % 60
    m = (int(seconds) // 60) % 60
    h = int(seconds) // 3600
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def format_timestamp_vtt(seconds):
    # Chuyển giây sang định dạng hh:mm:ss.ms (dấu chấm thay vì dấu phẩy)
    ms = int((seconds - int(seconds)) * 1000)
    s = int(seconds) % 60
    m = (int(seconds) // 60) % 60
    h = int(seconds) // 3600
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"

if __name__ == "__main__":
    main()
