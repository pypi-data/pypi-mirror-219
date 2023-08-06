import libsql_client

create_table_keyvalue = '''
CREATE TABLE keyvalue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    namespace TEXT NOT NULL,
    key TEXT UNIQUE NOT NULL,
    value TEXT
);
'''

create_table_leaderboard = '''
CREATE TABLE leaderboard (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gamename TEXT NOT NULL,
    username TEXT unique NOT NULL,
    score INTEGER NOT NULL
);
'''

create_table_counter = '''
CREATE TABLE counter (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    namespace TEXT NOT NULL,
    key TEXT UNIQUE NOT NULL,
    value INTEGER NOT NULL
);
'''

def sql_stmt(stmnt, args):
    return [stmnt, args]

def insert_leaderboard_value(gamename, player, score):
    return sql_stmt('insert into leaderboard (gamename, username, score) values (?, ?, ?)\
                    ON CONFLICT(username) DO UPDATE SET score=score;', 
                    [gamename, player, score])

def select_game(gamename):
    return sql_stmt('select username,score from leaderboard where gamename = ?;', [gamename])

def insert_kv(key, value, namespace='default'):
    return sql_stmt('INSERT into keyvalue (namespace, key, value) values (?, ?, ?)\
                    ON CONFLICT(key) DO UPDATE SET value=value;', [namespace, key, value])

def increase_counter(key, value, namespace='default'):
    return sql_stmt('INSERT into counter (namespace, key, value) values (?, ?, ?)\
                    ON CONFLICT (key) DO UPDATE SET value = value + 1;', [namespace, key, value])

def select_counter(key, namespace='default'):
    return sql_stmt('''select IFNULL(key, '') key, IFNULL(value, 0) value
                    from counter 
                    where namespace = ? and key = ?;''', [namespace, key])

def select_kv(namespace='default'):
    return sql_stmt('select key,value from keyvalue where namespace = ?;', [namespace])

# def check_kv_exists(key, namespace='default'):
#     return sql_stmt('select value from keyvalue where namespace=? and key=?;', [namespace, key])

def libsql_batch(stmnts):
    '''
    stmnts: 
        [sql_stmt(stmnt, args),]
    '''
    return [
    libsql_client.Statement(
        s[0],
        s[1]
    ) for s in stmnts]

create_tables = [
    [create_table_keyvalue, []],
    [create_table_leaderboard, []],
    [create_table_counter, []],
]
