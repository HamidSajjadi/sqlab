var $content = $('.nav-content');

function showContent(selector) {
    $content.hide();
    $(selector).show();
}
//
$(document).ready(function () {

    if (window.location.hash) {
        var hash = location.hash;
        showContent(hash);
    } else {
        showContent('#main');
    }
});

$('.nav').on('click', '.nav-btn', function (e) {
    alert("okay");
    showContent(e.currentTarget.hash);
});