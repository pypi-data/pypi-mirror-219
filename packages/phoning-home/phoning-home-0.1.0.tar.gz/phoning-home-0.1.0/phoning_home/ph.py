import libsql_client

from . import _sql

from functools import wraps

class PhoningHome:
    URL = ''
    TOKEN = ''
    con = None

    @classmethod
    def connect(cls, url, token):
        cls.URL = url
        cls.TOKEN = token
        cls.create_tables()
    
    @classmethod
    def create_tables(cls):
        client = libsql_client.create_client_sync(
            url=cls.URL,
            auth_token=cls.TOKEN
        )
        with client:
            try:
                libsql_statements = [
                    libsql_client.Statement(
                        s[0],
                        s[1]
                    ) for s in _sql.create_tables]
                rss = client.batch(libsql_statements)
            except libsql_client.client.LibsqlError as e:
                pass
    
    @classmethod
    def fetch(cls, *args):
        if len(args) in [0]:
            raise Exception('Should have more arguments')
        
        optype = args[0]

        if optype == 'leaderboard':
            if len(args) != 2:
                raise Exception('Args should be: leaderboard, <gamename>')
            
            gamename = args[1]
            client = libsql_client.create_client_sync(
                url=cls.URL,
                auth_token=cls.TOKEN
            )
            with client:
                try:
                    stmnts = [_sql.select_game(gamename)]
                    libsql_stmnts = _sql.libsql_batch(stmnts)
                    rss = client.batch(libsql_stmnts)
                    return rss[0].rows
                except libsql_client.client.LibsqlError:
                    pass
        elif optype == 'info':
            client = libsql_client.create_client_sync(
                url=cls.URL,
                auth_token=cls.TOKEN
            )
            with client:
                try:
                    stmnts = [_sql.select_kv(namespace='default')]
                    libsql_stmnts = _sql.libsql_batch(stmnts)
                    rss = client.batch(libsql_stmnts)
                    return rss[0].rows
                except libsql_client.client.LibsqlError:
                    pass
        elif optype == 'namedinfo':
            if len(args) != 2:
                raise Exception('Args should be: namedinfo, <namespace>')
            
            namespace = args[1]
            client = libsql_client.create_client_sync(
                url=cls.URL,
                auth_token=cls.TOKEN
            )
            with client:
                try:
                    stmnts = [_sql.select_kv(namespace=namespace)]
                    libsql_stmnts = _sql.libsql_batch(stmnts)
                    rss = client.batch(libsql_stmnts)
                    return rss[0].rows
                except libsql_client.client.LibsqlError:
                    pass
        
        elif optype == 'counter':
            if len(args) != 2:
                raise Exception('Args should be: counter, <key value>')
            
            key = args[1]
            client = libsql_client.create_client_sync(
                url=cls.URL,
                auth_token=cls.TOKEN
            )
            with client:
                try:
                    stmnts = [_sql.select_counter(key, namespace='default')]
                    libsql_stmnts = _sql.libsql_batch(stmnts)
                    rss = client.batch(libsql_stmnts)
                    return rss[0].rows
                except libsql_client.client.LibsqlError:
                    pass
    
    @classmethod
    def leaderboard(cls, gamename, player, score):
        client = libsql_client.create_client_sync(
            url=cls.URL,
            auth_token=cls.TOKEN
        )
        with client:
            try:
                stmnts = [_sql.insert_leaderboard_value(gamename, player, score)]
                libsql_stmnts = _sql.libsql_batch(stmnts)
                rss = client.batch(libsql_stmnts)
            except libsql_client.client.LibsqlError:
                pass

    @classmethod
    def info(cls, kv_dict):
        client = libsql_client.create_client_sync(
            url=cls.URL,
            auth_token=cls.TOKEN
        )
        with client:
            try:
                stmnts = []
                for key, value in kv_dict.items():
                    stmnts.append(_sql.insert_kv(key, value))
                libsql_stmnts = _sql.libsql_batch(stmnts)
                rss = client.batch(libsql_stmnts)
            except libsql_client.client.LibsqlError as e:
                raise e

    @classmethod
    def namedinfo(cls, namespace, kv_dict):
        client = libsql_client.create_client_sync(
            url=cls.URL,
            auth_token=cls.TOKEN
        )
        with client:
            try:
                stmnts = []
                for key, value in kv_dict.items():
                    stmnts.append(_sql.insert_kv(key, value, namespace=namespace))
                libsql_stmnts = _sql.libsql_batch(stmnts)
                rss = client.batch(libsql_stmnts)
            except libsql_client.client.LibsqlError:
                pass

    @classmethod
    def counter(cls, counter_key):
        def actual_decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                client = libsql_client.create_client_sync(
                    url=cls.URL,
                    auth_token=cls.TOKEN
                )
                with client:
                    try:
                        stmnts = [_sql.increase_counter(counter_key, 1, namespace='default')]
                        libsql_stmnts = _sql.libsql_batch(stmnts)
                        rss = client.batch(libsql_stmnts)
                    except libsql_client.client.LibsqlError as e:
                        print(e)
                return func(*args, **kwargs)
            return wrapper
        return actual_decorator
