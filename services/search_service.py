import requests
from config import Config

class SearchService:
    
    def __init__(self):
        self.api_key = Config.GOOGLE_SEARCH_API_KEY
        self.search_engine_id = Config.GOOGLE_SEARCH_ENGINE_ID
        self.base_url = "https://www.googleapis.com/customsearch/v1"
    
    def search(self, query, num_results=5):
        try:
            params = {
                'key': self.api_key,
                'cx': self.search_engine_id,
                'q': query,
                'num': min(num_results, 10)
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract relevant information
            results = []
            if 'items' in data:
                for item in data['items']:
                    results.append({
                        'title': item.get('title', 'No title'),
                        'snippet': item.get('snippet', 'No description'),
                        'link': item.get('link', ''),
                        'displayLink': item.get('displayLink', '')
                    })
            
            return {
                'success': True,
                'results': results,
                'query': query,
                'total_results': data.get('searchInformation', {}).get('totalResults', 0)
            }
            
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f'Search API error: {str(e)}',
                'results': []
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}',
                'results': []
            }
    
    def extract_search_query(self, user_message):
        # Remove common question words and clean up
        remove_words = ['please', 'can you', 'could you', 'tell me', 'what is', 'what are']
        
        query = user_message.lower()
        for word in remove_words:
            query = query.replace(word, '')
        
        return query.strip()