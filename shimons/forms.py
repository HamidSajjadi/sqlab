from shimons import models
from django import forms


class UserForm(forms.ModelForm):
    # education = forms.CharField(widget=forms.CharField(attrs={'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "First Name"}))
    education = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "Education"}))
    university = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "University"}))

    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "Last Name"}))
    field = forms.ModelChoiceField(queryset=models.Field.objects.all(),
                                   widget=forms.Select(attrs={'class': 'form-control', "placeholder": "Field"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control', "placeholder": "Email"}))
    # password = forms.PasswordInput(attrs={'required': True, 'class': 'form-control'})
    password = forms.CharField(max_length=32,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', "placeholder": "Password"}))

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    class Meta:
        model = models.User
        fields = ('education', 'first_name', 'last_name', 'field', 'email', 'password', 'university')


class PatternForm(forms.Form):
    user = None

    request = forms.ModelChoiceField(queryset=models.Request.objects.all(),
                                     widget=forms.Select())

    files = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True, 'style': 'color:#d0cdcd;', 'accept': '.txt', 'name':'pattern-files'}))
