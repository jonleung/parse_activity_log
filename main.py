import re

RE_SETTINGS = re.MULTILINE |re.DOTALL | re.IGNORECASE

with open("hard.txt", "r") as f:
    file_contents = f.read()

date_regex = re.compile(r"-\s\w{3},\s\w{3}\s\d{1,2},\s\d{4}\n(?:(?!-\s\w{3},\s\w{3}\s\d{1,2},\s\d{4}\n).)*", RE_SETTINGS);
for a, date_match in enumerate(date_regex.finditer(file_contents)):
    date_string = date_match.group()
    # print(f"# Date Match {a+1}:\n{date_string}")
    
    task_regex = re.compile(r"^\s{2}-\s(.*?\#koya.*?)$\n(?:(?!^\s{2}-\s.*?\#koya.*?$\n).)*", RE_SETTINGS);
    for b, task_match in enumerate(task_regex.finditer(date_string)):
        task_level_string = task_match.group()

        task_first_line = task_match.group(1).replace("#koya", "")
        hashtag_match = re.findall(r"#[\w|-]+", task_first_line)
        match = re.findall(r"#\w+", task_first_line)
        if match:
            hashtag = match[0]
            task_first_line = task_first_line.replace(hashtag, "")
        else:
            hashtag = "n/a"

        # remove extra spaces from first line
        task_first_line = re.sub(r"\s+", " ", task_first_line).strip()

        print(f"## Task Match {b+1}: \t {hashtag} \t Deets: {task_first_line}\n{task_level_string}")