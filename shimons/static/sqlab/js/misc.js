$(document).ready(function () {
    $('#reg-btn').attr("disabled", true);
    $("#terms-checkbox").click(function () {
        $("#reg-btn").attr("disabled", !this.checked);
    });

});
