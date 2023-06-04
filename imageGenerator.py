from PIL import Image, ImageDraw, ImageFont
import accountCreationSystem
from dotenv import load_dotenv
from MClient import MClient
import os
load_dotenv()
acc = accountCreationSystem.acuSystem(MClient(CONNECTION_URI=os.getenv('mongo')))


def createImage(temperature: str, weatherConditon: str, iconCode: str, location: str, userID: str):

    if len(location) <= 0:
        location = "Unknown Location"
    image = Image.open(f'weatherCards/{iconCode}.png').convert('RGBA')
    font1 = ImageFont.truetype('fonts/Inter-Bold.ttf', size=120)
    font2 = ImageFont.truetype('fonts/Inter-Bold.ttf', size=70)
    font3 = ImageFont.truetype('fonts/Inter-Medium.ttf', size=35)
    txt = Image.new('RGBA', image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(im=txt)
    draw.text(xy=(58, 42), text=f'{temperature}', font=font1, fill='white')
    draw.text(xy=(58, 230), text=f'{weatherConditon}',
              font=font2, fill=(255, 255, 255, 150))
    draw.text(xy=(58, 305), text=f'{location}.',
              font=font3, fill=(255, 255, 255, 150))

    Image.alpha_composite(image, txt).save(f'users/{userID}/imf.png')
    tw = Image.open(f'users/{userID}/imf.png')

# 507 x 263 - fixed size....


def createImageSub(temperature: str, weatherConditon: str, iconCode: str, location: str, channelID: str, serverID="something"):

    if len(location) <= 0:
        location = "Unknown Location"
    image = Image.open(f'weatherCards/{iconCode}.png').convert('RGBA')
    rect = Image.open('weatherCards/rectang.png').convert('RGBA')
    font1 = ImageFont.truetype('fonts/Inter-Bold.ttf', size=120)
    font2 = ImageFont.truetype('fonts/Inter-Bold.ttf', size=70)
    font3 = ImageFont.truetype('fonts/Inter-Medium.ttf', size=35)
    font4 = ImageFont.truetype('fonts/Inter-Regular.ttf', size=25)
    txt = Image.new('RGBA', image.size, (255, 255, 255, 0))
    rectangle = Image.new('RGBA', image.size, (255, 255, 255, 0))
    rectangle.paste(rect, (582, 18))
    draw = ImageDraw.Draw(im=txt)
    draw.text(xy=(58, 42), text=f'{temperature}', font=font1, fill='white')
    draw.text(xy=(58, 230), text=f'{weatherConditon}',
              font=font2, fill=(255, 255, 255, 150))
    draw.text(xy=(58, 305), text=f'{location}.',
              font=font3, fill=(255, 255, 255, 150))

    data = acc.getSubInfo(channelId=channelID, serverID=serverID)
    draw.text(xy=(610, 71),
              text=f'{data.get("minT")}', font=font4, fill='white')
    draw.text(xy=(610, 128),
              text=f'{data.get("maxT")}', font=font4, fill='white')
    Image.alpha_composite(image, txt).save(f'subimages/{channelID}.png')
    tw = Image.open(f'subimages/{channelID}.png')
    Image.alpha_composite(tw, rectangle).save(f'subimages/{channelID}.png')



