from django import forms


class AddProductForm(forms.Form):
    name = forms.CharField(max_length=500, required=True, error_messages={"max_length": "Tên sản phẩm quá dài",
                                                                          "required": "Tên sản phẩm là trường bắt buộc"})
    describe = forms.CharField(max_length=500, required=False,
                               error_messages={"max_length": "Trường mô tả chỉ được tối đa gồm 500 kí tự"})
    content = forms.CharField(max_length=1000, required=False,
                              error_messages={"max_length": "Trường nội dung chỉ được tối đa gồm 1000 kí tự"})
    available = forms.IntegerField(min_value=0, required=True,
                                   error_messages={"min_value": "Số sản phẩm phải là số nguyên dương"})
    price = forms.IntegerField(min_value=0, required=False,
                               error_messages={"min_value": "Giá tiền phải là số nguyên dương"})
    discount = forms.IntegerField(min_value=0, max_value=100, required=False,
                                  error_messages={"min_value": "Giá tiền phải là số nguyên dương từ 0 đến 100",
                                                  "max_value": "Giá tiền phải là số nguyên dương từ 0 đến 100"})
    mainPicture = forms.ImageField(required=False)
    pictures = forms.ImageField(widget=forms.ClearableFileInput(attrs={"multiple": True}), required=False)
