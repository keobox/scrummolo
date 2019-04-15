
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
    var dimensions = resize(image.displayWidth, image.displayHeight, app.width / 2, app.height / 2);
    image.displayWidth = dimensions[0];
    image.displayHeight = dimensions[1];
}

// Game Code

var app = {
    width: 800,
    height: 600,
    yMargin: 10,
    setConfig: function (config) {
        this.cfg = config;
    },
    setTeam: function (team) {
        this.team = team;
    }
}

var gameLoop = {
    preload: function () {
        var game = this;
        var team = shuffle(app.cfg.team);
        app.setTeam(team);
        team.forEach(function (player) {
            var imgPath = app.cfg.resources + '/' + player.toLowerCase() + '.png';
            game.load.image(player, imgPath);
        });
    },
    create: function () {
        var game = this;
        var image = game.add.image(app.width / 2, app.yMargin, app.team[0]).setOrigin(0, 0);
        resizeImage(image);
    },
    update: function () {
    }

}

var game_engine_config = {
    type: Phaser.AUTO,
    width: app.width,
    height: app.height,
    scene: {
        preload: gameLoop.preload,
        create: gameLoop.create,
        update: gameLoop.update
    }
}
