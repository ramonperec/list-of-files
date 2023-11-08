import hashlib
import os
from bs4 import BeautifulSoup
from datetime import datetime

exts = ['.c', '.h']

def format_time_to_date(time):
    date_format = datetime.fromtimestamp(time)
    return date_format.strftime("%d:%m:%Y")

def get_file_info(filepath):
    file_size = os.path.getsize(filepath)
    mod_time = os.path.getmtime(filepath)
    return {
        'name': filepath,
        'size': file_size,
        'mod_time': format_time_to_date(mod_time),
    }

def calculate_checksum(filepath):
    with open(filepath, 'rb') as f:
        buf = f.read()
    return hashlib.sha1(buf).hexdigest()

root_dir = 'd:\\work\\'
html_data_template = '''
<tr>
    <td>{name}</td>
    <td>{size}</td>
    <td>{mod_time}</td>
    <td>-</td>
    <td>{checksum}</td>
</tr>'''

html_table_template = '''
<table>
    <tr>
        <th>Name</th>
        <th>Size</th>
        <th>Last Modified</th>
        <th>Author</th>
        <th>Checksum</th>
    </tr>
{data}
</table>'''

files = {}
for subdir, dirs, file_list in os.walk(root_dir):
    for f in file_list:
        filepath = os.path.join(subdir, f)

        if any(filepath.endswith(ext) for ext in exts):
            files[filepath] = get_file_info(filepath)
            files[filepath]['checksum'] = calculate_checksum(filepath)

data = ''.join(html_data_template.format(**file_dict) for file_dict in files.values())
soup = BeautifulSoup(html_table_template.format(data=data), 'html.parser')

with open('file_list.html', 'w', encoding='utf-8') as f:
    f.write(soup.prettify())