import google.generativeai as genai
from config import Config
import json

class GeminiService:
    """Service for interacting with Google Gemini API"""
    
    def __init__(self):
        """Initialize Gemini with API key"""
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
        self.conversation_history = []
        
    def add_to_history(self, role, content):
        """Add message to conversation history"""
        self.conversation_history.append({
            'role': role,
            'parts': [{'text': content}]
        })
        
        # Keep only last N messages
        if len(self.conversation_history) > Config.MAX_CONVERSATION_HISTORY:
            self.conversation_history = self.conversation_history[-Config.MAX_CONVERSATION_HISTORY:]
    
    def should_search(self, message):
        """Determine if we should perform a web search for this query"""
        
        real_time_keywords = [
            'current', 'now', 'today', 'latest', 'recent',
            'price', 'weather', 'news', 'score', 'stock',
            'what is the', 'how much', 'when is'
        ]
        
        message_lower = message.lower()
        
        for keyword in real_time_keywords:
            if keyword in message_lower:
                return True

        question_words = ['what', 'when', 'where', 'who', 'how', 'why', 'which']
        if any(word in message_lower.split()[:3] for word in question_words):
            return True
        
        return False
    
    def generate_response(self, user_message, search_results=None):
        """Generate response using Gemini"""
        try:
            # Build the conversation for the API
            conversation = []
            
            # Add system instruction if we have search results
            if search_results:
                system_prompt = "You are a helpful AI assistant with access to real-time information.\n\n"
                system_prompt += "Real-Time Search Results:\n"
                for idx, result in enumerate(search_results[:5], 1):
                    system_prompt += f"\n{idx}. {result['title']}"
                    system_prompt += f"\n   {result['snippet']}"
                    system_prompt += f"\n   Source: {result['link']}\n"
                system_prompt += "\nUse these search results to provide an accurate, up-to-date answer.\n"
                conversation.append({'role': 'user', 'parts': [{'text': system_prompt}]})
            
            # Add conversation history
            for msg in self.conversation_history[-10:]:
                conversation.append(msg)
            
            # Add current user message
            conversation.append({'role': 'user', 'parts': [{'text': user_message}]})
            
            # Generate response
            response = self.model.generate_content(
                conversation,
                generation_config=genai.types.GenerationConfig(
                    temperature=Config.TEMPERATURE,
                    max_output_tokens=Config.MAX_TOKENS,
                )
            )
            
            assistant_message = response.text
            
            # Add to history
            self.add_to_history('user', user_message)
            self.add_to_history('model', assistant_message)
            
            return {
                'success': True,
                'response': assistant_message,
                'used_search': search_results is not None,
                'history_length': len(self.conversation_history)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        return {'success': True, 'message': 'Conversation history cleared'}
    
    def get_history(self):
        """Get conversation history"""
        # Convert the new format back to a display-friendly format
        display_history = []
        for msg in self.conversation_history:
            if 'parts' in msg and len(msg['parts']) > 0:
                display_history.append({
                    'role': msg['role'],
                    'content': msg['parts'][0]['text']
                })
        
        return {
            'success': True,
            'history': display_history,
            'count': len(display_history)
        }