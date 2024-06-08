import os
from pathlib import Path
import sys
import logging

logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"
logging_dir = "logging"
log_file_path = os.path.join(logging_dir, "running_logs.log")
os.makedirs(logging_dir, exist_ok= True)

logging.basicConfig(
    level=logging.INFO,
    format=logging_str,
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("textSummarizerLogger")