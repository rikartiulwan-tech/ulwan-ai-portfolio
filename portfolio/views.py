import json
import os
from pathlib import Path
from dotenv import load_dotenv
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from google import genai
from google.genai import types
from .models import ClientInquiry

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / '.env', override=True)

def home(request):
    return render(request, 'portfolio/index.html')

@csrf_exempt
def submit_inquiry(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ClientInquiry.objects.create(
                name=data.get('name'),
                email=data.get('email'),
                business_type=data.get('business_type'),
                package=data.get('package'),
                details=data.get('details', '')
            )
            return JsonResponse({
                'status': 'success',
                'message': 'Thanks! Your project inquiry is received. We will reply within 2 hours!'
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=405)

@csrf_exempt
def ai_chat(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')

            client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
            system_prompt = (
                "You are the AI Project Consultant for 'Ulwan AI Studio Web & AI Studio' founded by Ulwan. "
                "We build high-converting websites with 24/7 AI Chatbots and Auto-Booking systems for Dental Clinics, Gyms, and Local Businesses. "
                "Packages: Starter ($399 - 5 days), AI Growth ($799 - 7 days, includes AI Chatbot + Booking DB), Custom App ($1,499+). "
                "Live Demo: Lumiere Dental Care (https://lumiere-dental-ai.onrender.com). "
                "WhatsApp: +91 9481469827. Keep replies confident, concise (2-3 sentences), and guide visitors to submit the inquiry form."
            )

            response = client.models.generate_content(
                model='gemini-3.5-flash-lite',
                contents=user_message,
                config=types.GenerateContentConfig(system_instruction=system_prompt)
            )
            return JsonResponse({'reply': response.text})
        except Exception as e:
            print("CHATBOT ERROR:", e)
            return JsonResponse({'reply': 'Message us on WhatsApp at +91 9481469827 for an instant quote!'}, status=500)
    return JsonResponse({'error': 'Invalid method'}, status=405)