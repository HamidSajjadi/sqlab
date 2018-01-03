from shimons import models
from django import forms


class UserForm(forms.ModelForm):
    options = (('Option 1 v', 'Option 1 t'), ('Option 2 v', 'Option 2 t'),)

    # education = forms.CharField(widget=forms.CharField(attrs={'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "First Name"}))
    education = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "Education"}))
    university = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "University"}))

    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "Last Name"}))
    field = forms.ModelChoiceField(queryset=models.Field.objects.all(),
                                   widget=forms.Select(attrs={'class': 'form-control', "placeholder": "Field"}))
    # field = forms.ChoiceField(choices=options,
    #                           widget=forms.ModelChoiceField(attrs={'class': 'form-control', "placeholder": "Field"},
    #                                                         queryset=models.Field.objects.all()))
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
        model = models.UserProfile
        fields = ('education', 'first_name', 'last_name', 'field', 'email', 'password', 'university')
