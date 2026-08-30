import os
import time


def main():

    # Create Pipe
    r, w = os.pipe()

    # Create child process
    pid = os.fork()

    if pid > 0:

        # -------------------------
        # PARENT PROCESS
        # ML Trainer
        # -------------------------

        os.close(w)

        r_file = os.fdopen(r)

        print(
            f"[Trainer PID:{os.getpid()}] "
            "Waiting for data from DataLoader..."
        )

        # Wait for data
        data = r_file.read()

        print(
            f"[Trainer PID:{os.getpid()}] "
            f"Received Data: '{data}'"
        )

        print(
            f"[Trainer PID:{os.getpid()}] "
            "Training complete."
        )

        # Wait for child
        os.wait()

    elif pid == 0:

        # -------------------------
        # CHILD PROCESS
        # DataLoader
        # -------------------------

        os.close(r)

        w_file = os.fdopen(w, 'w')

        print(
            f" -> [DataLoader PID:{os.getpid()}] "
            "Loading image from disk..."
        )

        # Simulate I/O delay
        time.sleep(2)

        image_data = "Image_Tensor_Batch_01"

        print(
            f" -> [DataLoader PID:{os.getpid()}] "
            "Sending data through OS Pipe..."
        )

        w_file.write(image_data)

        # Closing signals EOF
        w_file.close()


if __name__ == "__main__":
    main()