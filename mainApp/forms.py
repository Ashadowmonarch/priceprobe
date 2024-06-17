from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

class UserLoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'id': 'UserLoginFormUsername', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'id': 'UserLoginFormPassword', 'placeholder': 'Password'})
    )


class UserSignupForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'userSignupFormInformation'}))
    phoneNumber = forms.CharField(max_length=10, required=False,
                                  widget=forms.TextInput(attrs={'placeholder': 'Mobile Number', 'class': 'userSignupFormInformation'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'userSignupFormInformation'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'userSignupFormInformation'}))
    class Meta:
        model = User
        fields = ['email', 'phoneNumber', 'username', 'password1']


class ChangeUserInformationForm(forms.Form):
    changeUsername = forms.CharField(disabled=True,widget=forms.TextInput(attrs={'placeholder': 'Username',
    'class':'userChangeAccountInformation','name': 'changeUsernameField'}))

    changeFullName = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Full Name',
    'class':'userChangeAccountInformation',"name":"changeFullNameField"}))

    changePhoneNumber = forms.CharField(max_length=12, required=False,widget=forms.TextInput(attrs={'placeholder': 'Mobile Number',
    'class':'userChangeAccountInformation',"name":"changePhoneNumberField"}))

    changeEmail = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email',
    'class':'userChangeAccountInformation',"name":"changeEmailField"}))

    changeProfilePicture = forms.ImageField(widget=forms.FileInput(attrs={
    "class":"changeProfilePicture","name":"changeProfilePicture","id":"changeProfilePicture"}));

class SearchPageSearchForm(forms.Form):
    searchBar = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Search for deals on your favourite items',
    'class':'searchBar','name': 'searchBarName'}))

class SavedPageSearchForm(forms.Form):
    savedPageSearchBar = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Search your saved items...',
    'class':'searchBar','name': 'savedPageSearchBar'}))

class TrendingPageSearchForm(forms.Form):
    trendingPageSearchBar = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Search for trending deals...',
    'class':'searchBar','name': 'trendingPageSearchBar'}))
