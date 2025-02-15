import os
import glob

log_dir = "/data/logs/"
output_file = "/data/logs-recent.txt"

try:
    log_files = sorted(glob.glob(os.path.join(log_dir, "*.log")), key=os.path.getmtime, reverse=True)[:10]

    with open(output_file, "w") as out:
        for file in log_files:
            with open(file, "r") as log:
                first_line = log.readline().strip()
                out.write(first_line + "\n")

    print("Extracted first lines from 10 most recent logs.")

except Exception as e:
    print(f"Error processing logs: {e}")
