
// Scrummolo game starts from here

// Start jquery
$(function() {
    // Get config data from REST API
    $.getJSON($SCRIPT_ROOT + '/team/1', function(data) {
        app.setConfig(data.team);
        new Phaser.Game(game_engine_config);
    });
});
