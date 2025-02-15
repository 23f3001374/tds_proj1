from datetime import datetime

input_file = "/data/dates.txt"
output_file = "/data/dates-wednesdays.txt"

try:
    with open(input_file, "r") as f:
        dates = f.readlines()

    wednesday_count = sum(1 for date in dates if datetime.strptime(date.strip(), "%Y-%m-%d").weekday() == 2)

    with open(output_file, "w") as f:
        f.write(str(wednesday_count))

    print(f"Counted {wednesday_count} Wednesdays.")

except Exception as e:
    print(f"Error processing file: {e}")
