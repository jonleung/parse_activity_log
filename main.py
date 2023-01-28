import re

with open("hard.txt", "r") as f:
    file_contents = f.read()

pattern = re.compile(r"-\s\w{3},\s\w{3}\s\d{1,2},\s\d{4}\n(?:(?!-\s\w{3},\s\w{3}\s\d{1,2},\s\d{4}\n).)*", re.MULTILINE |re.DOTALL | re.IGNORECASE);

for a, match in enumerate(pattern.finditer(file_contents)):
    print(f"### Match {a+1}:\n{match.group()}")

