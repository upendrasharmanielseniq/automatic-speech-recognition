import subprocess
import tkinter as tk
from tkinter import messagebox, scrolledtext
import os
import platform
import datetime
import threading
import re
import json

whisper_process = None
final_output_path = ""

def run_whisper():
    global whisper_process, final_output_path

    audio_file = audio_entry.get().strip()
    model_file = model_entry.get().strip()
    output_file = output_entry.get().strip()
    threads = threads_entry.get().strip()

    if not all([audio_file, model_file, threads]):
        messagebox.showerror("Missing Input", "Please fill in all required fields.")
        return

    is_windows = platform.system() == "Windows"
    cli_executable = "whisper-cli.exe" if is_windows else "./whisper-cli"
    cli_path = os.path.join("whisper_cpp", cli_executable)

    model_path = os.path.join("whisper_cpp", "models", model_file)
    audio_path = os.path.join("whisper_cpp", "samples", audio_file)

    if not output_file:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join("whisper_cpp", "output", f"transcript_{timestamp}.txt")
    else:
        if not os.path.isabs(output_file):
            output_file = os.path.join("whisper_cpp", "output", output_file)

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    final_output_path = output_file

    cmd = [
        cli_path,
        "-m", model_path,
        "-f", audio_path,
        "-l", "auto",
        "-t", threads
    ]

    def read_output():
        nonlocal output_file
        try:
            with open(output_file, "w", encoding="utf-8") as out_f:
                whisper_process = subprocess.Popen(
                    cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    text=True, encoding='utf-8', errors='replace', bufsize=1
                )
                run_button.config(state=tk.DISABLED)
                stop_button.config(state=tk.NORMAL)
                convert_button.config(state=tk.DISABLED)

                for line in whisper_process.stdout:
                    lang_conf_match = re.search(r"auto-detected language:\s*([a-z]{2})\s*\(p\s*=\s*([0-9.]+)\)", line)
                    if lang_conf_match:
                        language_var.set(lang_conf_match.group(1))
                        confidence_var.set(lang_conf_match.group(2))

                    if re.match(r"\[\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}\]", line):
                        output_text.insert(tk.END, line)
                        output_text.see(tk.END)
                        out_f.write(line)

                whisper_process.wait()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run whisper: {e}")
        finally:
            run_button.config(state=tk.NORMAL)
            stop_button.config(state=tk.DISABLED)
            convert_button.config(state=tk.NORMAL)  # Enable JSON button

    threading.Thread(target=read_output, daemon=True).start()

def stop_whisper():
    global whisper_process
    if whisper_process:
        whisper_process.terminate()
        run_button.config(state=tk.NORMAL)
        stop_button.config(state=tk.DISABLED)

def convert_to_json():
    global final_output_path

    if not os.path.exists(final_output_path):
        messagebox.showerror("Error", "Transcription output file not found.")
        return

    json_output_path = final_output_path.replace(".txt", ".json")
    json_data = []

    try:
        with open(final_output_path, "r", encoding="utf-8") as f:
            for line in f:
                match = re.match(r"\[(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})\](.*)", line)
                if match:
                    start, end, text = match.groups()
                    json_data.append({
                        "start": start.strip(),
                        "end": end.strip(),
                        "text": text.strip()
                    })

        with open(json_output_path, "w", encoding="utf-8") as jf:
            json.dump(json_data, jf, ensure_ascii=False, indent=2)

        messagebox.showinfo("Success", f"Transcript converted to JSON:\n{json_output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to convert to JSON: {e}")

# GUI Setup
root = tk.Tk()
root.title("Whisper.cpp Transcription GUI")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

fields = [
    ("Audio File (inside samples_folder/):", "audio_entry"),
    ("Model File (inside models/):", "model_entry"),
    ("Output File Name (.txt, optional):", "output_entry"),
    ("Number of Threads:", "threads_entry")
]

for label_text, var_name in fields:
    tk.Label(frame, text=label_text).pack(anchor="w")
    entry = tk.Entry(frame, width=50)
    entry.pack(anchor="w", pady=2)
    globals()[var_name] = entry

language_var = tk.StringVar()
tk.Label(frame, text="Language Detected:").pack(anchor="w")
language_label = tk.Label(frame, textvariable=language_var, fg="blue")
language_label.pack(anchor="w")

confidence_var = tk.StringVar()
tk.Label(frame, text="Confidence:").pack(anchor="w")
confidence_label = tk.Label(frame, textvariable=confidence_var, fg="green")
confidence_label.pack(anchor="w")

run_button = tk.Button(frame, text="Run Transcription", command=run_whisper)
run_button.pack(pady=(10, 0))

stop_button = tk.Button(frame, text="Stop", state=tk.DISABLED, command=stop_whisper)
stop_button.pack(pady=(5, 0))

convert_button = tk.Button(frame, text="Convert to JSON", state=tk.DISABLED, command=convert_to_json)
convert_button.pack(pady=(5, 10))

output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=30, font=("Courier", 10))
output_text.pack(padx=10, pady=(0, 10))

root.mainloop()