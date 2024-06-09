from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
import json
from app import assistant
from .models import Search

def check_user(username, password):
    try:
        user = User.objects.get(username=username)
        if user.password == password:
            print('incorrecr pass')
            return user
    except User.DoesNotExist:
        print()
    return None

def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = check_user(username, password)
        if user is not None:
            login(request, user)
            # Store the username in the session
            request.session['username'] = username
            print(f'{request.session["username"]} has logged in successfully')
            # Redirect to corresponding dashboard page based on user type
            if user.is_staff:
                return redirect('expert_dashboard')
            else:
                return redirect('farmer_dashboard')
        else:
            # Handle invalid login
            print('No login')
    return render(request, 'index.html')

def chatbot_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message')
        response = assistant.generate_response(message)
        return JsonResponse({'response': response})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

from django.shortcuts import render
from .models import Search


def search_crops(request):
    if request.method == 'POST':    
        search_query = request.POST.get('search_query')
        results = Search.objects.filter(name__icontains=search_query)
        print(f"Search query: {search_query}")  # Debug print
        print(f"Number of results: {results.count()}")  # Debug print
        print(f"Results: {results}")  # Debug print
        res = []
        for i in results:
            g = {}
            x = i.articles.split()
            g['link'] = i.videos
            g['name'] = x[1]
            g['articles'] = x[0]
            res.append(g)
            print(x)
            
        return render(request, 'farmer_dashboard.html', {'results': res})
    return render(request, 'farmer_dashboard.html')

def farmer_dashboard(request):
    articles = []
    videos = []
    if request.method == 'POST':
        search_query = request.POST.get('search_query')
        print(f"Search query received: {search_query}")  # Debug print
        search_results = Search.objects.filter(name__icontains=search_query)
        if search_results.exists():
            for search_result in search_results:
                articles.extend(search_result.articles.split(','))
                videos.extend(search_result.videos.split(','))
            print(f"Articles found: {articles}")  # Debug print
            print(f"Videos found: {videos}")  # Debug print
    return render(request, 'farmer_dashboard.html', {'articles': articles, 'videos': videos})


def farmer_chat(request):
    #logic
    return render(request, 'farmer_chat.html')

def farmer_notification(request):
    #logic
    return render(request, 'farmer_notification.html')

def farmer_profile(request):
    user = User.objects.get(username=request.session["username"])
    res={}
    try:
        res['name'] = user.first_name.split('_')[1]
        res['email'] = user.email
        res['uname'] = user.username
        res['loc'] = user.last_name.split('_')[1]
        print(res)
    except IndexError as e:
        res['name'] = user.first_name
        res['email'] = user.email
        res['uname'] = user.username
        res['loc'] = user.last_name
        print(res)

    return render(request, 'farmer_profile.html',{'current_user': res})

def farmer_profile_save(request):
    user = User.objects.get(username=request.session["username"])
    if request.method == "POST":
        user.first_name = request.POST.get('name')
        user.email = request.POST.get('email')
        user.last_name = request.POST.get('location')
        user.save()
    return redirect('farmer_profile')

# for expert
def expert_dashboard(request):
    #logic
    return render(request, 'expert_dashboard.html')

def expert_chat(request):
    #logic
    return render(request, 'expert_dashboard.html')

def expert_notification(request):
    #logic
    return render(request, 'expert_dashboard.html')

def expert_profile(request):
    user = User.objects.get(username=request.session["username"])
    full_name = f"{user.first_name} {user.last_name}".strip()
    print(full_name)
    return render(request, 'expert_profile.html')


