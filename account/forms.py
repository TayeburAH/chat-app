from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from .models import Account


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')

    class Meta:
        model = Account
        fields = ('email', 'username', 'password1', 'password2',)
        # 'password1', 'password2' are obtained from built in UserCreationForm

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % account)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError('Username "%s" is already in use.' % username)


# ----------------------------- Build you own UserCreationForm  --------------------------
'''
forms.py
class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'password1',
        'placeholder': 'Enter password here'
    }))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={
        'class': 'password2',
        'placeholder': 'Enter same password here'
    }))
    email = forms.CharField(label='Email or mobile number', widget=forms.EmailInput(attrs={
        'class': 'email',
        'placeholder': 'email'
    }))

    class Meta:
        model = User
        fields = []  # add the required field here

    def clean(self):
        """
        Verify both passwords match.
        """
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 is not None and password1 != password2:
            self.add_error("password2", "Your passwords must match")
        return cleaned_data

    # All emails are saved as lower case, lower case the email you get in the form and check
    # Otherwise it will be saved as new email same, but upper and lowercase mixtures
    # def clean_email(self):
    #     email = self.cleaned_data['email'].lower()
    #     try:
    #         user = User.objects.get(email=email)
    #     except Exception as e:
    #         return email
    # raise forms.ValidationError("Email already exists")
    #     self.add_error("email", "Email already exists")
    @transaction.atomic
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password2"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['email', 'password', 'is_active', 'is_superuser']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
        # This removes the password too short and 8 characters rules
        
 """
 Than use it in class CustomerForm(UserAdminCreationForm): 
 """


In admin.py
 
 
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm


User = get_user_model()


# Remove Group Model from admin. We're not using it.
# admin.site.unregister(Group)


class AccountAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the custom User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['email', 'date_joined', 'last_joined', 'is_active', 'is_superuser',
                    'is_customer','first_name',
                    'is_superuser', ]
    list_filter = ['date_joined', 'email']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('profile_image', 'first_name', 'last_name', 'otp', 'DOB')}),
        ('Permissions', {'fields': ('is_superuser', 'is_customer', 'is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}  # add required field
         ),
    )
    search_fields = ['email']
    ordering = ['email']
    readonly_fields = ('id', 'date_joined', 'last_joined', 'otp')  # to prevent from changing
    # filter_horizontal = ()   # Enabling this distorts Gropus and permission table
    
    
    admin.site.register(User, UserAdmin)
'''


class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login")


class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('username', 'email', 'profile_image', 'hide_email')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % account)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError('Username "%s" is already in use.' % username)

    def save(self, commit=True):
        account = super(AccountUpdateForm, self).save(commit=False)
        account.username = self.cleaned_data['username']
        account.email = self.cleaned_data['email'].lower()
        account.profile_image = self.cleaned_data['profile_image']
        account.hide_email = self.cleaned_data['hide_email']
        if commit:
            account.save()
        return account
