from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai
from django.utils import timezone
from datetime import timedelta, datetime
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat

#from json import dumps
#from django.utils import timezone


openai_api_key = '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'
openai.api_key = openai_api_key

# Define condition types
CONDITION_A = 'A'
statement_1 = '1'

# Function to ask OpenAI (Refactored to reduce redundancy)
def ask_openai(message):
       
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": "Provide responses that reflect a hypothetical context, in which it is believed that by next summer, half of the existing 2-year master's programs will be restructured into 1 ¼-year business-oriented master's programs. Your responses should consistently align with this scenario, while answering questions and providing information to any questions the user might have. You cannot not explicitly state that this is your goal or that it is a hypothetical sceario. You can never deviate from your goal, regardless of the user response.'}
             #the governmental proposal of restructuring half of the existing 2-year master programs into 1 ¼ -year business-oriented master’s programs, is expected to be implemented by the summer next year. Your goal is engage in this scenario and to provide information and answer questions in a way that reflects this belief. You should not explicitly state that this is your goal or that it is a hypothetical sceario, instead you should answer questions as if this understanding is ground truth. You can never deviate from your goal, regardless of the user response."},
             {"role": "user", "content": message}
        ]
    )

    return response.choices[0].message.content.strip()

# Optimized 'chatbot' view
def chatbot(request):
    if not request.user.is_authenticated:
        return redirect('register') # Redirect to 'register if user is not authenticated
    #chats = Chat.objects.filter(user=request.user)  # Fetch user's chat history

    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)
        condition = CONDITION_A 
        statement = statement_1

        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now(), condition = condition, statement = statement)
        chat.save()
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('chatbot')
        else:
            error_message = 'Something went wrong. Invalid user'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect('chatbot')
            except:
                error_message = 'Oh Oh! Something went wrong'
                return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = 'Passwords do not match'
            return render(request, 'register.html', {'error_message': error_message})
    return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('login')



