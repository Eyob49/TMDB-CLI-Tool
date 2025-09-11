import requests
import os
import argparse
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")

if not api_key:
    raise ValueError("❌ API key not found. Please set API_KEY in your .env file.")

parser = argparse.ArgumentParser()
parser.add_argument("--type", type=str, help="Movie Category")
args = parser.parse_args()

def get_movies(category):
  
  VALID_CATEGORIES = { 
                       "p": "popular",
                      "tr": "top_rated",
                      "up": "upcoming",
                      "np": "now_playing"
}
  
  if category in VALID_CATEGORIES.keys():
    category = VALID_CATEGORIES.get(category)

  elif category in VALID_CATEGORIES.values():
     category = category

  else:
   if len(category) <= 2:

    print(f"⚠️ Invalid category short key: {category}. Try one of {', '.join(VALID_CATEGORIES.keys())}")

   else:
     print(f"⚠️ Invalid category: {category}. Try one of {', '.join(VALID_CATEGORIES.values())}")
   return

  url = f"https://api.themoviedb.org/3/movie/{category}?api_key={api_key}"

  try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()  
    
  except requests.exceptions.RequestException as e:
    print(f"❌ Network error: please check your connection")
    return
    
  except KeyError:
    print("⚠️ Unexpected response format from API.")
    return
    
  results = data.get("results", [])
  
  if not results:
        print("⚠️ No movies found for this category.")
        return
  
  for movie in data["results"]:
         print(f' 🎬 Title: {movie["title"]}\n 📆 Release: {movie["release_date"]}\n ⭐️ Rating: {movie["vote_average"]}\n')
        
get_movies(args.type)
