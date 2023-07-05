from flask import Flask, jsonify
from sqlalchemy import create_engine, Table, MetaData

app = Flask(__name__)

CONN_STRING = 'mssql+pyodbc://sqlserver:Ibottest1@db-1.database.windows.net/db_1?driver=ODBC+Driver+17+for+SQL+Server'

@app.route('/')
def hello_world():
    engine = create_engine(CONN_STRING)

    metadata = MetaData()
    test_table = Table('test_table', metadata, autoload_with=engine)

    with engine.connect() as connection:
        result = connection.execute(test_table.select())
        rows = [dict(row) for row in result]

    return jsonify(rows)  # convert the result to a list of dicts

if __name__ == '__main__':
    app.run(debug=True)




