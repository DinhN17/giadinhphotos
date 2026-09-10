#!/usr/bin/env python3
"""
GUI front-end for Family Photo Categorizer.
Provides a simple graphical interface for users with no IT knowledge.

Uses tkinter (standard library) so no additional packages are needed.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import subprocess
import os
import sys
from pathlib import Path

# Default categories
DEFAULT_CATEGORIES = [
    "birthday", "vacation", "holiday", "wedding",
    "everyday", "pet", "food", "landscape", "family_event", "other"
]

# Default device detection
def detect_device():
    """Detect the best available device for inference."""
    try:
        import torch
        if torch.cuda.is_available():
            return "cuda"
        if sys.platform == "darwin" and torch.backends.mps.is_available():
            return "mps"
    except ImportError:
        pass
    return "cpu"

class PhotoCategorizerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Family Photo Categorizer")
        master.geometry("720x540")
        master.resizable(True, True)

        # Variables
        self.source_var = tk.StringVar(value="")
        self.dest_var = tk.StringVar(value="")
        self.device_var = tk.StringVar(value=detect_device())
        self.cat_var = tk.StringVar(value=" ".join(DEFAULT_CATEGORIES))  # default categories
        self.is_processing = False
        self.process_thread = None

        self._build_ui()

    def _build_ui(self):
        # Header
        header = tk.Label(
            self.master,
            text="Family Photo Categorizer\nOrganize your photos with local AI",
            font=("Segoe UI", 14, "bold"),
            pady=10,
        )
        header.pack()

        # Source folder selector
        src_frame = ttk.LabelFrame(self.master, text="📁 Folder with Photos")
        src_frame.pack(fill="x", padx=10, pady=5)
        src_inner = ttk.Frame(src_frame)
        src_inner.pack(fill="x", padx=5, pady=5)
        ttk.Entry(src_inner, textvariable=self.source_var, width=55, state="readonly").pack(side="left", padx=5)
        ttk.Button(src_inner, text=" Choose Folder ", command=self.select_source).pack(side="right", padx=5)

        # Destination folder selector
        dst_frame = ttk.LabelFrame(self.master, text="📂 Output Folder")
        dst_frame.pack(fill="x", padx=10, pady=5)
        dst_inner = ttk.Frame(dst_frame)
        dst_inner.pack(fill="x", padx=5, pady=5)
        ttk.Entry(dst_inner, textvariable=self.dest_var, width=55, state="readonly").pack(side="left", padx=5)
        ttk.Button(dst_inner, text=" Choose Folder ", command=self.select_dest).pack(side="right", padx=5)

        # Custom categories entry
        cat_frame = ttk.LabelFrame(self.master, text="🏷 Custom Categories")
        cat_frame.pack(fill="x", padx=10, pady=5)
        cat_inner = ttk.Frame(cat_frame)
        cat_inner.pack(fill="x", padx=5, pady=5)
        ttk.Label(cat_inner, text="Enter categories (space separated):").pack(side="left", padx=5)
        ttk.Entry(cat_inner, textvariable=self.cat_var, width=70).pack(side="left", padx=5)

        # Device selection
        device_frame = ttk.LabelFrame(self.master, text="⚙ Options")
        device_frame.pack(fill="x", padx=10, pady=5)
        dev_inner = ttk.Frame(device_frame)
        dev_inner.pack(padx=5, pady=5)
        ttk.Label(dev_inner, text="Processing Device:").pack(side="left", padx=5)
        device_combo = ttk.Combobox(
            dev_inner,
            textvariable=self.device_var,
            values=["cpu", "cuda", "mps"],
            state="readonly",
            width=10,
        )
        device_combo.pack(side="left", padx=5)
        device_tooltip = "cpu = slowest but works everywhere\ncuda = fastest (NVIDIA GPU)\nmps = Apple Silicon (M1/M2/M3)"



        # Progress bar and log output
        self.progress = ttk.Progressbar(self.master, mode="determinate")
        self.progress.pack(fill="x", padx=10, pady=5)
        self.progress_label = ttk.Label(self.master, text="Ready.")
        self.progress_label.pack(pady=5)

        log_frame = ttk.LabelFrame(self.master, text="📝 Log")
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.log_box = scrolledtext.ScrolledText(log_frame, height=10, state="disabled", wrap="word")
        self.log_box.pack(fill="both", expand=True, padx=5, pady=5)

        # Start / Stop buttons
        button_frame = ttk.Frame(self.master)
        button_frame.pack(pady=10)
        self.start_btn = ttk.Button(button_frame, text="Start Categorizing", command=self.start_process)
        self.start_btn.pack(side="left", padx=10)
        self.stop_btn = ttk.Button(button_frame, text="Stop", command=self.stop_process, state="disabled")
        self.stop_btn.pack(side="left", padx=10)

    def select_source(self):
        folder = filedialog.askdirectory(title="Select folder with photos")
        if folder:
            self.source_var.set(folder)
            if not self.dest_var.get():
                self.dest_var.set(str(Path(folder).parent / "Categorized"))

    def select_dest(self):
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            self.dest_var.set(folder)

    def log(self, msg):
        self.log_box.config(state="normal")
        self.log_box.insert("end", msg + "\n")
        self.log_box.see("end")
        self.log_box.config(state="disabled")

    def start_process(self):
        src = self.source_var.get()
        dst = self.dest_var.get()
        if not src or not Path(src).exists():
            messagebox.showerror("Error", "Please select a valid folder with photos.")
            return
        if not dst:
            messagebox.showerror("Error", "Please select an output folder.")
            return
        if self.is_processing:
            messagebox.showwarning("Warning", "Processing is already running.")
            return

        # Get custom categories from the entry field
        categories_input = self.cat_var.get().strip()
        categories = categories_input.split() if categories_input else DEFAULT_CATEGORIES

        self.is_processing = True
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.log(f"Starting categorization...")
        self.log(f"Source: {src}")
        self.log(f"Output: {dst}")
        self.log(f"Device: {self.device_var.get()}")
        self.log(f"Custom categories: {categories}")

        self.process_thread = threading.Thread(
            target=self._run_script, args=(src, dst, categories), daemon=True
        )
        self.process_thread.start()

    def _run_script(self, src, dst, categories):
        try:
            cmd = [
                sys.executable, "-u",
                os.path.join(os.path.dirname(sys.argv[0]), "main.py"),
                "--source", src,
                "--dest", dst,
                "--device", self.device_var.get(),
            ]
            # Add custom categories if any
            if categories:
                cmd.extend(["--categories"] + categories)

            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
            )

            for line in process.stdout:
                self.log(line.strip())

            process.wait()
            if process.returncode == 0:
                self.log("\n✅ Done! Your photos have been categorized successfully.")
            else:
                self.log(f"\n❌ Process exited with code {process.returncode}. Check the log for errors.")
        except Exception as exc:
            self.log(f"\n❌ Error running script: {exc}")
        finally:
            self.is_processing = False
            self.master.after(0, self._reset_ui)

    def _reset_ui(self):
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.progress.stop()
        self.progress_label.config(text="Ready.")

    def stop_process(self):
        if self.process_thread and self.process_thread.is_alive():
            if messagebox.askyesno("Stop", "Stopping will interrupt the current categorization.\nAre you sure?"):
                self.log("\n⚠ Stop requested. Please wait for current image to finish.")
                self.log("To fully stop, close this window and re-run the program.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoCategorizerGUI(root)
    root.mainloop()