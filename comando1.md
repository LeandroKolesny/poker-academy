root@poker-academy-server:~/poker-academy# docker logs poker_backend
[2025-07-03 07:23:59 +0000] [1] [INFO] Starting gunicorn 23.0.0
[2025-07-03 07:23:59 +0000] [1] [INFO] Listening at: http://0.0.0.0:5000 (1)
[2025-07-03 07:23:59 +0000] [1] [INFO] Using worker: sync
[2025-07-03 07:23:59 +0000] [6] [INFO] Booting worker with pid: 6
[2025-07-03 07:23:59 +0000] [7] [INFO] Booting worker with pid: 7
[2025-07-03 07:23:59 +0000] [8] [INFO] Booting worker with pid: 8
[2025-07-03 07:23:59 +0000] [9] [INFO] Booting worker with pid: 9
Pasta de upload: /app/uploads/videosPasta de upload: /app/uploads/videosPasta de upload: /app/uploads/videos

'FLASK_ENV' is deprecated and will not be used in Flask 2.3. Use 'FLASK_DEBUG' instead.'FLASK_ENV' is deprecated and will not be used in Flask 2.3. Use 'FLASK_DEBUG' instead.


'FLASK_ENV' is deprecated and will not be used in Flask 2.3. Use 'FLASK_DEBUG' instead.
Pasta de upload: /app/uploads/videos
'FLASK_ENV' is deprecated and will not be used in Flask 2.3. Use 'FLASK_DEBUG' instead.
🔐 Tentativa de login: admin@pokeracademy.com
[2025-07-03 07:24:46,693] ERROR in auth_routes: Erro no login: (pymysql.err.OperationalError) (2003, "Can't connect to MySQL server on 'Sql159357@mysql' ([Errno -2] Name or service not known)")
(Background on this error at: https://sqlalche.me/e/14/e3q8)
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/pymysql/connections.py", line 613, in connect
    sock = socket.create_connection(
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/socket.py", line 839, in create_connection
    for res in getaddrinfo(host, port, 0, SOCK_STREAM):
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/socket.py", line 974, in getaddrinfo
    for res in _socket.getaddrinfo(host, port, family, type, proto, flags):
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
socket.gaierror: [Errno -2] Name or service not known

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3280, in _wrap_pool_connect
    return fn()
           ^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 310, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 868, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 476, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 145, in _do_get
    with util.safe_reraise():
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 70, in __exit__
    compat.raise_(
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/util/compat.py", line 208, in raise_
    raise exception
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 143, in _do_get
    return self._create_connection()
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 256, in _create_connection
    return _ConnectionRecord(self)
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 371, in __init__
    self.__connect()
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 665, in __connect
    with util.safe_reraise():
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 70, in __exit__
    compat.raise_(
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/util/compat.py", line 208, in raise_
    raise exception
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 661, in __connect
    self.dbapi_connection = connection = pool._invoke_creator(self)
                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 590, in connect
    return dialect.connect(*cargs, **cparams)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 597, in connect
    return self.dbapi.connect(*cargs, **cparams)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/pymysql/connections.py", line 353, in __init__
    self.connect()
  File "/usr/local/lib/python3.11/site-packages/pymysql/connections.py", line 664, in connect
    raise exc
pymysql.err.OperationalError: (2003, "Can't connect to MySQL server on 'Sql159357@mysql' ([Errno -2] Name or service not known)")

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/src/routes/auth_routes.py", line 32, in login
    user = AuthService.authenticate_user(username_or_email, password)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/src/auth.py", line 46, in authenticate_user
    user = Users.query.filter_by(username=username_or_email).first()
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/query.py", line 2819, in first
    return self.limit(1)._iter().first()
           ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/query.py", line 2903, in _iter
    result = self.session.execute(
             ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 1711, in execute
    conn = self._connection_for_bind(bind)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 1552, in _connection_for_bind
    return self._transaction._connection_for_bind(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 747, in _connection_for_bind
    conn = bind.connect()
           ^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3234, in connect
    return self._connection_cls(self, close_with_result=close_with_result)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 96, in __init__
    else engine.raw_connection()
         ^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3313, in raw_connection
    return self._wrap_pool_connect(self.pool.connect, _connection)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3283, in _wrap_pool_connect
    Connection._handle_dbapi_exception_noconnection(
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 2117, in _handle_dbapi_exception_noconnection
    util.raise_(
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/util/compat.py", line 208, in raise_
    raise exception
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3280, in _wrap_pool_connect
    return fn()
           ^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 310, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 868, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 476, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 145, in _do_get
    with util.safe_reraise():
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 70, in __exit__
    compat.raise_(
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/util/compat.py", line 208, in raise_
    raise exception
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 143, in _do_get
    return self._create_connection()
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 256, in _create_connection
    return _ConnectionRecord(self)
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 371, in __init__
    self.__connect()
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 665, in __connect
    with util.safe_reraise():
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 70, in __exit__
    compat.raise_(
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/util/compat.py", line 208, in raise_
    raise exception
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 661, in __connect
    self.dbapi_connection = connection = pool._invoke_creator(self)
                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 590, in connect
    return dialect.connect(*cargs, **cparams)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 597, in connect
    return self.dbapi.connect(*cargs, **cparams)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/pymysql/connections.py", line 353, in __init__
    self.connect()
  File "/usr/local/lib/python3.11/site-packages/pymysql/connections.py", line 664, in connect
    raise exc
sqlalchemy.exc.OperationalError: (pymysql.err.OperationalError) (2003, "Can't connect to MySQL server on 'Sql159357@mysql' ([Errno -2] Name or service not known)")
(Background on this error at: https://sqlalche.me/e/14/e3q8)
172.18.0.4 - - [03/Jul/2025:07:24:46 +0000] "POST /api/auth/login HTTP/1.1" 500 37 "-" "curl/7.81.0"
[2025-07-03 07:28:51 +0000] [1] [INFO] Handling signal: term
[2025-07-03 07:28:51 +0000] [6] [INFO] Worker exiting (pid: 6)
[2025-07-03 07:28:51 +0000] [7] [INFO] Worker exiting (pid: 7)
[2025-07-03 07:28:51 +0000] [8] [INFO] Worker exiting (pid: 8)
[2025-07-03 07:28:51 +0000] [9] [INFO] Worker exiting (pid: 9)
[2025-07-03 07:28:52 +0000] [1] [INFO] Shutting down: Master
[2025-07-03 07:28:54 +0000] [1] [INFO] Starting gunicorn 23.0.0
[2025-07-03 07:28:54 +0000] [1] [INFO] Listening at: http://0.0.0.0:5000 (1)
[2025-07-03 07:28:54 +0000] [1] [INFO] Using worker: sync
[2025-07-03 07:28:54 +0000] [6] [INFO] Booting worker with pid: 6
[2025-07-03 07:28:54 +0000] [7] [INFO] Booting worker with pid: 7
[2025-07-03 07:28:54 +0000] [8] [INFO] Booting worker with pid: 8
[2025-07-03 07:28:54 +0000] [9] [INFO] Booting worker with pid: 9
Pasta de upload: /app/uploads/videos
'FLASK_ENV' is deprecated and will not be used in Flask 2.3. Use 'FLASK_DEBUG' instead.
Pasta de upload: /app/uploads/videos
'FLASK_ENV' is deprecated and will not be used in Flask 2.3. Use 'FLASK_DEBUG' instead.
Pasta de upload: /app/uploads/videos
'FLASK_ENV' is deprecated and will not be used in Flask 2.3. Use 'FLASK_DEBUG' instead.
Pasta de upload: /app/uploads/videos
'FLASK_ENV' is deprecated and will not be used in Flask 2.3. Use 'FLASK_DEBUG' instead.
[2025-07-03 07:31:47 +0000] [1] [INFO] Handling signal: term
[2025-07-03 07:31:47 +0000] [6] [INFO] Worker exiting (pid: 6)
[2025-07-03 07:31:47 +0000] [7] [INFO] Worker exiting (pid: 7)
[2025-07-03 07:31:47 +0000] [8] [INFO] Worker exiting (pid: 8)
[2025-07-03 07:31:47 +0000] [9] [INFO] Worker exiting (pid: 9)
[2025-07-03 07:31:48 +0000] [1] [INFO] Shutting down: Master
[2025-07-03 07:31:49 +0000] [1] [INFO] Starting gunicorn 23.0.0
[2025-07-03 07:31:49 +0000] [1] [INFO] Listening at: http://0.0.0.0:5000 (1)
[2025-07-03 07:31:49 +0000] [1] [INFO] Using worker: sync
[2025-07-03 07:31:49 +0000] [6] [INFO] Booting worker with pid: 6
[2025-07-03 07:31:50 +0000] [7] [INFO] Booting worker with pid: 7
[2025-07-03 07:31:50 +0000] [8] [INFO] Booting worker with pid: 8
[2025-07-03 07:31:50 +0000] [9] [INFO] Booting worker with pid: 9
Pasta de upload: /app/uploads/videos
'FLASK_ENV' is deprecated and will not be used in Flask 2.3. Use 'FLASK_DEBUG' instead.
Pasta de upload: /app/uploads/videos
'FLASK_ENV' is deprecated and will not be used in Flask 2.3. Use 'FLASK_DEBUG' instead.
Pasta de upload: /app/uploads/videos
'FLASK_ENV' is deprecated and will not be used in Flask 2.3. Use 'FLASK_DEBUG' instead.
Pasta de upload: /app/uploads/videos
'FLASK_ENV' is deprecated and will not be used in Flask 2.3. Use 'FLASK_DEBUG' instead.
🔐 Tentativa de login: admin@pokeracademy.com
✅ Login bem-sucedido: admin (Administrador)
172.18.0.4 - - [03/Jul/2025:07:32:42 +0000] "POST /api/auth/login HTTP/1.1" 200 346 "-" "curl/7.81.0"
🔐 Tentativa de login: admin@pokeracademy.com
✅ Login bem-sucedido: admin (Administrador)
172.18.0.4 - - [03/Jul/2025:07:58:45 +0000] "POST /api/auth/login HTTP/1.1" 200 346 "-" "curl/7.81.0"
172.18.0.4 - - [03/Jul/2025:08:29:03 +0000] "HEAD /api/auth/login HTTP/1.1" 405 0 "-" "curl/7.81.0"
🔐 Tentativa de login: admin@pokeracademy.com
✅ Login bem-sucedido: admin (Administrador)
172.18.0.4 - - [03/Jul/2025:08:31:54 +0000] "POST /api/auth/login HTTP/1.1" 200 346 "-" "curl/7.81.0"
🔐 Tentativa de login: admin@pokeracademy.com
✅ Login bem-sucedido: admin (Administrador)
172.18.0.4 - - [03/Jul/2025:08:51:31 +0000] "POST /api/auth/login HTTP/1.1" 200 346 "-" "curl/8.14.1"
172.18.0.4 - - [03/Jul/2025:08:51:49 +0000] "GET /api/auth/login HTTP/1.1" 405 153 "-" "curl/8.14.1"
🔐 Tentativa de login: admin@pokeracademy.com
✅ Login bem-sucedido: admin (Administrador)
172.18.0.4 - - [03/Jul/2025:09:38:34 +0000] "POST /api/auth/login HTTP/1.1" 200 346 "-" "curl/7.81.0"
172.18.0.4 - - [03/Jul/2025:09:39:50 +0000] "POST /api/api/auth/login HTTP/1.1" 404 207 "http://142.93.206.128/login" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:09:40:02 +0000] "POST /api/api/auth/login HTTP/1.1" 404 207 "http://142.93.206.128/login" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:09:48:16 +0000] "POST /api/api/auth/login HTTP/1.1" 404 207 "http://142.93.206.128/login" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:09:56:41 +0000] "POST /api/api/auth/login HTTP/1.1" 404 207 "http://142.93.206.128/login" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:09:57:09 +0000] "POST /api/api/auth/login HTTP/1.1" 404 207 "http://142.93.206.128/login" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:10:03:54 +0000] "POST /api/api/auth/login HTTP/1.1" 404 207 "http://142.93.206.128/login" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:10:04:19 +0000] "POST /api/api/auth/login HTTP/1.1" 404 207 "http://142.93.206.128/login" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
🔐 Tentativa de login: admin@pokeracademy.com
✅ Login bem-sucedido: admin (Administrador)
172.18.0.4 - - [03/Jul/2025:10:12:07 +0000] "POST /api/auth/login HTTP/1.1" 200 346 "-" "curl/7.81.0"
🔐 Tentativa de login: admin
✅ Login bem-sucedido: admin (Administrador)
172.18.0.4 - - [03/Jul/2025:10:12:27 +0000] "POST /api/auth/login HTTP/1.1" 200 346 "http://142.93.206.128/login" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:10:12:27 +0000] "GET /api/api/analytics/stats HTTP/1.1" 404 207 "http://142.93.206.128/admin/analytics" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:10:13:27 +0000] "GET /api/api/users HTTP/1.1" 404 207 "http://142.93.206.128/admin/students" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:10:13:29 +0000] "GET /api/api/classes HTTP/1.1" 404 207 "http://142.93.206.128/admin/classes" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:10:13:29 +0000] "GET /api/api/instructors HTTP/1.1" 404 207 "http://142.93.206.128/admin/classes" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:10:13:31 +0000] "GET /api/api/analytics/stats HTTP/1.1" 404 207 "http://142.93.206.128/admin/analytics" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
🔐 Tentativa de login: admin
✅ Login bem-sucedido: admin (Administrador)
172.18.0.4 - - [03/Jul/2025:10:22:05 +0000] "POST /api/auth/login HTTP/1.1" 200 346 "http://142.93.206.128/login" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
[2025-07-03 10:22:05,889] ERROR in class_routes: Erro ao buscar estatísticas: (pymysql.err.ProgrammingError) (1146, "Table 'poker_academy.classes' doesn't exist")
[SQL: SELECT count(*) AS count_1 
FROM (SELECT classes.id AS classes_id, classes.name AS classes_name, classes.instructor AS classes_instructor, classes.date AS classes_date, classes.category AS classes_category, classes.video_type AS classes_video_type, classes.video_path AS classes_video_path, classes.priority AS classes_priority, classes.views AS classes_views, classes.created_at AS classes_created_at 
FROM classes) AS anon_1]
(Background on this error at: https://sqlalche.me/e/14/f405)
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1819, in _execute_context
    self.dialect.do_execute(
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 732, in do_execute
    cursor.execute(statement, parameters)
  File "/usr/local/lib/python3.11/site-packages/pymysql/cursors.py", line 148, in execute
    result = self._query(query)
             ^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/pymysql/cursors.py", line 310, in _query
    conn.query(q)
  File "/usr/local/lib/python3.11/site-packages/pymysql/connections.py", line 548, in query
    self._affected_rows = self._read_query_result(unbuffered=unbuffered)
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/pymysql/connections.py", line 775, in _read_query_result
    result.read()
  File "/usr/local/lib/python3.11/site-packages/pymysql/connections.py", line 1156, in read
    first_packet = self.connection._read_packet()
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/pymysql/connections.py", line 725, in _read_packet
    packet.raise_for_error()
  File "/usr/local/lib/python3.11/site-packages/pymysql/protocol.py", line 221, in raise_for_error
    err.raise_mysql_exception(self._data)
  File "/usr/local/lib/python3.11/site-packages/pymysql/err.py", line 143, in raise_mysql_exception
    raise errorclass(errno, errval)
pymysql.err.ProgrammingError: (1146, "Table 'poker_academy.classes' doesn't exist")

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/src/routes/class_routes.py", line 391, in get_analytics_stats
    total_classes = Classes.query.count()
                    ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/query.py", line 3163, in count
    return self._from_self(col).enable_eagerloads(False).scalar()
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/query.py", line 2888, in scalar
    ret = self.one()
          ^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/query.py", line 2865, in one
    return self._iter().one()
           ^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/query.py", line 2903, in _iter
    result = self.session.execute(
             ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 1712, in execute
    result = conn._execute_20(statement, params or {}, execution_options)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1631, in _execute_20
    return meth(self, args_10style, kwargs_10style, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/sql/elements.py", line 332, in _execute_on_connection
    return connection._execute_clauseelement(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1498, in _execute_clauseelement
    ret = self._execute_context(
          ^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1862, in _execute_context
    self._handle_dbapi_exception(
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 2043, in _handle_dbapi_exception
    util.raise_(
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/util/compat.py", line 208, in raise_
    raise exception
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1819, in _execute_context
    self.dialect.do_execute(
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 732, in do_execute
    cursor.execute(statement, parameters)
  File "/usr/local/lib/python3.11/site-packages/pymysql/cursors.py", line 148, in execute
    result = self._query(query)
             ^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/pymysql/cursors.py", line 310, in _query
    conn.query(q)
  File "/usr/local/lib/python3.11/site-packages/pymysql/connections.py", line 548, in query
    self._affected_rows = self._read_query_result(unbuffered=unbuffered)
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/pymysql/connections.py", line 775, in _read_query_result
    result.read()
  File "/usr/local/lib/python3.11/site-packages/pymysql/connections.py", line 1156, in read
    first_packet = self.connection._read_packet()
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/pymysql/connections.py", line 725, in _read_packet
    packet.raise_for_error()
  File "/usr/local/lib/python3.11/site-packages/pymysql/protocol.py", line 221, in raise_for_error
    err.raise_mysql_exception(self._data)
  File "/usr/local/lib/python3.11/site-packages/pymysql/err.py", line 143, in raise_mysql_exception
    raise errorclass(errno, errval)
sqlalchemy.exc.ProgrammingError: (pymysql.err.ProgrammingError) (1146, "Table 'poker_academy.classes' doesn't exist")
[SQL: SELECT count(*) AS count_1 
FROM (SELECT classes.id AS classes_id, classes.name AS classes_name, classes.instructor AS classes_instructor, classes.date AS classes_date, classes.category AS classes_category, classes.video_type AS classes_video_type, classes.video_path AS classes_video_path, classes.priority AS classes_priority, classes.views AS classes_views, classes.created_at AS classes_created_at 
FROM classes) AS anon_1]
(Background on this error at: https://sqlalche.me/e/14/f405)
172.18.0.4 - - [03/Jul/2025:10:22:05 +0000] "GET /api/analytics/stats HTTP/1.1" 500 45 "http://142.93.206.128/admin/analytics" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:10:24:23 +0000] "GET /api/analytics/stats HTTP/1.1" 401 29 "-" "curl/7.81.0"
172.18.0.4 - - [03/Jul/2025:10:24:52 +0000] "GET /api/auth/verify HTTP/1.1" 200 137 "http://142.93.206.128/admin/analytics" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
[2025-07-03 10:24:52,920] ERROR in class_routes: Erro ao buscar estatísticas: (pymysql.err.ProgrammingError) (1146, "Table 'poker_academy.classes' doesn't exist")
[SQL: SELECT count(*) AS count_1 
FROM (SELECT classes.id AS classes_id, classes.name AS classes_name, classes.instructor AS classes_instructor, classes.date AS classes_date, classes.category AS classes_category, classes.video_type AS classes_video_type, classes.video_path AS classes_video_path, classes.priority AS classes_priority, classes.views AS classes_views, classes.created_at AS classes_created_at 
FROM classes) AS anon_1]
(Background on this error at: https://sqlalche.me/e/14/f405)
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1819, in _execute_context
    self.dialect.do_execute(
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 732, in do_execute
    cursor.execute(statement, parameters)
  File "/usr/local/lib/python3.11/site-packages/pymysql/cursors.py", line 148, in execute
    result = self._query(query)
             ^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/pymysql/cursors.py", line 310, in _query
    conn.query(q)
  File "/usr/local/lib/python3.11/site-packages/pymysql/connections.py", line 548, in query
    self._affected_rows = self._read_query_result(unbuffered=unbuffered)
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/pymysql/connections.py", line 775, in _read_query_result
    result.read()
  File "/usr/local/lib/python3.11/site-packages/pymysql/connections.py", line 1156, in read
    first_packet = self.connection._read_packet()
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/pymysql/connections.py", line 725, in _read_packet
    packet.raise_for_error()
  File "/usr/local/lib/python3.11/site-packages/pymysql/protocol.py", line 221, in raise_for_error
    err.raise_mysql_exception(self._data)
  File "/usr/local/lib/python3.11/site-packages/pymysql/err.py", line 143, in raise_mysql_exception
    raise errorclass(errno, errval)
pymysql.err.ProgrammingError: (1146, "Table 'poker_academy.classes' doesn't exist")

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/src/routes/class_routes.py", line 391, in get_analytics_stats
    total_classes = Classes.query.count()
                    ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/query.py", line 3163, in count
    return self._from_self(col).enable_eagerloads(False).scalar()
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/query.py", line 2888, in scalar
    ret = self.one()
          ^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/query.py", line 2865, in one
    return self._iter().one()
           ^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/query.py", line 2903, in _iter
    result = self.session.execute(
             ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 1712, in execute
    result = conn._execute_20(statement, params or {}, execution_options)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1631, in _execute_20
    return meth(self, args_10style, kwargs_10style, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/sql/elements.py", line 332, in _execute_on_connection
    return connection._execute_clauseelement(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1498, in _execute_clauseelement
    ret = self._execute_context(
          ^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1862, in _execute_context
    self._handle_dbapi_exception(
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 2043, in _handle_dbapi_exception
    util.raise_(
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/util/compat.py", line 208, in raise_
    raise exception
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1819, in _execute_context
    self.dialect.do_execute(
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 732, in do_execute
    cursor.execute(statement, parameters)
  File "/usr/local/lib/python3.11/site-packages/pymysql/cursors.py", line 148, in execute
    result = self._query(query)
             ^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/pymysql/cursors.py", line 310, in _query
    conn.query(q)
  File "/usr/local/lib/python3.11/site-packages/pymysql/connections.py", line 548, in query
    self._affected_rows = self._read_query_result(unbuffered=unbuffered)
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/pymysql/connections.py", line 775, in _read_query_result
    result.read()
  File "/usr/local/lib/python3.11/site-packages/pymysql/connections.py", line 1156, in read
    first_packet = self.connection._read_packet()
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/pymysql/connections.py", line 725, in _read_packet
    packet.raise_for_error()
  File "/usr/local/lib/python3.11/site-packages/pymysql/protocol.py", line 221, in raise_for_error
    err.raise_mysql_exception(self._data)
  File "/usr/local/lib/python3.11/site-packages/pymysql/err.py", line 143, in raise_mysql_exception
    raise errorclass(errno, errval)
sqlalchemy.exc.ProgrammingError: (pymysql.err.ProgrammingError) (1146, "Table 'poker_academy.classes' doesn't exist")
[SQL: SELECT count(*) AS count_1 
FROM (SELECT classes.id AS classes_id, classes.name AS classes_name, classes.instructor AS classes_instructor, classes.date AS classes_date, classes.category AS classes_category, classes.video_type AS classes_video_type, classes.video_path AS classes_video_path, classes.priority AS classes_priority, classes.views AS classes_views, classes.created_at AS classes_created_at 
FROM classes) AS anon_1]
(Background on this error at: https://sqlalche.me/e/14/f405)
172.18.0.4 - - [03/Jul/2025:10:24:52 +0000] "GET /api/analytics/stats HTTP/1.1" 500 45 "http://142.93.206.128/admin/analytics" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:10:25:02 +0000] "GET /api/auth/verify HTTP/1.1" 200 137 "http://142.93.206.128/admin/analytics" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
[2025-07-03 10:25:02,169] ERROR in class_routes: Erro ao buscar estatísticas: (pymysql.err.ProgrammingError) (1146, "Table 'poker_academy.classes' doesn't exist")
[SQL: SELECT count(*) AS count_1 
FROM (SELECT classes.id AS classes_id, classes.name AS classes_name, classes.instructor AS classes_instructor, classes.date AS classes_date, classes.category AS classes_category, classes.video_type AS classes_video_type, classes.video_path AS classes_video_path, classes.priority AS classes_priority, classes.views AS classes_views, classes.created_at AS classes_created_at 
FROM classes) AS anon_1]
(Background on this error at: https://sqlalche.me/e/14/f405)
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1819, in _execute_context
    self.dialect.do_execute(
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 732, in do_execute
    cursor.execute(statement, parameters)
  File "/usr/local/lib/python3.11/site-packages/pymysql/cursors.py", line 148, in execute
    result = self._query(query)
             ^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/pymysql/cursors.py", line 310, in _query
    conn.query(q)
  File "/usr/local/lib/python3.11/site-packages/pymysql/connections.py", line 548, in query
    self._affected_rows = self._read_query_result(unbuffered=unbuffered)
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/pymysql/connections.py", line 775, in _read_query_result
    result.read()
  File "/usr/local/lib/python3.11/site-packages/pymysql/connections.py", line 1156, in read
    first_packet = self.connection._read_packet()
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/pymysql/connections.py", line 725, in _read_packet
    packet.raise_for_error()
  File "/usr/local/lib/python3.11/site-packages/pymysql/protocol.py", line 221, in raise_for_error
    err.raise_mysql_exception(self._data)
  File "/usr/local/lib/python3.11/site-packages/pymysql/err.py", line 143, in raise_mysql_exception
    raise errorclass(errno, errval)
pymysql.err.ProgrammingError: (1146, "Table 'poker_academy.classes' doesn't exist")

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/src/routes/class_routes.py", line 391, in get_analytics_stats
    total_classes = Classes.query.count()
                    ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/query.py", line 3163, in count
    return self._from_self(col).enable_eagerloads(False).scalar()
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/query.py", line 2888, in scalar
    ret = self.one()
          ^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/query.py", line 2865, in one
    return self._iter().one()
           ^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/query.py", line 2903, in _iter
    result = self.session.execute(
             ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 1712, in execute
    result = conn._execute_20(statement, params or {}, execution_options)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1631, in _execute_20
    return meth(self, args_10style, kwargs_10style, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/sql/elements.py", line 332, in _execute_on_connection
    return connection._execute_clauseelement(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1498, in _execute_clauseelement
    ret = self._execute_context(
          ^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1862, in _execute_context
    self._handle_dbapi_exception(
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 2043, in _handle_dbapi_exception
    util.raise_(
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/util/compat.py", line 208, in raise_
    raise exception
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1819, in _execute_context
    self.dialect.do_execute(
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 732, in do_execute
    cursor.execute(statement, parameters)
  File "/usr/local/lib/python3.11/site-packages/pymysql/cursors.py", line 148, in execute
    result = self._query(query)
             ^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/pymysql/cursors.py", line 310, in _query
    conn.query(q)
  File "/usr/local/lib/python3.11/site-packages/pymysql/connections.py", line 548, in query
    self._affected_rows = self._read_query_result(unbuffered=unbuffered)
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/pymysql/connections.py", line 775, in _read_query_result
    result.read()
  File "/usr/local/lib/python3.11/site-packages/pymysql/connections.py", line 1156, in read
    first_packet = self.connection._read_packet()
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/pymysql/connections.py", line 725, in _read_packet
    packet.raise_for_error()
  File "/usr/local/lib/python3.11/site-packages/pymysql/protocol.py", line 221, in raise_for_error
    err.raise_mysql_exception(self._data)
  File "/usr/local/lib/python3.11/site-packages/pymysql/err.py", line 143, in raise_mysql_exception
    raise errorclass(errno, errval)
sqlalchemy.exc.ProgrammingError: (pymysql.err.ProgrammingError) (1146, "Table 'poker_academy.classes' doesn't exist")
[SQL: SELECT count(*) AS count_1 
FROM (SELECT classes.id AS classes_id, classes.name AS classes_name, classes.instructor AS classes_instructor, classes.date AS classes_date, classes.category AS classes_category, classes.video_type AS classes_video_type, classes.video_path AS classes_video_path, classes.priority AS classes_priority, classes.views AS classes_views, classes.created_at AS classes_created_at 
FROM classes) AS anon_1]
(Background on this error at: https://sqlalche.me/e/14/f405)
172.18.0.4 - - [03/Jul/2025:10:25:02 +0000] "GET /api/analytics/stats HTTP/1.1" 500 45 "http://142.93.206.128/admin/analytics" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
🔐 Tentativa de login: admin@pokeracademy.com
✅ Login bem-sucedido: admin (Administrador)
172.18.0.4 - - [03/Jul/2025:10:29:01 +0000] "POST /api/auth/login HTTP/1.1" 200 346 "-" "curl/7.81.0"
[2025-07-03 10:29:17,750] ERROR in class_routes: Erro ao buscar estatísticas: (pymysql.err.ProgrammingError) (1146, "Table 'poker_academy.classes' doesn't exist")
[SQL: SELECT count(*) AS count_1 
FROM (SELECT classes.id AS classes_id, classes.name AS classes_name, classes.instructor AS classes_instructor, classes.date AS classes_date, classes.category AS classes_category, classes.video_type AS classes_video_type, classes.video_path AS classes_video_path, classes.priority AS classes_priority, classes.views AS classes_views, classes.created_at AS classes_created_at 
FROM classes) AS anon_1]
(Background on this error at: https://sqlalche.me/e/14/f405)
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1819, in _execute_context
    self.dialect.do_execute(
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 732, in do_execute
    cursor.execute(statement, parameters)
  File "/usr/local/lib/python3.11/site-packages/pymysql/cursors.py", line 148, in execute
    result = self._query(query)
             ^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/pymysql/cursors.py", line 310, in _query
    conn.query(q)
  File "/usr/local/lib/python3.11/site-packages/pymysql/connections.py", line 548, in query
    self._affected_rows = self._read_query_result(unbuffered=unbuffered)
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/pymysql/connections.py", line 775, in _read_query_result
    result.read()
  File "/usr/local/lib/python3.11/site-packages/pymysql/connections.py", line 1156, in read
    first_packet = self.connection._read_packet()
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/pymysql/connections.py", line 725, in _read_packet
    packet.raise_for_error()
  File "/usr/local/lib/python3.11/site-packages/pymysql/protocol.py", line 221, in raise_for_error
    err.raise_mysql_exception(self._data)
  File "/usr/local/lib/python3.11/site-packages/pymysql/err.py", line 143, in raise_mysql_exception
    raise errorclass(errno, errval)
pymysql.err.ProgrammingError: (1146, "Table 'poker_academy.classes' doesn't exist")

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/src/routes/class_routes.py", line 391, in get_analytics_stats
    total_classes = Classes.query.count()
                    ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/query.py", line 3163, in count
    return self._from_self(col).enable_eagerloads(False).scalar()
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/query.py", line 2888, in scalar
    ret = self.one()
          ^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/query.py", line 2865, in one
    return self._iter().one()
           ^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/query.py", line 2903, in _iter
    result = self.session.execute(
             ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 1712, in execute
    result = conn._execute_20(statement, params or {}, execution_options)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1631, in _execute_20
    return meth(self, args_10style, kwargs_10style, execution_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/sql/elements.py", line 332, in _execute_on_connection
    return connection._execute_clauseelement(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1498, in _execute_clauseelement
    ret = self._execute_context(
          ^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1862, in _execute_context
    self._handle_dbapi_exception(
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 2043, in _handle_dbapi_exception
    util.raise_(
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/util/compat.py", line 208, in raise_
    raise exception
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1819, in _execute_context
    self.dialect.do_execute(
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 732, in do_execute
    cursor.execute(statement, parameters)
  File "/usr/local/lib/python3.11/site-packages/pymysql/cursors.py", line 148, in execute
    result = self._query(query)
             ^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/pymysql/cursors.py", line 310, in _query
    conn.query(q)
  File "/usr/local/lib/python3.11/site-packages/pymysql/connections.py", line 548, in query
    self._affected_rows = self._read_query_result(unbuffered=unbuffered)
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/pymysql/connections.py", line 775, in _read_query_result
    result.read()
  File "/usr/local/lib/python3.11/site-packages/pymysql/connections.py", line 1156, in read
    first_packet = self.connection._read_packet()
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/pymysql/connections.py", line 725, in _read_packet
    packet.raise_for_error()
  File "/usr/local/lib/python3.11/site-packages/pymysql/protocol.py", line 221, in raise_for_error
    err.raise_mysql_exception(self._data)
  File "/usr/local/lib/python3.11/site-packages/pymysql/err.py", line 143, in raise_mysql_exception
    raise errorclass(errno, errval)
sqlalchemy.exc.ProgrammingError: (pymysql.err.ProgrammingError) (1146, "Table 'poker_academy.classes' doesn't exist")
[SQL: SELECT count(*) AS count_1 
FROM (SELECT classes.id AS classes_id, classes.name AS classes_name, classes.instructor AS classes_instructor, classes.date AS classes_date, classes.category AS classes_category, classes.video_type AS classes_video_type, classes.video_path AS classes_video_path, classes.priority AS classes_priority, classes.views AS classes_views, classes.created_at AS classes_created_at 
FROM classes) AS anon_1]
(Background on this error at: https://sqlalche.me/e/14/f405)
172.18.0.4 - - [03/Jul/2025:10:29:17 +0000] "GET /api/analytics/stats HTTP/1.1" 500 45 "-" "curl/7.81.0"
172.18.0.4 - - [03/Jul/2025:11:14:05 +0000] "GET /api/auth/verify HTTP/1.1" 200 137 "http://142.93.206.128/admin/analytics" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:11:14:05 +0000] "GET /api/analytics/stats HTTP/1.1" 200 163 "http://142.93.206.128/admin/analytics" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
🔍 Buscando aulas...
📊 Total de aulas: 0
✅ Retornando 0 aulas
172.18.0.4 - - [03/Jul/2025:11:14:07 +0000] "GET /api/classes HTTP/1.1" 200 3 "http://142.93.206.128/admin/classes" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:11:14:07 +0000] "GET /api/instructors HTTP/1.1" 200 67 "http://142.93.206.128/admin/classes" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:11:14:10 +0000] "GET /api/users HTTP/1.1" 200 196 "http://142.93.206.128/admin/students" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:11:14:14 +0000] "GET /api/instructors HTTP/1.1" 200 67 "http://142.93.206.128/admin/classes" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
🔍 Buscando aulas...
📊 Total de aulas: 0
✅ Retornando 0 aulas
172.18.0.4 - - [03/Jul/2025:11:14:14 +0000] "GET /api/classes HTTP/1.1" 200 3 "http://142.93.206.128/admin/classes" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:11:14:35 +0000] "GET /api/auth/verify HTTP/1.1" 200 137 "http://142.93.206.128/admin/analytics" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:11:14:36 +0000] "GET /api/analytics/stats HTTP/1.1" 200 163 "http://142.93.206.128/admin/analytics" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:11:17:54 +0000] "GET /api/auth/verify HTTP/1.1" 200 137 "http://142.93.206.128/admin/classes" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
🔍 Buscando aulas...
📊 Total de aulas: 0
✅ Retornando 0 aulas
172.18.0.4 - - [03/Jul/2025:11:17:54 +0000] "GET /api/instructors HTTP/1.1" 200 67 "http://142.93.206.128/admin/classes" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:11:17:54 +0000] "GET /api/classes HTTP/1.1" 200 3 "http://142.93.206.128/admin/classes" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:11:17:56 +0000] "GET /api/users HTTP/1.1" 200 196 "http://142.93.206.128/admin/students" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:11:18:04 +0000] "GET /api/auth/verify HTTP/1.1" 200 137 "http://142.93.206.128/admin/students" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:11:18:04 +0000] "GET /api/users HTTP/1.1" 200 196 "http://142.93.206.128/admin/students" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:11:19:03 +0000] "GET /api/auth/verify HTTP/1.1" 200 137 "http://142.93.206.128/admin/students" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:11:19:03 +0000] "GET /api/users HTTP/1.1" 200 196 "http://142.93.206.128/admin/students" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:11:25:53 +0000] "GET /api/auth/verify HTTP/1.1" 200 137 "http://142.93.206.128/admin/students" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:11:25:53 +0000] "GET /api/users HTTP/1.1" 200 196 "http://142.93.206.128/admin/students" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
🔍 Buscando aulas...
📊 Total de aulas: 0
✅ Retornando 0 aulas
172.18.0.4 - - [03/Jul/2025:11:25:54 +0000] "GET /api/instructors HTTP/1.1" 200 67 "http://142.93.206.128/admin/classes" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:11:25:54 +0000] "GET /api/classes HTTP/1.1" 200 3 "http://142.93.206.128/admin/classes" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:11:25:59 +0000] "GET /api/auth/verify HTTP/1.1" 200 137 "http://142.93.206.128/admin/classes" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
🔍 Buscando aulas...
📊 Total de aulas: 0
✅ Retornando 0 aulas
172.18.0.4 - - [03/Jul/2025:11:25:59 +0000] "GET /api/instructors HTTP/1.1" 200 67 "http://142.93.206.128/admin/classes" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:11:25:59 +0000] "GET /api/classes HTTP/1.1" 200 3 "http://142.93.206.128/admin/classes" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:11:56:37 +0000] "GET /api/auth/verify HTTP/1.1" 200 137 "http://142.93.206.128/admin/classes" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
🔍 Buscando aulas...
📊 Total de aulas: 0
✅ Retornando 0 aulas
172.18.0.4 - - [03/Jul/2025:11:56:37 +0000] "GET /api/classes HTTP/1.1" 200 3 "http://142.93.206.128/admin/classes" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:11:56:37 +0000] "GET /api/instructors HTTP/1.1" 200 67 "http://142.93.206.128/admin/classes" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:11:56:43 +0000] "GET /api/users HTTP/1.1" 200 196 "http://142.93.206.128/admin/students" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:12:21:13 +0000] "GET /api/auth/verify HTTP/1.1" 200 137 "http://142.93.206.128/admin/students" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:12:21:13 +0000] "GET /api/users HTTP/1.1" 200 196 "http://142.93.206.128/admin/students" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
🔍 Buscando aulas...
📊 Total de aulas: 0
✅ Retornando 0 aulas
172.18.0.4 - - [03/Jul/2025:12:21:18 +0000] "GET /api/classes HTTP/1.1" 200 3 "http://142.93.206.128/admin/classes" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:12:21:18 +0000] "GET /api/instructors HTTP/1.1" 200 67 "http://142.93.206.128/admin/classes" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:12:21:19 +0000] "GET /api/analytics/stats HTTP/1.1" 200 163 "http://142.93.206.128/admin/analytics" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:12:21:25 +0000] "GET /api/users HTTP/1.1" 200 196 "http://142.93.206.128/admin/students" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
🔐 Tentativa de login: admin123
❌ Login falhou para: admin123
172.18.0.4 - - [03/Jul/2025:12:22:21 +0000] "POST /api/auth/login HTTP/1.1" 401 51 "http://142.93.206.128/login" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
🔐 Tentativa de login: admin@pokeracademy.com
✅ Login bem-sucedido: admin (Administrador)
172.18.0.4 - - [03/Jul/2025:12:22:38 +0000] "POST /api/auth/login HTTP/1.1" 200 346 "http://142.93.206.128/login" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:12:22:38 +0000] "GET /api/analytics/stats HTTP/1.1" 200 163 "http://142.93.206.128/admin/analytics" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:12:22:54 +0000] "GET /api/users HTTP/1.1" 200 196 "http://142.93.206.128/admin/students" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:12:23:10 +0000] "GET /api/analytics/stats HTTP/1.1" 200 163 "http://142.93.206.128/admin/analytics" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
🔐 Tentativa de login: admin@pokeracademy.com
✅ Login bem-sucedido: admin (Administrador)
172.18.0.4 - - [03/Jul/2025:12:23:16 +0000] "POST /api/auth/login HTTP/1.1" 200 346 "http://142.93.206.128/login" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:12:23:16 +0000] "GET /api/analytics/stats HTTP/1.1" 200 163 "http://142.93.206.128/admin/analytics" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:12:25:21 +0000] "GET /api/users HTTP/1.1" 200 196 "http://142.93.206.128/admin/students" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
🔍 Buscando aulas...
📊 Total de aulas: 0
✅ Retornando 0 aulas
172.18.0.4 - - [03/Jul/2025:12:26:29 +0000] "GET /api/classes HTTP/1.1" 200 3 "http://142.93.206.128/admin/classes" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:12:26:29 +0000] "GET /api/instructors HTTP/1.1" 200 67 "http://142.93.206.128/admin/classes" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
🔍 Buscando aulas...
📊 Total de aulas: 0
✅ Retornando 0 aulas
172.18.0.4 - - [03/Jul/2025:12:27:42 +0000] "GET /api/classes HTTP/1.1" 200 3 "http://142.93.206.128/admin/classes" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:12:27:42 +0000] "GET /api/instructors HTTP/1.1" 200 67 "http://142.93.206.128/admin/classes" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:12:33:20 +0000] "GET /api/analytics/stats HTTP/1.1" 200 163 "http://142.93.206.128/admin/analytics" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:13:00:53 +0000] "GET /api/auth/verify HTTP/1.1" 200 137 "http://142.93.206.128/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:13:00:53 +0000] "GET /api/analytics/stats HTTP/1.1" 200 163 "http://142.93.206.128/admin/analytics" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
172.18.0.4 - - [03/Jul/2025:13:00:55 +0000] "GET /api/users HTTP/1.1" 200 196 "http://142.93.206.128/admin/students" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
root@poker-academy-server:~/poker-academy# docker exec -it poker_mysql mysql -u poker_user -p poker_academy
Enter password: 
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 719
Server version: 8.0.42 MySQL Community Server - GPL

Copyright (c) 2000, 2025, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> SHOW TABLES;
+-------------------------+
| Tables_in_poker_academy |
+-------------------------+
| classes                 |
| favorites               |
| particoes               |
| playlist_classes        |
| playlists               |
| user_progress           |
| users                   |
+-------------------------+
7 rows in set (0.00 sec)

mysql> SELECT * FROM particoes;
+----+------+------------------------------+-------+---------------------+---------------------+
| id | nome | descricao                    | ativa | created_at          | updated_at          |
+----+------+------------------------------+-------+---------------------+---------------------+
|  1 | Dojo | Partição principal do Dojo |     1 | 2025-07-02 17:57:06 | 2025-07-02 17:57:06 |
|  2 | Coco | Partição secundária Coco  |     1 | 2025-07-02 17:57:06 | 2025-07-02 17:57:06 |
+----+------+------------------------------+-------+---------------------+---------------------+
2 rows in set (0.00 sec)