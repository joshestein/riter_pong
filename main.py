import time

from pynput import keyboard
from pynput.keyboard import Key
from pythonosc import udp_client

WIDTH = 96
HEIGHT = 38

left_start = 5
right_start = 10
paddle_length = 5

leds = [str(0) for i in range(WIDTH * HEIGHT)]


class Ball:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def move(self):
        leds[self.y * WIDTH + self.x] = "0"

        if self.y == 0 or self.y == HEIGHT - 1:
            self.dy *= -1

        if self.x == 0 or self.x == WIDTH - 1:
            self.dx *= -1

        self.x += self.dx
        self.y += self.dy

        self.render()

    def render(self):
        global leds
        print(self.y * WIDTH + self.x)
        leds[self.y * WIDTH + self.x] = "1"


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

    # TODO: only reset what has been changed
    leds = [str(0) for i in range(WIDTH * HEIGHT)]

    # Handle out of bounds
    if left_start < 0:
        left_start = 0
    elif left_start + paddle_length > HEIGHT:
        left_start = HEIGHT - paddle_length

    if right_start < 0:
        right_start = 0
    elif right_start + paddle_length > HEIGHT:
        right_start = HEIGHT - paddle_length

    for i in range(left_start, left_start + paddle_length):
        leds[i * WIDTH] = "1"

    for i in range(right_start, right_start + paddle_length):
        leds[(i + 1) * WIDTH - 1] = "1"


def on_press(key):
    global left_start, right_start

    try:
        if key.char == "w":
            left_start -= 1
            render()
        elif key.char == "s":
            left_start += 1
            render()
        elif key.char == "j":
            right_start += 1
            render()
        elif key.char == "k":
            right_start -= 1
            render()
    except AttributeError:
        if key == Key.down:
            right_start += 1
            render()
        elif key == Key.up:
            right_start -= 1
            render()
        elif key == Key.esc:
            return False


def main():
    ball = Ball(WIDTH // 2, HEIGHT // 2, 1, 1)
    render()

    with keyboard.Listener(on_press=on_press) as listener:
        while listener.is_alive():
            ball.move()
            rite(leds)
            time.sleep(0.1)
        listener.join()


if __name__ == "__main__":
    main()
