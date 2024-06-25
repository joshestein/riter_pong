class Ball:
    def __init__(self, width, height, dx, dy):
        self.dx = dx
        self.dy = dy
        self.width = width
        self.height = height
        self.x = width // 2
        self.y = height // 2

    def _reset(self):
        self.x = self.width // 2
        self.y = self.height // 2
        self.dx *= -1
        self.dy *= -1

    def move(self, leds, left_start, right_start, paddle_length):
        leds[self.y * self.width + self.x] = "0"

        if self.y == 0 or self.y == self.height - 1:
            self.dy *= -1

        if self.x == 1 and left_start <= self.y < left_start + paddle_length:
            self.dx *= -1
        elif (
            self.x == self.width - 2
            and right_start <= self.y < right_start + paddle_length
        ):
            self.dx *= -1
        elif self.x == 1:
            # TODO: increment right player score
            self._reset()
        elif self.x == self.width - 2:
            # TODO: increment right player score
            self._reset()

        self.x += self.dx
        self.y += self.dy

        self.render(leds)

    def render(self, leds):
        leds[self.y * self.width + self.x] = "1"
