import threading
import time
import random

# Shared Memory: Bounded Buffer
BUFFER_SIZE = 5

buffer = [None] * BUFFER_SIZE

in_index = 0
out_index = 0


# OS Synchronization Tools

# Mutex protects critical sections
mutex = threading.Lock()

# Number of empty slots
empty = threading.Semaphore(BUFFER_SIZE)

# Number of filled slots
full = threading.Semaphore(0)


def data_loader_producer():

    """
    Simulates loading images
    from Disk to RAM Buffer
    """

    global in_index

    for i in range(10):

        item = f"Image_Batch_{i}"

        # Simulating Disk I/O delay
        time.sleep(random.uniform(0.1, 0.3))

        # Wait if buffer is full
        empty.acquire()

        # Lock buffer
        mutex.acquire()

        # --- CRITICAL SECTION ---

        buffer[in_index] = item

        print(
            f"[Producer] Loaded: {item} "
            f"into slot {in_index}"
        )

        in_index = (in_index + 1) % BUFFER_SIZE

        # ------------------------

        # Unlock buffer
        mutex.release()

        # Signal that new item is available
        full.release()


def gpu_trainer_consumer():

    """
    Simulates taking images
    from RAM Buffer to train model
    """

    global out_index

    for i in range(10):

        # Wait if buffer is empty
        full.acquire()

        # Lock buffer
        mutex.acquire()

        # --- CRITICAL SECTION ---

        item = buffer[out_index]

        print(
            f" -> [Consumer] Training on: "
            f"{item} from slot {out_index}"
        )

        out_index = (out_index + 1) % BUFFER_SIZE

        # ------------------------

        # Unlock buffer
        mutex.release()

        # Signal that a slot is empty
        empty.release()

        # Simulating GPU training delay
        time.sleep(random.uniform(0.2, 0.5))


def main():

    print(
        "--- Starting ML Data Pipeline "
        "(Bounded Buffer) ---"
    )

    # Create Producer Thread
    producer_thread = threading.Thread(
        target=data_loader_producer
    )

    # Create Consumer Thread
    consumer_thread = threading.Thread(
        target=gpu_trainer_consumer
    )

    # Start threads
    producer_thread.start()
    consumer_thread.start()

    # Wait for threads
    producer_thread.join()
    consumer_thread.join()

    print(
        "--- Pipeline Execution "
        "Completed Successfully ---"
    )


if __name__ == "__main__":
    main()