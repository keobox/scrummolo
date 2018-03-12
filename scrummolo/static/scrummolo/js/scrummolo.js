
$(function() {
    $.getJSON($SCRIPT_ROOT + '/scrummolo/api/v1.0/configs/1', null, function(data) {
        console.log(data.config);
    });
});
