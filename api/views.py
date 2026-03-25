from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import HotelRoom
# Import the brain we built in orchestrator.py
from .agents.orchestrator import agent_brain

logger = logging.getLogger(__name__)

def index(request):
    """Renders the main EcoTrail dashboard/map page."""
    return render(request, "index.html") # Make sure your HTML file is named index.html!

class ChatbotView(APIView):
    """
    Main entry point for the EcoTrail AI Agent.
    Handles user messages, routes them to specific agents (Weather, SQL, Vector),
    and returns the synthesized response.
    """
    
    def post(self, request):
        # 1. Extract message from the POST request body
        user_query = request.data.get("message")
        
        # 2. Basic Validation
        if not user_query:
            return Response(
                {"status": "error", "message": "No message provided. What would you like to ask EcoBot?"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            logger.info(f"📩 Received query: {user_query}")

            # 3. Call the Orchestrator (The "Brain")
            ai_response = agent_brain.process_query(user_query)
            
            # 4. Return successful JSON response
            return Response({
                "status": "success",
                "response": ai_response
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            # Log the exact error for debugging in your terminal
            logger.error(f"❌ Chatbot View Error: {str(e)}")
            
            return Response({
                "status": "error",
                "response": "EcoBot is currently recalibrating sensors in Dharamshala. Please try again in a moment."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import HotelRoom 



@login_required(login_url='/api/login/')
def add_hotel_room(request):
    if request.method == "POST":
        hotel_name = request.POST.get('hotel_name')
        location = request.POST.get('location')
        total_rooms = request.POST.get('total_rooms')
        available_rooms = request.POST.get('available_rooms')
        price = request.POST.get('price')

        try:
            HotelRoom.objects.create(
                name=hotel_name,
                location=location,
                total_rooms=int(total_rooms),
                available_rooms=int(available_rooms),
                price=price
            )
            messages.success(request, f"✅ Successfully added '{hotel_name}' data!")
            return redirect('add_hotel_room')
            
        except Exception as e:
            messages.error(request, f"❌ Error saving to database: {str(e)}")

    recent_rooms = HotelRoom.objects.all().order_by('-id')[:5]
    return render(request, 'add_hotel.html', {'recent_rooms': recent_rooms})   


def carbon_calculator(request):
    """Renders the Carbon Footprint Calculator page."""
    return render(request, "calculator.html")