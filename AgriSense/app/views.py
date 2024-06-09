from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
import json
from app import assistant
from .models import  Chats, Req, Search
from django.views.decorators.csrf import csrf_exempt

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
        request.session["otheruser"] = None
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


def process_image(image):
    # Implement your image processing logic here
    # For example, use an image recognition library or a pre-trained model
    # to extract relevant information from the image
    # Return the extracted information as a search query string
    search_query = "potato"  # Replace with actual logic
    return search_query

def image_search(request):
    if request.method == 'POST':
        try:
            image = request.FILES['image']
            # Process the image and extract the search query
            search_query = process_image(image)

            return JsonResponse({'search_query': search_query}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

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

@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message')
            user = request.user
            other = 'farmer0'
            if request.session.get("otheruser"):
                other = request.session["otheruser"]
                
            if message and user.is_authenticated:
                # Save the chat message to the database
                chat = Chats.objects.create(name=user.username, text=message, user=other)
                chat.save()

                return JsonResponse({'name': user.username, 'text': message}, status=200)
            else:
                return JsonResponse({'error': 'Invalid data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def send_request(request):
    if request.method == 'POST':
        try:
            # Update all rows of Req model to set request field to 1
            Req.objects.update(request=1)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

# for farmer
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
    chats = Chats.objects.filter(user=request.session["username"])
    return render(request, 'farmer_chat.html', {'chats': chats})

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
    chats = Chats.objects.filter(user='farmer0')
    return render(request, 'expert_chat.html', {'chats': chats})

def expert_upload(request):
    #logic
    return render(request, 'expert_upload.html')

def expert_profile(request):
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

    return render(request, 'expert_profile.html',{'current_user': res})

def expert_profile_save(request):
    user = User.objects.get(username=request.session["username"])
    if request.method == "POST":
        user.first_name = request.POST.get('name')
        user.email = request.POST.get('email')
        user.last_name = request.POST.get('location')
        user.save()
    return redirect('expert_profile')


