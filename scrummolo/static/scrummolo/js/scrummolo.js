
// Game module

function scrummolo(config) {

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

    var game_engine_config = {
        type: Phaser.AUTO,
        width: 800,
        height: 600,
        scene : {
            preload : preload,
            create: create,
            update: update
        }
    }

    var game = new Phaser.Game(game_engine_config);

    function preload() {
        console.log(config);
        var team = shuffle(config.team);
        var playerImagePaths = [];
        team.forEach(function(player) {
            playerImagePaths.push(config.resources + '/' + player.toLowerCase() + '.png');
        });
        // TODO continue
        // var playerImages = [];
    }

    function create() {

    }

    function update() {

    }
}