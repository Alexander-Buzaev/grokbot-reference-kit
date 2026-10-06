"""Download the recorded public references for local study; never adds them to Git."""
import concurrent.futures
import hashlib
import json
import urllib.request
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
manifest = json.loads((ROOT/'assets.json').read_text())
def download(asset):
    path = (ROOT/asset['path']).resolve()
    if not path.is_relative_to(ROOT):
        raise ValueError('Path outside repository')
    request = urllib.request.Request(asset['url'], headers={'User-Agent': 'Mozilla/5.0', 'Referer':manifest['source']})
    try:
        data = path.read_bytes() if path.exists() else urllib.request.urlopen(request,timeout=45).read()
        if hashlib.sha256(data).hexdigest() != asset['sha256']:
            raise ValueError('Source changed; does not match recorded SHA-256')
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(data)
        asset['status'] = 'downloaded'
    except Exception as error:
        asset['status'] = 'failed'
        asset['error'] = str(error)
    print(asset['id'], asset['status'], flush=True)
    return asset
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    manifest['assets'] = list(pool.map(download,manifest['assets']))
(ROOT/'assets.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
failed = sum(x['status']=='failed' for x in manifest['assets'])
print('Failed:', failed)
raise SystemExit(1 if failed else 0)
