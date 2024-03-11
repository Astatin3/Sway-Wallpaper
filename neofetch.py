import subprocess
import datetime
import os
import random

from PIL import Image
from PIL import ImageFilter
from PIL import ImageFont
from PIL import ImageDraw
import PIL.ImageOps

try:
    os.ulink("/tmp/wallpaper.png")
except:
    x = None # Do nothing

#file = open("/home/astatin3/.config/sway/icon.txt","r")
#lines = file.readlines()
#file.close()

output = (subprocess.run(['neofetch', '--stdout'], capture_output=True, text=True).stdout).split("\n")

screenX = 0
screenY = 0

def getSubfolders(path):
    try:
        return os.listdir(path)
    except:
        return None

def getRandWallpaper():
    wallpapers = getSubfolders("/home/astatin3/.config/sway/wallpapers/")
    return "/home/astatin3/.config/sway/wallpapers/" + random.choice(wallpapers) 

for i in range(0, len(output)-2, 1):
    #lines[i] = lines[i][:-1] + output[i]

    #print(lines[i])

    if i == 0:
        output[0] += f"at ({datetime.datetime.now().strftime('%m-%d %H:%M:%S')})"

    if i == 8:
        res = output[i].split(" ")[1].split("x")
        screenX = int(res[0])
        screenY = int(res[1])

#neofetch = "\n".join(lines)

icon = Image.open("/home/astatin3/.config/sway/icon.png").convert("RGBA")

iconsizeX, iconsizeY = icon.size

neofetch = "\n".join(output)

textSize = 0.01

iconscale = 0.0005

textoffsetX = 0.0 #Percentages
textoffsetY = -0.16

iconoffsetX = -0.145
iconoffsetY = -0.16

color = (199,0,57)
# color = (255, 255, 255)

# img = Image.new('RGB', (screenX, screenY), (31, 26, 32))
img = Image.open(getRandWallpaper()).resize((screenX, screenY)).convert("RGB")

solidColorImage = Image.new('RGBA', (screenX, screenY),color)
blackImage = Image.new('RGBA', (screenX, screenY),(0,0,0,255))
invertImg = PIL.ImageOps.invert(img).convert('LA').filter(ImageFilter.BoxBlur(2))
# invertImg = invertImg.filter(ImageFilter.FIND_EDGES)

mask = Image.new('RGBA', (screenX, screenY),(0, 0, 0, 0))
draw = ImageDraw.Draw(mask)
font = ImageFont.truetype("/home/astatin3/.config/sway/UbuntuMonoNerdFontMono-Regular.ttf", textSize*screenX)

draw.text((textoffsetX*screenX+screenX/2, textoffsetY*screenY+screenY/2),neofetch,color,font=font)

icon = icon.resize((round(iconscale*iconsizeX*screenY), round(iconscale*iconsizeY*screenY)), Image.Resampling.LANCZOS)
mask.paste(icon, (round(iconoffsetX*screenX+screenX/2), round(iconoffsetY*screenY+screenY/2)), icon)

# Outline
mask2 = Image.new('RGBA', (screenX, screenY),(0, 0, 0, 0))

d = 2

mask2.paste(mask, (d, d), mask)
#mask2.paste(mask, (d, -d), mask)
#mask2.paste(mask, (-d, d), mask)
#mask2.paste(mask, (-d, -d), mask)

mask2.paste(mask, (d, 0), mask)
#mask2.paste(mask, (-d, 0), mask)
mask2.paste(mask, (0, d), mask)
#mask2.paste(mask, (0, -d), mask)



wallpaper = Image.composite(blackImage, img, mask2)
wallpaper = Image.composite(solidColorImage, wallpaper, mask)
wallpaper.save("/tmp/wallpaper.png")

# img.save("/tmp/wallpaper.png")
#img.show()

subprocess.run(["swaybg", "-m", "fill", "-i", "/tmp/wallpaper.png"])
