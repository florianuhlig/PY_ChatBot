db_type = "sqlite"
import sqlLite
sqlLite.set_db_name("databases/test.db")

if db_type == "sqlite":
    import sqlLite.get as getter
    import sqlLite.create as create
    import sqlLite.set as setter
    import testing as testing
    create.create_table_t_user()
    setter.set_login("test@test.test", "password")
    getter.get_user()
    #testing.sqllite_reset(sqlitename)

