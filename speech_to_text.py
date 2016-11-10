#!/usr/bin/python
# -*- coding: utf8 -*-

import subprocess
import sys
from text_to_speech import speak
import time

# Adapted version from https://github.com/rob-mccann/Pi-Voice/blob/e67872c15cc5b1d00d835598246bb0b6b7aaabba/listen.py
LM = "./pocketsphinx/5715.lm"
DIC = "./pocketsphinx/5715.dic"
pocketsphinx_commands = [
    'pocketsphinx_continuous',
    '-hmm', '/usr/local/share/pocketsphinx/model/en-us/en-us',
    '-samprate', '16000/8000/48000',
    '-inmic', 'yes',
    '-lm', LM,
    '-dict', DIC]

def hear_computer():
    """Start the subprocess to continuously listen for 'computer'"""
    psphinx_process = subprocess.Popen(
        pocketsphinx_commands,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)

    speak("Listener started. Say 'computer' to activate.")
    time.sleep(0.3)
    counter = 0
    while 1:
        # read each line of output, strip the newline and index numbers
        psphinx_output = psphinx_process.stdout.readline().rstrip(b'\n').decode()
        print(psphinx_output)
        if 'computer' in psphinx_output.lower():
            # kill continuous listening so it does not trigger during listen()
            psphinx_process.kill()
            speak("Understood 'computer'. Stopping program.")
            sys.exit(0)
            # restart continuous listening
            psphinx_process = subprocess.Popen(
                pocketsphinx_commands,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        sys.stdout.flush()

class TimeoutException(Exception):
    pass

def get_voice_feedback(words, timeout=float("inf")):
    psphinx_process = subprocess.Popen(
        pocketsphinx_commands,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    counter = 0
    start_time = time.time()
    while True:
        psphinx_output = psphinx_process.stdout.readline().rstrip(b'\n').decode().lower()
        if psphinx_output.lower().startswith("info: "):
            continue
        elif psphinx_output.startswith("current configuration:"):
            counter += 115
            continue
        elif counter > 0:
            counter -= 1
            continue
        for word in words:
            if word in psphinx_output:
                psphinx_process.kill()
                return word
        if time.time() - start_time > timeout:
            psphinx_process.kill()
            raise TimeoutException()

if __name__ == '__main__':
    try:
        get_voice_feedback(["yes", "no"], timeout=5)
    except KeyboardInterrupt:
        pass
