import os

os.system('echo y | python -m PyInstaller --noconsole --name "Lights Out" --icon game/data/icon.ico game/app.py')

with open("Lights Out.spec", "r+") as f:
    spec = f.readlines()
    spec.insert(1, 'from kivy.deps import sdl2, glew\n')
    
    for line, text in enumerate(spec):
        if 'a.datas,' in text:
            spec.insert(line + 1, text[:text.find('a.datas')] + '*[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],\n')
        if text == 'coll = COLLECT(exe,\n':
            spec[line] = text[:-1] + ' Tree("game"),\n'
    
    f.seek(0)
    f.writelines(spec)

os.system('echo y | python -m PyInstaller "Lights Out.spec"')
