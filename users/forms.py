# from django import forms
# from .models import UserProfile
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm

# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ('profile_pic','bio')
#         # exclude= ('user',)
#  #exclude dememizin sebebi biz oluşturduğumuz kullanıcının userProfileini oluşturmak iistiyoruz
# #bunu yaptığımız içinde views kısmında register olan kullanıcıyıya userprofile ı kaydettik 
# #eğer fieldsları all olark tanımlasaydık kayıtlı olan kullanıcılardan seçim yaptıracaktık

# class UserForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ('username', 'email')

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_pic', 'bio')

class UserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.exclude(pk=self.user.pk).filter(username=username).exists():
            raise forms.ValidationError('A user with that username already exists.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.exclude(pk=self.user.pk).filter(email=email).exists():
            raise forms.ValidationError('A user with that email already exists.')
        return email