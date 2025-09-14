import requests
import os
import argparse
import time
from rich.console import Console
from rich.table import Table

parser = argparse.ArgumentParser()
parser.add_argument("--type", "-t",type=str, help="Movie Category")

args = parser.parse_args()

api_key = os.environ["API_KEY"]

def get_movies(category):
  
  VALID_CATEGORIES = {"p": "popular"
                      ,
                     "tr": "top_rated"
                      ,
                      "up": "upcoming"
                      ,
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
    
  except requests.exceptions.RequestException:
    print("❌ Network error: please check your connection")
    return
    
  except KeyError:
    print("⚠️ Unexpected response format from API.")
    return
    
  results = data.get("results", [])
  
  if not results:
        print("⚠️ No movies found for this category.")
        return

  category_keys = {"t":"title",
                  "d":"release_date",                   "r":"vote_average"}
  
  while True:
      user_choice = input("Choose how to sort the movies:\n\n .title(t)\n .release_date(d)\n .vote_average(r)\n\n ➡️ ").strip().lower()
      if user_choice in category_keys.values():
          break
      elif user_choice in category_keys.keys():
        user_choice = category_keys.get(user_choice)
        break
      print("Please be sure you chose title, release_date or vote_average")
   
  sorted_data = sorted(data["results"], key=lambda item: item[user_choice])
  
  def do_something_important():
    time.sleep(5.0)
    
  console = Console()
  with console.status(f"Please wait, fetching {category} movies", spinner="earth"):
    do_something_important()
  console.print(":rocket: Here's it...\n")
                      
  
  def display_movies(movies):
    table = Table(title=":clapper_board: Movies")
    table.add_column("Title", style="cyan", no_wrap=True)
    table.add_column("Released date", style="blue")
    table.add_column("Rating", style="yellow")

    for movie in movies:
        table.add_row(
            movie["title"],
          str(movie["release_date"]),
          str(movie["vote_average"])
        )

    console.print(table)

    display_movies(sorted_data)


get_movies(args.type)
