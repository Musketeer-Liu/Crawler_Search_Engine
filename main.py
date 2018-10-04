import threading
from queue import Queue


from spider import Spider
from domain import *
from storage import *




PROJECT_NAME = 'Musketeer'
HOMEPAGE = 'http://www.musketeer-liu.info'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
THREAD_NUMBER = 8


# Thread Queue
queue = Queue()
# Call Spider Class
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)




# Create worker threads (will die when main exits)
def create_workers():
    for _ in range(THREAD_NUMBER):
        # work is the function name
        t = threading.Thread(target=work)
        # thread die when main exits
        t.daemon = True
        t.start()


# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# Each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


# Check if there are items in the queue, if so crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()




# if __name__ == '__main__':
create_workers()
crawl()
