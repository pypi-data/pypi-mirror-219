import requests
import datetime

class Toodaloo:
    def __init__(self, base_id, table_name, api_key):
        self.base_id = base_id
        self.table_name = table_name
        self.api_key = api_key
        self.endpoint = f"https://api.airtable.com/v0/{self.base_id}/{self.table_name}"
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
    
    def track_ai_usage(self, user_message, ai_response):
        data = {
            'fields': {
                'User Message': user_message,
                'AI Response': ai_response,
                'Timestamp': datetime.datetime.now().isoformat(),
                # Add more fields as needed
            }
        }
        
        try:
            response = requests.post(self.endpoint, json=data, headers=self.headers)
            if response.status_code == 200:
                print("Data tracked successfully!")
            else:
                print("Failed to track data:", response.text)
        except requests.exceptions.RequestException as e:
            print("Error while sending data:", e)

# Instantiate the Requesty class with the provided Airtable details
toodaloo = Toodaloo('appcbsXdAC8Kt2A6b', 'Toodaloo', 'patLFXJmCGDOZAkeO.8b39d527b9a8793ec376f123bd7218a4a7d605a9711dd2e1c4f5a23c9e87b766')
