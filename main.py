import sqlLite

from frontend.app import app

sqlLite.set_db_name("databases/test.db")

import sqlLite.create as create

create.create_table_t_user()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
