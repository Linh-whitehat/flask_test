{% if fail_rows and fail_rows|length > 0 %}
<h3>Chi tiết lỗi</h3>
<table>
    <tr>
        <th>Dòng</th>
        <th>Nội dung</th>
    </tr>
    {% for row in fail_rows %}
    <tr>
        <td>{{ row.line }}</td>
        <td>{{ row.data }}</td>
    </tr>
    {% endfor %}
</table>
{% endif %}


from flask import Flask, render_template, request
from openpyxl import load_workbook
import csv
import io
import re

app = Flask(__name__)

# 👉 Lấy ngày từ tên file
def get_date_from_filename(filename):
    match = re.search(r'\d{6}', filename)
    if match:
        d = match.group()
        return f"20{d[0:2]}-{d[2:4]}-{d[4:6]}"
    return filename


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    fail_rows = []   # 👉 lưu dòng lỗi

    if request.method == 'POST':
        file = request.files.get('file')

        if not file or file.filename == '':
            return render_template('index.html', result=None, fail_rows=[])

        file_date = get_date_from_filename(file.filename)
        fail_count = 0

        try:
            # 👉 Excel
            if file.filename.endswith('.xlsx'):
                wb = load_workbook(file)
                ws = wb.active
                rows = ws.iter_rows(min_row=2, values_only=True)

            # 👉 CSV
            else:
                content = file.read().decode("utf-8", errors='ignore')
                stream = io.StringIO(content)
                reader = csv.reader(stream)
                next(reader, None)
                rows = reader

            # 👉 Đếm + lưu dòng lỗi
            for idx, row in enumerate(rows, start=2):
                if not row:
                    continue

                if any('fail' in str(cell).lower() for cell in row):
                    fail_count += 1

                    # 👉 lưu dòng lỗi (join lại cho dễ đọc)
                    fail_rows.append({
                        "line": idx,
                        "data": " | ".join(str(x) for x in row)
                    })

            result = {file_date: fail_count}

        except Exception as e:
            result = {"Lỗi": str(e)}

    return render_template('index.html', result=result, fail_rows=fail_rows)


if __name__ == '__main__':
    app.run(debug=True) 


😁
from flask import Flask, render_template, request
from openpyxl import load_workbook
import csv
import io
import re

app = Flask(__name__)

# 👉 Hàm lấy ngày từ tên file
def get_date_from_filename(filename):
    match = re.search(r'\d{6}', filename)
    if match:
        d = match.group()
        return f"20{d[0:2]}-{d[2:4]}-{d[4:6]}"
    return filename  # fallback nếu không match


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None

    if request.method == 'POST':
        file = request.files.get('file')

        if not file or file.filename == '':
            return render_template('index.html', result=None)

        # 👉 lấy ngày từ tên file
        file_date = get_date_from_filename(file.filename)

        fail_count = 0

        try:
            # 👉 Excel
            if file.filename.endswith('.xlsx'):
                wb = load_workbook(file)
                ws = wb.active
                rows = ws.iter_rows(min_row=2, values_only=True)

            # 👉 CSV
            else:
                content = file.read().decode("utf-8", errors='ignore')
                stream = io.StringIO(content)
                reader = csv.reader(stream)
                next(reader, None)
                rows = reader

            # 👉 Đếm FAIL
            for row in rows:
                if not row:
                    continue

                if any('fail' in str(cell).lower() for cell in row):
                    fail_count += 1

            # 👉 Kết quả dạng dict
            result = {file_date: fail_count}

            print("RESULT:", result)

        except Exception as e:
            print("ERROR:", e)
            result = {"Lỗi": str(e)}

    return render_template('index.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)
UnboundLocalError: cannot access local variable 'ws' where it is not associated with a value

Traceback (most recent call last)

from flask import Flask, render_template, request
from openpyxl import load_workbook
from collections import defaultdict
from datetime import datetime
import csv
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = {}

    if request.method == 'POST':
        file = request.files['file']

        if file:
            fail_count = defaultdict(int)

            # 👉 Excel
            if file.filename.endswith('.xlsx'):
                wb = load_workbook(file)
                ws = wb.active
                rows = ws.iter_rows(min_row=2, values_only=True)

            # 👉 CSV
            else:
                stream = io.StringIO(file.stream.read().decode("utf-8"))
                reader = csv.reader(stream)
                next(reader)
                rows = reader

            for row in rows:
                date = row[0]
                status = str(row[1]).strip().lower()

                if date and status == 'fail':
                    if isinstance(date, datetime):
                        date_str = date.strftime('%Y-%m-%d')
                    else:
                        date_str = str(date)

                    fail_count[date_str] += 1

            result = dict(fail_count)

    return render_template('index.html', result=result)


if __name__ == '__main__':
    app.run(debug=True) 


----------------------
# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from flask import Flask, render_template, request
from openpyxl import load_workbook
import os
from collections import defaultdict
app = Flask(__name__)
@app.route('/', methods=['GET','POST'])

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

--------------------------------------
from flask import Flask, render_template, request
from openpyxl import load_workbook
import os
from collections import defaultdict

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    result = {}

    if request.method == 'POST':
        file = request.files['file']

        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            wb = load_workbook(filepath)
            ws = wb.active

            fail_count = defaultdict(int)

            for row in ws.iter_rows(min_row=2, values_only=True):
                date = row[0]
                status = str(row[1]).strip().lower()

                if date and status == 'fail':
                    date_str = date.strftime('%Y-%m-%d')
                    fail_count[date_str] += 1

            result = dict(fail_count)

    # 👉 ĐẶT Ở ĐÂY
    return render_template('index.html', result=result)
