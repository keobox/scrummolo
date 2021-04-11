
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
    var delta_width = width - maxWidth;
    var delta_height = height - maxHeight;
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

// Game Logic

var app = {
    width: 800,
    height: 600,
    yMargin: 10,
    playerIndex: 0,
    questionIndex: 0,
    gameOver: false,
    isFinalScreenDisplayed: false,
    isTimerElapsed: false,
    setConfig: function (config) {
        this.cfg = config;
        this.questions = config.questions;
        this.timerSeconds = config.duration * 60;
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
            if (this.playerIndex == this.team.length - 1 && this.questionIndex === this.questions.length - 1) {
                this.gameOver = true;
            }
        } else {
            if (this.playerIndex < this.team.length - 1) {
                this.questionIndex = 0;
                this.playerIndex++;
            }
        }
    },
    tick: function () {
        if (this.timerSeconds > 0) {
            this.timerSeconds--;
            var minute = parseInt(this.timerSeconds / 60);
            var seconds = this.timerSeconds % 60;
            this.timerText.setText(this.fillWithZero(minute) + ':' + this.fillWithZero(seconds));
        } else {
            if (!this.isTimerElapsed) {
                this.isTimerElapsed = true;
                this.timerText.setColor('#ff0000');
            }
        }
    },
    fillWithZero: function (n) {
        if (n < 10) {
            return '0' + n;
        }
        return n;
    }
}

// Game Loop Scene

var gameLoop = new Phaser.scene('gameLoop');

gameLoop.preload = function () {
    app.game = this;
    var team = shuffle(app.cfg.team);
    app.team = team;
    team.forEach(function (player) {
        var imgPath = app.cfg.resources + '/' + getPlayerResourceName(player) + '.png';
        app.game.load.image(player, imgPath);
    });
    app.game.load.image('gameOverImage', app.cfg.gameOverImage);
    app.game.load.audio('gameOverSound', app.cfg.gameOverSound);
}

gameLoop.create = function () {
    var playerImage = app.game.add.image(app.width / 2, app.yMargin, app.team[0]).setOrigin(0, 0);
    resizeImage(playerImage);
    app.playerImage = playerImage;
    app.playerText = app.game.add.text(100, 100, app.getPlayer() + ', is your turn!', { font: '21px Arial', fill: '#fff' });
    app.questionsText = app.game.add.text(100, 500, app.getQuestion(), { font: '40px Arial', fill: '#fff' });
    app.spaceKey = app.game.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.SPACE);
    app.gameOverSound = app.game.sound.add('gameOverSound');
    app.timerText = app.game.add.text(100, 300, app.cfg.duration + ':00', { font: '36px Arial', fill: '#fff' });
    app.timer = this.time.addEvent({ delay: 1000, callback: app.tick, callbackScope: app, loop: true });
}

gameLoop.update = function () {
    if (Phaser.Input.Keyboard.JustDown(app.spaceKey)) {
        if (!app.gameOver) {
            app.step();
            app.questionsText.setText(app.getQuestion());
            app.playerText.setText(app.getPlayer() + ', is your turn!');
            app.playerImage.setTexture(app.getPlayer());
            resizeImage(app.playerImage);
        } else {
            if (!app.isFinalScreenDisplayed) {
                app.isFinalScreenDisplayed = true;
                app.playerText.destroy();
                app.questionsText.destroy();
                app.playerImage.destroy();
                app.timerText.destroy();
                app.game.add.text(100, 500, app.cfg.gameOverText, { font: '40px Arial', fill: '#fff' });
                var gameOverImage = app.game.add.image(app.width / 2, app.yMargin, 'gameOverImage').setOrigin(0, 0);
                resizeImage(gameOverImage);
                app.gameOverSound.play();
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
