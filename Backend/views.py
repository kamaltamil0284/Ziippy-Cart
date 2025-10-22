from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from django.utils import timezone
from .forms import *
from .models import *
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


def IndexPage(request):
    category = Category.objects.filter(status=0)
    return render(request,'index.html',{'category':category})


def ProductCollections(request,name):
    if(Category.objects.filter(name=name,status=0)):
        products = Products.objects.filter(category__name=name)
        if products:    return render(request,'collections.html',{'products':products,'category_name':name})
        else:
            messages.warning(request,"No products available")
            return render(request,'collections.html',{'category_name':name})
    else:
        messages.warning(request,"No such category found!")
        return redirect('index')


def ProductView(request,name,product):
    if(Category.objects.filter(name=name,status=0)):
        products = Products.objects.get(product_name=product,status=0)
        if products:    return render(request,'products.html',{'product':products})
        else:
            messages.warning(request,"No products available")
            return render(request,'products.html')
    else:
        messages.warning(request,"No such category found!")
        return render(request,'products.html')


class SingupView(View):
    def get(self, request):
        form = UserForm()
        return render(request,'register.html',{'form':form})
    
    def post(self, request):
        form = UserForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration succesfull!")
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:    messages.warning(request,error)
        return render(request,'register.html',{'form':form})


def LoginUser(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        pwd = request.POST.get('password')
        user = authenticate(request,username=name,password=pwd)
        if user is not None:
            if not user.is_staff:
                login(request, user)
                messages.success(request,"Login successfull")
                return redirect('index')
            else:   return redirect('index')
        else:   messages.warning(request,"Invalid Username or Password")
    return render(request,'login.html')

@login_required(login_url='index')
def LogoutUser(request):
    if request.user.is_authenticated or not request.user.is_superuser:
        logout(request)
        messages.success(request,"Logout successfull")
        return redirect('index')

class ProfileView(LoginRequiredMixin, View):
    login_url = 'register'

    def get(self, request):
        user = request.user
        try:    user_details = UserDetails.objects.get(user=user)
        except UserDetails.DoesNotExist:    user_details = None
        userform = UserDetailsForm(instance=user_details)
        return render(request, 'profile.html', {'user': user,'user_detail': user_details,'userform': userform})

    def post(self, request):
        user = request.user
        try:    user_details = UserDetails.objects.get(user=user)
        except UserDetails.DoesNotExist:    user_details = None
        userform = UserDetailsForm(request.POST, instance=user_details)
        if userform.is_valid():
            user_details = userform.save(commit=False)
            user_details.user = user 
            user_details.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile') 
        else:   messages.error(request, 'There was an error updating your profile.')
        return render(request, 'profile.html', {'user': user,'user_detail': user_details,'userform': userform})

class CartView(LoginRequiredMixin, View):
    login_url = 'register'

    def get(self, request):
        cart =Cart.objects.filter(user=request.user.id).all().order_by('-created_at')
        if cart:
            total_amount = 0
            for item in cart:   total_amount += item.quantity * item.product.selling_price
            return render(request,'cart.html',{'cart':cart,'total':total_amount})
        else:   
            messages.warning(request,"Cart is empty")
            return render(request,'cart.html')

class AddCart(LoginRequiredMixin, View):
    login_url = 'register'

    def post(self,request,pid):
        uid = request.user.id
        quantity = int(request.POST.get('ProQty'))
        product_details = Products.objects.get(id=pid,status=0)
        if product_details:
            if product_details.quantity>=quantity:
                cart_item = Cart.objects.filter(user=uid,product=pid).first()
                if cart_item:
                    date = timezone.now()
                    print('date', date)
                    if cart_item.quantity != quantity:
                        Cart.objects.filter(user=uid,product=pid).update(quantity=quantity,created_at=date)
                        return redirect('cart')
                    else:   
                        Cart.objects.filter(user=uid,product=pid).update(created_at=date)
                        return redirect('cart')
                else:
                    Cart.objects.create(user=User.objects.get(id=uid),product=Products.objects.get(id=pid),quantity=quantity)
                    return redirect('cart')
            else:   messages.warning(request,"Limited stock is available")
        else:   messages.warning(request,"Not available")
        return redirect('cart')

class DeleteCart(LoginRequiredMixin, View):
    login_url = 'register'

    def post(self,request,id):
        cart_item = Cart.objects.get(id=id,user=request.user.id)
        cart_item.delete()
        return redirect('cart')
    

class FavouritView(LoginRequiredMixin, View):
    login_url = 'register'

    def get(self,request):
        fave_item = Favourite.objects.filter(user=request.user.id).all().order_by('-created_at')
        if fave_item:   return render(request,'favourite.html',{'favourite':fave_item})
        else:
            messages.success(request,"No items added to favourite")
            return render(request,'favourite.html')
    
    
class ToggleFavourite(LoginRequiredMixin, View):
    login_url = 'register'

    def post(self,request,pid):
        uid = request.user.id
        fave_item = Favourite.objects.filter(user=uid,product=pid).first()
        if fave_item:
            fave_item.delete()
            return redirect('favourite')
        else:
            Favourite.objects.create(user=User.objects.get(id=uid),product=Products.objects.get(id=pid))
            return redirect('favourite')
        
class PaymentView(LoginRequiredMixin, View):
    login_url = 'register'  

    def post(self, request, all):
        try:
            client = razorpay.Client(auth=("rzp_test_RTg9mWaNVjSuGb", "MOGKtpT6e05jaZnc3FEPFwbD"))

            if all == 'buy':
                total_amount = 0
                products = Cart.objects.filter(user=request.user).order_by('-created_at')

                for item in products:   total_amount += item.quantity * item.product.selling_price
                amount = int(total_amount * 100)  
                
                DATA = {
                    "amount": amount,
                    "currency": "INR",
                    "payment_capture": 1,
                }
                payment = client.order.create(data=DATA)
                return render(request, 'payment.html', {'buy': products,'total': total_amount,'payment': payment,'amount': amount,})
            else:
                pid = request.POST.get('pid')
                ProQty = int(request.POST.get('ProQty', 1))
                product = Products.objects.get(id=pid, status=0)
                if product.quantity >= ProQty:
                    total_amount = product.selling_price * ProQty
                    amount = int(total_amount * 100)
                    DATA = {
                        "amount": amount,
                        "currency": "INR",
                        "payment_capture": 1,
                    }
                    payment = client.order.create(data=DATA)
                    return render(request, 'payment.html', {'product': product,'ProQty': ProQty,'total': total_amount,'payment': payment,'amount': amount,})
                else:
                    messages.warning(request, "Product not available.")
                    return redirect('cart')

        except Exception as e:
            print("PaymentView Error:", e)
            messages.error(request, "Something went wrong with the payment.")
            return redirect('cart')


@method_decorator(csrf_exempt, name='dispatch')
class SuccessView(LoginRequiredMixin, View):
    login_url = 'profile'

    