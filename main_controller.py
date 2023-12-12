from flask import Flask, render_template, request
from models import ZooFacade, ZooObserver

app = Flask(__name__)

TABLE_NAMES = ['ВОЛЬЄР', 'ТВАРИНИ', 'ПЕРСОНАЛ', 'ТУРИСТИ', 'КВИТОК']
DATABASE_PATH = r"F:\Denis\WOOOOORRRRKKK\SKBD\ZOO.accdb"

zoo_facade = ZooFacade(DATABASE_PATH)
zoo_observer = ZooObserver()

# Register the observer
zoo_facade.register_observer(zoo_observer)

@app.route('/')
def index():
    return render_template('index.html', table_names=TABLE_NAMES)

@app.route('/table', methods=['POST'])
def show_table():
    selected_table = request.form.get('table')
    columns, data = zoo_facade.get_table_data(selected_table)
    return render_template('table.html', table_name=selected_table, columns=columns, data=data)

@app.route('/personal', methods=['POST'])
def show_personal_by_id():
    personal_id = request.form.get('personalId')
    columns, data = zoo_facade.get_personal_data_by_id(personal_id)
    
    if not data:
        return render_template('error.html')
    else:
        return render_template('table.html', table_name="ПЕРСОНАЛ", columns=columns, data=data)

if __name__ == '__main__':
    app.run(debug=True)
