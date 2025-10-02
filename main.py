db_type = "sqlite"
import sqlLite

from frontend.app import app

sqlLite.set_db_name("databases/test.db")

if db_type == "sqlite":
    import sqlLite.create as create
    import sqlLite.set as setter
    import sqlLite.get as getter
    #import testing as testing
    #testing.sqllite_reset()
    create.create_table_t_user()
    setter.set_login("test", "test@test.test", "password")
    setter.set_login("admin","admin@test.test", "admin")
    getter.get_password_by_email("admin@fuhlig.de")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
