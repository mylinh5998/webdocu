//see small img
$(".small-img").click((event) => {
    $("#main-img").attr("src", event.target.src)
})
//order
$("#orderBtn").click((event) => {
    $.ajax({
        type: "POST",
        url: "/order/new-order/",
        data: $("#form-order").serialize(),
        success: (response) => {
            if (response["result"] === "OK") swal("Thành công!", "Cảm ơn bạn đặt hàng", "success")
            else swal("Đã xảy ra lỗi!", response["message"], "error")
        }
    })
})