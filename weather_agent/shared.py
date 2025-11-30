import os
from dotenv import load_dotenv
from api.meteoblue_client import MeteoblueClient

# Load environment variables
load_dotenv()

# Initialize Meteoblue client
client = MeteoblueClient(api_key=os.getenv("METEOBLUE_API_KEY"))
