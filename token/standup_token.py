
"A virtual talking stick."

from random import shuffle

import pyglet
from pyglet.window import key

import settings

#index all resources. Resources folder must be on same level as this file.
pyglet.resource.path = settings.RESOURCES
pyglet.resource.reindex()

#create window object
screen = pyglet.window.Window(800, 600)

#create Team
team = settings.TEAM
shuffle(team)

def resize(w, h, maxw, maxh):
    "Calculates new width and height but leave w/h ratio invariant."
    dw = w - maxw
    dh = h - maxh
    if dh <= 0 and dw <= 0:
        return w, h
    if dh >= dw:
        return w*maxh/h, maxh
    return maxw, h*maxw/w

#image dimensions
W = 400
H = 300
HBORDER = 10

def resize_image(image):
    "Resize but leave the ratio invariant."
    w, h = resize(image.width, image.height, W, H)
    image.width = w
    image.height = h

#create player objects. Player image must be in resource folder.
player_images = []
for player in team:
    player_image = pyglet.resource.image(player.lower() + ".png")
    resize_image(player_image)
    player_images.append(player_image)

game_over_image = pyglet.resource.image(settings.GAME_OVER_IMAGE)
resize_image(game_over_image)

applause = pyglet.resource.media(settings.GAME_OVER_SOUND, streaming=False)

#create text labels for questions
questions = ["On what I worked yesterday?", "On what I will work today?", "Do I have any blocker?"]
questions = [pyglet.text.Label(text="{0}".format(q), font_size=36, x=100, y=100) for q in questions]

player_names = [pyglet.text.Label(text="{0}, is your turn!".format(name), font_size=18, x=100, y=500) for name in team]

game_over_msg = pyglet.text.Label(text="That's all Folks, Thank You!", font_size=36, x=100, y=100)

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

game = GameLogic(len(questions), len(team))

@screen.event
def on_draw():
    screen.clear()
    if game.over():
        game_over_image.blit(W, H - HBORDER)
        game_over_msg.draw()
        applause.play()
        game.goodbye()
    else:
        player_names[game.get_player()].draw()
        questions[game.get_question()].draw()
        player_images[game.get_player()].blit(W, H - HBORDER)

@screen.event
def on_key_press(symbol, modifiers):
    if symbol == key.SPACE:
        if game.said_goodbye():
            pyglet.app.exit()
        game.step()

if __name__ == "__main__":
    pyglet.app.run()
