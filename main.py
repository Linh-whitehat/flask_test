
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
