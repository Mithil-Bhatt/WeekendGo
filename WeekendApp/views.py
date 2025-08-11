from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse
from .models import *
from django.views import View
from .forms import *
import uuid


# Create your views here.
@login_required(login_url='/login/')
def home(request):
    print("View loaded!")
    p=pg.objects.all()
    latest_pg=pg.objects.all().order_by('-id')[:2]
    o=owner.objects.all()
    f=feedback.objects.all()

    if request.GET.get('search'):
        print(request.GET.get('search'))
        p=pg.objects.filter(pg_name__icontains=request.GET.get('search'))

    for i in p:
        print(i.id, i.pg_name)


    context = {

        'p': p,
        'o': o,
        'f': f,
        'latest_pg': latest_pg
    }
    return render(request, "home.html", context)

@login_required(login_url='/login/')
def about(request):
    return render(request,'about.html')
@login_required(login_url='/login/')
def owners(request):
    p= pg.objects.all()
    context={
        'p':p
    }
    return render(request,'owners.html',context)

@login_required(login_url='/login/')
def feedback_view(request):
    if request.method == 'POST':
        feedback_text = request.POST.get('feedback')  # Get feedback from the form
        if feedback_text:  # Ensure feedback is not empty
            f=feedback.objects.create(user=request.user, feedback=feedback_text)
            f.save()
            return render(request, 'thank_you.html')  # Redirect to a thank-you page
    return render(request, 'feedback.html')  # Render the feedback form

@login_required(login_url='/login/')
def pgs(request):
    print("View loaded!")
    p = pg.objects.all()

    if request.GET.get('search'):
        print(request.GET.get('search'))
        p = pg.objects.filter(pg_name__icontains=request.GET.get('search'))


    for i in p:
        print(i.id, i.pg_name)
    context={
        'p':p
    }
    return render(request,'pg.html',context)


@login_required(login_url='/login/')
def singlepg(request, pg_id,):
    p = get_object_or_404(pg, id=pg_id)  # Use get_object_or_404 to fetch the PG
    hostel = pg.objects.only("amenities").get(id=pg_id)

    amenities = hostel.amenities
    if amenities:
        amenities_list = amenities.split(",")  # Split amenities by commas
    else:
        amenities_list = []

    context = {
        'p': p,
        'amenities_list': amenities_list,  # Pass the amenities list to the template
    }
    return render(request, 'singlepg.html', context)

def signup(request):
    if request.method == 'POST':
        data = request.POST
        print(data)
        uname = data.get('username')
        fname = data.get('first_name')
        lname = data.get('last_name')
        email = data.get('email')
        password = data.get('password')
        print(uname, fname, lname, email, password)
        u = User.objects.filter(username=uname)
        if u.exists():
            messages.info(request, 'username already exists')
            return redirect('/signup/')
        user = User.objects.create_user(username=uname,
                                        first_name=fname,
                                        last_name=lname,
                                        email=email,
                                        )
        user.set_password(password)
        user.save()
        auth_user = authenticate(username=uname, password=password)
        if auth_user is not None:
            login(request, auth_user)
            messages.info(request, 'User registered successfully')
            return redirect('/home/')

        messages.error(request, 'Authentication failed. Please log in manually.')
        return redirect('/login/')

    return render(request, 'signup.html')


def Login(request):
    if request.method == 'POST':
        data = request.POST
        uname = data.get('username')
        password = data.get('password')
        print(uname, password)
        if not User.objects.filter(username=uname).exists():
            messages.error(request, 'Invalid username')
            return redirect('/login/')

        else:
            u = authenticate(username=uname, password=password)
            if u is None:
                messages.error(request, 'password is Invalid')
                return redirect('/login/')
            else:
                login(request, u)
                return redirect('/home/')

    return render(request, 'login.html')

def Logout(request):
    logout(request)
    return redirect('/home/')




@login_required(login_url='/login/')
def feedback_thank_you(request):
    return render(request, 'thank_you.html')
@login_required(login_url='/login/')
def paymentdone(request):
    return render(request, 'paymentdone.html')
@login_required(login_url='/login/')
def pgbooked(request):
    return render(request, 'pgbooked.html')

@login_required(login_url='/login/')
def add_to_bookmarks(request, pg_id):
    # Get the 'pg' to be bookmarked
    pg_to_bookmark = get_object_or_404(pg, id=pg_id)

    # Check if the user has already bookmarked this 'pg'
    if not bookmark.objects.filter(user=request.user, pg=pg_to_bookmark).exists():
        bookmark.objects.create(user=request.user, pg=pg_to_bookmark)

    return redirect('/bookmarks/')  # Redirect to the bookmarks page


@login_required(login_url='/login/')
def remove_from_bookmark(request, bookmark_id):
    if request.method == "POST":
        bookmark_instance = get_object_or_404(bookmark, id=bookmark_id, user=request.user)
    # Call the remove_pg method
        bookmark_instance.remove_pg()
        bookmark_instance.delete()
        return JsonResponse({'success': True})  # Respond with JSON
    return JsonResponse({'success': False}, status=400)
    #return redirect('/bookmarks/')

@login_required(login_url='/login/')
def user_bookmarks(request):
    # Fetch all bookmarks for the logged-in user
    bookmarks = bookmark.objects.filter(user=request.user).select_related('pg')
    return render(request, 'bookmarks.html', {'bookmarks': bookmarks})