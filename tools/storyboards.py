import concurrent.futures
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
manifest = json.loads((ROOT/'assets.json').read_text())
videos = [x for x in manifest['assets'] if x['type']=='video' and x['status']=='downloaded']

def build(item):
    source = ROOT/item['path']
    info = json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(source)]))
    duration = float(info['format']['duration'])
    video = next(s for s in info['streams'] if s['codec_type']=='video')
    item['durationSeconds'] = duration
    item['width'], item['height'] = video['width'], video['height']
    folder = ROOT/'frames'/item['id']
    folder.mkdir(parents=True, exist_ok=True)
    times = [duration*i/8 for i in range(8)]
    for i,time in enumerate(times):
        target=folder/f'{i:02d}-{time:.3f}s.png'
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(time),'-i',str(source),'-frames:v','1','-vf','scale=640:480:force_original_aspect_ratio=decrease,pad=640:480:(ow-iw)/2:(oh-ih)/2:color=0x17191f','-threads','1',str(target)],check=True)
    target=ROOT/'sheets'/f'{item["id"]}.png'
    target.parent.mkdir(exist_ok=True)
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-framerate','1','-pattern_type','glob','-i',str(folder/'*.png'),'-vf','scale=384:288,tile=4x2:padding=8:margin=12:color=0x101115','-frames:v','1','-threads','1',str(target)],check=True)
    item['storyboard']=str(target.relative_to(ROOT))
    item['frames']=[{'path':str(p.relative_to(ROOT)),'timeSeconds':time} for p,time in zip(sorted(folder.glob('*.png')),times)]
    print(item['id'],item['title'],round(duration,2),'s',flush=True)
    return item

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results=list(pool.map(build,videos))
mapping={x['id']:x for x in results}
manifest['assets']=[mapping.get(x['id'],x) for x in manifest['assets']]
(ROOT/'assets.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print('Storyboards:',len(results),'Frames:',sum(len(x['frames']) for x in results),flush=True)
