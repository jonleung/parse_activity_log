import re
from datetime import datetime
# from dateutil import parser
import csv

RE_SETTINGS = re.MULTILINE |re.DOTALL | re.IGNORECASE

rows = []

with open("real2.txt", "r") as f:
    file_contents = f.read()

date_regex = re.compile(r"-\s(\w{3},\s\w{3}\s\d{1,2},\s\d{4})\n(?:(?!-\s\w{3},\s\w{3}\s\d{1,2},\s\d{4}\n).)*", RE_SETTINGS);
for a, date_match in enumerate(date_regex.finditer(file_contents)):
    date_string = date_match.group()
    # print(f"# Date Match {a+1}:\n{date_string}")
    date_first_line = date_match.group(1)
    date_output = date_first_line[5:]
    # print("----------------------------------------------------------------------------------------------------------------------------------------")
    # print(f"# Date Match {a+1}:\t '{date_first_line}'")
    # print("----------------------------------------------------------------------------------------------------------------------------------------")

    task_regex = re.compile(r"^\s{2}-\s(.*?\#koya.*?)$\n(?:(?!^\s{2}-\s.*?\#koya.*?$\n).)*", RE_SETTINGS);
    # 🔴 If there is no tasks, then flag an error
    b = -1
    for b, task_match in enumerate(task_regex.finditer(date_string)):
        task_level_string = task_match.group()

        task_first_line = task_match.group(1).replace("#koya", "")
        hashtag_match = re.findall(r"#[\w|-]+", task_first_line)
        if hashtag_match:
            hashtag = hashtag_match[0]
            task_first_line = task_first_line.replace(hashtag, "")
        else:
            hashtag = "n/a"

        # remove extra spaces from first line
        task_first_line = re.sub(r"\s+", " ", task_first_line).strip()

        if task_first_line == "":
            task_first_line = "n/a"
        # print(f"## Task Match {b+1}: \t '{hashtag}' \t Deets: '{task_first_line}'\n{task_level_string}")
        # print(f"\nTask Match {b+1}: '{hashtag}', {task_first_line}")

        time_regex = re.compile(r"(\s{4}-\s(\d{1,2}:?\d{0,2}\s*\w{0,2})\s*-\s*(\d{1,2}:?\d{0,2}\s*\w{0,2})\s*$\n)", RE_SETTINGS)
        # 🔴 If there is no time, then flag an error
        c = -1
        for c, time_match in enumerate(time_regex.finditer(task_level_string)):
            start_time_string = time_match.group(2)
            end_time_string = time_match.group(3)

            # print(f"\t Time Match {c+1}: {time_match.group(2)} - {time_match.group(3)}")

            # Date
            # print(date_output)

            # # Hashtag
            # print(hashtag)

            # # Deets
            # print(task_first_line)

            # # Start Time
            # print(start_time_string)

            # # End Time
            # print(end_time_string)

            # Duration
            try:
                start_time = datetime.strptime(start_time_string, "%I:%M%p")
            except ValueError as e:
                print(f"🚨 Error parsing Start Time {start_time_string} in {date_string} 🚨")
                exit()
            try:
                end_time = datetime.strptime(end_time_string, "%I:%M%p")
            except ValueError as e:
                print(f"🚨 Error parsing Start Time {end_time_string} in {date_string} 🚨")
                exit()
            # start_time = parser.parse(start_time_string)
            # end_time = parser.parse(end_time_string)
            time_diff = end_time - start_time
            duration_in_minutes = int(time_diff.total_seconds() / 60)
            # print(duration_in_minutes)

            row = [date_output, hashtag, task_first_line, start_time_string, end_time_string, duration_in_minutes]
            rows.append(row)
            
            print(f"{date_output}\t{hashtag}\t{task_first_line}\t{start_time_string}\t{end_time_string}\t{duration_in_minutes}")

        if c == -1:  # this means that the for loop for iterating through time stamps never ran
            print(f"🚨 Error: No times found on date: '{date_first_line}' in task '{task_level_string}' 🚨")
            exit()

    if b == -1: # this means that the for loop for iterating through tasks never ran
        print(f"🚨 Error: No tasks found on date: '{date_first_line}': '{date_string}' 🚨")
        exit()

with open("tasks.csv", "w", newline="") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerows(rows)

print("\n✅ Completed with no errors detected.\n")




