
import sys
try:
    with open('verification_result.txt', 'w') as f:
        f.write("Starting verification...\n")
        try:
            import flask
            f.write("flask imported\n")
        except ImportError as e:
            f.write(f"FAILED: flask - {e}\n")
            
        try:
            from config import Config
            f.write("config imported\n")
        except ImportError as e:
            f.write(f"FAILED: config - {e}\n")
            
        try:
            import google.generativeai as genai
            f.write("google.generativeai imported\n")
        except ImportError as e:
            f.write(f"FAILED: google.generativeai - {e}\n")
            
        try:
            import requests
            f.write("requests imported\n")
        except ImportError as e:
            f.write(f"FAILED: requests - {e}\n")
            
        try:
            import dotenv
            f.write("dotenv imported\n")
        except ImportError as e:
            f.write(f"FAILED: dotenv - {e}\n")
            
        f.write("Verification complete.\n")
except Exception as e:
    # If we can't write to file, that's a bigger problem
    pass
