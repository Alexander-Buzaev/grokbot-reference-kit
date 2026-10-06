"""Generate remote reference gallery, or local gallery after downloading assets."""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
parser = argparse.ArgumentParser()
parser.add_argument('--local', action='store_true')
args = parser.parse_args()
subprocess.run([sys.executable, str(ROOT/'tools/local_gallery.py')], check=True)
if args.local:
    raise SystemExit(0)
page = (ROOT/'index.html').read_text()
page = re.sub(r'<details>.*?</details>', '', page, flags=re.S)
page = re.sub(r'<a href="sheets/[^"]+"><img[^>]+></a>', '', page)
page = re.sub(r' · <a href="sheets/[^"]+" download>PNG раскадровка</a>', '', page)
for asset in json.loads((ROOT/'assets.json').read_text())['assets']:
    page = page.replace(asset['path'], asset['url'].replace('&', '&amp;'))
page = page.replace('29 раскадровок / 232 кадра', '29 раскадровок / 232 кадра — локальный экспорт')
page = page.replace('Сохранённый .riv', 'Исходный .riv')
page = page.replace('Ролики показываются из локальных копий. Для сравнения движения используйте воспроизведение; PNG-листы содержат восемь равномерно выбранных кадров, а не все ключевые позы. Происхождение и SHA-256 сохранены в assets.json.', 'Видео и изображения загружаются с исходных серверов авторов. В репозитории нет копий этих материалов. Для локальных раскадровок и кадров используйте скрипты из README. Ссылки могут перестать работать; происхождение и SHA-256 исходного сбора сохранены в assets.json.')
page = page.replace('Сохранённые материалы предназначены для изучения', 'Материалы по исходным ссылкам предназначены для изучения')
page = page.replace('runtime-сборка Rive и технические источники', 'ссылка на runtime-сборку Rive и технические источники')
for name in ['TASK.md','RESEARCH.md']:
    page = page.replace(f'href="{name}"',f'href="https://github.com/Alexander-Buzaev/grokbot-reference-kit/blob/main/{name}"')
(ROOT/'index.html').write_text(page)
