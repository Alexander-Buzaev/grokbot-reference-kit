import html
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
manifest=json.loads((ROOT/'assets.json').read_text())
titles={
 '01':'Исходный персонаж и motion Benji Taylor', '03':'Notch-концепт John Bai',
 '12':'Mac notch во время работы', '14':'Mac greeting и раскрытие',
 '16':'Виджет от работы к завершению', '18':'Live Activity со сменой состояния',
 '20':'Follow', '22':'Annoyed', '24':'Slap', '26':'Dizzy', '28':'Upload', '30':'Error', '32':'Finished', '34':'Working',
 '36':'Схема логики в Figma', '37':'State machine в Rive',
 '38':'Развитие интерфейса виджета 1', '40':'Развитие интерфейса виджета 2',
 '42':'Lock Screen exploration 1', '43':'Lock Screen exploration 2',
 '44':'Другие исследования движения 3', '46':'Другие исследования движения 4',
 '48':'Другие исследования движения 5', '50':'Другие исследования движения 6', '52':'Другие исследования движения 7',
 '54':'Sketches', '55':'Vector explorations',
 '56':'Исследования характера и композиции', '57':'Исследования характера и композиции',
 '58':'Исследования характера и композиции', '59':'Исследования характера и композиции', '60':'Исследования характера и композиции',
 '61':'Персонаж в системе 6', '63':'Персонаж в системе 7', '65':'Персонаж в системе 8',
 '67':'Персонаж в системе 9', '69':'Персонаж в системе 10', '71':'Персонаж в системе 11',
 '73':'Персонаж в системе 12', '75':'Персонаж в системе 13',
 '05':'Размещение персонажа на разных поверхностях', '06':'Размещение персонажа',
 '07':'Размещение персонажа', '08':'Размещение персонажа',
 '09':'Интерфейс нескольких агентов', '10':'Интерфейс нескольких агентов', '11':'Интерфейс нескольких агентов'
}
for item in manifest['assets']:
 if item['id'] in titles:item['displayTitle']=titles[item['id']]
(ROOT/'assets.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
e=html.escape
videos=[x for x in manifest['assets'] if x['type']=='video']
images=[x for x in manifest['assets'] if x['type']=='image']
posters=[x for x in manifest['assets'] if x['type']=='poster']
def video_card(x):
 frames=x.get('frames',[])
 return f'''<article><h3>{x['id']} · {e(x.get('displayTitle',x['title']))}</h3><p>{e(x['group'])} · {x['durationSeconds']:.2f} s · {x['width']}×{x['height']}</p><video controls preload="none" src="{x['path']}" poster="{next((p['path'] for p in posters if int(p['id'])==int(x['id'])+1), '')}"></video><p><a href="{x['path']}" download>Исходное видео</a> · <a href="{e(x['url'])}" target="_blank">Источник</a> · <a href="{x['storyboard']}" download>PNG раскадровка</a></p><a href="{x['storyboard']}"><img loading="lazy" src="{x['storyboard']}" alt="Раскадровка"></a><details><summary>8 кадров с таймкодами</summary><div class="frames">{''.join(f'<figure><a href="{f["path"]}" download><img loading="lazy" src="{f["path"]}" alt="Кадр"></a><figcaption>{i+1} · {f["timeSeconds"]:.3f} s</figcaption></figure>' for i,f in enumerate(frames))}</div></details></article>'''
motion=[x for x in videos if x['id'] in ['20','22','24','26','28','30','32','34']]
other=[x for x in videos if x not in motion]
page=f'''<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>MYOR · Grokbot reference kit</title><style>html{{background:#111318;color:#eef0f5;font:16px/1.5 system-ui}}body{{max-width:1240px;margin:auto;padding:28px}}h1{{font-size:34px}}h2{{margin-top:48px}}p{{color:#b4bdcf}}a{{color:#a3c5ff}}nav{{display:flex;gap:18px;flex-wrap:wrap}}article{{background:#1b1f28;border-radius:12px;padding:20px;margin:20px 0}}img,video{{max-width:100%;height:auto;display:block}}video{{max-height:520px;margin:auto;background:#000}}.images{{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:16px}}.images article{{margin:0}}.frames{{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}}figure{{margin:0}}figcaption{{font-size:13px;color:#c1c9d9}}summary{{cursor:pointer;padding:12px 0}}.stats{{display:flex;gap:12px;flex-wrap:wrap}}.stats span{{padding:14px;background:#252b37;border-radius:8px}}@media(max-width:600px){{body{{padding:12px}}.images{{display:block}}.frames{{grid-template-columns:repeat(2,1fr)}}}}</style><h1>Grokbot · референсы и задача для MYOR</h1><p>06.10.2026 · Собраны публичные материалы кейса Novra, runtime-сборка Rive и технические источники для своего персонажа 1:1 в онбординге и чате.</p><div class="stats"><span>29 видео</span><span>18 изображений</span><span>29 постеров</span><span>1 Rive</span><span>29 раскадровок / 232 кадра</span></div><p><a href="TASK.md">Конкретная задача</a> · <a href="RESEARCH.md">Выводы и варианты интеграции</a> · <a href="assets.json">Реестр ассетов и происхождение</a></p><p>Novra — Independent Concept. Сохранённые материалы предназначены для изучения; публичная доступность файла не предоставляет права на использование персонажа в MYOR. Для своего дизайна нужен собственный исходник или права и редактируемый проект автора.</p><nav><a href="#key">Логика</a><a href="#motion">Движения</a><a href="#images">Изображения</a><a href="#scenes">Полные сцены</a><a href="#runtime">Rive</a><a href="#sources">Исходники и интеграции</a></nav><h2 id="key">Схема поведения и state machine</h2><div class="images">{''.join(f'<article><h3>{e(x["displayTitle"])}</h3><a href="{x["path"]}"><img src="{x["path"]}" alt="{e(x["displayTitle"])}"></a></article>' for x in images if x['id'] in ['36','37'])}</div><h2 id="motion">8 движений персонажа</h2>{''.join(video_card(x) for x in motion)}<h2 id="images">Изображения и исследования дизайна</h2><div class="images">{''.join(f'<article><h3>{x["id"]} · {e(x.get("displayTitle",x["title"]))}</h3><a href="{x["path"]}"><img loading="lazy" src="{x["path"]}" alt="{e(x.get("displayTitle",x["title"]))}"></a><p><a href="{x["path"]}" download>Исходное изображение</a> · <a href="{e(x["url"])}">Источник</a></p></article>' for x in images if x['id'] not in ['36','37'])}</div><h2 id="scenes">Интерфейсы и полные сценарии</h2>{''.join(video_card(x) for x in other)}<h2 id="runtime">Исходный runtime Rive</h2><article><p>Проверен в отдельном веб-плеере. Артборд Main 2, state machine State Machine_Main, управление через View Model. В файле содержится вся notch-композиция.</p><p><a href="rive-player.html">Открыть интерактивный плеер</a> · <a href="assets/rive/77-Novra-Grokbot-interactive-runtime.riv" download>Сохранённый .riv</a> · <a href="rive-inspection.json">Артборды, таймлайны и свойства</a> · <a href="rive-qa.json">Проверенные переходы</a></p><p>.riv — runtime-экспорт. Для изменения дизайна в Rive Editor нужен .rev или доступ к исходному проекту.</p></article><h2 id="sources">Источники для интеграции</h2><article><ul><li><a href="https://www.novra.design/case-studies/grokbot">Novra — оригинальный кейс и playable build</a></li><li><a href="https://github.com/iduu/grokbot-animation">Morph Bot SVG study</a> — 39 состояний, 18 шейпов, 14 morph-эффектов, редактор. Общая разрешительная лицензия не найдена.</li><li><a href="https://github.com/nasawz/GrokBot">Flutter GrokBot</a> — BSD-3-Clause для авторского кода; прямой интеграции в React Native нет.</li><li><a href="https://rive.app/docs/runtimes/react-native/adding-rive-to-expo">Rive и Expo</a> — development build, без Expo Go.</li><li><a href="https://rive.app/docs/runtimes/react/react">Rive и React Web</a></li><li><a href="https://github.com/Louis-CFM/coucou">Coucou</a> — предыдущая процедурная база и готовые локальные раскадровки.</li><li><a href="https://player.mediadelivery.net/embed/758467/92b79cf7-4662-4754-bdf2-7caf81bc7ea7">Обзорный ролик Novra в исходном embed</a> — сохранён как ссылка, вне 29 скачанных роликов.</li></ul></article><p>Ролики показываются из локальных копий. Для сравнения движения используйте воспроизведение; PNG-листы содержат восемь равномерно выбранных кадров, а не все ключевые позы. Происхождение и SHA-256 сохранены в assets.json.</p></html>'''
(ROOT/'index.html').write_text(page)
print('Gallery built', len(videos), 'videos',len(images),'images')
