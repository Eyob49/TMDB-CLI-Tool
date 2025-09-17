import requests
import os
import argparse
import time
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")

console = Console()

parser = argparse.ArgumentParser()
parser.add_argument("--type", "-t",type=str, help="Movie Category")
parser.add_argument("--search", type=str ,help="Search movies by key word")
parser.add_argument("--page", type=int , default=1, help="Page number (default: 1)")
args = parser.parse_args()


def fetch_movies(url):
   response = requests.get(url, timeout=10)
   response.raise_for_status()
   return response.json()


def get_movies_by_search(search, data):
    try:
        for movie in data["results"]:
            title = movie.get("title", "Unknown Title")
            release_date = movie.get("release_date", "Unknown Date")
            rating = movie.get("vote_average", "N/A")
            console.print(f" Title: [bold cyan]{title}[/]\n Release Date: {release_date}\n Rating: {rating}\n") 
    except requests.exceptions.RequestException:
        console.print("⚠️  Oops! Couldn't reach TMDB servers. Please check your internet.", style="bold red")
        return
    except KeyError:
        console.print("⚠️  Unexpected response format from API.", style="bold red")
        return
    except Exception:
        console.print("💥  Something went wrong! Please try again.", style="bold red")
        return

    if not data.get("results"):
        console.print(f"😕  No movies found for '{search}'. Try again later!", style="italic cyan")
        return


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
    try:
      url = f"https://api.themoviedb.org/3/movie/{category}?api_key={api_key}&page={page}"
      data = fetch_movies(url)
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

if __name__ == "__main__":
 if args.search:
  url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={args.search}&page={args.page}"
  data = fetch_movies(url)
  get_movies_by_search(args.search, data)
 elif args.type:
   get_movies(args.type)
 else:
  console.print("[red] Please provide either --category or --search[/]")
  
