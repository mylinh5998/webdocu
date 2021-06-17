function updateProfile() {
    $.ajax({
        type: "POST",
        url: '/user/profile/edit/',
        data: $('#formUpdate').serialize(),
        success: function (response) {
            if (response["result"] != "OK") return
            if (response["errors"].length == 0) {
                window.location.replace($(location).attr("href"))
                return
            }
            strError = ""
            response["errors"].forEach((item) => {
                strError += item + "<br>"
            })
            $("#errors").html(strError)
            return
        }
    });
    return false;
}