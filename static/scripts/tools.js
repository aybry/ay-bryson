$("document").ready(function () {
    $("#flash-container").delay(400).animate({ opacity: 1 }, 800);
});

function showDetails(elem) {
    pageScroll();
    $("#details-cont").hide();
}


function pageScroll() {
    var pageHeight = $(window).height();
    $('body, html').animate({scrollTop: pageHeight}, 800); 
}