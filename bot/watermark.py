from pathlib import Path
from .utils import ensure_dir, LOG
from .ffmpeg_helpers import build_overlay_image_cmd, build_text_overlay_cmd, run_ffmpeg


BASE_TEMP = 'tmp'


async def save_user_image(user_id: int, src_path: str) -> str:
await ensure_dir(BASE_TEMP)
dest = Path(BASE_TEMP) / f'{user_id}_wm.png'
dest_str = str(dest)
try:
# move or copy file
Path(src_path).replace(dest)
except Exception:
import shutil
shutil.copy(src_path, dest_str)
LOG.info('Saved watermark image to %s', dest_str)
return dest_str


async def apply_image_watermark(input_video: str, watermark_image: str, out_file: str, **kwargs):
cmd = build_overlay_image_cmd(input_video, watermark_image, out_file, **kwargs)
code, stderr = await run_ffmpeg(cmd)
return code, stderr


async def apply_text_watermark(input_video: str, text: str, out_file: str, **kwargs):
cmd = build_text_overlay_cmd(input_video, out_file, text, **kwargs)
code, stderr = await run_ffmpeg(cmd)
return code, stderr
