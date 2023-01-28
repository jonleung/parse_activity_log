import re

with open("test.txt", "r") as f:
    file_contents = f.read()

pattern = re.compile(r"\w*")

for match in pattern.finditer(file_contents):
    print(match.group())
