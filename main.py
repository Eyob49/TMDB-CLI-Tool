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
  
  category_keys = ["title","release_date", "vote_average"]
  
    
  except KeyError:
    print("⚠️ Unexpected response format from API.")
    return
    
  results = data.get("results", [])
  
  if not results:
        print("⚠️ No movies found for this category.")
        return

  category_keys = {
                  "t":"title",
                  "d":"release_date",              
                  "r":"vote_average"
}
  
  while True:
      user_choice = input("Choose how to sort the movies:\n\n .title(t)\n .release_date(d)\n .vote_average(r)\n\n ➡️ ").strip().lower()
      if user_choice in category_keys.values():
          break
      elif user_choice in category_keys.keys():
        user_choice = category_keys.get(user_choice)
        break
      print("Please be sure you chose title, release_date or vote_average")
   
  
  sorted_data = sorted(data["results"], key=lambda item: item[user_choice])
  
  for i,movie in enumerate(sorted_data):
         print(f'{i+1}.🎬 Title: {movie["title"]}\n .📆 Release: {movie["release_date"]}\n .⭐️ Rating: {movie["vote_average"]}\n')

get_movies(args.type)
