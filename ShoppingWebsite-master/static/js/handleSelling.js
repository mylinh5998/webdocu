$(".show-detail").click((event) => {
    let id = event.target.dataset["id"]
    let stt = document.getElementById("view-" + id).style.display
    if (stt == "none") document.getElementById("view-" + id).style.display = "block";
    else document.getElementById("view-" + id).style.display = "none";
})

$(".accept").click((event) => {
    let id = event.target.dataset["id"]
    $.ajax({
        url: "/order/accept/",
        type: "POST",
        data: {
            id: id,
            csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
        },
        success: (response) => {
            if (response["result"] == "OK") {
                window.location.href = "/order/selling/"
            } else {
                swal("Đã xảy ra lỗi", response["error"], "error")
            }
        }
    })
})