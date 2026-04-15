import requests
from inky import InkyPHAT
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne
# Get the current message on the annunciator
baseURLhost = 'https://now-api.parliament.uk'
baseURLAPIBit = '/api/Message/message/'
baseURLEnd = '/current'
house = 'CommonsMain'
response = requests.get(baseURLhost + baseURLAPIBit + house + baseURLEnd, timeout=10)
responseCode = response.status_code
data = response.json()
style = data['slides'][0]['lines'][0]['style']


WESTMINSTER_HALL_STYLE = 'WestminsterHallInfo'


def get_lines_text(skip_last=False):
    lines = data['slides'][0]['lines']
    selected = lines[:-1] if skip_last else lines
    return ' '.join(line['content'] for line in selected).title().strip()


def westminster_hall():
    lines = data['slides'][0]['lines']
    return ', '.join(lines[i]['content'] for i in range(0, len(lines), 2)).title().strip()


if responseCode != 200:
    message = str(response.status_code)
elif style == WESTMINSTER_HALL_STYLE:
    message = "Westminster Hall: " + westminster_hall()
elif data['slides'][0]['lines'][-1]['member'] is None:
    message = get_lines_text()
else:
    message = get_lines_text(skip_last=True)

# Inky section shamelessly stolen from their guide
# https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-inky-phat
inky_display = InkyPHAT("red")
inky_display.set_border(inky_display.WHITE)
img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)
font = ImageFont.truetype(FredokaOne, 16)

# Reflow function from
# https://github.com/pimoroni/inky/blob/master/examples/what/quotes-what.py


def reflow_text(quote, width, font):
    words = quote.split(" ")
    reflowed = ' '
    line_length = 0

    for i in range(len(words)):
        word = words[i] + " "
        word_length = font.getlength(word)
        line_length += word_length

        if line_length < width:
            reflowed += word
        else:
            line_length = word_length
            reflowed = reflowed[:-1] + "\n " + word

    # reflowed = reflowed.rstrip() + '"'

    return reflowed


reflowed_message = reflow_text(message, inky_display.WIDTH, font)
draw.text((0, 0), reflowed_message, inky_display.BLACK, font)
inky_display.set_image(img)
inky_display.show()
