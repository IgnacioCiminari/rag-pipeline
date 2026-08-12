# Compatibility layer for deepdoc to run standalone outside of RAGFlow.

import os
import re
import asyncio
import logging
from io import BytesIO
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

MAXIMUM_PAGE_NUMBER = 10000

# Thread Pool for background execution in async methods
_default_executor = ThreadPoolExecutor()

async def thread_pool_exec(fn, *args, **kwargs):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(_default_executor, lambda: fn(*args, **kwargs))

def get_project_base_directory():
    # Return the parent folder of deepdoc, i.e., the pipeline root
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Simple tokenizer approximation
class RagTokenizer:
    @staticmethod
    def tokenize(text):
        if not text:
            return ""
        # Basic regex-based splitting / cleaning
        text = re.sub(r'\s+', ' ', text)
        return text

    @staticmethod
    def tag(word):
        if word.isalpha():
            return "n"
        return "other"

    @staticmethod
    def is_chinese(text):
        if not text:
            return False
        return ord(text[0]) >= 0x4e00 and ord(text[0]) <= 0x9fff

    @staticmethod
    def tradi2simp(text):
        return text

    @staticmethod
    def strQ2B(text):
        return text

    @staticmethod
    def fine_grained_tokenize(text):
        return RagTokenizer.tokenize(text)

rag_tokenizer = RagTokenizer()
surname = []

def find_codec(blob):
    try:
        from charset_normalizer import detect
        res = detect(blob[:8192])
        if res and res['encoding']:
            return res['encoding']
    except Exception:
        pass
    
    for codec in ["utf-8", "gbk", "gb18030", "utf-16", "latin1", "cp1252"]:
        try:
            blob[:1024].decode(codec)
            blob.decode(codec)
            return codec
        except Exception:
            continue
    return "utf-8"

# Image processing helpers
class LazyImage:
    def __init__(self, blobs, source=None):
        self._blobs = [b for b in (blobs or []) if b]
        self.source = source
        self._pil = None

    def __bool__(self):
        return bool(self._blobs)

    def to_pil(self):
        if self._pil is not None:
            try:
                self._pil.load()
                return self._pil
            except Exception:
                try:
                    self._pil.close()
                except Exception:
                    pass
                self._pil = None
        res_img = None
        for blob in self._blobs:
            try:
                image = Image.open(BytesIO(blob)).convert("RGB")
            except Exception as e:
                logging.info(f"LazyImage: skip bad image blob: {e}")
                continue
            if res_img is None:
                res_img = image
            else:
                # Vertical concatenation
                w1, h1 = res_img.size
                w2, h2 = image.size
                new_img = Image.new("RGB", (max(w1, w2), h1 + h2))
                new_img.paste(res_img, (0, 0))
                new_img.paste(image, (0, h1))
                res_img = new_img
        self._pil = res_img
        return self._pil

def ensure_pil_image(image):
    if isinstance(image, Image.Image):
        return image
    if isinstance(image, LazyImage):
        return image.to_pil()
    import numpy as np
    if isinstance(image, np.ndarray):
        if image.dtype != np.uint8:
            if image.dtype in (np.float32, np.float64) and image.max() <= 1.0:
                image = (image * 255).astype(np.uint8)
            else:
                image = image.astype(np.uint8)
        # Squeeze leading dimensions of size 1 if it makes it 3D, though (1,1,3) is valid height=1, width=1, channels=3
        return Image.fromarray(image)
    if isinstance(image, bytes):
        return Image.open(BytesIO(image)).convert("RGB")
    return image

def is_image_like(image):
    if isinstance(image, (Image.Image, LazyImage)):
        return True
    import numpy as np
    if isinstance(image, np.ndarray):
        return True
    if isinstance(image, bytes):
        return True
    return False

def open_image_for_processing(image, allow_bytes=False):
    return ensure_pil_image(image), False

# Vision LLM & prompt dummies
class LLMType:
    IMAGE2TEXT = "image2text"
    CHAT = "chat"

def timeout(seconds=10, retries=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator

def vision_llm_chunk(*args, **kwargs):
    return ""

def vision_llm_describe_prompt(*args, **kwargs):
    return "Describe the image."

def vision_llm_figure_describe_prompt(*args, **kwargs):
    return "Describe the figure."

def vision_llm_figure_describe_prompt_with_context(*args, **kwargs):
    return "Describe the figure with context."

def append_context2table_image4pdf(*args, **kwargs):
    return []

# Config / settings dummies
class Settings:
    PARALLEL_DEVICES = 0

settings = Settings()

def pip_install_torch(*args, **kwargs):
    pass

def get_base_config(config_name, default=None):
    return default or {}

def num_tokens_from_string(text):
    try:
        import tiktoken
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text, disallowed_special=()))
    except Exception:
        return len(text) // 4 + 1

def traversal_files(inputs):
    file_list = []
    if os.path.isdir(inputs):
        for root, dirs, files in os.walk(inputs):
            for file in files:
                file_list.append(os.path.join(root, file))
    else:
        file_list.append(inputs)
    return file_list
