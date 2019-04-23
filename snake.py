#! ./venv/bin/python3

from blessings import Terminal
import blessings

import random
import time
import getpass
import math
from pynput.keyboard import Key, Listener
import os

class GameOver(KeyboardInterrupt):
    def __init__(self, text):
        super().__init__(text)

class Clock:
    tps = 20
    def __init__(self, tps=20):
        self.tps = tps
        self.last_tick = 0

    def tick(self):
        now = time.perf_counter()
        sleep_time = (1-math.modf((now-self.last_tick)*self.tps)[0])/self.tps
        time.sleep(sleep_time)
        self.last_tick = now+1/self.tps

def spinner(n):
    string = "-/|\\"
    index = 0
    while index < n:
        yield string[index%len(string)]
        index+=1

if __name__ == "__main__":
    t = Terminal()
    TPS = 10
    STARTING_DIRECTION = (1, 0)
    V_SCALE = 1
    os.system("stty -echo")
    START_POS = (t.width//2, t.height//2)
    clock = Clock(tps=TPS)
    loc = START_POS
    direction = STARTING_DIRECTION
    pause = False


    def on_press(key):
        global direction, pause
        if key == Key.space:
            pause = not pause
        if key == Key.left:
            if direction != (1, 0):
                direction = (-1, 0)
        if key == Key.right:
            if direction != (-1, 0):
                direction = (1, 0)
        if key == Key.up:
            if direction != (0, 1):
                direction = (0, -1)
        if key == Key.down:
            if direction != (0, -1):
                direction = (0, 1)

    listener = Listener(on_press=on_press)
    listener.start()
    try:
        with t.hidden_cursor(), t.fullscreen():
            counter = 0
            score = 0
            old_pos = []                
            h_w = None
            fruit = None
            while True:
                clock.tick()
                if t._height_and_width() != h_w:
                    h_w = t._height_and_width()
                    with t.location(0, 0):
                        print(
                            ("╔"+"═"*(t.width-2)+"╗")+"\n"+
                            (("║"+" "*(t.width-2)+"║")+"\n")*(t.height-3)+
                            ("╚"+"═"*(t.width-2)+"╝")
                        )
                if fruit == None:
                    while True:
                        fruit = (random.randint(1, t.width-2), random.randint(1, t.height-3))
                        if fruit not in old_pos:
                            break
                with t.location(fruit[0], fruit[1]):
                    print("♥︎")
                if pause:
                    continue
                if direction[0] == 0:
                    counter += 1
                    if counter >= V_SCALE:
                        counter = 0
                        old_pos.append(loc)
                        if len(old_pos) > score:
                            r = old_pos.pop(0)
                            with t.location(r[0], r[1]):
                                print(" ")
                        loc = (loc[0], 1+(loc[1]+direction[1]-1)%(t.height-1-2))
                else:
                    counter = 0
                    old_pos.append(loc)
                    if len(old_pos) > score:
                        r = old_pos.pop(0)
                        with t.location(r[0], r[1]):
                            print(" ")
                    loc = (1+(loc[0]+direction[0]-1)%(t.width-2), loc[1])
                if loc in old_pos:
                    raise GameOver(f"Game over, your score is {score}")
                if loc == fruit:
                    score+=1 
                    fruit = None
                for pos in range(len(old_pos)):
                    with t.location(old_pos[pos][0], old_pos[pos][1]):
                        if pos in [0, 1]:
                            print("•")
                        else:
                            print("o")
                with t.location(loc[0], loc[1]):
                    if direction == (1, 0):
                        print("ᗧ")
                    elif direction == (-1, 0):
                        print("ᗤ")
                    elif direction == (0, 1):
                        print("ᗣ")
                    elif direction == (0, -1):
                        print("ᗢ")
                    
                    # print([i for i in key_buffer.get()])
                with t.location(2, t.height-1):
                    print(f"Score: {score} pts", end="")
    except BaseException as e:
        
        os.system("stty echo")
        raise e