import os

from dotenv import load_dotenv

load_dotenv(".env")

# Get environment (defaults to "development")
ENV = os.getenv("ENVIRONMENT", "development")

# Pick correct .env file
if ENV == "production":
    load_dotenv(".env.production")
else:
    load_dotenv(".env.development")

# Now you can access vars
BOT_TOKEN = os.getenv("BOT_TOKEN")
NEBIUS_API_KEY = os.getenv("NEBIUS_API_KEY")

print(f"Running in {ENV} mode")
