from io import BytesIO
from urllib.request import urlopen

from PIL import Image, ImageDraw, ImageFont

from utils.logger import logger
from utils.namecard import random_namecard


async def generate_welcome_card(
    name: str, members_count: int, status: str, avatar, status_text: str = None
) -> BytesIO:
    W = 800
    H = 100

    # URLS
    namecard_url = random_namecard()

    # CANVAS
    base = Image.new("RGBA", (W, H), (255, 255, 255, 0))
    canvas = Image.new("RGBA", (W, H), (220, 215, 202, 255))
    white_base = Image.new("RGBA", (W, H), (255, 255, 255, 255))

    # PFP
    pfp = Image.open(BytesIO(avatar)).convert("RGBA").resize((80, 80))

    r = 42
    left, top = 23, 8
    pfpbox = (left, top, left + 2 * r, top + 2 * r)

    draw = ImageDraw.Draw(canvas)
    draw.ellipse(pfpbox, fill=(255, 255, 255, 255))

    pfp_mask = Image.new("L", (80, 80), 0)
    draw = ImageDraw.Draw(pfp_mask)
    draw.ellipse((0, 0, 80, 80), fill=255)
    pfp.putalpha(pfp_mask)

    # PFP on canvas
    canvas.paste(pfp, (25, 10), pfp)

    # Namecard
    namecard = (
        Image.open(BytesIO(urlopen(namecard_url).read()))
        .convert("RGBA")
        .resize((420, 200))
    )
    namecard = namecard.crop((10, 50, 410, 150))

    shape_mask = Image.new("L", (400, 100), 0)
    draw = ImageDraw.Draw(shape_mask)
    draw.rounded_rectangle((0, 0, 400, 100), radius=H / 2, fill=255)

    fade_mask = Image.new("L", (400, 100), 255)
    for x in range(400):
        alpha = 255 if x >= 100 else int(255 * (x / 100) ** 1.6)
        for y in range(100):
            fade_mask.putpixel((x, y), alpha)

    mask = Image.open("assets/mask.png").convert("RGBA").resize((800, 100))
    # namecard_mask.show()

    namecard.putalpha(fade_mask)
    canvas.paste(namecard, (400, 0), namecard)
    canvas = Image.composite(canvas, base, mask=mask)

    border_mask = (
        Image.open("assets/border_mask.png").convert("RGBA").resize((800, 100))
    )
    canvas = Image.composite(white_base, canvas, mask=border_mask)

    chat_icon = Image.open("assets/icon.png").convert("RGBA").resize((25, 25))

    draw = ImageDraw.Draw(canvas)
    try:
        font_title = ImageFont.truetype("assets/zh-cn.ttf", size=30, encoding="utf-16")
        font_subtitle = ImageFont.truetype(
            "assets/Montserrat-SemiBold.ttf", size=18, encoding="utf-16"
        )
    except Exception as e:
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
        logger.logger.warning(e)

    status_color = (128, 128, 128)
    match status:
        case "online":
            status_color = (134, 166, 60)
        case "dnd":
            status_color = (242, 72, 69)
        case "idle":
            status_color = (249, 166, 27)
        case "invisible":
            status_color = (110, 126, 139)

    # --- Status circle ---
    status_x, status_y = 292, 66  # adjust position so it aligns with text
    radius = 6
    draw.ellipse(
        (status_x, status_y, status_x + radius * 2, status_y + radius * 2),
        fill=status_color,
    )

    draw.text((150, 18), name, font=font_title, fill=(34, 38, 48))
    draw.text(
        (150, 60),
        f"Traveler #{str(members_count)}",
        font=font_subtitle,
        fill=(34, 38, 48),
    )
    draw.text((310, 60), status, font=font_subtitle, fill=status_color)
    draw.text((310, 60), status, font=font_subtitle, fill=status_color)
    if status_text:
        status_text = status_text[:30] + "..." if len(status_text) > 30 else status_text
        canvas.paste(chat_icon, (390, 60), chat_icon)
        draw.text((425, 60), status_text, font=font_subtitle, fill=(75, 53, 42))

    canvas.save("assets/card.png")
    image = BytesIO()
    canvas.save(image, "PNG")
    image.seek(0)
    return image
