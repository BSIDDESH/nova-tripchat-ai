import boto3
import os
from dotenv import load_dotenv

load_dotenv()

client = boto3.client(
    "bedrock-runtime",
    region_name="us-east-1",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

MODEL_ID = "amazon.nova-lite-v1:0"

def chat_nova(user_message, conversation_history=None):
    if conversation_history is None:
        conversation_history = []

    system_prompt = """You are Nova TripChat AI, a friendly and expert AI travel planner.
    You help users plan trips, find hotels, estimate budgets, and create packing lists.
    Always give structured, detailed, and helpful responses with emojis.
    Format itineraries with clear Day headers. Be specific with names, prices, and tips."""

    messages = conversation_history.copy()
    messages.append({
        "role": "user",
        "content": [{"text": user_message}]
    })

    response = client.converse(
        modelId=MODEL_ID,
        system=[{"text": system_prompt}],
        messages=messages,
        inferenceConfig={"maxTokens": 1000, "temperature": 0.7}
    )

    assistant_message = response["output"]["message"]["content"][0]["text"]
    messages.append({
        "role": "assistant",
        "content": [{"text": assistant_message}]
    })

    return assistant_message, messages


def plan_trip(destination, days, budget):
    prompt = f"""Plan a detailed {days}-day trip to {destination} with a budget of ${budget}.
    Include:
    🗓️ Day-by-day itinerary with timings
    🍽️ Food recommendations
    🏛️ Top attractions with entry fees
    💡 Local tips
    🚗 How to get around"""
    return chat_nova(prompt)


def find_hotels(destination, budget_level):
    prompt = f"""Recommend the best {budget_level} hotels in {destination}.
    For each hotel include:
    🏨 Hotel name and star rating
    💰 Price per night
    📍 Location and nearby attractions
    ✨ Why it's recommended
    List at least 3 options."""
    return chat_nova(prompt)


def estimate_budget(destination, days, total_budget):
    prompt = f"""Create a detailed budget breakdown for {days} days in {destination} with total budget ${total_budget}.
    Include:
    ✈️ Flights, 🏨 Accommodation, 🍽️ Food, 🎯 Activities, 🚗 Transport, 🛍️ Shopping
    💰 Total estimated cost and 💡 money-saving tips"""
    return chat_nova(prompt)


def packing_list(destination, days, trip_type):
    prompt = f"""Create a complete packing list for {days} days in {destination} for a {trip_type} trip.
    Organize into:
    📄 Documents, 👕 Clothing, 🧴 Toiletries, 💊 Medicine, 📱 Electronics, 🎒 Accessories"""
    return chat_nova(prompt)