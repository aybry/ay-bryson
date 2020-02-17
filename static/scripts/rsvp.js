function radioToggleRSVP(val) {
    if (val == "1") {
        $("#rsvp-radio-yes").addClass("selected");
        $("#rsvp-radio-no").removeClass("selected");
        $("#rsvp-response").text(val);
        $("#attendees").attr("type", "number").attr("required", true);
    } else if (val == "0") {
        $("#rsvp-radio-no").addClass("selected");
        $("#rsvp-radio-yes").removeClass("selected");
        $("#rsvp-response").text(val);
        $("#attendees").attr("type", "hidden").attr("required", false);
    }
}

// function sendRSVP() {
//     $("#rsvp-form").submit();
// }