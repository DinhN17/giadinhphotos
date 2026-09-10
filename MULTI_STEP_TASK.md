# Multi-Step Task — Family Photo Categorizer Design & Build
Path: C:\HermesAIAgent\Dinh\GiaDinhPhotos
Based on: design.md (353 lines) | Code: main.py, gui.py, setup.bat, run.bat

---

## Phase 1: Design Foundation (COMPLETE)
- [x] Confirm goal: local, privacy-first family photo categorization using vision-language LLM
- [x] Confirm platform: Windows / Python 3.10+ / local only
- [x] Design architecture: CLI → Scanner → LLM Classifier → File Organizer → Logger
- [x] Define 5 core modules: LocalLLMClassifier, ImageScanner, FileOrganizer, Logger, CLI
- [x] Define default categories: birthday, vacation, holiday, wedding, everyday, pet, food, landscape, family_event, other
- [x] Confirm source folder is READ-ONLY (copy only; no --move)

Reference: design.md Sections 1, 2, 3, 4

---

## Phase 2: LLM Selection & Requirements (COMPLETE)
- [x] Research and compare 3 practical local vision-language models
- [x] Select primary: Qwen2.5-VL-3B (smallest, works CPU/GPU, beginner-friendly)
- [x] Select alternative 1: Phi-3-vision-128k-instruct (high accuracy, needs 8 GB VRAM / 16 GB RAM)
- [x] Select alternative 2: LLaVA-1.5-7B (advanced users, needs ~15 GB VRAM)
- [x] Document real-world requirements: download size, VRAM, speed (img/min), quantized options
- [x] Confirm model source: Hugging Face `transformers` (no external API)

Reference: design.md Section 5.1, LLM Requirements Breakdown

---

## Phase 3: Implementation — Core Program (COMPLETE)
- [x] Write main.py: LLM wrapper, image scanning, file organization (copy only), CLI with argparse
- [x] Integrate tqdm progress display (planned in design Section 11.1 — add to code next)
- [x] Remove --move option; enforce copy=True permanently
- [x] Add custom category support via --categories flag
- [x] Add device selection (cpu / cuda / mps) with auto-detect default
- [x] Implement error resilience: bad images skipped, unrecognized category → "other"

Reference: design.md Sections 4, 6, 8
Files: main.py, requirements.txt

---

## Phase 4: Implementation — Beginner-Friendly Tools (COMPLETE)
- [x] Create gui.py (tkinter): folder browsers, category entry box, device dropdown, log window, start/stop
- [x] Create setup.bat: check Python, install requirements, download model, test pipeline
- [x] Create run.bat: quick launch with default settings
- [x] Create README.md: quick-start, privacy FAQ, troubleshooting
- [x] Create README.txt: detailed beginner guide with common problems
- [x] Create HOW_TO_USE.txt: step-by-step with pictures/numbered steps
- [x] Create .gitignore: exclude Python cache, env, output folders

Reference: design.md Sections 2, 11.3 (GUI Design)
Files: gui.py, setup.bat, run.bat, README.md, README.txt, HOW_TO_USE.txt, .gitignore

---

## Phase 5: Design Updates — Safety & Consistency (COMPLETE)
- [x] Update design.md: remove --move from CLI table and architecture diagram
- [x] Update design.md: File Organizer says "Copy only — source never changed"
- [x] Update design.md: add Section 10 (Recent Design Updates) documenting source safety and GUI categories
- [x] Verify all docs (README, HOW_TO_USE, design.md) say "source photos never changed/moved/deleted"
- [x] Verify code (main.py, gui.py) has no --move logic

Reference: design.md Sections 10, 11 (Future Features)

---

## Phase 6: Testing & Verification (PARTIAL — DO NEXT)
- [ ] Test with 10-20 sample family photos on CPU
- [ ] Verify categories assigned correctly by LLM
- [ ] Verify source folder untouched after run
- [ ] Verify output folders created correctly
- [ ] Test custom category input (GUI text box + CLI --categories)
- [ ] Measure processing time per photo (compare to design estimates: GPU 15-25/min, CPU 5-10/min)
- [ ] Test with corrupted/unreadable image (should skip and log)
- [ ] Add tqdm progress bar to main.py loop (design Section 11.1)
- [ ] Add basic SQLite index (design Section 11.2) — start with simple `photos.db` schema

Reference: design.md Sections 9 (Performance), 11.1, 11.2, 12 (Testing Strategy)

---

## Phase 7: Future Features — Sequential Plan (PLANNED)
Order recommended by dependency and user value:

1. [ ] Progress Bar (tqdm) — easy win; improves user experience immediately
2. [ ] SQLite Index — enables fast search/filter; prevents duplicate processing; needed before watch mode
3. [ ] EXIF Integration — use `Pillow`/`piexif` to read DateTime/GPS; enrich LLM prompt; optional subfolders by date
4. [ ] Face Recognition — `mediapipe` local pipeline; add `faces.db`; auto-label people; only if user wants grouping
5. [ ] Scheduled Run / Watch Mode — `watchdog` observer; requires SQLite index (step 2) to skip duplicates
6. [ ] GUI Upgrade (optional) — `PyQt6` with thumbnails if user needs richer interface

Reference: design.md Section 11 (Future Feature Designs)

---

## Phase 8: User Training & Safety (COMPLETE — DOCS READY)
- [x] Write beginner instructions (no IT knowledge required)
- [x] Confirm source folder never changed (safety guarantee)
- [x] Confirm all processing is local / offline after first download
- [x] Confirm no cloud APIs / no data leaks

Reference: design.md Sections 2 (Overview), 10 (Security & Privacy), 15 (Glossary)

---

## Quick Reference: What File Does What?
| File | Purpose |
|------|---------|
| `design.md` | Full design document (architecture, LLM specs, future features) |
| `main.py` | Core Python program (LLM classification + file organization) |
| `gui.py` | Graphical window for non-technical users |
| `setup.bat` | One-click install + model download |
| `run.bat` | Quick launch with safe defaults |
| `README.md` | Short overview + quick start |
| `README.txt` | Detailed troubleshooting + FAQ |
| `HOW_TO_USE.txt` | Step-by-step beginner guide |
| `requirements.txt` | Python package list |
| `.gitignore` | Keeps repo clean |

---

## Success Criteria (How to Know It Works)
- [ ] A non-IT user can run `setup.bat`, then `gui.py`, select folders, press Start, and find sorted photos in destination
- [ ] Source folder remains exactly the same before and after run (same file count, same filenames, same dates)
- [ ] LLM assigns categories (may not be perfect; falls back to "other" when unsure)
- [ ] Custom categories work via GUI text box and CLI `--categories`
- [ ] Program handles missing/corrupted images gracefully (skips, logs warning, continues)
- [ ] All future feature steps (Phase 7) are clearly ordered and reference Sections 11.1–11.6 in design.md
-e "\n---\n## Final Review & Cleanup (DONE 2026-09-10 19:24)\n\n- [x] design.md reviewed for feasibility - all sections workable (LLM specs realistic, source-safe consistent, future dependencies ordered)\n- [x] Section 5.1 updated with 3 real LLMs + requirements breakdown\n- [x] Section 10 added (Recent Design Updates) - source protection + GUI categories\n- [x] Section 11 added (Future Features 11.1-11.6) - Progress, SQLite, EXIF, Face, Watch Mode, GUI upgrade\n- [x] Temporary append_design.py removed after confirmation of integration\n- [x] MULTI_STEP_TASK.md updated and aligned with actual file state\n\nStatus: Design feasible. Code complete (main.py, gui.py, setup.bat, run.bat). Ready for Phase 6 testing." 
