import concurrent.futures
import logging
import pytube
import urlextract

extractor = urlextract.URLExtract()

def extract_youtube_title(link):
    return pytube.YouTube(link).title

def extract_youtube_urls(list_urls):
    return [url for url in list_urls if 'youtu' in url]

def extract_youtube_titles(list_urls):
    """
    Creates a pytube object for each url and extracts the title
    WARNING: Multithreaded
    """
    list_failed = []
    list_successful = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2**3) as executor:
        dict_futures = {}
        for url in list_urls:
            future = executor.submit(extract_youtube_title, url)
            dict_futures[future] = url

        for future in concurrent.futures.as_completed(dict_futures.keys()):
            if future.exception():
                logging.exception(future.exception())
                list_failed.append(dict_futures[future])
            else:
                list_successful.append(future.result())

    return list_successful

if __name__ == "__main__":
    s = "https://youtube/NUC2EQvdzmY"
    print(extract_youtube_title(s))