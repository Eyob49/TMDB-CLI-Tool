🎬 Movie CLI (TMDB API)

A simple Python command-line tool to fetch and display movies from [The Movie Database (TMDb)](https://www.themoviedb.org/). This project(https://roadmap.sh/projects/tmdb-cli) uses the TMDb API and supports different movie categories such as popular, top rated, upcoming, and now playing.

![Python](https://img.shields.io/badge/Python-3.9-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-green)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)

---

✨ Features
 - 🎥 Fetch movies by category (popular, top_rated, upcoming, now_playing).
 - 📆 Displays title, release date, and rating in a clean format.
- 🚫 Handles invalid categories gracefully.
- 🔐 Secure API key handling using environment variables.

---

🛠️ Installation

1.Clone this repository:
 - git clone https://github.com/Eyob49/TMDB-CLI-Tool.git
 - cd TMDB-CLI-Tool

2.Install dependencies:
- pip install -r requirements.txt

3.Set your TMDB API key as an environment variable:

- export API_KEY = "your_api_key_here" # for Linux/Mac

- setx API_KEY "your_api_key_here"   # for Windows

▶️ Usage 
Run the script with a category:

- python main.py --type popular

- Example output:

-   🎬 Title: War of the Worlds
    📅 Release: 2025-07-29
    ⭐ Rating: 4.3

⚠️ Valid Categories
• popular
• top_rated
• upcoming
• now_playing

🚀 Future Enhancements
• Add colorful tables using the rich library for better CLI output
• Implement pagination (view more than 1 page of results)
• Add movie search by keyword (e.g., --search "Inception")
• Export results to JSON/CSV file

📜 License
This project is licensed under the MIT License.



