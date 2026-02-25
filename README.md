# Random Book Picker

A Python tool that selects a random book from a Goodreads shelf.
This script fetches the RSS feed for a specified Goodreads shelf and prints one random book from it (title, author, and link).

## How It Works

The program:

1. Converts a Goodreads shelved books page URL into its RSS feed URL.
2. Parses the RSS feed to extract book entries.
3. Picks **one random book** and displays it in the console.

## Requirements

To run this script, you need:

- **Python 3.7+**
- `requests` (for HTTP requests)
- Standard library modules (no extra install needed beyond `requests`)

Install `requests` with:

```bash
pip install requests
````

## Usage

1. Clone the repository:

```bash
git clone https://github.com/claudiax9/random-book-picker.git
```

2. Open `main.py` and replace the `GOODREADS_SHELF_URL` constant with your own Goodreads shelf URL.
   It must be a shelf link that contains `?shelf=...`.

Example Goodreads shelf link format:

```
https://www.goodreads.com/review/list/YOUR_USER_ID?shelf=YOUR_SHELF_NAME
```

3. Run the script:

```bash
python main.py
```

You’ll see output like:

```
Randomly selected book:
 Book Title — Author Name
 Link: https://www.goodreads.com/…
```

## Notes

* The script expects the Goodreads shelf URL to include a `shelf=...` query parameter.
* If Goodreads blocks access or requires authentication, the RSS feed may not return correctly.
