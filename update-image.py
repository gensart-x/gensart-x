import argparse, requests
from PIL import Image, ImageDraw, ImageFont

parser = argparse.ArgumentParser()
parser.add_argument('--api-url')
parser.add_argument('--key')
parser.add_argument('--command')
parser.add_argument('--model')
args = parser.parse_args()

try:
    response = requests.post(
      args.api_url,
      headers={
        "Authorization": args.key
      },
      json={
        "messages": [
          {
            "content": "You are a helpful assistant.",
            "role": "system"
          },
          {
            "content": args.command,
            "role": "user"
          }
        ],
        "max_tokens": 120,
        "model": args.model,
        "temperature": 0.9
      },
    )

    response_data = response.json()
    desired_text = response_data['choices'][0]['message']['content']
    desired_text = desired_text.strip().replace('"', '')

    TEXT = desired_text
    IMG_WIDTH = 600
    IMG_HEIGHT = 200
    PADDING = 40
    FONT_PATH = "pixel.ttf"
    START_FONT_SIZE = 50
    MIN_FONT_SIZE = 10

    img = Image.new("RGBA", (IMG_WIDTH, IMG_HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    font = None
    text_width, text_height = 0, 0

    # Try to find a fitting font size
    for size in range(START_FONT_SIZE, MIN_FONT_SIZE - 1, -1):
        test_font = ImageFont.truetype(FONT_PATH, size)

        bbox = draw.textbbox((0, 0), TEXT, font=test_font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]

        if w <= (IMG_WIDTH - PADDING):
            font = test_font
            text_width, text_height = w, h
            break

    # Fallback if nothing fits (text is just too long)
    if font is None:
        font = ImageFont.truetype(FONT_PATH, MIN_FONT_SIZE)
        bbox = draw.textbbox((0, 0), TEXT, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

    # Center position
    x = (IMG_WIDTH - text_width) / 2
    y = (IMG_HEIGHT - text_height) / 2

    # Draw text
    draw.text((x, y), TEXT, font=font, fill=(255, 99, 146))

    img.save("quote.png")
except Exception as e:
    print(e)
