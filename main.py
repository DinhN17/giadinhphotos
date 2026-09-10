#!/usr/bin/env python3
"""
Family Photo Categorizer using a local multimodal LLM.

For non-technical users:
- Use the GUI (double-click gui.py) for the easiest experience
- The program processes photos one at a time and copies them
  into folders based on the AI's category labels.

Default behavior is designed to be safe:
- Copies photos instead of moving them
- Uses CPU by default (works on most computers)
- Falls back to "other" if the AI can't understand a photo

Requires:
- Python 3.10+
- torch
- transformers
- Pillow
"""

import os
import sys
import shutil
import logging
import argparse
import traceback
from pathlib import Path
from typing import List, Optional, Iterable

from PIL import Image

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("photo_categorizer")

# Predefined family photo categories (customizable)
DEFAULT_CATEGORIES = [
    "birthday",
    "vacation",
    "holiday",
    "wedding",
    "everyday",
    "pet",
    "food",
    "landscape",
    "family_event",
    "other",
]

# Supported image extensions
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}

# AI model that works well for photo categorization
DEFAULT_MODEL = "Qwen/Qwen2.5-VL-3B-Instruct"


class LocalLLMClassifier:
    """
    Wrapper around a local multimodal LLM for image classification.

    This class loads a vision-language model once, then uses it to
    categorize many photos. The model is loaded from a local path or
    downloaded from Hugging Face on first use.

    Parameters
    ----------
    model_path : str
        Path to local model files, or a Hugging Face model id.
    categories : list of str
        Allowed category labels.
    max_new_tokens : int
        Maximum characters/words to generate per image.
    device : str
        "cpu", "cuda", or "mps".
    """

    def __init__(
        self,
        model_path: str = DEFAULT_MODEL,
        categories: Optional[List[str]] = None,
        max_new_tokens: int = 30,
        device: str = "cpu",
    ):
        self.model_path = model_path
        self.categories = categories or DEFAULT_CATEGORIES
        self.max_new_tokens = max_new_tokens
        self.device = device
        self.processor = None
        self.model = None
        self._load_model()

    def _load_model(self):
        """Load the model and its processor (text/image conversion)."""
        logger.info("Loading local AI model: %s", self.model_path)
        try:
            from transformers import AutoProcessor, AutoModelForVision2Seq

            # Some models need remote code execution enabled
            trust_remote_code = True
            self.processor = AutoProcessor.from_pretrained(
                self.model_path,
                trust_remote_code=trust_remote_code,
            )
            self.model = AutoModelForVision2Seq.from_pretrained(
                self.model_path,
                trust_remote_code=trust_remote_code,
            ).to(self.device).eval()
            logger.info("AI model loaded successfully.")
        except ImportError:
            logger.error(
                "Missing dependency. Please run setup.bat first, or install: "
                "pip install torch transformers Pillow"
            )
            raise
        except Exception as exc:
            logger.error("Failed to load model: %s", exc)
            logger.error(
                "If this is the first run, the model may be downloading. "
                "If download fails, check your internet connection."
            )
            raise

    def classify(self, image_path: str) -> str:
        """
        Categorize one image.

        Returns
        -------
        str
            A category label from self.categories, or "other".
        """
        image_path = Path(image_path)
        if not image_path.exists():
            logger.error("Image not found: %s", image_path)
            return "other"

        try:
            # Load image and convert to RGB
            image = Image.open(image_path).convert("RGB")

            # Build a prompt that asks the AI to choose from our categories
            category_list = ", ".join(self.categories)
            prompt_text = (
                f"Look at this family photo and choose the best category from this list: "
                f"{category_list}. Answer with only one category word, nothing else."
            )

            # Convert image + text to model input format
            inputs = self.processor(
                text=prompt_text,
                images=image,
                return_tensors="pt",
            )

            # Move inputs to the selected device (GPU if available, otherwise CPU)
            inputs = {
                k: v.to(self.device) if hasattr(v, "to") else v
                for k, v in inputs.items()
            }

            # Generate a category label
            with __import__("torch").no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=self.max_new_tokens,
                    do_sample=False,
                )

            # Decode the generated text
            generated_text = self.processor.batch_decode(outputs, skip_special_tokens=True)[0]
            cleaned = generated_text.lower().strip().rstrip(".")

            # Try to match the AI's response to one of our categories
            for cat in self.categories:
                if cat.lower() in cleaned:
                    return cat

            # If no match, try the first word as a guess
            first_word = cleaned.split()[0] if cleaned.split() else "other"
            if first_word in [c.lower() for c in self.categories]:
                for c in self.categories:
                    if c.lower() == first_word:
                        return c

            # If nothing matched, use the safe default
            return "other"

        except Exception as exc:
            logger.warning("Classification failed for %s: %s", image_path, exc)
            return "other"


def gather_images(src_dir: str) -> List[Path]:
    """
    Recursively collect all image files from a source folder.

    Parameters
    ----------
    src_dir : str
        Path to source folder.

    Returns
    -------
    list of Path
        Sorted list of image paths.
    """
    src_path = Path(src_dir)
    image_files = []
    for root, _, files in os.walk(src_path):
        for f in files:
            ext = Path(f).suffix.lower()
            if ext in IMAGE_EXTENSIONS:
                image_files.append(Path(root) / f)
    return sorted(image_files)


def organize_file(src_path: Path, dest_dir: Path, category: str, copy: bool = True) -> Path:
    """
    Create the category folder and copy/move a file into it.

    Parameters
    ----------
    src_path : Path
        Source image path.
    dest_dir : Path
        Destination root folder.
    category : str
        Category label.
    copy : bool
        If True, copy the file. If False, move the file.

    Returns
    -------
    Path
        Final destination path.
    """
    category_dir = dest_dir / category
    category_dir.mkdir(parents=True, exist_ok=True)

    target_path = category_dir / src_path.name
    original_target = target_path
    counter = 1

    # If the file already exists, add a number before the extension
    while target_path.exists():
        stem = original_target.stem
        suffix = original_target.suffix
        target_path = category_dir / f"{stem}_{counter}{suffix}"
        counter += 1

    try:
        if copy:
            shutil.copy2(str(src_path), str(target_path))
        else:
            shutil.move(str(src_path), str(target_path))
    except Exception as exc:
        logger.error("File operation failed for %s: %s", src_path, exc)
        raise

    return target_path


def process_folder(
    src_dir: str,
    dest_dir: str,
    classifier: LocalLLMClassifier,
    copy: bool = True,
) -> int:
    """
    Process all images in a source folder.

    Parameters
    ----------
    src_dir : str
        Source folder.
    dest_dir : str
        Destination folder.
    classifier : LocalLLMClassifier
        AI classifier object.
    copy : bool
        If True, copy files. If False, move files.

    Returns
    -------
    int
        Number of successfully processed images.
    """
    src_path = Path(src_dir)
    dest_path = Path(dest_dir)

    if not src_path.exists():
        logger.error("Source folder does not exist: %s", src_path)
        raise FileNotFoundError(f"Source folder does not exist: {src_path}")

    if not src_path.is_dir():
        logger.error("Source path is not a folder: %s", src_path)
        raise NotADirectoryError(f"Source path is not a folder: {src_path}")

    dest_path.mkdir(parents=True, exist_ok=True)

    image_files = gather_images(src_dir)
    logger.info("Found %d image(s) in %s", len(image_files), src_path)

    if not image_files:
        logger.warning("No supported images found in %s", src_path)
        return 0

    processed = 0
    total = len(image_files)

    for idx, img_path in enumerate(image_files, start=1):
        logger.info("Processing %d/%d: %s", idx, total, img_path.name)
        try:
            category = classifier.classify(str(img_path))
            target_path = organize_file(img_path, dest_path, category, copy=copy)
            logger.info("✅ %s -> %s", img_path.name, category)
            processed += 1
        except Exception as exc:
            logger.error("Failed to process %s: %s", img_path, exc)

    logger.info("Done. Processed %d image(s).", processed)
    return processed


def detect_device() -> str:
    """
    Detect the best available device for AI inference.

    Returns
    -------
    str
        "cuda", "mps", or "cpu".
    """
    try:
        import torch
        if torch.cuda.is_available():
            return "cuda"
        if sys.platform == "darwin" and torch.backends.mps.is_available():
            return "mps"
    except Exception:
        pass
    return "cpu"


def main():
    parser = argparse.ArgumentParser(
        description="Categorize family photos with a local multimodal LLM."
    )
    parser.add_argument(
        "--source",
        type=str,
        default=".",
        help="Source folder with images (default: current directory)",
    )
    parser.add_argument(
        "--dest",
        type=str,
        default="categorized",
        help="Destination folder for categorized images (default: categorized/)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_MODEL,
        help=f"Local model path or HF model id (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--categories",
        type=str,
        nargs="*",
        default=DEFAULT_CATEGORIES,
        help="Custom category list",
    )
    parser.add_argument(
        "--device",
        type=str,
        default=detect_device(),
        choices=["cpu", "cuda", "mps"],
        help="Device for model inference (default: auto-detect)",
    )
    parser.add_argument(
        "--max-new-tokens",
        type=int,
        default=30,
        help="Maximum text length to generate per image (default: 30)",
    )
    args = parser.parse_args()

    try:
        classifier = LocalLLMClassifier(
            model_path=args.model,
            categories=args.categories,
            max_new_tokens=args.max_new_tokens,
            device=args.device,
        )
        process_folder(args.source, args.dest, classifier, copy=True)
    except Exception as exc:
        logger.error("ERROR: %s", exc)
        logger.error("If you are new to this program, please read README.txt.")
        logger.error("You can also run gui.py for a graphical interface.")
        logger.error("Full error details:")
        logger.debug(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
