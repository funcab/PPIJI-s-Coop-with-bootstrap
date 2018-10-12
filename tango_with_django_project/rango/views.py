from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from rango.models import Category, Page, UserProfile
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from datetime import datetime
from django.conf import settings
from rango.webhose_search import run_query


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val



def visitor_cookie_handler(request):

    visits = int(get_server_side_cookie(request, 'visits', '1'))

    last_visit_cookie = get_server_side_cookie(request,'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).seconds >0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits



def index(request):
    #request.session.set_test_cookie()
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    print(page_list)
    visitor_cookie_handler(request)
    context_dict = {'categories': category_list, 'pages': page_list}
    context_dict['visits'] = request.session['visits']
    return render(request, 'rango/index.html', context_dict)


def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        category.views += 1
        category.save()
        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages

        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None


    return render(request, 'rango/category.html', context_dict)

def show_page(request, page_name_slug):
    context_dict = {}

    try:
        pages = Page.objects.get(slug=page_name_slug)
        pages.views += 1
        pages.save()
        context_dict['pages'] = pages

    except Page.DoesNotExist:
        context_dict['pages'] = None


    return render(request, 'rango/page.html', context_dict)

@login_required
def add_category(request):
    form = CategoryForm()


    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)

            return index(request)
        else:
            print(form.errors)
    return render(request, 'rango/add_category.html',{'form':form})



@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST, request.FILES)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                if 'file' in request.FILES:
                    page.file = request.FILES['file']
                page.save()
                return show_category(request, category_name_slug)
            else:
                print(form.errors)
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)








def about(request):
    # if request.session.test_cookie_worked():
    #     print("TEST COOKIE WORKED")
    #     request.session.delete_test_cookie()
    #context_dict = {'boldmessage': "love, loop, forever!!!"}
    return render(request, 'rango/about.html')

@login_required
def register(request):
    registered = False
    profile_form = UserProfileForm()
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES)

        if profile_form.is_valid():

            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()

            registered = True

        else:
                print(profile_form.errors)


    return render(request,
                  'rango/profile_registration.html',
                  {'registered':registered,
                   'profile_form': profile_form,
                   'registered':registered})


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')

# @login_required
# def user_logout(request):
#
#     logout(request)
#
#     return HttpResponseRedirect(reverse('index'))

def search(request):
    result_list = []
    query =''
    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:

            result_list = run_query(query)
    return render(request, 'rango/search.html', {'result_list':result_list, 'query':query})


def profile(request,username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExits:
        return redirect('index')

    userform = UserForm({'username':user.username, 'email':user.email})
    #print(userform.username)
    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    userprofileform = UserProfileForm({'website':userprofile.website, 'picture':userprofile.picture})

    if request.method =='POST':
        userform = UserForm(request.POST, instance = user)
        userprofileform = UserProfileForm(request.POST, request.FILES, instance=user)
        if userprofileform.is_valid() and userform.is_valid():
            userform.save(commit=True)
            userprofileform.save(commit=True)
            return redirect('index')
        else:
            if not userprofileform.is_valid():
                print(userprofileforms.error)
            else:
                print(userform.error)

    return render(request, 'rango/profile.html', {'userprofile': userprofile, 'selecteduser': user, 'userform': userform, 'userprofileform': userprofileform})


@login_required
def like_category(request):

    cat_id = None
    print(9999)
    likes = 10
    if request.method == 'GET':

        cat_id = request.GET['category_id']

        if cat_id:
            cat = Category.objects.get(id=int(cat_id))
            if cat:
                likes = cat.likes +1
                cat.likes = likes
                cat.save()

    return HttpResponse(likes)

#def suggest_category():
