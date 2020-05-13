import requests
from inky import InkyPHAT
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne
# Get the current message on the annunciator
baseURLhost = 'https://parliamentnow-api.parliament.uk'
baseURLAPIBit = '/api/Message/message/'
baseURLEnd = '/current'
house = 0
response = requests.get(baseURLhost + baseURLAPIBit + str(house) + baseURLEnd)
data = response.json()
style = data['slides'][0]['lines'][0]['style']


def withMember():
    x = data['slides'][0]['lines']
    y = len(x)
    z = y - 1
    i = 0
    holder = []
    while z > i:
        holder.append(data['slides'][0]['lines'][i]['content'])
        i += 1
    string = ' '.join(holder).title().strip()
    return string


def noMember():
    x = data['slides'][0]['lines']
    y = len(x)
    i = 0
    holder = []
    while y > i:
        holder.append(data['slides'][0]['lines'][i]['content'])
        i += 1
    string = ' '.join(holder).title().strip()
    return string


def committeeMeetings():
    x = data['slides'][0]['lines']
    y = len(x)
    i = 0
    holder = []
    while y > i:
        holder.append(data['slides'][0]['lines'][i]['content'])
        i += 2
    string = ', '.join(holder).title().strip()
    return string


if style == 16:
    message = "Today's Committeess: " + committeeMeetings()
elif data['slides'][0]['lines'][-1]['member'] is None:
    message = noMember()
else:
    message = withMember()

# Inky section shamelessly stolen from their guide
# https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-inky-phat
inky_display = InkyPHAT("red")
inky_display.set_border(inky_display.WHITE)
img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)
font = ImageFont.truetype(FredokaOne, 16)
w, h = font.getsize(message)
x = (inky_display.WIDTH / 2) - (w / 2)
y = (inky_display.HEIGHT / 2) - (h / 2)

# Reflow function from
# https://github.com/pimoroni/inky/blob/master/examples/what/quotes-what.py


def reflow_text(quote, width, font):
    words = quote.split(" ")
    reflowed = ' '
    line_length = 0

    for i in range(len(words)):
        word = words[i] + " "
        word_length = font.getsize(word)[0]
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
