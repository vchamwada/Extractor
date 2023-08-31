import requests
import queue
import threading
from bs4 import BeautifulSoup

# Using requests module to fetch the markup from a URL
def fetch_url(url, markup_queue):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            markup = response.text
            markup_queue.put(markup)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")


def process_markup(markup, output_file):
    """Parse the markup using BeautifulSoup to extract hyperlinks"""
    soup = BeautifulSoup(markup, "html.parser")
    links = [a["href"] for a in soup.find_all("a", href=True)]

    # Write the extracted hyperlinks to the output file
    with open(output_file, "a") as file:
        for link in links:
            file.write(f"{link}\n")


def producer_consumer(url_list, output_file, max_queue_size=10):
    """Create a queue to hold fetched markups"""
    markup_queue = queue.Queue(max_queue_size)

    def consumer():
        """The consumer thread processes markups from the queue"""
        while True:
            markup = markup_queue.get()
            if markup is None:
                break
            process_markup(markup, output_file)
            markup_queue.task_done()

    # Start the consumer thread
    consumer_thread = threading.Thread(target=consumer)
    consumer_thread.start()

    # Start producer threads to fetch markups from URLs
    producer_threads = []
    for url in url_list:
        thread = threading.Thread(target=fetch_url, args=(url, markup_queue))
        thread.start()
        producer_threads.append(thread)

    # Wait for all producer threads to finish fetching markups
    for thread in producer_threads:
        thread.join()

    # Signal consumer to stop after all URLs are fetched
    markup_queue.put(None)
    consumer_thread.join()


if __name__ == "__main__":
    # Read URL list from a file
    url_file = "urls.txt"
    with open(url_file, "r") as file:
        url_list = [url.strip() for url in file]

    # Specify the output file for parsed links
    output_file = "output/parsed_links.txt"

    # Run producer-consumer workflow
    producer_consumer(url_list, output_file)

    # Print completion message
    print("Parsing and extracting links complete.")
