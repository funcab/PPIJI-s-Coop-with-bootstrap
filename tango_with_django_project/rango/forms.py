from django import forms
from django.contrib.auth.models import User
from rango.models import Page, Category, UserProfile

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128,
                           help_text='Please enter the category name.')
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:

        #connect with model-category
        model = Category
        fields = ('name',)

class PageForm(forms.ModelForm):

    title = forms.CharField(max_length=128,
                            help_text='Please enter the title of the page.')
    url = forms.URLField(max_length=128,
                         help_text='Please enter the URL of the page.')
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    txt = forms.CharField(widget=forms.Textarea, help_text='Please enter the description of the page or the attachment you may upload.')

    file = forms.FileField(max_length=100, help_text='Please upload your attachment of the page.', required=False)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # def clean(self):
    #     cleaned_data = self.cleaned_data
    #     url = cleaned_data.get('url')
    #
    #     if url and not url.startwitch('http://'):
    #         url = 'http://'+url
    #         cleaned_data['url'] = url
    #
    #         return cleaned_data

    class Meta:
        model = Page
        exclude = ('category',)

class UserForm(forms.ModelForm):
    #password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email')

class UserProfileForm(forms.ModelForm):
    website = forms.URLField(required=False)
    picture = forms.ImageField(required=False)
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')