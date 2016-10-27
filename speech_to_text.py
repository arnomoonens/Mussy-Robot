#!/usr/bin/python
# -*- coding: utf8 -*-

import subprocess
import sys
from text_to_speech import speak

# Adapted version from https://github.com/rob-mccann/Pi-Voice/blob/e67872c15cc5b1d00d835598246bb0b6b7aaabba/listen.py
LM = "./pocketsphinx/5715.lm"
DIC = "./pocketsphinx/5715.dic"

def hear_computer():
    """Start the subprocess to continuously listen for 'computer'"""
    pocketsphinx_commands = ['pocketsphinx_continuous', '-inmic', 'yes', '-lm', LM, '-dict', DIC]
    psphinx_process = subprocess.Popen(
        pocketsphinx_commands,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)

    speak("Listener started. Say 'computer' to activate.")

    while 1:
        # read each line of output, strip the newline and index numbers
        psphinx_output = psphinx_process.stdout.readline().rstrip(b'\n')[11:]
        print(psphinx_output)
        if b'computer' in psphinx_output.lower():
            # kill continuous listening so it does not trigger during listen()
            psphinx_process.kill()
            speak("Understood 'computer'. Stopping program.")
            sys.exit(0)
            # restart continuous listening
            psphinx_process = subprocess.Popen(
                pocketsphinx_commands,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        sys.stdout.flush()

if __name__ == '__main__':
    try:
        hear_computer()
    except KeyboardInterrupt:
        pass
