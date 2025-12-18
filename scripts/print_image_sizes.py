from PIL import Image
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'images'/'canva'
files=['hero-home.jpg','hero-pickleball.jpg','pickleball-1.jpg','pickleball-2.jpg','pickleball-3.jpg']
for name in files:
    fp=p/name
    if fp.exists():
        try:
            with Image.open(fp) as im:
                print(f"{name}\t{im.size[0]}x{im.size[1]}\t{fp}")
        except Exception as e:
            print(f"{name}\tERROR\t{e}")
    else:
        print(f"{name}\tMISSING\t{fp}")
