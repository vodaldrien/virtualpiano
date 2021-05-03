from pynput.keyboard import Key, Controller
import time
import argparse
import random

symbols = {
    "!" : "1",
    "@" : "2",
    "$" : "4",
    "%" : "5",
    "^" : "6",
    "*" : "8",
    "(" : "9",
}
keyboard = Controller()
getSongText = lambda filename: open(filename, 'r').read()
usleep = lambda x: time.sleep(x/1000000.0)
sleep = lambda x: time.sleep(x)
isKey = lambda key: key.isalnum() or key in symbols
log = lambda s: print(s, flush=True)
multiPress = lambda chars: [[nPress(x, True) for x in chars], log("Multipress: [%s]" %chars)]
pause = lambda t=.3: [log("Sleeping %f" %t), sleep(t)]
intro = lambda seconds: [[log(i+1), sleep(1)] for i in range (seconds)]

def nPress(key, noLog=False):
    # usleep(random.randrange(0,100000))
    if key.isupper():
        with keyboard.pressed(Key.shift):
            keyboard.press(key.lower())
            keyboard.release(key.lower())
    elif key in symbols:
        with keyboard.pressed(Key.shift):
            keyboard.press(symbols[key])
            keyboard.release(symbols[key])
    else:
        keyboard.press(key)
        keyboard.release(key)

    noLog or log("Pressing: '%s'" %key)

def main():
    # Time to click away...
    intro(4)

    storeSequence = "";
    sequenceOpen = 0;
    for c in getSongText('song.txt'):
        if c == "[":
            sequenceOpen -= 1;
        elif c == "]":
            sequenceOpen += 1;
            if sequenceOpen == 0:
                multiPress(storeSequence)
                storeSequence = ""
        elif sequenceOpen < 0 and isKey(c):
            storeSequence += c
        elif isKey(c):
            nPress(c)

        if c == "-":
            pause(random.uniform(.3, .5))
        elif c == "\n" and sequenceOpen == 0:
            pause(.3)
            pass
        elif c == " " and sequenceOpen == 0:
            pause()
            # pause(random.uniform(.1, .3))
        elif sequenceOpen == 0:
            usleep(random.uniform(1500, 2000))
            # pause(.1)
            pass

main()


