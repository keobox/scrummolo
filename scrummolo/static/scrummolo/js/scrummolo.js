
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
    setConfig: function (config) {
        this.cfg = config;
    },
    preload: function () {
        var game = this;
        var team = shuffle(app.cfg.team);
        app.cfg.team = team;
        team.forEach(function (player) {
            var imgPath = app.cfg.resources + '/' + player.toLowerCase() + '.png';
            game.load.image(player, imgPath);
        });
        console.log(game);

    },
    create: function () {
        var game = this;
        var team = app.cfg.team;
        game.add.image(400, 10, team[0]).setOrigin(0,0);
    },
    update: function () {
    }
}

var game_engine_config = {
    type: Phaser.AUTO,
    width: 800,
    height: 600,
    scene: {
        preload: app.preload,
        create: app.create,
        update: app.update
    }
}