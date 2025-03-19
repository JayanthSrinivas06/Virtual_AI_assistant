$(document).ready(function () {
    
    eel.expose(DisplayMessage);
    function DisplayMessage(message) {
        $(".voiceMessage").addClass("animated").text(message);
    }
});