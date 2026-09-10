# Family Photo Categorizer — Design Document

**Project**: Local Family Photo Classification using a Local Multimodal LLM  
**Author**: Hermes AI Agent  
**Date**: 2026-09-10  
**Platform**: Windows (Python 3.10+)

---

## 1. Purpose

Design a Python-based local program that automatically categorizes family photos (birthday, vacation, wedding, everyday, pet, food, landscape, family_event, other) using a **local multimodal large language model (LLM)** — without requiring any cloud or external API.

## 2. Overview & Motivation

| Aspect | Detail |
|--------|--------|
| **Problem** | Families accumulate thousands of photos with no organization. Manual sorting is time-consuming and error-prone. |
| **Solution** | A local Python program that uses a vision-language LLM to inspect each photo and assign it a category, then organizes the photos into categorized folders. |
| **Key Benefit** | Full privacy — all processing happens locally. No photos leave the user's machine. |

## 3. System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE (CLI)                        │
│            python main.py --source ./photos --dest ./organized      │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       ARGUMENT PARSER (argparse)                    │
│  source │ dest │ model │ categories │ device                 │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        IMAGE SCANNER                                │
│  Walks source folder → collects files with supported extensions     │
│  (.jpg, .jpeg, .png, .gif, .bmp, .tiff, .webp)                     │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    LOCAL LLM CLASSIFIER                             │
│  ┌──────────────────────┐    ┌──────────────────────────────┐      │
│  │  Vision-Language LLM │    │  Prompt + Category List       │      │
│  │  (e.g., Qwen2.5-VL) │───▶│  "Look at this photo. Choose │      │
│  │  (local inference)  │    │  one category:"               │      │
│  └──────────────────────┘    └──────────────────────────────┘      │
│                                │                                    │
│                                ▼                                    │
│                          Category Label                             │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      FILE ORGANIZER                                 │
│  Creates dest/<category>/ if needed                                 │
│  Copies the image to the category folder (source never changed)      │
│  Handles name collisions (original_1.jpg, original_2.jpg, ...)      │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       LOGGER & REPORT                               │
│  Progress messages, warnings, and error summaries to stdout         │
└─────────────────────────────────────────────────────────────────────┘
```

## 4. Component Design

### 4.1. Core Modules

| Module | Responsibility | Key Functions |
|--------|---------------|---------------|
| `LocalLLMClassifier` | Load and query the local multimodal LLM | `_load_model()`, `classify(image_path)` |
| `ImageScanner` | Discover image files recursively | `gather_images(source_dir)` |
| `FileOrganizer` | Create category folders and move/copy files | `organize(image_path, category)` |
| `Logger` | Unified logging | `info()`, `warning()`, `error()` |
| `CLI` | Argument parsing and orchestration | `main()` |

### 4.2. Classification Workflow

1. **Load Image** → `PIL.Image.open(path).convert("RGB")`
2. **Build Prompt** → `"Look at this family photo and choose the best category from: {category_list}. Answer with only one category word."`
3. **Generate Output** → Vision-language model processes image + text
4. **Parse Response** → Extract category string, match against known list
5. **Fallback** → If match fails, return `"other"`

### 4.3. File Organization Logic

```
dest/
├── birthday/
│   ├── img_001.jpg
│   └── img_042.png
├── vacation/
│   └── beach_trip.jpeg
├── wedding/
│   └── ceremony.jpg
└── other/
    └── unidentified.png
```

- If a file with the same name already exists in the target folder, append `_1`, `_2`, etc. before the extension.

## 5. Technology Stack

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| **Language** | Python 3.10+ | Cross-platform, rich ecosystem |
| **LLM Backend** | Hugging Face `transformers` | Supports vision-language models, well-documented |
| **Image Loading** | `Pillow` (PIL) | Lightweight, reliable image handling |
| **Deep Learning** | `torch` | GPU/CPU inference backend |
| **Model Format** | Hugging Face model hub | Easy download and local caching |
| **CLI** | `argparse` | Standard library, no extra dependency |
| **Logging** | `logging` | Standard library, configurable |
| **File Operations** | `shutil`, `os` | Standard library |

### 5.1. Recommended Local Models (Updated — 3 Useful Options)

| # | Model | Params | Download ≈ | VRAM (FP16) | CPU / Low VRAM | Best For | Beginner Note |
|---|-------|--------|-----------|-------------|----------------|----------|---------------|
| **1** | `Qwen/Qwen2.5-VL-3B-Instruct` (primary) | 3B | ~6 GB | ~6 GB GPU | Works on CPU (~5-10 img/min) | Accuracy + speed balance | **Best for beginners** — small, reliable, works without GPU |
| **2** | `microsoft/Phi-3-vision-128k-instruct` | 3.8B | ~7.7 GB | ~8 GB GPU / ~7 GB RAM | Optimized ONNX-CPU version exists | Very high instruction accuracy; 128K context | Good if you have 8-16 GB RAM; slower on pure CPU |
| **3** | `llava-v1.5-7b-hf` | 7B | ~15 GB | ~15 GB GPU | Needs GPU or long CPU time | Strong vision + reasoning | **Advanced users only** — needs GPU (RTX 3060+ / 16 GB VRAM) |

### LLM Requirements Breakdown (Real-World)

**Qwen2.5-VL-3B (Recommended)**
- **Hardware**: GPU with 6 GB VRAM (RTX 3060, RTX 4060) or 16 GB system RAM for CPU
- **Download**: ~6 GB (cached in `~/.cache/huggingface/`)
- **First load**: 10-30 sec (model download + warm-up)
- **Speed**: GPU ~15-25 img/min; CPU ~5-10 img/min
- **Quantized options**: `Q4_K_M` via Ollama / GGUF drops to ~4 GB VRAM if needed

**Phi-3 Vision (Alternative)**
- **Hardware**: 8 GB VRAM or 16 GB RAM (ONNX-CPU optimized)
- **Download**: ~7.7 GB
- **Strength**: Follows category instructions very precisely; good for strict classification
- **Limitation**: Slightly slower than Qwen3 on CPU; 128K context is overkill for photo labels

**LLaVA-1.5 7B (High Quality / High Cost)**
- **Hardware**: ~15 GB VRAM (FP16) → needs RTX 4080 / 4090 / 3090; quantized (INT4) works on 8 GB
- **Download**: ~15 GB (full) / ~4 GB (Q4_K_M quantized)
- **Strength**: Best vision reasoning; handles complex scenes (multiple people + objects)
- **Limitation**: Heavy for family albums (thousands of images); use only if accuracy is critical and GPU is available

### 5.2. Device Support

| Device | Backend | Notes |
|--------|---------|-------|
| `cpu` | PyTorch CPU | Works everywhere, slower |
| `cuda` | CUDA | Requires NVIDIA GPU + cuDNN |
| `mps` | Metal Performance Shaders | Apple Silicon (M1/M2/M3/M4) |

## 6. Command-Line Interface (CLI)

```
usage: main.py [-h] [--source SOURCE] [--dest DEST] [--model MODEL]
               [--categories [CATEGORIES ...]] [--device {cpu,cuda,mps}]
```

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--source` | `str` | `.` | Source folder with images |
| `--dest` | `str` | `categorized` | Destination folder for organized photos |
| `--model` | `str` | `Qwen/Qwen2.5-VL-3B-Instruct` | Local model path or HF model ID |
| `--categories` | `list[str]` | `['birthday', 'vacation', ...]` | Custom category list |
| `--device` | `str` | `cpu` | Inference device |

## 7. Categories Design

### 7.1. Default Category Set

```python
DEFAULT_CATEGORIES = [
    "birthday",      # Birthday parties, celebrations
    "vacation",      # Travel, holidays, trips
    "holiday",       # Seasonal/cultural holidays (Christmas, New Year)
    "wedding",       # Weddings, engagements, anniversaries
    "everyday",      # Daily life, routine moments
    "pet",           # Pets and animals
    "food",          # Meals, cooking, dining
    "landscape",     # Nature, scenery, architecture
    "family_event",  # Gatherings, reunions, parties
    "other",         # Anything that doesn't fit above
]
```

### 7.2. Customization

Users can override categories via CLI or the GUI text field:
```bash
python main.py --categories birthday vacation wedding everyday pet food
```

## 8. Error Handling & Resilience

| Scenario | Behavior |
|----------|----------|
| Image cannot be opened | Log warning, skip to next image |
| LLM returns unrecognized category | Default to `"other"` |
| File name collision | Append `_1`, `_2`, etc. |
| Model loading fails | Raise error, exit with message |
| Source folder missing | Log error, exit with code 1 |
| Insufficient disk space | Log error, skip file |

## 9. Performance Considerations

| Factor | Design Decision |
|--------|----------------|
| **Batch Processing** | Images processed one-by-one to limit memory usage |
| **GPU Memory** | Model loaded once, reused for all images |
| **Disk I/O** | Copy operation (not move) to preserve originals |
| **Logging** | Async-friendly, minimal I/O overhead |
| **Startup Time** | Model loaded once at start; first image may take longer |

### Estimated Performance (Qwen2.5-VL-3B)

| Device | Images per Minute | Notes |
|--------|-------------------|-------|
| GPU (RTX 3060) | ~30-50 images/min | First image ~5s, subsequent ~1-2s |
| CPU (i7-12700) | ~5-10 images/min | ~5-10s per image |
| Apple M2 | ~15-25 images/min | Good thermal efficiency |

## 10. Security & Privacy

- **No data leaves the machine** — all inference happens locally
- **No network calls** after model download
- **No telemetry** or external logging
- **Local model files** stored in user's cache directory
- **User controls** source/destination paths explicitly

## 11. Testing Strategy

### 11.1. Unit Tests
- `test_classification.py` — Verify LLM output matches expected categories
- `test_file_organizer.py` — Verify folder creation and file movement
- `test_scanner.py` — Verify image discovery logic

### 11.2. Integration Tests
- Process a sample folder of 10-20 images
- Verify all images are categorized and placed correctly
- Check log output for errors

### 11.3. Edge Cases
- Empty source folder
- Single image
- Duplicate filenames
- Corrupted image files
- Very large images (>10MB)

## 12. Future Enhancements

| Enhancement | Description |
|-------------|-------------|
| **Batch API** | Option to send multiple images per prompt for throughput |
| **Progress Bar** | `tqdm` integration for visual progress |
| **SQLite Index** | Store metadata (category, date, confidence) in a local database |
| **GUI** | Tkinter/PyQt interface for non-technical users |
| **Face Recognition** | Group photos by detected faces using local face detection |
| **EXIF Integration** | Use photo metadata (date, location) alongside LLM classification |
| **Config File** | YAML/JSON config for categories, model, paths |
| **Scheduled Run** | Watch folder mode — auto-process new images |

## 13. Dependencies

| Package | Purpose | Version |
|---------|---------|---------|
| `torch` | Deep learning framework | >=2.0 |
| `transformers` | Hugging Face model loading | >=4.30 |
| `Pillow` | Image processing | >=10.0 |
| `tqdm` | Progress bars | >=4.65 |

**Install command**:
```bash
python -m pip install torch transformers Pillow tqdm
```

## 14. File Manifest

```
C:\HermesAIAgent\Dinh\GiaDinhPhotos\
├── design.md              # This design document
├── main.py                # Application entry point
├── requirements.txt       # Python dependencies
├── README.md              # User-facing documentation
├── .gitignore             # Ignore __pycache__, .env, etc.
├── src/
│   ├── __init__.py
│   ├── classifier.py      # LocalLLMClassifier class
│   ├── scanner.py         # Image discovery
│   ├── organizer.py       # File operations
│   ├── config.py          # Configuration management
│   └── utils.py           # Helper functions
├── tests/
│   ├── __init__.py
│   ├── test_classifier.py
│   ├── test_organizer.py
│   └── test_scanner.py
├── sample_photos/         # Test images
└── categorized/           # Output folder (created on run)
```

## 15. Glossary

| Term | Definition |
|------|-----------|
| **LLM** | Large Language Model |
| **Vision-Language Model** | LLM that can process both images and text |
| **Multimodal** | Capable of understanding multiple data types (images, text, audio) |
| **Hugging Face** | Platform for sharing and hosting ML models |
| **Transformers** | Hugging Face library for transformer-based models |
| **CUDA** | NVIDIA's parallel computing platform |
| **MPS** | Apple's Metal Performance Shaders (GPU backend) |

---

*Document version: 1.0 | Last updated: 2026-09-10*
-e "\n---\n## 10. Recent Design Updates (2026-09-10)\n\n- **Source Safety**: Source folder is read-only. Only copies are made; no `--move` option exists.\n- **GUI Categories**: Added `gui.py` text field for user-defined categories (space-separated).\n- **CLI Simplified**: Removed `--move` flag; `copy=True` is fixed behavior.\n- **Immute Source Guarantee**: Architecture and all docs updated to clarify source photos are never changed, moved, or deleted." 

---
## 11. Future Feature Designs (Proposed Additions)

| Feature | Status | Design Notes |
|---------|--------|--------------|
| **Progress Bar** | Planned | `tqdm` integration in `process_folder()`; show image count / total, estimated time, and category breakdown. Keeps CLI and GUI responsive. |
| **SQLite Index** | Planned | Local `photos.db` (SQLite) storing: image_path, category, date_taken, confidence_score, face_ids (if enabled), exif_location. Enables fast search / filtering without re-classifying. |
| **GUI** | Implemented | `gui.py` uses `tkinter`. Adds folder browsers, category entry, device selector, log window, Start/Stop buttons. Planned upgrade: `PyQt6` for richer widgets, drag-and-drop, thumbnail previews. |
| **Face Recognition** | Planned | Local face detection (e.g., `face_recognition`, `insightface`, or `mediapipe`) runs before/after LLM classification. Results stored in SQLite `face_ids`. Grouping mode: copy into `family_event/` if face count >= 2, or create `family/<name>/` folders. No cloud APIs. |
| **EXIF Integration** | Planned | Use `PIL.ExifTags` / `piexif` to read `DateTime`, `GPSInfo`, `Make/Model`. Combine with LLM output: if EXIF date is 2025-12-25 and LLM says `holiday`, boost confidence / tag `holiday_christmas`. Use date for folder naming (`vacation_2025/`). |
| **Scheduled Run** | Planned | `watchdog` library monitors source folder. On `FileCreatedEvent`, enqueue image for processing. Mode options: `once` / `interval` (every 1h) / `continuous`. Runs as Windows service or background tray icon. |

### 11.1. Progress Bar Design
- Module: `progress.py`
- Integrate `from tqdm.auto import tqdm` into `process_folder()` loop.
- Update both CLI (terminal bar) and GUI (progress bar widget + percentage label).
- Show: `N / M [time left] [current file] [current category]`

### 11.2. SQLite Index Design
- Schema (`photos.db`):
  - `photos(id, path, category, confidence, date_exif, face_ids_json, created_at)`
  - `categories(name, count, last_used)`
- Functions: `index_photo()`, `search_by_category()`, `get_stats()`, `export_csv()`
- Used by GUI for "Search / Filter" pane and by scheduled run to skip already-processed files.

### 11.3. GUI Design (Formal)
- Technology: `tkinter` (default) → `PyQt6` (future)
- Components: Source/Dest selectors, Category text entry, Device dropdown, Copy/Move toggle (currently fixed to Copy), Log window, Start/Stop, Preview thumbnail (optional).
- State management: `threading` for processing, `queue.Queue` for image processing pipeline.

### 11.4. Face Recognition Design
- Library: `mediapipe` or `face_recognition` (local only)
- Pipeline: Load image → detect faces → encode faces → compare with known embeddings (stored in `faces.db` SQLite table) → assign `face_ids`.
- If new face: prompt user via GUI ("Name this face?") or auto-label `person_001`.
- Integration with categories: if face_ids contains >= 2 entries → category `family_event`.

### 11.5. EXIF Integration Design
- Library: `Pillow` (`Image._getexif()`) + `piexif`
- Extract: `DateTimeOriginal`, `GPSLatitude/Longitude`, `ImageDescription`.
- Use `date_exif` for sorting into `YYYY-MM/` subfolders or tagging.
- Combine with LLM: prompt can include EXIF info (e.g., "Photo taken 2024-07-20 at beach" → stronger `vacation` signal).

### 11.6. Scheduled Run Design
- Library: `watchdog.observers.Observer`
- Modes:
  - `one_time`: process then exit
  - `watch`: continuous loop with `Observer` thread
  - `cron`: scheduled via `schedule` library (every hour/day)
- GUI addition: "Start Watch Mode" button; tray icon to pause/resume.
- SQLite index prevents duplicate processing by checking `path` hash.
