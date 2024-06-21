from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from django.core.mail import send_mail


from .models import *
from .forms import *
from .selenium import *
from django.utils import timezone
from datetime import timedelta



lastSearch = ""

def landingPage(request):
    if request.user.is_authenticated:
        return redirect("dashboardPage")
    context={}
    return render(request, "mainApp/landingPage.html",context=context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect("dashboardPage")
    userLoginForm = UserLoginForm()
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboardPage') 
        else:
            return redirect("loginPage")

    context = {"userLoginForm": userLoginForm}

    return render(request, "mainApp/loginPage.html",context=context)

def signupPage(request):
    if request.user.is_authenticated:
        return redirect("dashboardPage")
    userSignupForm =  UserSignupForm()

    if request.method == "POST":
        username = request.POST["username"]
        password1 = request.POST["password1"]
        if User.objects.filter(username=username):
            return redirect("loginPage")
    
        User.objects.create_user(username=username, password=password1)

        user = authenticate(request, username=username, password=password1)
        if user is not None:
            login(request, user)
            return redirect('dashboardPage') 
        return redirect('signupPage')

    context = {"userSignupForm":userSignupForm}
    return render(request, "mainApp/signupPage.html",context=context)

@login_required(login_url='/login')
def dashboardPage(request):
    currentUser = request.user

    dashboardProducts = Product.objects.filter(users=currentUser,isProductSaved=True)

    context = {"currentUser": currentUser,
               "dashboardProducts":dashboardProducts}
    return render(request, "mainApp/dashboardPage.html",context=context)

@login_required(login_url='/login')
def searchPage(request):
    global lastSearch
    currentUser = request.user
    searchBarForm = SearchPageSearchForm()
    collectedItemsContainer = []

    if request.method == "POST":
        if "searchBar" in request.POST:
            lastSearch = request.POST["searchBar"]
            collectedItemsContainer = searchAmazon((request.POST["searchBar"]))
            for i in collectedItemsContainer:
                if Product.objects.filter(users = currentUser,
                                          productHeaderText=i[0],
                                          productPrice=i[1],
                                          productImage=i[3]).exists():
                    i.append(True)
                else:
                    i.append(False)
            context = {"currentUser": currentUser,"searchBarForm":searchBarForm,"collectedItemsContainer":collectedItemsContainer}
            return render(request, "mainApp/searchPage.html",context=context)
        elif "buyNowButton" in request.POST:
            return HttpResponseRedirect(request.POST["buyNowButton"])
        elif "saveProduct" in request.POST:

            isProductAlreadySaved = Product.objects.filter(
                                        productHeaderText=request.POST["productHeaderText"],
                                        productImage=request.POST["productImage"])
            
            if isProductAlreadySaved.exists():
                product = isProductAlreadySaved.first()
                if currentUser in product.users.all():
                    product.users.remove(currentUser)
                    product.save()
                else:
                    product.users.add(currentUser)
                    product.save()

            else:
                newProduct = Product.objects.create(
                    productHeaderText=request.POST["productHeaderText"],
                    productPrice=request.POST["productPrice"],
                    productLink=request.POST["productLink"],
                    productImage=request.POST["productImage"],
                    isProductSaved=True
                )
                newProduct.users.add(currentUser)
                newProduct.save()


            collectedItemsContainer = searchAmazon(lastSearch)

            for i in collectedItemsContainer:
                if Product.objects.filter(users = currentUser,
                                          productHeaderText=i[0],
                                          productPrice=i[1],
                                          productImage=i[3]).exists():
                    i.append(True)
                else:
                    i.append(False)
            
            context = {"currentUser": currentUser,"searchBarForm":searchBarForm,"collectedItemsContainer":collectedItemsContainer}
            return render(request, "mainApp/searchPage.html",context=context)
        
    context = {"currentUser": currentUser,"searchBarForm":searchBarForm,"collectedItemsContainer":collectedItemsContainer}
    return render(request, "mainApp/searchPage.html",context=context)

@login_required(login_url='/login')
def accountPage(request):
    currentUser = request.user
    changeUserInformationForm = ChangeUserInformationForm(initial={
        'changeUsername': currentUser.username,
        'changeFullName': currentUser.first_name,
        'changePhoneNumber': currentUser.phoneNumber,
        'changeEmail': currentUser.email,
        'changeProfilePicture': currentUser.profilePicture
    })
    if request.method == "POST":
        if "changeUsername" in request.POST:
            pass
        elif "logoutButton" in request.POST:
            logout(request)
            return redirect("landingPage")
        elif "changeFullName" in request.POST:
            currentUser.first_name = request.POST["changeFullName"]
            currentUser.save()
            return redirect("accountPage")
        elif "changePhoneNumber" in request.POST:
            currentUser.phoneNumber = request.POST["changePhoneNumber"]
            currentUser.save()
            return redirect("accountPage")
        elif "changeEmail" in request.POST:
            currentUser.email = request.POST["changeEmail"]
            currentUser.save()
            return redirect("accountPage")
        elif "changeProfilePicture" in request.FILES:
            currentUser.profilePicture = request.FILES["changeProfilePicture"]
            currentUser.save()
            return redirect("accountPage")
        else:
            return redirect("errorLol")
            
    context = {"currentUser": currentUser, "changeUserInformationForm":changeUserInformationForm}
    return render(request, "mainApp/accountPage.html",context=context)

@login_required(login_url='/login')
def savedPage(request):
    currentUser = request.user
    savedItems = Product.objects.filter(users=currentUser)
    savedPagesearch = SavedPageSearchForm()
    if request.method == "POST":
        if "buyNowButton" in request.POST:
            return HttpResponseRedirect(request.POST["buyNowButton"])
        elif "unsaveProduct" in request.POST:
            isProductAlreadySaved = Product.objects.filter(
                                        productHeaderText=request.POST["productHeaderText"],
                                        productImage=request.POST["productImage"])
            
            if isProductAlreadySaved.exists():
                product = isProductAlreadySaved.first()
                if currentUser in product.users.all():
                    product.users.remove(currentUser)
                    product.save()
                else:
                    product.users.add(currentUser)
                    product.save()
        elif "savedPageSearchBar" in request.POST:
            savedItems = Product.objects.filter(users=currentUser, 
            productHeaderText__icontains=request.POST["savedPageSearchBar"])
            context = {"currentUser": currentUser,"savedItems":savedItems, "savedPagesearch":savedPagesearch}
            return render(request, "mainApp/savedPage.html",context=context)
    context = {"currentUser": currentUser,"savedItems":savedItems, "savedPagesearch":savedPagesearch}
    return render(request, "mainApp/savedPage.html",context=context)

@login_required(login_url='/login')
def trendingPage(request):
    currentUser = request.user
    now = timezone.now()
    start_of_week = now - timedelta(days=7)
    start_of_month = now - timedelta(days=30)
    displayedItems = Product.objects.filter(isProductSaved=True)
    trendingPageSearch = TrendingPageSearchForm()
    if request.method == "POST":
        if "overAllFilter" in request.POST:
            displayedItems = Product.objects.filter(isProductSaved=True)
        elif "overPastMonthFilter" in request.POST:
            displayedItems = Product.objects.filter(isProductSaved=True,dateCreated__gte=start_of_month)
        elif "overPastWeekFilter" in request.POST:
            displayedItems = Product.objects.filter(isProductSaved=True,dateCreated__gte=start_of_week)
        elif "buyNowButton" in request.POST:
            return HttpResponseRedirect(request.POST["buyNowButton"])
        elif "saveProduct" in request.POST:
            isProductAlreadySaved = Product.objects.filter(
                                        productHeaderText=request.POST["productHeaderText"],
                                        productImage=request.POST["productImage"])
            
            if isProductAlreadySaved.exists():
                product = isProductAlreadySaved.first()
                if currentUser in product.users.all():
                    product.users.remove(currentUser)
                    product.save()
                else:
                    product.users.add(currentUser)
                    product.save()
        elif "trendingPageSearchBar" in request.POST:
            displayedItems = Product.objects.filter(
            productHeaderText__icontains=request.POST["trendingPageSearchBar"])
        
    context = {"currentUser": currentUser,
               "displayedItems":displayedItems,
               "trendingPageSearch":trendingPageSearch}
    return render(request, "mainApp/trendingPage.html",context=context)

@login_required(login_url='/login')
def notificationsPage(request):
    currentUser = request.user
    context = {"currentUser": currentUser}
    return render(request, "mainApp/notificationsPage.html",context=context)

@login_required(login_url='/login')
def helpPage(request):
    currentUser = request.user
    frequentlyAskedQuestions = FrequentlyAskedQuestion.objects.all()
    context = {"currentUser": currentUser,"frequentlyAskedQuestions":frequentlyAskedQuestions}
    return render(request, "mainApp/helpPage.html",context=context)