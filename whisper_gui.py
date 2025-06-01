import subprocess
import tkinter as tk
from tkinter import messagebox
import os
import platform
import datetime

whisper_process = None

def run_whisper():
    global whisper_process

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

    # Auto-generate output file if empty
    if not output_file:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join("whisper_cpp", "output", f"transcript_{timestamp}.txt")
    else:
        if not os.path.isabs(output_file):
            output_file = os.path.join("whisper_cpp", "output", output_file)

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    cmd = [
        cli_path,
        "-m", model_path,
        "-f", audio_path,
        "-t", threads,
        output_file
    ]

    try:
        whisper_process = subprocess.Popen(cmd)
        run_button.config(state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)
        root.after(100, check_process)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start whisper-cli.\n\nError:\n{e}")
        run_button.config(state=tk.NORMAL)
        stop_button.config(state=tk.DISABLED)

def check_process():
    global whisper_process
    if whisper_process is not None:
        retcode = whisper_process.poll()
        if retcode is None:
            root.after(100, check_process)
        else:
            if retcode == 0:
                messagebox.showinfo("Success", "Transcription completed successfully.")
            else:
                messagebox.showerror("Error", f"whisper-cli exited with status {retcode}.")
            run_button.config(state=tk.NORMAL)
            stop_button.config(state=tk.DISABLED)
            whisper_process = None

def stop_whisper():
    global whisper_process
    if whisper_process is not None:
        whisper_process.terminate()
        whisper_process = None
        run_button.config(state=tk.NORMAL)
        stop_button.config(state=tk.DISABLED)
        messagebox.showinfo("Stopped", "Transcription has been stopped.")

# GUI Setup
root = tk.Tk()
root.title("Whisper.cpp Transcription GUI")

tk.Label(root, text="Audio File (e.g., audio.mp3):").grid(row=0, column=0, sticky='e', padx=5, pady=5)
audio_entry = tk.Entry(root, width=40)
audio_entry.grid(row=0, column=1, padx=5)

tk.Label(root, text="Model File (e.g., ggml-base.en.bin):").grid(row=1, column=0, sticky='e', padx=5, pady=5)
model_entry = tk.Entry(root, width=40)
model_entry.grid(row=1, column=1, padx=5)

tk.Label(root, text="Output File (optional):").grid(row=2, column=0, sticky='e', padx=5, pady=5)
output_entry = tk.Entry(root, width=40)
default_output = f"transcript_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
output_entry.insert(0, default_output)
output_entry.grid(row=2, column=1, padx=5)

tk.Label(root, text="Threads (-t):").grid(row=3, column=0, sticky='e', padx=5, pady=5)
threads_entry = tk.Entry(root, width=10)
threads_entry.grid(row=3, column=1, sticky='w', padx=5)

run_button = tk.Button(root, text="Run", command=run_whisper)
run_button.grid(row=4, column=0, pady=15)

stop_button = tk.Button(root, text="Stop", command=stop_whisper, state=tk.DISABLED)
stop_button.grid(row=4, column=1, pady=15, sticky='w')

root.mainloop()