
// Scrummolo game starts from here

// Start jquery
$(function() {
    // Get config data from REST API
    $.getJSON($SCRIPT_ROOT + '/scrummolo/api/v1/configs/1', function(data) {
        scrummolo(data.config);
    });
});
