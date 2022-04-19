from django import forms
from .models import Account

class RegisterForm(forms.ModelForm):
    # first_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={
    #     'class':'form-control'
    # }))
    # last_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={
    #     'class':'form-control'
    # }))
    # email = forms.CharField(max_length=100,widget=forms.TextInput(attrs={
    #     'class':'form-control'
    # }))
    # phone_number = forms.CharField(max_length=13,widget=forms.NumberInput(attrs={
    #     'class':'form-control'
    # }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter Password',
        # 'class':'form-control'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Repeat Password',
        # 'class':'form-control'
    }))
    
    class Meta:
        model = Account
        fields = ["first_name","last_name","phone_number","email","password","confirm_password"]
        
    def clean(self):
        clean_data = super(RegisterForm,self).clean()
        password = clean_data.get('password')
        confirm_password = clean_data.get('confirm_password')
        
        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )
            
    def __init__(self,*args,**kwargs):
        super(RegisterForm,self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
    
    