import asyncio
'top-right': 'main_w-overlay_w-10:10',
'bottom-left': '10:main_h-overlay_h-10',
'bottom-right': 'main_w-overlay_w-10:main_h-overlay_h-10'
}[position]
cmd = (
f'ffmpeg -y -i {shlex.quote(input_video)} -i {shlex.quote(watermark_image)} '
f'-filter_complex "[1]format=rgba,scale=iw:ih[wm];[0][wm]overlay={x}:{y}" '
f'-c:a copy -c:v libx264 -preset {preset} -crf {crf} {shlex.quote(out_file)}'
)
return cmd




def build_text_overlay_cmd(
input_video: str,
out_file: str,
text: str,
fontfile: Optional[str] = None,
fontsize: int = 24,
fontcolor: str = 'white',
position: str = 'center',
movement: Optional[str] = None, # 'left-right' or 'top-bottom' or None
preset: str = 'superfast',
crf: int = 23,
) -> str:
# Escape text for drawtext
esc_text = text.replace("\n", "\\n").replace("'", "\\'")
# x and y expressions
if position == 'center':
x_expr = '(w-text_w)/2'
y_expr = '(h-text_h)/2'
elif position == 'top-left':
x_expr = '10'
y_expr = '10'
elif position == 'top-right':
x_expr = 'w-text_w-10'
y_expr = '10'
elif position == 'bottom-left':
x_expr = '10'
y_expr = 'h-text_h-10'
else: # bottom-right
x_expr = 'w-text_w-10'
y_expr = 'h-text_h-10'


if movement == 'left-right':
# move horizontally across the screen over duration
x_expr = "'if(gt(t,0), mod( (w+text_w) * t/ max(1,n_forced), w+text_w)-text_w , %s)" % x_expr
# simpler: use t to move at fixed speed
if movement == 'top-bottom':
y_expr = "'if(gt(t,0), mod( (h+text_h) * t/ max(1,n_forced), h+text_h)-text_h , %s)" % y_expr


fontopt = f":fontfile={fontfile}" if fontfile else ''


drawtext = (
f"drawtext=text='{esc_text}':fontsize={fontsize}:fontcolor={fontcolor}{fontopt}:x={x_expr}:y={y_expr}"
)


cmd = (
f"ffmpeg -y -i {shlex.quote(input_video)} -vf \"{drawtext}\" -c:a copy -c:v libx264 -preset {preset} -crf {crf} {shlex.quote(out_file)}"
)
return cmd
