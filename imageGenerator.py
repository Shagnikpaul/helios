from PIL import Image, ImageDraw, ImageFont


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
# 507 x 263 - fixed size....
