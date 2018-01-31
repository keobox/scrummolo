
"A virtual talking stick."

from random import shuffle

import pyglet
from pyglet.window import key

import settings

#index all resources. Resources folder must be on same level as this file.
pyglet.resource.path = settings.RESOURCES
pyglet.resource.reindex()

#create window object
SCREEN = pyglet.window.Window(800, 600)

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
        return width*max_height/height, max_height
    return max_width, height*max_width/width

#image dimensions
W = 400
H = 300
HBORDER = 10

def resize_image(image):
    "Resize but leave the ratio invariant."
    width, height = resize(image.width, image.height, W, H)
    image.width = width
    image.height = height

#create player objects. Player image must be in resource folder.
PLAYER_IMAGES = []
for player in TEAM:
    player_image = pyglet.resource.image(player.lower() + ".png")
    resize_image(player_image)
    PLAYER_IMAGES.append(player_image)

GAME_OVER_IMAGE = pyglet.resource.image(settings.GAME_OVER_IMAGE)
resize_image(GAME_OVER_IMAGE)
GAME_OVER_SOUND = pyglet.resource.media(settings.GAME_OVER_SOUND, streaming=False)
#create text labels for questions
QUESTIONS = ["On what I worked yesterday?", "On what I will work today?", "Do I have any blocker?"]
QUESTIONS = [pyglet.text.Label(text="{0}".format(q), font_size=36, x=100, y=100) for q in QUESTIONS]

PLAYER_MESSAGES = [pyglet.text.Label(text="{0}, is your turn!".format(name),
                   font_size=18, x=100, y=500) for name in TEAM]
GAME_OVER_MESSAGE = pyglet.text.Label(text="That's all Folks, Thank You!",
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

@SCREEN.event
def on_draw():
    """Window draw event handler."""
    SCREEN.clear()
    if GAME.over():
        GAME_OVER_IMAGE.blit(W, H - HBORDER)
        GAME_OVER_MESSAGE.draw()
        GAME_OVER_SOUND.play()
        GAME.goodbye()
    else:
        PLAYER_MESSAGES[GAME.get_player()].draw()
        QUESTIONS[GAME.get_question()].draw()
        PLAYER_IMAGES[GAME.get_player()].blit(W, H - HBORDER)

@SCREEN.event
def on_key_press(symbol, modifiers):
    """Key pressed event handler."""
    if symbol == key.SPACE:
        if GAME.said_goodbye():
            pyglet.app.exit()
        GAME.step()

if __name__ == "__main__":
    pyglet.app.run()
