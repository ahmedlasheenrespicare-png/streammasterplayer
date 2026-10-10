"""Create a standalone HTML file with local assets embedded for offline UI preview."""
from pathlib import Path
import base64
import mimetypes

root = Path(__file__).resolve().parent
html = (root / 'index.html').read_text()
css = (root / 'style.css').read_text()
app = (root / 'app.js').read_text()
hls = (root / 'assets/hls.min.js').read_text()

html = html.replace('<link rel="stylesheet" href="style.css" />', '<style>\n' + css + '\n</style>')
html = html.replace('<script src="assets/hls.min.js" defer></script>', '<script>\n' + hls + '\n</script>')
html = html.replace('<script src="app.js" defer></script>', '<script>\n' + app + '\n</script>')

for asset in sorted((root / 'assets').rglob('*')):
    if not asset.is_file() or asset.suffix.lower() not in {'.svg', '.png', '.jpg', '.jpeg', '.webp', '.ttf'}:
        continue
    relative = asset.relative_to(root).as_posix()
    mime = mimetypes.guess_type(asset.name)[0] or 'application/octet-stream'
    data = base64.b64encode(asset.read_bytes()).decode('ascii')
    html = html.replace(relative, f'data:{mime};base64,{data}')

output = root.parent / 'Stream-Master-Player.html'
output.write_text(html)
print(f'{output}: {output.stat().st_size:,} bytes')
