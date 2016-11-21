#!/usr/bin/python
# -*- coding: utf8 -*-

# Adapted version from: https://github.com/mattdy/googletts/tree/0f16287624f792ad74e92bd7bb12c090faa59ee3

from subprocess import call
import sys
import re
from urllib import urlencode

MAX_LEN = 100  # Maximum length of a segment to send to Google for TTS
LANGUAGE = "en"  # Language to use with TTS - this won't do any translation, just the voice it's spoken with
ENCODING = "UTF-8"  # Character encoding to use


def speak(text, language=LANGUAGE):
    """Speak text in a certain language out loud"""
    # Split our full text by any available punctuation
    parts = re.split("[\.\,\;\:]", text)

    # The final list of parts to send to Google TTS
    processedParts = []

    while len(parts) > 0:  # While we have parts to process
        part = parts.pop(0)  # Get first entry from our list

        if len(part) > MAX_LEN:
            # We need to do some cutting
            cutAt = part.rfind(" ", 0, MAX_LEN)  # Find the last space within the bounds of our MAX_LEN

            cut = part[:cutAt]

            # We need to process the remainder of this part next
            # Reverse our queue, add our remainder to the end, then reverse again
            parts.reverse()
            parts.append(part[cutAt:])
            parts.reverse()
        else:
            # No cutting needed
            cut = part

        cut = cut.strip()  # Strip any whitespace
        if cut is not "":  # Make sure there's something left to read
            # Add into our final list
            processedParts.append(cut.strip())

    for part in processedParts:
        # Encode our query
        query = urlencode({
            'q': part,
            'client': 'tw-ob',
            'tl': language,
            'ie': ENCODING,
            'total': '1',
            'idx': '0'
        })
        # Use mpg123 to play the resultant MP3 file from Google TTS
        call(["mpg123", "-q", "http://translate.google.com/translate_tts?%s" % (query)])

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please provide text.")
    else:
        speak(" ".join(sys.argv[1:]))
