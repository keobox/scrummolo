
"A virtual talking stick."

from datetime import datetime
from random import shuffle

import pyglet
from pyglet.window import key

import settings

#index all resources. Resources folder must be on same level as this file.
pyglet.resource.path = settings.RESOURCES
pyglet.resource.reindex()

#create window object
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pyglet.window.Window(SCREEN_WIDTH, SCREEN_HEIGHT)

#create Team
TEAM = settings.TEAM
shuffle(TEAM)

def resize(width, height, max_width, max_height):
    "Calculates new width and height but leave w/h ratio invariant."
    delta_width = width - max_width
    delta_height = height - max_height
    if delta_height <= 0 and delta_width <= 0:
        return width, height
    if delta_height >= delta_width:
        return width * max_height / height, max_height
    return max_width, height * max_width / width

#image dimensions
WIDTH = SCREEN_WIDTH // 2
HEIGHT = SCREEN_HEIGHT // 2
HEIGHT_BORDER = 10

def resize_image(image):
    "Resize but leave the ratio invariant."
    width, height = resize(image.width, image.height, WIDTH, HEIGHT)
    image.width = width
    image.height = height

#create player objects. Player image must be in resource folder.
PLAYER_IMAGES = []
for player in TEAM:
    player = player.replace('.', '')
    player = player.replace(' ', '_')
    player_image = pyglet.resource.image(player.lower() + ".png")
    resize_image(player_image)
    PLAYER_IMAGES.append(player_image)

class GameOverAnimation:
    """Animation for GIF files."""

    def __init__(self, animation_resource_name, pos_x, pos_y):
        """Constructor."""
        animation = pyglet.resource.animation(animation_resource_name)
        self.sprite = pyglet.sprite.Sprite(animation, pos_x, pos_y)

    def draw(self):
        """Draw game over animation."""
        self.sprite.draw()


class GameOverImage:
    """Image for PNG files."""

    def __init__(self, image_resource_name, pos_x, pos_y):
        """Constructor."""
        self.image = pyglet.resource.image(image_resource_name)
        resize_image(self.image)
        self.pos_x = pos_x
        self.pos_y = pos_y

    def draw(self):
        """Draw game over animation."""
        self.image.blit(self.pos_x, self.pos_y)


def create_game_over_image(image_path):
    if image_path.split('.')[1] == 'gif':
        return GameOverAnimation(settings.GAME_OVER_IMAGE, 0, HEIGHT * 2 // 3)
    else:
        return GameOverImage(settings.GAME_OVER_IMAGE, WIDTH, HEIGHT - HEIGHT_BORDER)

GAME_OVER_IMAGE = create_game_over_image(settings.GAME_OVER_IMAGE)
GAME_OVER_SOUND = pyglet.resource.media(settings.GAME_OVER_SOUND, streaming=False)

#create text labels for questions
QUESTIONS = settings.QUESTIONS
QUESTIONS = [pyglet.text.Label(text="{0}".format(q), font_size=36, x=100, y=100) for q in QUESTIONS]

PLAYER_MESSAGES = [pyglet.text.Label(text="{0}, is your turn!".format(name),
                  font_size=18, x=100, y=500) for name in TEAM]
GAME_OVER_MESSAGE = pyglet.text.Label(text=settings.GAME_OVER_TEXT,
                                      font_size=36, x=100, y=100)

class GameLogic(object):
    "Game Logic"

    def __init__(self, number_of_questions, number_of_players):
        "Constructor"
        self.number_of_questions = number_of_questions
        self.number_of_players = number_of_players
        self.player = 0
        self.question = 0
        self.game_over = False
        self.bye = False

    def step(self):
        "Move forward in the game"
        if self.question < self.number_of_questions - 1:
            self.question += 1
        else:
            if self.player == self.number_of_players - 1:
                self.game_over = True
            else:
                self.question = 0
                self.player += 1

    def get_player(self):
        "Returns the current player."
        return self.player

    def get_question(self):
        "Returns the current question."
        return self.question

    def over(self):
        "Returns True if the game is over."
        return self.game_over

    def goodbye(self):
        "Set the end of the game."
        self.bye = True

    def said_goodbye(self):
        "Check if is time to exit."
        return self.bye

GAME = GameLogic(len(QUESTIONS), len(TEAM))

class Timer:
    """Timer class"""

    def __init__(self, minutes, seconds, label):
        """Constructor."""
        self.duration = minutes * 60 + seconds
        self.label = label
        self.tick = 0.0

    def update(self, delta_time):
        """Update timer."""
        self.tick = self.tick + delta_time
        if self.tick > 1.0 and self.duration > 0:
            self.duration -= 1
            self.mins, self.secs = divmod(self.duration, 60)
            self.label.text = "{:02d}:{:02d}".format(self.mins, self.secs)
            self.tick = 0

def adjust_time(duration, start_meeting_minutes, start_minutes, start_seconds):
    if start_minutes > start_meeting_minutes:
        adjust_minutes = start_minutes - start_meeting_minutes
        return duration - adjust_minutes, start_seconds
    elif start_minutes == start_meeting_minutes:
        return duration - 1, start_seconds
    else:
        return duration, 0

NOW = datetime.now()
MINUTES, SECONDS = adjust_time(settings.DURATION, settings.START_MEETING_MINUTE, NOW.minute, NOW.second)
TIME_LABEL = pyglet.text.Label(text="{:02d}:{:02d}".format(MINUTES, SECONDS), font_size=36, x=100, y=300)
TIMER = Timer(MINUTES, SECONDS, TIME_LABEL)

# FPS = pyglet.clock.ClockDisplay()

@SCREEN.event
def on_draw():
    """Window draw event handler."""
    SCREEN.clear()
    # FPS.draw()
    if GAME.over():
        GAME_OVER_IMAGE.draw()
        GAME_OVER_MESSAGE.draw()
        if not GAME.said_goodbye():
            GAME_OVER_SOUND.play()
            GAME.goodbye()
    else:
        PLAYER_MESSAGES[GAME.get_player()].draw()
        QUESTIONS[GAME.get_question()].draw()
        PLAYER_IMAGES[GAME.get_player()].blit(WIDTH, HEIGHT - HEIGHT_BORDER)
        TIMER.label.draw()

@SCREEN.event
def on_key_press(symbol, modifiers):
    """Key pressed event handler."""
    if symbol == key.SPACE:
        if GAME.said_goodbye():
            pyglet.app.exit()
        GAME.step()

if __name__ == "__main__":
    pyglet.clock.schedule_interval(TIMER.update, 0.1)
    pyglet.app.run()
