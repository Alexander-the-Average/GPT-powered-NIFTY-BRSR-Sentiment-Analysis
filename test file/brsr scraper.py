import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

# Function to search Google and retrieve search result links
def google_search(query):
    base_url = "https://www.google.com/search"
    params = {"q": query}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    response = requests.get(base_url, params=params, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    search_results = soup.find_all("a")

    result_links = []
    for link in search_results:
        href = link.get("href")
        if href.startswith("/url?"):
            parsed = parse_qs(urlparse(href).query)
            if "q" in parsed:
                result_links.append(parsed["q"][0])

    return result_links

# Function to download PDF files with error handling
def download_pdf(url, filename):
    try:
        response = requests.get(url, timeout=60)  # Set a timeout of 60 seconds

        # Handle non-2xx HTTP status codes
        response.raise_for_status()

        # Specify the folder path for storing PDFs
        folder_path = "pdf_downloads"

        # Ensure the folder exists
        os.makedirs(folder_path, exist_ok=True)

        # Create the full path to the PDF file
        full_path = os.path.join(folder_path, filename)

        with open(full_path, "wb") as pdf_file:
            pdf_file.write(response.content)

        # Print a message when a PDF is downloaded
        print(f"Downloaded: {filename}")
    except (requests.exceptions.RequestException, requests.exceptions.Timeout) as e:
        # Handle errors (including timeouts) during download and print an error message
        print(f"Error downloading {filename}: {str(e)}")

# List to store skipped downloads
skipped_downloads = []

# Read each line from nifty200.txt and perform the tasks
with open("nifty200.txt", "r") as file:
    for line in file:
        # Append " BRSR Report" to the line
        search_query = line.strip() + " BRSR Report"

        # Search Google and retrieve result links
        result_links = google_search(search_query)

        if result_links:
            # Get the first result link
            first_link = result_links[0]

            # Check if the link points to a PDF
            if first_link.endswith(".pdf"):
                # Download the PDF file with error handling
                download_pdf(first_link, f"{search_query}.pdf")
            else:
                print(f"No PDF found for: {search_query}")

        # To avoid overloading Google, add a delay before the next search
        time.sleep(5)

# Retry the skipped downloads
for filename, url in skipped_downloads:
    download_pdf(url, filename)
