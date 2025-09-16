import requests
import os
import argparse
import time
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from dotenv import load_dotenv

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("--type", "-t",type=str, help="Movie Category")

args = parser.parse_args()

api_key = os.getenv("API_KEY")

console = Console()

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
      console.print(f"⚠️  Invalid category short key: {category}. Try one of {', '.join(VALID_CATEGORIES.keys())}", style="bold red")
    else:
      console.print(f"🚫 '{category}' is not a valid category. Try: popular, top_rated, upcoming, now_playing.", style="bold yellow")
    return

  category_keys = {
    "t": "title",
    "d": "release_date",
    "r": "vote_average"
  }

  while True:
    user_choice = input("Choose how to sort the movies:\n\n .title(t)\n .release_date(d)\n .vote_average(r)\n\n ➡️ ").strip().lower()
    if user_choice in category_keys.values():
      break
    elif user_choice in category_keys.keys():
      user_choice = category_keys.get(user_choice)
      break
    console.print("Please be sure you've chosen title(t), release_date(d) or vote_average(r)", style="bold red")

  def do_something_important():
    time.sleep(1.0)

  def display_movies(movies):
    table = Table(title=":clapper_board: Movies", show_header=True, title_justify="left")
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

  page = 1
  while True:
    url = f"https://api.themoviedb.org/3/movie/{category}?api_key={api_key}&page={page}"
    try:
      response = requests.get(url, timeout=10)
      response.raise_for_status()
      data = response.json()
      total_pages = data["total_pages"]
    except requests.exceptions.RequestException:
      console.print("⚠️  Oops! Couldn’t reach TMDB servers. Please check your internet.", style="bold red")
      break
    except KeyError:
      console.print("⚠️  Unexpected response format from API.", style="bold red")
      break
    except Exception:
      console.print("💥  Something went wrong! Please try again.", style="bold red")
      break

    results = data.get("results", [])
    if not results:
      console.print(f"😕  No {category} movies found. Try again later!", style="italic cyan")
      break

    with console.status(f"Exploring TMDB universe for {category} movies (page {page})", spinner="earth"):
      do_something_important()
    console.print(f":rocket: All set! Here are the {category} movies (page {page})\n")

    sorted_data = sorted(results, key=lambda item: item[user_choice])
    display_movies(sorted_data)

    if page < total_pages:
      choice = Prompt.ask("\n[bold yellow]Do you want to see the next page?[/]", choices=["y","n"], default='n')
      if choice == "y":
        page += 1
        continue
      elif choice == "n":
        console.print(":party_popper:[bold green] Done browsing movies![/]")
        break
    else:
      console.print("[bold red]No more pages available.[/]")
      break

get_movies(args.type)






