import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = FLASK_ENV == 'development'
    
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GEMINI_MODEL = 'gemini-2.5-flash'
    
    GOOGLE_SEARCH_API_KEY = os.getenv('GOOGLE_SEARCH_API_KEY')
    GOOGLE_SEARCH_ENGINE_ID = os.getenv('GOOGLE_SEARCH_ENGINE_ID')
    
    MAX_CONVERSATION_HISTORY = 20
    TEMPERATURE = 0.7
    MAX_TOKENS = 1000
    
    @staticmethod
    def validate():
        """Validate that all required config is present"""
        errors = []
        
        if not Config.GEMINI_API_KEY:
            errors.append("GEMINI_API_KEY not set in .env file")
        
        if not Config.GOOGLE_SEARCH_API_KEY:
            errors.append("GOOGLE_SEARCH_API_KEY not set in .env file")
            
        if not Config.GOOGLE_SEARCH_ENGINE_ID:
            errors.append("GOOGLE_SEARCH_ENGINE_ID not set in .env file")
        
        if errors:
            raise ValueError("Configuration errors:\n" + "\n".join(errors))
        
        return True