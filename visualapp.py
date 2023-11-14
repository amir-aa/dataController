import time
import threading

class ValueUpdater(threading.Thread):
    def __init__(self):
        super(ValueUpdater, self).__init__()
        self.value_to_display = 0
        self.stop_event = threading.Event()

    def run(self):
        while not self.stop_event.is_set():
            # Your logic to update the integer value (replace this with your own code)
            # For example, incrementing the value each iteration
            self.value_to_display += 1

            # Display the current value
            self.display_values()

            # Pause for 3 seconds
            time.sleep(3)

    def display_values(self):
        print(f"Current value: {self.value_to_display}")

    def stop(self):
        self.stop_event.set()
