
// Game engine configuration

var game_engine_config = {
    type: Phaser.AUTO,
    width: app.width,
    height: app.height,
    scene: [gameLoop]
}

// Game starts here, starting jQuery
$(function() {
    // Get config data from REST API
    $.getJSON('/js/config.json', function(data) {
        app.setConfig(data.config)
        app.setTeam(data.teams[0]);
        $('#loading').fadeOut('slow');
        new Phaser.Game(game_engine_config);
    });
});
