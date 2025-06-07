import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
import threading
import os
import datetime
import re
import json

whisper_process = None
final_output_path = ""

ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
timestamp_pattern = re.compile(r'\[\d{2}:\d{2}:\d{2}\.\d{3} *--> *\d{2}:\d{2}:\d{2}\.\d{3}\]')

def list_models():
    model_folder = os.path.join("whisper_cpp", "models")
    return [f for f in os.listdir(model_folder) if f.endswith(".bin")] if os.path.exists(model_folder) else []

def run_whisper_stream():
    global whisper_process, final_output_path

    model_file = model_var.get()
    output_file = output_entry.get().strip()
    threads = threads_entry.get().strip() or "4"

    if not model_file:
        messagebox.showerror("Missing Input", "Please select a model.")
        return

    output_dir, output_filename = os.path.split(output_file)
    if not output_filename:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"transcript_{timestamp}.txt"
    if not output_dir:
        output_dir = os.path.join("whisper_cpp", "output")

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_filename)
    final_output_path = output_path

    cli_path = os.path.join("whisper_cpp", "build", "bin", "whisper-stream")
    model_path = os.path.join("whisper_cpp", "models", model_file)

    cmd = [
        cli_path,
        "-m", model_path,
        "-l", "auto",
        "-t", threads,
        "--step", "0",
        "--length", "5000"
    ]

    print("Running:", " ".join(cmd))
    threading.Thread(target=read_output, args=(cmd, output_path), daemon=True).start()

def read_output(cmd, output_path):
    global whisper_process

    seen_lines = set()
    try:
        whisper_process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )

        def on_start():
            listen_button.config(state=tk.DISABLED)
            stop_button.config(state=tk.NORMAL)
            convert_button.config(state=tk.DISABLED)
            output_text.delete(1.0, tk.END)
        root.after(0, on_start)

        with open(output_path, "w", encoding="utf-8") as out_f:
            for line in whisper_process.stdout:
                clean_line = ansi_escape.sub("", line).strip()

                # Display in GUI
                def append():
                    output_text.insert(tk.END, clean_line + "\n")
                    output_text.see(tk.END)
                root.after(0, append)

                # Write only unique timestamped lines
                if timestamp_pattern.search(clean_line) and clean_line not in seen_lines:
                    out_f.write(clean_line + "\n")
                    seen_lines.add(clean_line)

                # Language and confidence
                match = re.search(r"auto-detected language:\s*([a-z]{2})\s*\(p\s*=\s*([0-9.]+)\)", clean_line)
                if match:
                    lang, conf = match.groups()
                    root.after(0, lambda: language_var.set(lang))
                    root.after(0, lambda: confidence_var.set(conf))

    except Exception as e:
        root.after(0, lambda: messagebox.showerror("Error", str(e)))
    finally:
        def on_finish():
            listen_button.config(state=tk.NORMAL)
            stop_button.config(state=tk.DISABLED)
            convert_button.config(state=tk.NORMAL)
        root.after(0, on_finish)

def stop_whisper():
    global whisper_process
    if whisper_process:
        whisper_process.terminate()
        whisper_process = None
        stop_button.config(state=tk.DISABLED)
        listen_button.config(state=tk.NORMAL)

def convert_to_json():
    global final_output_path
    if not os.path.exists(final_output_path):
        messagebox.showerror("Error", "Transcript file not found.")
        return

    json_output_path = final_output_path.replace(".txt", ".json")
    json_data = []

    try:
        with open(final_output_path, "r", encoding="utf-8") as f:
            for line in f:
                match = re.match(r"\[(\d{2}:\d{2}:\d{2}\.\d{3}) *--> *(\d{2}:\d{2}:\d{2}\.\d{3})\](.*)", line)
                if match:
                    start, end, text = match.groups()
                    json_data.append({"start": start.strip(), "end": end.strip(), "text": text.strip()})

        with open(json_output_path, "w", encoding="utf-8") as jf:
            json.dump(json_data, jf, ensure_ascii=False, indent=2)

        messagebox.showinfo("Success", f"Saved JSON:\n{json_output_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# === GUI ===
root = tk.Tk()
root.title("Whisper.cpp Streaming Transcriptor")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

tk.Label(frame, text="Select Model:").pack(anchor="w")
model_var = tk.StringVar()
model_dropdown = tk.OptionMenu(frame, model_var, *list_models())
model_dropdown.pack(anchor="w", fill="x")

tk.Label(frame, text="Output Filename (optional, can include folder):").pack(anchor="w")
output_entry = tk.Entry(frame, width=50)
output_entry.pack(anchor="w", pady=2)

tk.Label(frame, text="Number of Threads:").pack(anchor="w")
threads_entry = tk.Entry(frame, width=10)
threads_entry.insert(0, "4")
threads_entry.pack(anchor="w", pady=2)

tk.Label(frame, text="Language Detected:").pack(anchor="w")
language_var = tk.StringVar()
tk.Label(frame, textvariable=language_var, fg="blue").pack(anchor="w")

tk.Label(frame, text="Confidence:").pack(anchor="w")
confidence_var = tk.StringVar()
tk.Label(frame, textvariable=confidence_var, fg="green").pack(anchor="w")

listen_button = tk.Button(frame, text="🎧 Listen", command=run_whisper_stream)
listen_button.pack(pady=5)

stop_button = tk.Button(frame, text="🛑 Stop", state=tk.DISABLED, command=stop_whisper)
stop_button.pack(pady=5)

convert_button = tk.Button(frame, text="Convert to JSON", state=tk.DISABLED, command=convert_to_json)
convert_button.pack(pady=10)

output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=30, font=("Courier", 10))
output_text.pack(padx=10, pady=10)

root.mainloop()
