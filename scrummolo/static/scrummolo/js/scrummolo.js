
// Game module

// Fisher-Yates
function shuffle(array) {
    var m = array.length, t, i;
    // While there remain elements to shuffle…
    while (m) {
        // Pick a remaining element…
        i = Math.floor(Math.random() * m--);
        // And swap it with the current element.
        t = array[m];
        array[m] = array[i];
        array[i] = t;
    }
    return array;
}

// Calculates new width and height but leave w/h ratio invariant.
function resize(width, height, maxWidth, maxHeight) {
    delta_width = width - maxWidth;
    delta_height = height - maxHeight;
    if (delta_height <= 0 && delta_width <= 0) {
        return [width, height];
    }
    if (delta_height >= delta_width) {
        return [width * maxHeight / height, maxHeight];
    }
    return [maxWidth, height * maxWidth / width];
}

function resizeImage(image) {
    var dimensions = resize(image.width, image.height, app.width / 2, app.height / 2);
    image.displayWidth = dimensions[0];
    image.displayHeight = dimensions[1];
}

function getPlayerResourceName(playerName) {
    return playerName.replace(/\./, '').replace(/\s/, '_').toLowerCase();
}

// Game Code

var app = {
    width: 800,
    height: 600,
    yMargin: 10,
    playerIndex: 0,
    questionIndex: 0,
    gameOver: false,
    setConfig: function (config) {
        this.cfg = config;
        this.questions = config.questions;
    },
    getPlayer: function () {
        return this.team[this.playerIndex];
    },
    getQuestion: function () {
        return this.questions[this.questionIndex];
    },
    step: function () {
        if (this.questionIndex < this.questions.length - 1) {
            this.questionIndex++;
        } else {
            if (this.playerIndex === this.team.length -1) {
                this.gameOver = true;
            } else {
                this.questionIndex = 0;
                this.playerIndex++;
            }
        }
    }
}

var gameLoop = {
    preload: function () {
        app.game = this;
        var team = shuffle(app.cfg.team);
        app.team = team;
        team.forEach(function (player) {
            var imgPath = app.cfg.resources + '/' + getPlayerResourceName(player) + '.png';
            app.game.load.image(player, imgPath);
        });
    },
    create: function () {
        var playerImage = app.game.add.image(app.width / 2, app.yMargin, app.team[0]).setOrigin(0, 0);
        resizeImage(playerImage);
        app.playerImage = playerImage;
        app.playerText = app.game.add.text(100, 100, app.getPlayer() + ', is your turn!', { font: '20px Arial', fill: '#fff' });
        app.questionsText = app.game.add.text(100, 500, app.getQuestion(), { font: '40px Arial', fill: '#fff' });
        app.spaceKey = app.game.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.SPACE);
    },
    update: function () {
        if (Phaser.Input.Keyboard.JustDown(app.spaceKey)) {
            if (!app.gameOver) {
                app.step();
                app.questionsText.setText(app.getQuestion());
                app.playerText.setText(app.getPlayer() + ', is your turn!');
                app.playerImage.setTexture(app.getPlayer());
                resizeImage(app.playerImage);
            }
        }
    }
}

var game_engine_config = {
    type: Phaser.AUTO,
    width: app.width,
    height: app.height,
    scene: [gameLoop]
}
