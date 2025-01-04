import logging
import os

# Configure the logging
LOG_DIR = "/var/log/DCore"  # Directory for log files
os.makedirs(LOG_DIR, exist_ok=True)  # Ensure the directory exists

LOG_FILE = os.path.join(LOG_DIR, "dcore.log")
logging.basicConfig(
    level=logging.DEBUG,  # Log level
    format="%(asctime)s [%(levelname)s] %(message)s",  # Log format
    handlers=[
        logging.FileHandler(LOG_FILE),  # Log to file
        logging.StreamHandler()  # Log to console
    ]
)

# Example logging functions
def log_startup():
    logging.info("DCore display manager started.")

def log_shutdown():
    logging.info("DCore display manager shutting down.")

def log_error(error_message):
    logging.error(f"Error occurred: {error_message}")

def log_event(event_description):
    logging.debug(f"Event: {event_description}")

# Example usage
if __name__ == "__main__":
    log_startup()
    try:
        # Simulate some events
        log_event("Initialized display configuration.")
        log_event("Loaded UI components.")
        # Simulate an error
        raise ValueError("Simulated error for demonstration.")
    except Exception as e:
        log_error(str(e))
    finally:
        log_shutdown()
