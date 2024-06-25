from pynput import keyboard
from pynput.keyboard import Key
from pythonosc import udp_client

WIDTH = 96
HEIGHT = 38

left_start = 5
right_start = 10
paddle_length = 5

leds = [str(0) for i in range(WIDTH * HEIGHT)]


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

    leds = [str(0) for i in range(WIDTH * HEIGHT)]

    for i in range(HEIGHT):
        for j in range(WIDTH):
            if left_start < i < left_start + paddle_length:
                leds[i * WIDTH] = "1"

            if right_start < i < right_start + paddle_length:
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
    render()

    # riter_thread = Thread(target=rite, args=(leds,), daemon=True)
    # riter_thread.start()
    with keyboard.Listener(on_press=on_press) as listener:
        while listener.is_alive():
            rite(leds)
        listener.join()


if __name__ == "__main__":
    main()
