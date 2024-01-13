import argparse
from PIL import Image
import threading
import signal
import queue
import time
import os

from logic import classify_image

STOP_THREADS = False
threads = []
detected_images = 0
deleted_images = 0

threads_remove_semaphore = threading.Semaphore(1)
data_update_mux = threading.Semaphore(1)
threads_semaphore = None

def is_image(file_path, filename):
    if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif', ".svg")):
        return False
    try:
        with Image.open(file_path):
            return True
    except (IOError, OSError):
        return False
    

# Function to gracefully stop the program on CTRL + C
def stop_program(signum, frame, img_queue):
    global STOP_THREADS, threads, threads_semaphore, threads_remove_semaphore, deleted_images, detected_images
    STOP_THREADS = True
    if signum != None:
        print("Ctrl + C detected. Emptying queue")
    else:
        print("Internal Call for program termination")

    print("Clearing queue: ", end="")
    img_queue.mutex
    while not img_queue.empty():
        img_queue.get()
        img_queue.task_done()
    print("Done")

    print("Clearing threads: ", end="")
    time.sleep(2)
    threads_remove_semaphore.acquire()
    for thread in threads:
            thread.join()
            threads.remove(thread)
            threads_semaphore.release()
    threads_remove_semaphore.release()
    print(f"Deleted {deleted_images} of {detected_images} detected wishtender images.")
    print("Done")
    exit(0)

def get_files(path:str, recursive=False):
    images = []
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
    
        # Check if it's a file (not a directory)
        if is_image(file_path, filename):
            images.append([file_path, filename])
        if recursive:
            if os.isdir(file_path):
                more_images = get_files(file_path, recursive=recursive)
                for img in more_images:
                    images.append(img)
    return images

def delete_img(img):
    try:
        os.remove(img[0])
        return True
    except OSError as e:
        return False

def classify_manager(img_queue:queue, delete=False):
    global data_update_mux, detected_images, deleted_images

    img = img_queue.get(timeout=1)

    class_name, confidence =  classify_image(img[0])
    if class_name == "wishtender\n" and float(confidence) >= 0.9:
        deleted = False
        if delete:
            deleted = delete_img(img)
        
        if deleted:
            data_update_mux.acquire()
            detected_images += 1
            deleted_images += 1
            data_update_mux.release()
        else:
            data_update_mux.acquire()
            detected_images += 1
            data_update_mux.release()
    img_queue.task_done()
    threads_semaphore.release()

def main():
    parser = argparse.ArgumentParser(prog='Wishtender-Remover', description='Remove all wishtender images in a folder', epilog='https://github.com/vanishedbydefa')
    parser.add_argument('-p', '--path', default=str(os.getcwd()), type=str, help='Path to the folder in which to find wishtender images')
    parser.add_argument('-d', '--delete', action='store_true', help='Delete found wishtender images')
    parser.add_argument('-t', '--threads', default=4, type=int, help='Maximum amount of running threads')
    parser.add_argument('-r', '--recursive', action='store_true', help='Also search for wishtender images in sub-folders')

    args = parser.parse_args()
    param_path = args.path
    param_delete = args.delete
    param_threads = args.threads
    param_recursive = args.recursive

    img_queue = queue.Queue()
    images = get_files(param_path,param_recursive)
    for img in images:
        img_queue.put(img)

    while not STOP_THREADS:
        # Thread logic
        global threads_semaphore, threads, threads_remove_semaphore
        threads_semaphore = threading.Semaphore(param_threads)

        while int(img_queue.qsize()) != 0:
            print(f"Remaining Images: {str(img_queue.qsize())} get classyfied by {str(str(len(threads)))}/{param_threads} Threads      ", flush=True)
            threads_semaphore.acquire()
            thread = threading.Thread(target=classify_manager, args=(img_queue, param_delete,))
            thread.start()
            threads.append(thread)
            
            for thread in threads:
                if not thread.is_alive():
                    thread.join()
                    threads_remove_semaphore.acquire()
                    threads.remove(thread)
                    threads_remove_semaphore.release()

            # Register signal handler for Ctrl + C
            signal.signal(signal.SIGINT, lambda sig, frame: stop_program(sig, frame, img_queue))

            if STOP_THREADS:
                stop_program(None, None, img_queue)

        threads_remove_semaphore.acquire()
        for thread in threads:
            thread.join()
            threads.remove(thread)
            threads_semaphore.release()
        threads_remove_semaphore.release()
        print(f"Deleted {deleted_images} of {detected_images} detected wishtender images.")
        print(f"All threads terminated")
        break
    print(f"Program done")

main()
