# Mental Health Chatbot

A supportive AI-powered chatbot designed to provide mental health resources, song recommendations based on mood, and wellness center information.

## 🌟 Features

- **Emotional Support**: Responds empathetically to both positive and negative emotions
- **Music Therapy**: Recommends songs based on your mood with YouTube links
- **Wellness Resources**: Suggests mental health centers and online resources with Google search links
- **Fallback System**: Continues to provide helpful responses even when the AI service is unavailable
- **Location-Aware**: Can recommend wellness centers based on location information
- Simple, user-friendly chat interface
- Dark/light theme toggle
- Emergency mental health resources
- Conversation history saved locally
- Typing indicators for a more natural feel
- Keyboard shortcuts for accessibility
- Multiple AI backend options (Rule-based, Llama, OpenAI)

## Setup Instructions

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/RANUSINGH-S/mentle_health_chatbot.git
   cd mentle_health_chatbot
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up your API keys:
   - Create a file named `.env` in the project root
   - For OpenAI: `OPENAI_API_KEY=your_api_key_here`
   - For HuggingFace: `HUGGINGFACE_API_KEY=your_api_key_here`

### Running the Application

1. Start the HTTP server to serve the frontend:
   ```
   python server.py
   ```

2. In a separate terminal, start one of the Flask backends:
   ```
   # For rule-based responses (no API key needed)
   python app.py

   # For OpenAI GPT-powered responses (requires API key)
   python gpti.py

   # For Llama-powered responses (requires HuggingFace API key)
   python llama_api.py
   ```

3. Open your browser and navigate to:
   ```
   http://localhost:8000/index.html
   ```

## Backend Options

### Rule-based (app.py)
- Simple pattern matching for common mental health concerns
- No external API dependencies
- Predefined responses for greetings, feelings, help requests
- Maintains conversation context for better follow-up responses

### OpenAI GPT (gpti.py)
- Integrates with OpenAI's API
- Uses GPT-3.5-turbo model
- Requires an OpenAI API key
- Provides more natural and contextually relevant responses
- Falls back to rule-based responses if API is unavailable
- **NEW**: Song recommendations based on mood with YouTube links
- **NEW**: Wellness center recommendations with Google search links
- **NEW**: Improved emotional support for both positive and negative feelings

### Llama (llama_api.py)
- Integrates with HuggingFace's Inference API for Llama models
- Uses Meta's Llama-2-7b-chat-hf model
- Requires a HuggingFace API key
- Provides free alternative to OpenAI
- Falls back to rule-based responses if API is unavailable

## 💬 New Features in Detail

### Song Recommendations
The chatbot can now recommend songs based on your mood:
- Ask for song recommendations by typing "suggest a song" or "recommend music"
- If you don't specify a mood, the chatbot will ask what kind of mood you're in
- Specify a mood (happy, sad, calm, energetic, focused, relaxed) to get tailored recommendations
- Each song recommendation includes a YouTube link for easy listening

### Wellness Center Recommendations
Get information about mental health centers and resources:
- Ask for wellness centers by typing "suggest wellness centers" or "recommend therapists"
- The chatbot provides information about mental health centers including:
  - Name and description
  - Location and contact information
  - Website link
  - Google search link for more information
- Online resources for mental health support are also provided
- Location-specific recommendations are available (e.g., "suggest wellness centers in Texas")

## Usage

### Basic Interaction
- Type your message in the input field and press Enter or click Send
- Click the moon/sun icon to toggle between dark and light themes
- Click the question mark button to access mental health resources
- Use keyboard shortcuts:
  - `/` to focus the input field
  - `Alt+R` to toggle resources panel
  - `Alt+T` to toggle theme

### Example Interactions

#### Emotional Support
```
User: "I am feeling sad today"
Chatbot: "I'm sorry to hear you're feeling that way. Remember that it's okay to seek help when you need it. Would you like to talk more about what's bothering you?"

User: "I am happy"
Chatbot: "I'm so glad to hear you're feeling happy! Positive emotions are worth celebrating. What's bringing you joy today?"
```

#### Song Recommendations
```
User: "Suggest me a song"
Chatbot: "What kind of mood are you in? I can suggest music for moods like happy, sad, calm, energetic, focused, or relaxed."

User: "I'm feeling happy"
Chatbot: "Here are some songs that might match your happy mood:

1. "Happy" by Pharrell Williams
   Listen here: https://www.youtube.com/results?search_query=pharrell+williams+happy
2. "Can't Stop the Feeling" by Justin Timberlake
   Listen here: https://www.youtube.com/results?search_query=justin+timberlake+cant+stop+the+feeling
3. "Walking on Sunshine" by Katrina & The Waves
   Listen here: https://www.youtube.com/results?search_query=katrina+and+the+waves+walking+on+sunshine

I hope these songs help enhance your mood! Let me know if you'd like more recommendations."
```

#### Wellness Center Recommendations
```
User: "Suggest wellness centers"
Chatbot: "Here are some wellness centers and mental health resources that might be helpful:

1. Mayo Clinic
   Comprehensive medical and mental health services
   Location: Multiple locations across the US
   Phone: 1-800-MAYO-CLINIC
   Website: https://www.mayoclinic.org/mental-health
   Google Search: https://www.google.com/search?q=mayo+clinic+mental+health+services

[Additional centers and resources listed...]

Remember that this is not an exhaustive list, and I recommend searching for 'mental health services near me' on Google for more localized options."
```

## Important Note

This chatbot is not a replacement for professional mental health services. If you or someone you know is in crisis, please contact a mental health professional or use one of the emergency resources listed in the application.

## 🔗 Project Links

- [GitHub Repository](https://github.com/RANUSINGH-S/mentle_health_chatbot)
- [Direct Link to Code](https://github.com/RANUSINGH-S/mentle_health_chatbot/tree/main/mental_health_chatbot)

## 📊 Future Enhancements

- Integration with more mental health resources and APIs
- User accounts and conversation history
- Mobile application version
- More personalized recommendations based on user preferences
- Integration with emergency services for crisis situations

## 📄 License

MIT

---

Created with ❤️ for mental health support and awareness.

For any questions or suggestions, please open an issue on GitHub.
