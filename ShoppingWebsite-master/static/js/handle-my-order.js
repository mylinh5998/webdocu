$(".number").change((event) => {
    const price = event.target.parentElement.parentElement.childNodes[5].innerText
    const number = event.target.value
    event.target.parentElement.parentElement.childNodes[9].innerText = Number(price) * Number(number) + "đ"
})

$("#delete").click(() => {
    const listOrders = []
    const listCheckbox = document.getElementsByClassName("cb-order")
    for (let i = 0; i < listCheckbox.length; i++)
        if (listCheckbox[i].checked)
            if (Number(listCheckbox[i].dataset.mode) == 2) {
                swal("Xảy ra lỗi", "Bạn không thể xóa mặt hàng đã được chấp nhận", "error")
                return;
            } else listOrders.push(listCheckbox[i].value)
    if (listOrders.length == 0) {
        swal("Đã xảy ra lỗi", "Vui lòng chọn ít nhất một đơn hàng", "error")
        return;
    }
    $.ajax({
        url: "/order/delete/",
        type: "POST",
        data: {
            orders: listOrders,
            csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
        },
        success: (response) => {
            if (response["result"] == "OK") {
                swal("Thành công", "Đã xóa sản phẩm bạn chọn", "success")
                for (let i = 0; i < listCheckbox.length; i++)
                    if (listCheckbox[i].checked) {
                        listCheckbox[i].parentElement.parentElement.remove()
                        i -= 1
                    }
            } else {
                swal("Đã xảy ra lỗi", response["error"], "error")
                window.location.href = "/order/my-order/"
            }
        }
    })
})

$("#updateNumber").click((event) => {
    const data = {
        csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
    }
    allNumber = $(".number")
    Array.from(allNumber).forEach((item) => {
        data[String(item.dataset["id"])] = Number(item.value)
    })
    $.ajax({
        url: "/order/update/",
        type: "POST",
        data: data,
        success: (response) => {
            if (response["result"] == "OK")
                swal("Thành công", "Đã cập nhật số lượng thành công", "success")
            else
                swal("Đã xảy ra lỗi", "Không thể cập nhật số lượng", "error")
        }
    })
})

$("#handleOrder").click(() => {
    const listOrders = []
    const listCheckbox = document.getElementsByClassName("cb-order")
    for (let i = 0; i < listCheckbox.length; i++)
        if (listCheckbox[i].checked)
            if (Number(listCheckbox[i].dataset.mode) >= 2) {
                swal("Xảy ra lỗi", "Bạn không thể đặt hàng đã được chấp nhận. Hãy xóa đơn hàng đã thành công để đặt mới", "error")
                return;
            } else listOrders.push(listCheckbox[i].value)
    if (listOrders.length == 0) {
        swal("Đã xảy ra lỗi", "Vui lòng chọn ít nhất một đơn hàng", "error")
        return;
    }
    $.ajax({
        url: "/order/handle-order/",
        type: "POST",
        data: {
            orders: listOrders,
            csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
        },
        success: (response) => {
            if (response["result"] == "OK") {
                window.location.href = "/order/my-order/"
            } else {
                swal("Đã xảy ra lỗi", response["error"], "error")
                window.location.href = "/order/my-order/"
            }
        }
    })
})

$(".addInfo").click(async (event) => {
    /* get data */
    let textarea = document.createElement('textarea');
    let oldContent = "";
    textarea.rows = 6;
    textarea.className = 'swal-content__textarea';
    await $.ajax({
        url: "/order/get-info/",
        type: "GET",
        data: {id: event.target.dataset["id"]},
        success: (response) => {
            if (response["result"] === "OK") {
                textarea.value = response["content"]
                oldContent = response["content"]
            } else {
                return;
            }
        }
    })
    let clickOk = await swal("Nhập ghi chú của bạn về đơn hàng:", {
        content: textarea,
    })
    if (oldContent === textarea.value) return;
    await $.ajax({
        url: "/order/update-info/",
        type: "POST",
        data: {
            id: event.target.dataset["id"],
            content: textarea.value,
            csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
        },
        success: (response) => {
            if (response["result"] === "OK") {
                swal("Cập nhật thành công")
            } else {
                swal("Cập nhật không thành công")
            }
        }
    })
})

$(".received").click((event) => {
    let id = event.target.dataset["id"]
    $.ajax({
        url: "/order/received/",
        type: "POST",
        data: {
            id: id,
            csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
        },
        success: (response) => {
            if (response["result"] == "OK") {
                window.location.href = "/order/my-order/"
            } else {
                swal("Đã xảy ra lỗi", response["error"], "error")
            }
        }
    })
})