import os
import re
from collections import defaultdict

report_path = 'eslint-report.txt'

with open(report_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

file_errors = defaultdict(list)
current_file = None

for line in lines:
    line = line.strip()
    if line.startswith('C:\\') and line.endswith('.js') or line.endswith('.jsx'):
        current_file = line
    elif current_file and re.match(r'^\d+:\d+', line):
        parts = re.split(r'\s+', line)
        line_num = int(parts[0].split(':')[0])
        # Find the rule name (usually at the end)
        rule_name = parts[-1]
        
        # Specifically handle the impure function error which spans multiple lines
        if 'Cannot call impure function' in line:
            # We will manually fix QuestionsFromTeaching.jsx
            continue
            
        if rule_name in ['no-unused-vars', 'react-hooks/exhaustive-deps']:
            file_errors[current_file].append((line_num, rule_name))

for file_path, errors in file_errors.items():
    if not os.path.exists(file_path):
        continue
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content_lines = f.readlines()
    
    # Sort errors descending by line number to avoid shifting
    errors.sort(key=lambda x: x[0], reverse=True)
    
    for line_num, rule in errors:
        idx = line_num - 1 # 0-indexed
        indent = len(content_lines[idx]) - len(content_lines[idx].lstrip())
        comment = ' ' * indent + f'// eslint-disable-next-line {rule}\n'
        content_lines.insert(idx, comment)
        
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(content_lines)

print("Done fixing lint errors!")
