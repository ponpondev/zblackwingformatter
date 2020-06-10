import io
import re
import pyperclip
from dateparser import parse
from slugify import slugify

# time_regex = re.compile('\d?\d:\d\d?')
removing_texts = [
    'during the times listed below',
    '.',
    'UTC:',
    'Available'
]
# Instruction:
# h2 should be the update/event item title
# h5 should be the date time of the event
# h3 is what idk \ :v /
cases = [
    re.compile('<h2>(.+)</h2>'),
    re.compile('<h3>(.+)</h3>'),
    re.compile('<h5>(.+)</h5>')
]

file = io.open('wordpress_parsed.html', 'r', encoding='utf-8')
lines = file.readlines()


def matching(string):
    matched = cases[0].match('')
    matched_item = -1
    for case in cases:
        matched = case.match(string)
        if matched:
            matched_item = cases.index(case)
            break
    return matched, matched_item


def clean_date_text(string):
    # time_regex.sub('', string)
    for removing in removing_texts:
        string = string.replace(removing, '')
    return string


def parse_date_text(string):
    final_text = ''
    # parsing the dates
    dates = string.split('-', 1)
    if len(dates) == 1:
        dates = string.split('–', 1)

    for _index, date in enumerate(dates):
        date = date.split('(', 1)
        cleaned_date = date[0].strip()
        # handles the hardship of cleaning and parsing dates
        date_obj = parse(cleaned_date)
        date_text = f'{date_obj:%d/%m}'
        followed_text = ''
        if len(date) > 1:
            followed_text = date[1]
            if 'after maintenance' in followed_text:
                followed_text = '(sau bảo trì)'
            elif 'before maintenance' in followed_text:
                followed_text = '(trước bảo trì)'
            else:
                followed_text = f'({followed_text}'

        final_text += f'{date_text}{f" {followed_text}"}'
        if _index == 0:
            final_text += ' – '
    return final_text.strip()


data = ''
first_match = False
for index, line in enumerate(lines):
    # ending the parse
    if len(lines) <= index + 1:
        data += '[/su_spoiler]'
        break
    # matching items
    matched1, matched_item1 = matching(line)
    matched2, matched_item2 = matching(lines[index + 1])

    # update item
    if matched1 and matched_item1 == 0:
        text1 = matched1.group(1)
        # check if updating item is date item
        text2 = matched2.group(1) if matched2 else None
        date_text = ''
        if text2:
            text2 = clean_date_text(text2)
            date_text = parse_date_text(text2)

        # do not insert this tag to the first matching update item
        text = '[/su_spoiler]\n' if first_match else ''
        text += (
            f'[su_spoiler title="{text1}{f" ({date_text})" if date_text else ""}" open="no" '
            f'icon="plus" style="fancy" anchor="#{slugify(text1)}"]\n'
        )
        first_match = True
    # normal line
    elif matched1 and matched_item1 == 2:
        continue
    else:
        text = line

    data += text

pyperclip.copy(data)
