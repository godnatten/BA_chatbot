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
CONDITION = 'A'
statement_A = '3' 

# Function to ask OpenAI (Refactored to reduce redundancy)
def ask_openai(message):
       
    response = openai.ChatCompletion.create(
        model='gpt-4-1106-preview',
        messages=[
            {"role": "system", "content": "Provide responses that reflect a context, in which it is believed that the human body has an internal clock naturally following a ~ 24 hours cycle, even in total darkness. Your responses should consistently align with this scenario, while answering questions and providing information to any questions the user might have about the human internal clock. You cannot not explicitly state that this is your goal or that it is a hypothetical scenario. You can never deviate from your goal, regardless of the user response"},  
             {"role": "user", "content": message}
        ]
    )

    return response.choices[0].message.content.strip()


# Optimized 'chatbot' view
def chatbot(request):
    chat = Chat.objects.all()  # Fetch all chat history
    initial_message = "How can I help you today? Feel free to ask any questions about the human internal clock that you might have!"  # Initial message
    
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)
        condition = CONDITION
        statement = statement_A

        if request.user.is_authenticated:
            user = request.user
        else:
            # Handle anonymous user here
            user = None  # Or use a predefined user for anonymous chats

        chat = Chat(user=user, message=message, response=response, created_at=timezone.now(), condition=condition, statement=statement)
        chat.save()
        #print(chat)
        #print(response)
        #print(message)
        return JsonResponse({'message': message, 'response': response})

    return render(request, 'chatbot.html', {'initial_message': initial_message})





