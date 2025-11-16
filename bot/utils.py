
import os
import asyncio
import logging
from pathlib import Path


LOG = logging.getLogger("watermark_bot")
LOG.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
LOG.addHandler(handler)


async def remove_file(path: str):
try:
os.remove(path)
except Exception:
LOG.exception("Failed to remove %s", path)


async def ensure_dir(path: str):
Path(path).mkdir(parents=True, exist_ok=True)


def validate_crf(crf: int) -> int:
return max(0, min(51, crf))
