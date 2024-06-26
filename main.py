import time

from pynput import keyboard
from pynput.keyboard import Key
from pythonosc import udp_client

from ball import Ball

WIDTH = 96
HEIGHT = 38
PADDLE_LENGTH = 5

left_start = 5
right_start = 10

leds = [str(0) for i in range(WIDTH * HEIGHT)]
scores = [0, 0]


def rite(leds):
    """96 x 38 matrix of LEDs"""

    if isinstance(leds, list):
        leds = "".join(leds)

    ip = "10.100.7.28"
    port = 12000
    client = udp_client.SimpleUDPClient(ip, port)
    return client.send_message("/test", leds)


def render():
    global left_start, right_start, leds

    # Handle out of bounds
    if left_start < 0:
        left_start = 0
    elif left_start + PADDLE_LENGTH > HEIGHT:
        left_start = HEIGHT - PADDLE_LENGTH

    if right_start < 0:
        right_start = 0
    elif right_start + PADDLE_LENGTH > HEIGHT:
        right_start = HEIGHT - PADDLE_LENGTH

    for i in range(left_start, left_start + PADDLE_LENGTH):
        leds[i * WIDTH] = "1"

    for i in range(right_start, right_start + PADDLE_LENGTH):
        leds[(i + 1) * WIDTH - 1] = "1"


def on_press(key):
    global left_start, right_start

    try:
        if key.char == "w":
            move_left_paddle_up()
        elif key.char == "s":
            move_left_paddle_down()
        elif key.char == "k":
            move_right_paddle_up()
        elif key.char == "j":
            move_right_paddle_down()
    except AttributeError:
        if key == Key.down:
            move_right_paddle_down()
        elif key == Key.up:
            move_right_paddle_up()
        elif key == Key.esc:
            return False


def move_left_paddle_up():
    global left_start
    leds[(left_start + PADDLE_LENGTH - 1) * WIDTH] = str(0)
    left_start -= 1
    render()


def move_left_paddle_down():
    global left_start
    leds[left_start * WIDTH] = str(0)
    left_start += 1
    render()


def move_right_paddle_up():
    global right_start
    leds[(right_start + PADDLE_LENGTH) * WIDTH - 1] = str(0)
    right_start -= 1
    render()


def move_right_paddle_down():
    global right_start
    leds[(right_start + 1) * WIDTH - 1] = str(0)
    right_start += 1
    render()


def main():
    global leds, left_start, right_start
    ball = Ball(WIDTH, HEIGHT, 1, 1)
    render()

    with keyboard.Listener(on_press=on_press) as listener:
        while listener.is_alive():
            ball.move(leds, left_start, right_start, PADDLE_LENGTH)

            if ball.x == 0:
                scores[1] += 1
                ball.reset()
            elif ball.x == WIDTH - 1:
                scores[0] += 1
                ball.reset()

            rite(leds)
            time.sleep(0.08)

        listener.join()


if __name__ == "__main__":
    main()
