import io
import re

import pyperclip

# remove extra <p id="someIdHere"> from inserting images to post
p_id = re.compile('<p id=".+">')

file = io.open('wordpress_parsed.html', 'r', encoding='utf-8')
lines = file.readlines()

data = ''
first_match = False
for index, line in enumerate(lines):
    text = p_id.sub('', line)
    data += text

pyperclip.copy(data)
