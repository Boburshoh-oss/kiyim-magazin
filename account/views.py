from django.forms import ValidationError
from django.shortcuts import redirect, render
from django.contrib import messages
from account.forms import RegisterForm
from account.models import Account
from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from cards.models import Card, CardItem
from cards.views import _card_id
import requests

# Create your views here.
def register(request):
    form = None
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            
            user = Account.objects.create_user(
                first_name = first_name,
                last_name = last_name,
                email = email,
                username = username,
                password = password
            )
            user.phone_number = phone_number
            user.save()
            
            #User activation
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            
            message = render_to_string('accounts/account_verification_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject,message, to=[to_email])
            # send_email.content_subtype = 'html'
            try:
                send_email.send()
            except:
                ValidationError("Please check your internet!")
            # messages.success(request,"Thanks you for registration with us. We have sent you a verification emailto your email address. Please verify it.")
            
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form = RegisterForm()
    context = {
        "form":form
    }
    return render(request,'accounts/register.html',context)

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request,email=email, password=password)
        if user is not None:
            try:
                cart = Card.objects.get(card_id=_card_id(request))
                is_cart_item_exists = CardItem.objects.filter(card=cart).exists()
                if is_cart_item_exists:
                    cart_item = CardItem.objects.filter(card=cart)
                    
                    #Getting the product variations by cart id
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))
                    
                    cart_item = CardItem.objects.filter(user=user)
            
                    ex_var_list = []
                    id = []
                    for it in cart_item:
                        existing_variation = it.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(int(it.id))
                    
                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CardItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user=user
                            item.save()
                        else:
                            cart_item = CardItem.objects.filter(card=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
                    
            except:
                pass
            
            login_auth(request,user)
            messages.success(request,"You are logged in.")
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                #next cart checkout
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('dashboard')
        
        else:
            messages.error(request,"Invalid login credentials")
            return redirect('login')
    return render(request,'accounts/login.html')

@login_required(login_url='login')
def logout(request):
    logout_auth(request)
    messages.success(request, "You are logged out.")
    return redirect('login')

def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request,'Congratulation! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request,'Invalid activation link')
        return  redirect('register')

@login_required(login_url='login')
def dashboard(request):
    return render(request,"accounts/dashboard.html")

def forgotpassword(request):
    if request.method == "POST":
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            
            #Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            
            message = render_to_string('accounts/reset_password_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject,message, to=[to_email])
            # send_email.content_subtype = 'html'
            try:
                send_email.send()
            except:
                ValidationError("Please check your internet!")
            messages.success(request,"Password reset email has been sent to your email address.")
            return redirect('login')
        else:
            messages.error(request,'Account does not exists')
            return redirect('forgotpassword')
    return render(request,'accounts/forgotPassword.html')

def resetpassword_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your passwor')
        return redirect('resetPassword')
    else:
        messages.error(request,"This link has been expired!")
        return redirect('login')

def resetPassword(request):
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Password reset successful')
            return redirect('login')
        else:
            messages.error(request,'Password do not match!')
            return redirect('resetPassword')
    else:
        return render(request,'accounts/resetPassword.html')