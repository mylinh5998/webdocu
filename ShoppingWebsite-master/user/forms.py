from django import forms
from . import models
from django.utils import timezone
import re


class RegisterForm(forms.ModelForm):
    class Meta:
        model = models.MyUser
        fields = ("username", "password", "first_name", "last_name", "sex", "date_of_birth", "email", "phone",
                  "address", "avatar")
        widgets = {
            "date_of_birth": forms.SelectDateWidget(years=range(timezone.datetime.today().year - 100,
                                                                timezone.datetime.today().year)),
            "address": forms.Textarea(attrs={"rows": "3", "placeholder": "Số nhà, quận (huyện), tỉnh (thành phố)"}),
            "username": forms.TextInput(attrs={"placeholder": "Nhập tên đăng nhập"}),
            "password": forms.PasswordInput(attrs={"placeholder": "Mật khẩu"}),
            "email": forms.EmailInput(attrs={"placeholder": "Nhập địa chỉ email"}),
            "first_name": forms.TextInput(attrs={"placeholder": "Minh"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Nguyễn Văn"}),
            "phone": forms.TextInput(attrs={"placeholder": "09094509"}),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data["first_name"]
        if not first_name:
            raise forms.ValidationError("Bạn không được để trống trường tên")
        if not "".join(first_name.split()).isalpha():
            raise forms.ValidationError("Tên chỉ được phép chứa các chữ cái")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data["last_name"]
        if not last_name:
            return last_name
        if not "".join(last_name.split()).isalpha():
            raise forms.ValidationError("Họ và tên lót chỉ được phép chứa các chữ cái")
        return last_name

    def clean_password(self):
        password = self.cleaned_data["password"]
        if not len(password) > 10:
            raise forms.ValidationError("Mật khẩu phải dài hơn 10 kí tự")
        if " " in password:
            raise forms.ValidationError("Mật khẩu không được chứa khoảng trắng")
        return password

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        if not phone:
            return phone
        if not re.match("^[0-9+]*$", phone):
            raise forms.ValidationError("Số điện thoại chỉ có thể chưa chữ số và kí tự +")
        return phone

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UpdateProfileForm(forms.Form):
    first_name = forms.CharField(required=True, max_length=255,
                                 widget=forms.TextInput(attrs={"class": "form-control input-md"}))
    last_name = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={"class": "form-control input-md"}))
    phone = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={"class": "form-control input-md"}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={"class": "form-control input-md"}))
    address = forms.CharField(required=False,
                              widget=forms.Textarea(attrs={"class": "form-control input-md", "rows": "3"}))
    password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={"class": "form-control input-md"}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control input-md"}))
    sex = forms.IntegerField(
        widget=forms.Select(choices=((0, "Không xác định"), (1, "Nam"), (-1, "Nữ")), attrs={"class": "form-control"}))
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(
        years=range(timezone.datetime.today().year - 100, timezone.datetime.today().year),
        months={
            1: "Tháng một",
            2: "Tháng hai",
            3: "Tháng ba",
            4: "Tháng tư",
            5: "Tháng năm",
            6: "Tháng sáu",
            7: "Tháng bảy",
            8: "Tháng tám",
            9: "Tháng chín",
            10: "Tháng mười",
            11: "Tháng mười một",
            12: "Tháng mười hai",
        },
        attrs={"class": "form-control"}), )

    # Validate

    def clean_first_name(self):
        first_name = self.cleaned_data["first_name"]
        if not first_name:
            raise forms.ValidationError("Bạn không được để trống trường tên")
        if not "".join(first_name.split()).isalpha():
            raise forms.ValidationError("Tên chỉ được phép chứa các chữ cái")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data["last_name"]
        if not last_name:
            return last_name
        if not "".join(last_name.split()).isalpha():
            raise forms.ValidationError("Họ và tên lót chỉ được phép chứa các chữ cái")
        return last_name

    def clean_password(self):
        password = self.cleaned_data["password"]
        if not len(password) > 10 and password != "":
            raise forms.ValidationError("Mật khẩu phải dài hơn 10 kí tự")
        if " " in password:
            raise forms.ValidationError("Mật khẩu không được chứa khoảng trắng")
        return password

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        if not phone:
            return phone
        if not re.match("^[0-9]*$", phone) or phone[0] != "0":
            raise forms.ValidationError("Số điện thoại không hợp lệ")
        return phone


class AvatarForm(forms.Form):
    avatar = forms.ImageField()
