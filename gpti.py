import logging
from flask import Flask, jsonify, request
import requests
import os
import uuid
import random
from datetime import datetime
from flask_cors import CORS
from dotenv import load_dotenv
from songs_data import get_song_recommendations
from wellness_centers import get_wellness_centers, format_wellness_center_recommendations

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
load_dotenv()

# Create Flask app instance
app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# Configure CORS to allow requests from any origin
CORS(app,
     supports_credentials=True,  # Enable CORS with credentials support
     resources={r"/*": {"origins": "*"}},  # Allow all origins
     allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
     methods=["GET", "POST", "OPTIONS"]
)

# Function to call OpenAI API
def get_chatgpt_response(user_message):
    api_key = os.getenv('OPENAI_API_KEY')  # Use environment variable for API key

    if not api_key:
        logging.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
        return "I'm sorry, but I'm not configured correctly. Please contact the administrator."
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    # Store conversation history in a dictionary with session IDs as keys
    conversation_history = getattr(app, 'conversation_history', {})

    # Get or create session ID from request
    session_id = request.cookies.get('session_id')
    if not session_id:
        session_id = str(uuid.uuid4())

    # Get or initialize conversation history for this session
    if session_id not in conversation_history:
        conversation_history[session_id] = []
        # Add system message to set the context for the AI
        conversation_history[session_id].append({
            'role': 'system',
            'content': 'You are a supportive mental health chatbot. Respond with empathy and care. ' +
                      'Provide helpful suggestions but make it clear you are not a replacement for professional help. ' +
                      'Keep responses concise and focused on the user\'s well-being.'
        })

    # Add the new user message to history
    conversation_history[session_id].append({'role': 'user', 'content': user_message})

    # Limit history to last 10 messages to prevent token limits
    if len(conversation_history[session_id]) > 10:
        # Keep the system message and the most recent messages
        conversation_history[session_id] = [conversation_history[session_id][0]] + conversation_history[session_id][-9:]

    # Save the conversation history back to the app
    app.conversation_history = conversation_history

    # Prepare the messages for the API call
    data = {
        'model': 'gpt-3.5-turbo',  # Use the appropriate model
        'messages': conversation_history[session_id],
        'max_tokens': 150,  # Adjust as needed
        'temperature': 0.7  # Add some variability but keep responses focused
    }

    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)

    if response.status_code == 200:
        try:
            reply = response.json()['choices'][0]['message']['content']
            # Add the bot's reply to the conversation history
            conversation_history[session_id].append({'role': 'assistant', 'content': reply})
            return reply
        except (KeyError, IndexError, ValueError) as e:
            logging.error(f"Error parsing OpenAI response: {e}")
            # If we can't parse the response, use fallback
            return fallback_response(user_message)
    else:
        logging.error(f"OpenAI API error: {response.status_code} - {response.text}")

        # Check for specific error types
        try:
            error_data = response.json().get('error', {})
            error_type = error_data.get('type', '')
            error_message = error_data.get('message', '')

            # For any API error, use the fallback response generator
            logging.info(f"Using fallback response due to API error: {error_type}")
            return fallback_response(user_message)
        except Exception as e:
            logging.error(f"Error handling API error response: {e}")
            return fallback_response(user_message)



# Fallback response generator when API is unavailable
def fallback_response(message):
    message = message.lower()

    # Expanded patterns for fallback responses
    greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening', 'howdy', 'greetings']
    negative_feelings = ['sad', 'depressed', 'unhappy', 'stress', 'anxiety', 'lonely', 'tired', 'angry', 'worried', 'overwhelmed', 'anxious', 'fear', 'scared', 'upset', 'down', 'blue', 'miserable', 'hopeless', 'helpless', 'frustrated']
    positive_feelings = ['happy', 'joy', 'joyful', 'glad', 'excited', 'content', 'grateful', 'thankful', 'good', 'great', 'wonderful', 'amazing', 'fantastic', 'excellent', 'blessed', 'cheerful', 'delighted', 'pleased', 'satisfied', 'thrilled', 'optimistic', 'positive', 'confident']
    jokes = ['joke', 'funny', 'laugh', 'humor', 'comedy', 'hilarious', 'amuse', 'entertain']
    thanks = ['thank', 'thanks', 'appreciate', 'grateful', 'gratitude']
    help_requests = ['help', 'advice', 'suggestion', 'guidance', 'assist', 'support', 'recommend', 'what should i do', 'how can i', 'tips', 'ideas']
    wellness = ['meditation', 'exercise', 'yoga', 'mindfulness', 'breathing', 'relax', 'calm', 'peace', 'wellness', 'health', 'self-care', 'sleep', 'rest']
    questions = ['what', 'how', 'why', 'when', 'where', 'who', 'can you', 'could you', 'would you', 'will you', '?']
    music_requests = ['song', 'music', 'playlist', 'recommend a song', 'suggest a song', 'recommend music', 'suggest music', 'listen to', 'track', 'tune', 'melody', 'recommend songs', 'suggest songs']
    wellness_center_requests = ['wellness center', 'wellness centers', 'mental health center', 'mental health centers', 'therapy center', 'therapy centers', 'counseling center', 'counseling centers', 'psychologist', 'psychiatrist', 'therapist', 'counselor', 'mental health clinic', 'mental health clinics', 'mental health service', 'mental health services']

    # Check for greetings
    if any(word in message for word in greetings):
        return random.choice([
            "Hello! How are you feeling today? I'm here to chat and support you.",
            "Hi there! I'm your mental health companion. How can I help you today?",
            "Hey! I'm here to listen and chat with you. How's your day going?",
            "Greetings! I'm here to provide support and a friendly conversation. How are you?"
        ])

    # Check for music or song requests first (higher priority)
    if any(word in message for word in music_requests):
        # Try to detect mood from the message
        detected_mood = None

        # Check for explicit mood mentions
        if any(word in message for word in positive_feelings) or "happy" in message:
            detected_mood = "happy"
        elif any(word in message for word in negative_feelings) or "sad" in message:
            detected_mood = "sad"
        elif "calm" in message or "relax" in message or "peaceful" in message:
            detected_mood = "calm"
        elif "energy" in message or "energetic" in message or "workout" in message or "exercise" in message:
            detected_mood = "energetic"
        elif "focus" in message or "concentrate" in message or "study" in message or "work" in message:
            detected_mood = "focused"

        # If no mood is detected, ask the user for their mood preference
        if not detected_mood:
            return "I'd be happy to recommend some songs! What kind of mood are you in? I can suggest music for moods like happy, sad, calm, energetic, focused, or relaxed."

        # Get song recommendations for the mood
        songs = get_song_recommendations(detected_mood, count=3)

        if songs:
            # Format the response with YouTube links
            response = f"Here are some songs that might match your {detected_mood} mood:\n\n"

            for i, song in enumerate(songs, 1):
                response += f"{i}. \"{song['title']}\" by {song['artist']}\n"
                if 'link' in song:
                    response += f"   Listen here: {song['link']}\n"
                else:
                    # Create a search link if not provided
                    search_query = f"{song['artist']} {song['title']}".replace(' ', '+')
                    response += f"   Listen here: https://www.youtube.com/results?search_query={search_query}\n"

            response += "\nI hope these songs help enhance your mood! Let me know if you'd like more recommendations."
            return response
        else:
            return "I'd be happy to recommend some songs! I can suggest music for different moods like happy, sad, calm, energetic, focused, or relaxed. Which mood would you like songs for?"

    # Check for positive feelings
    if any(word in message for word in positive_feelings):
        return random.choice([
            "I'm so glad to hear you're feeling happy! Positive emotions are worth celebrating. What's bringing you joy today?",
            "That's wonderful to hear! Happiness is such an important emotion. Would you like to share what's contributing to your positive mood?",
            "It's great that you're feeling good! Acknowledging positive emotions can help us appreciate the good moments in life. What's making you feel this way?",
            "I'm happy to hear that! Positive emotions can be a great source of energy and resilience. What activities or experiences are bringing you joy?",
            "That's fantastic! Celebrating moments of happiness is important for mental wellbeing. Is there something specific that's brightened your day?"
        ])

    # Check for negative feelings
    if any(word in message for word in negative_feelings):
        return random.choice([
            "I'm sorry to hear you're feeling that way. Remember that it's okay to seek help when you need it. Would you like to talk more about what's bothering you?",
            "That sounds difficult. I want you to know that your feelings are valid, and it's okay to not be okay sometimes. Taking small steps toward self-care can help.",
            "I understand this is hard. Consider reaching out to a mental health professional who can provide proper support. In the meantime, deep breathing exercises might help you feel a bit calmer.",
            "It's brave of you to share your feelings. Remember that difficult emotions are a normal part of being human. Would talking about specific situations help?",
            "I hear you're struggling right now. Sometimes just acknowledging our feelings can be the first step toward feeling better. What's one small thing you could do today to care for yourself?"
        ])

    # Check for joke requests
    if any(word in message for word in jokes):
        return random.choice([
            "Why don't scientists trust atoms? Because they make up everything!",
            "What did the ocean say to the beach? Nothing, it just waved!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "Why did the bicycle fall over? It was two-tired!",
            "What's orange and sounds like a parrot? A carrot!",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "How does a penguin build its house? Igloos it together!",
            "What do you call a fake noodle? An impasta!"
        ])

    # Check for thanks
    if any(word in message for word in thanks):
        return random.choice([
            "You're welcome! I'm happy to help and chat with you anytime.",
            "It's my pleasure! I'm here whenever you need someone to talk to.",
            "I'm glad I could be of assistance. Feel free to reach out anytime you need support.",
            "You're very welcome! Taking care of your mental health is important, and I'm here to support you on that journey."
        ])

    # Check for help requests
    if any(word in message for word in help_requests):
        return random.choice([
            "I'd be happy to help. For mental health support, consider practices like deep breathing, mindfulness, or talking with trusted friends. Professional help is also valuable when needed.",
            "When you're struggling, remember the basics: good sleep, healthy food, physical activity, and social connection can all make a difference. What area would you like to focus on?",
            "Sometimes small changes can have big impacts on how we feel. Setting realistic goals, practicing gratitude, or spending time in nature might help. Would you like more specific suggestions?",
            "Support can come in many forms. Consider journaling, meditation apps, support groups, or professional therapy. What resources do you currently have access to?"
        ])

    # Check for wellness center requests
    if any(word in message for word in wellness_center_requests) or ('suggest' in message and ('center' in message or 'clinic' in message or 'therapist' in message)):
        # Try to extract location information
        location = None
        location_indicators = ['in', 'near', 'around', 'close to', 'nearby']

        for indicator in location_indicators:
            if indicator in message:
                # Try to extract location after the indicator
                parts = message.split(indicator + ' ')
                if len(parts) > 1:
                    # Take the rest of the message after the indicator as potential location
                    potential_location = parts[1].strip()
                    # Limit to first few words to avoid taking the whole message
                    location_words = potential_location.split()[:3]
                    location = ' '.join(location_words)
                    break

        # Get wellness center recommendations
        centers = get_wellness_centers(location=location, count=3)
        return format_wellness_center_recommendations(centers)

    # Check for wellness topics
    if any(word in message for word in wellness):
        return random.choice([
            "Wellness practices can be powerful tools for mental health. Even 5 minutes of deep breathing or meditation can help reduce stress and improve focus.",
            "Regular physical activity is one of the most effective ways to improve mood and reduce anxiety. Even a short walk can make a difference.",
            "Mindfulness helps us stay present instead of worrying about the past or future. Try focusing on your senses: what do you see, hear, feel, smell, and taste right now?",
            "Good sleep is essential for mental health. Try to maintain a regular sleep schedule and create a calming bedtime routine without screens."
        ])



    # Check for questions
    if any(word in message for word in questions):
        return random.choice([
            "That's a good question. While I have limited responses right now, I'd be happy to chat about mental health topics like stress management, self-care, or emotional wellness.",
            "I wish I could give you a more detailed answer. Is there a specific aspect of mental health or wellbeing you'd like to discuss?",
            "I'd like to help with your question. Could you share more about what you're looking for? I can discuss topics like coping strategies, relaxation techniques, or general mental wellness.",
            "Great question. While I have some limitations, I can still chat about mental health basics, self-care practices, or emotional support strategies."
        ])

    # Default response - more varied options
    return random.choice([
        "I'm here to support you with mental health conversations. What's on your mind today?",
        "I'd love to chat about how you're feeling or any mental health topics you're interested in.",
        "I'm your mental health companion. Feel free to share what's on your mind or ask about wellness strategies.",
        "I'm here to listen and chat. Would you like to talk about how you're feeling today or discuss mental wellness strategies?",
        "I'm focused on supporting your mental wellbeing. What would you like to talk about today?"
    ])

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Log request details for debugging
        logging.info(f"Received request: {request.method} {request.path}")
        logging.info(f"Request headers: {dict(request.headers)}")

        data = request.get_json()
        logging.info(f"Request data: {data}")

        user_message = data.get('message', '').strip()
        logging.info(f"User message: {user_message}")

        if not user_message:
            return jsonify({'reply': "Please provide a message."}), 400

        # Get or create session ID
        session_id = request.cookies.get('session_id')
        if not session_id:
            session_id = str(uuid.uuid4())
            logging.info(f"Created new session ID: {session_id}")
        else:
            logging.info(f"Using existing session ID: {session_id}")

        # Call the OpenAI API
        reply = get_chatgpt_response(user_message)
        logging.info(f"Generated reply: {reply}")

        # Create response with session cookie
        response = jsonify({'reply': reply})
        response.set_cookie('session_id', session_id, max_age=86400)  # 24 hour expiry

        # Add CORS headers explicitly
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')

        logging.info(f"Sending response: {response.data}")
        return response
    except Exception as e:
        logging.error(f"Error processing request: {e}", exc_info=True)
        error_response = jsonify({'reply': f"Sorry, I couldn't process your request. Error: {str(e)}"})

        # Add CORS headers to error response too
        error_response.headers.add('Access-Control-Allow-Origin', '*')
        error_response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        error_response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
        error_response.headers.add('Access-Control-Allow-Credentials', 'true')

        return error_response, 400

# Add OPTIONS method handler for CORS preflight requests
@app.route('/chat', methods=['OPTIONS'])
def handle_options():
    response = app.make_default_options_response()
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)  # Set up logging
    app.run(host="0.0.0.0", port=5000)  # Run the app

