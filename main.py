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

    # Language selection - allow direct input of language name
    supported_languages = {
        "auto": None,
        "auto-detect": None,
        "english": "en",
        "vietnamese": "vi",
        "chinese": "zh",
        "japanese": "ja",
        "korean": "ko",
        "spanish": "es",
        "french": "fr",
        "german": "de",
        "russian": "ru",
        "portuguese": "pt",
        "italian": "it",
        "arabic": "ar",
        "hindi": "hi",
        "thai": "th",
        "dutch": "nl",
        "greek": "el",
        "turkish": "tr",
        "polish": "pl",
        "czech": "cs",
        "slovak": "sk",
        "hungarian": "hu",
        "romanian": "ro",
        "bulgarian": "bg",
        "croatian": "hr",
        "serbian": "sr",
        "slovenian": "sl",
        "estonian": "et",
        "latvian": "lv",
        "lithuanian": "lt",
        "finnish": "fi",
        "swedish": "sv",
        "danish": "da",
        "norwegian": "no",
        "icelandic": "is",
        "hebrew": "he",
        "malay": "ms",
        "indonesian": "id",
        "filipino": "tl",
        "ukrainian": "uk",
        "belarusian": "be",
        "macedonian": "mk",
        "albanian": "sq",
        "armenian": "hy",
        "azerbaijani": "az",
        "georgian": "ka",
        "kazakh": "kk",
        "kyrgyz": "ky",
        "mongolian": "mn",
        "nepali": "ne",
        "sinhala": "si",
        "tamil": "ta",
        "telugu": "te",
        "malayalam": "ml",
        "kannada": "kn",
        "gujarati": "gu",
        "punjabi": "pa",
        "bengali": "bn",
        "marathi": "mr",
        "oriya": "or",
        "urdu": "ur",
        "pashto": "ps",
        "persian": "fa",
        "swahili": "sw",
        "afrikaans": "af",
        "zulu": "zu",
        "xhosa": "xh"
    }
    
    print("\nAvailable languages (enter name or 'auto' for auto-detect):")
    print("Examples: english, vietnamese, chinese, japanese, korean, spanish, french, german, russian, portuguese, italian, arabic, hindi, thai, dutch, greek, turkish, polish, czech, slovak, hungarian, romanian, bulgarian, croatian, serbian, slovenian, estonian, latvian, lithuanian, finnish, swedish, danish, norwegian, icelandic, hebrew, malay, indonesian, filipino, ukrainian, belarusian, macedonian, albanian, armenian, azerbaijani, georgian, kazakh, kyrgyz, mongolian, nepali, sinhala, tamil, telugu, malayalam, kannada, gujarati, punjabi, bengali, marathi, oriya, urdu, pashto, persian, swahili, afrikaans, zulu, xhosa")
    
    language_input = input("\nEnter language name (or 'auto' for auto-detect): ").strip().lower()
    
    # Map common variations
    language_aliases = {
        "auto": None,
        "auto-detect": None,
        "eng": "en",
        "vie": "vi",
        "chi": "zh",
        "zho": "zh",
        "jpn": "ja",
        "kor": "ko",
        "spa": "es",
        "fra": "fr",
        "fre": "fr",
        "deu": "de",
        "ger": "de",
        "rus": "ru",
        "por": "pt",
        "ita": "it",
        "ara": "ar",
        "hin": "hi",
        "tha": "th",
        "dut": "nl",
        "nld": "nl",
        "gre": "el",
        "ell": "el",
        "tur": "tr",
        "pol": "pl",
        "cze": "cs",
        "ces": "cs",
        "slo": "sk",
        "slk": "sk",
        "hun": "hu",
        "rom": "ro",
        "ron": "ro",
        "bul": "bg",
        "hrv": "hr",
        "ser": "sr",
        "slv": "sl",
        "est": "et",
        "lav": "lv",
        "lit": "lt",
        "fin": "fi",
        "swe": "sv",
        "dan": "da",
        "nor": "no",
        "ice": "is",
        "isl": "is",
        "heb": "he",
        "mal": "ms",
        "ind": "id",
        "fil": "tl",
        "ukr": "uk",
        "bel": "be",
        "mac": "mk",
        "mkd": "mk",
        "alb": "sq",
        "sqi": "sq",
        "arm": "hy",
        "hye": "hy",
        "aze": "az",
        "geo": "ka",
        "kat": "ka",
        "kaz": "kk",
        "kyr": "ky",
        "mon": "mn",
        "nep": "ne",
        "sin": "si",
        "tam": "ta",
        "tel": "te",
        "mal": "ml",
        "kan": "kn",
        "guj": "gu",
        "pan": "pa",
        "ben": "bn",
        "mar": "mr",
        "ori": "or",
        "urd": "ur",
        "pus": "ps",
        "fas": "fa",
        "swa": "sw",
        "afr": "af",
        "zul": "zu",
        "xho": "xh"
    }
    
    # Merge aliases with main languages
    all_languages = {**supported_languages, **language_aliases}
    
    language = all_languages.get(language_input, None)
    
    if language is None:
        if language_input == "auto" or language_input == "auto-detect":
            print("Using auto-detect language mode")
        else:
            print(f"Warning: '{language_input}' is not a supported language. Using auto-detect mode.")
            language = None
    else:
        print(f"Using language: {language_input.title()}")

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
