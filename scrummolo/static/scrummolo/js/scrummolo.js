
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

// Game Code

var app = {
    width: 800,
    height: 600,
    setConfig: function (config) {
        this.cfg = config;
    },
    setTeam: function(team) {
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
        game.add.image(app.width / 2, 10, app.team[0]).setOrigin(0, 0);
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
