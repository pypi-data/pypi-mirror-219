import os
import random
import re
import socket
import ssl
import time
import urllib.parse
import urllib.request
from ftplib import FTP, FTP_TLS
from subprocess import run
from TheSilent.return_user_agent import return_user_agent
from TheSilent.clear import clear

verify = ssl.create_default_context()
verify.check_hostname = False
verify.verify_mode = ssl.CERT_NONE

RED = "\033[1;31m"
CYAN = "\033[1;36m"
GREEN = "\033[0;32m"

sql_errors = ["SQL syntax.*?MySQL",
        "Warning.*?\\Wmysqli?_",
        "MySQLSyntaxErrorException",
        "valid MySQL result",
        "check the manual that (corresponds to|fits) your MySQL server version",
        "check the manual that (corresponds to|fits) your MariaDB server version",
        "check the manual that (corresponds to|fits) your Drizzle server version",
        "Unknown column '[^ ]+' in 'field list'",
        "MySqlClient\\.",
        "com\\.mysql\\.jdbc",
        "Zend_Db_(Adapter|Statement)_Mysqli_Exception",
        "Pdo\\[./_\\]Mysql",
        "MySqlException",
        "SQLSTATE\\[\\d+\\]: Syntax error or access violation",
        "MemSQL does not support this type of query",
        "is not supported by MemSQL",
        "unsupported nested scalar subselect",
        "PostgreSQL.*?ERROR",
        "Warning.*?\\Wpg_",
        "valid PostgreSQL result",
        "Npgsql\\.",
        "PG::SyntaxError:",
        "org\\.postgresql\\.util\\.PSQLException",
        "ERROR:\\s\\ssyntax error at or near",
        "ERROR: parser: parse error at or near",
        "PostgreSQL query failed",
        "org\\.postgresql\\.jdbc",
        "Pdo\\[./_\\]Pgsql",
        "PSQLException",
        "OLE DB.*? SQL Server",
        "\bSQL Server[^&lt;&quot;]+Driver",
        "Warning.*?\\W(mssql|sqlsrv)_",
        "\bSQL Server[^&lt;&quot;]+[0-9a-fA-F]{8}",
        "System\\.Data\\.SqlClient\\.(SqlException|SqlConnection\\.OnError)",
        "(?s)Exception.*?\bRoadhouse\\.Cms\\.",
        "Microsoft SQL Native Client error '[0-9a-fA-F]{8}",
        "\\[SQL Server\\]",
        "ODBC SQL Server Driver",
        "ODBC Driver \\d+ for SQL Server",
        "SQLServer JDBC Driver",
        "com\\.jnetdirect\\.jsql",
        "macromedia\\.jdbc\\.sqlserver",
        "Zend_Db_(Adapter|Statement)_Sqlsrv_Exception",
        "com\\.microsoft\\.sqlserver\\.jdbc",
        "Pdo\\[./_\\](Mssql|SqlSrv)",
        "SQL(Srv|Server)Exception",
        "Unclosed quotation mark after the character string",
        "Microsoft Access (\\d+ )?Driver",
        "JET Database Engine",
        "Access Database Engine",
        "ODBC Microsoft Access",
        "Syntax error \\(missing operator\\) in query expression",
        "\bORA-\\d{5}",
        "Oracle error",
        "Oracle.*?Driver",
        "Warning.*?\\W(oci|ora)_",
        "quoted string not properly terminated",
        "SQL command not properly ended",
        "macromedia\\.jdbc\\.oracle",
        "oracle\\.jdbc",
        "Zend_Db_(Adapter|Statement)_Oracle_Exception",
        "Pdo\\[./_\\](Oracle|OCI)",
        "OracleException",
        "CLI Driver.*?DB2",
        "DB2 SQL error",
        "\bdb2_\\w+\\(",
        "SQLCODE[=:\\d, -]+SQLSTATE",
        "com\\.ibm\\.db2\\.jcc",
        "Zend_Db_(Adapter|Statement)_Db2_Exception",
        "Pdo\\[./_\\]Ibm",
        "DB2Exception",
        "ibm_db_dbi\\.ProgrammingError",
        "Warning.*?\\Wifx_",
        "Exception.*?Informix",
        "Informix ODBC Driver",
        "ODBC Informix driver",
        "com\\.informix\\.jdbc",
        "weblogic\\.jdbc\\.informix",
        "Pdo\\[./_\\]Informix",
        "IfxException",
        "Dynamic SQL Error",
        "Warning.*?\\Wibase_",
        "org\\.firebirdsql\\.jdbc",
        "Pdo\\[./_\\]Firebird",
        "SQLite/JDBCDriver",
        "SQLite\\.Exception",
        "(Microsoft|System)\\.Data\\.SQLite\\.SQLiteException",
        "Warning.*?\\W(sqlite_|SQLite3::)",
        "\\[SQLITE_ERROR\\]",
        "SQLite error \\d+:",
        "sqlite3.OperationalError:",
        "SQLite3::SQLException",
        "org\\.sqlite\\.JDBC",
        "Pdo\\[./_\\]Sqlite",
        "SQLiteException",
        "SQL error.*?POS([0-9]+)",
        "Warning.*?\\Wmaxdb_",
        "DriverSapDB",
        "-3014.*?Invalid end of SQL statement",
        "com\\.sap\\.dbtech\\.jdbc",
        "\\[-3008\\].*?: Invalid keyword or missing delimiter",
        "Warning.*?\\Wsybase_",
        "Sybase message",
        "Sybase.*?Server message",
        "SybSQLException",
        "Sybase\\.Data\\.AseClient",
        "com\\.sybase\\.jdbc",
        "Warning.*?\\Wingres_",
        "Ingres SQLSTATE",
        "Ingres\\W.*?Driver",
        "com\\.ingres\\.gcf\\.jdbc",
        "Exception (condition )?\\d+\\. Transaction rollback",
        "com\\.frontbase\\.jdbc",
        "Syntax error 1. Missing",
        "(Semantic|Syntax) error [1-4]\\d{2}\\.",
        "Unexpected end of command in statement \\[",
        "Unexpected token.*?in statement \\[",
        "org\\.hsqldb\\.jdbc",
        "org\\.h2\\.jdbc",
        "\\[42000-192\\]",
        "![0-9]{5}![^\n]+(failed|unexpected|error|syntax|expected|violation|exception)",
        "\\[MonetDB\\]\\[ODBC Driver",
        "nl\\.cwi\\.monetdb\\.jdbc",
        "Syntax error: EncounteCYAN",
        "org\\.apache\\.derby",
        "ERROR 42X01",
        ", Sqlstate: (3F|42).{3}, (Routine|Hint|Position):",
        "/vertica/Parser/scan",
        "com\\.vertica\\.jdbc",
        "org\\.jkiss\\.dbeaver\\.ext\\.vertica",
        "com\\.vertica\\.dsi\\.dataengine",
        "com\\.mckoi\\.JDBCDriver",
        "com\\.mckoi\\.database\\.jdbc",
        "&lt;REGEX_LITERAL&gt;",
        "com\\.facebook\\.presto\\.jdbc",
        "io\\.prestosql\\.jdbc",
        "com\\.simba\\.presto\\.jdbc",
        "UNION query has different number of fields: \\d+, \\d+",
        "Altibase\\.jdbc\\.driver",
        "com\\.mimer\\.jdbc",
        "Syntax error,[^\n]+assumed to mean",
        "io\\.crate\\.client\\.jdbc",
        "encounteCYAN after end of query",
        "A comparison operator is requiCYAN here",
        "-10048: Syntax error",
        "rdmStmtPrepare\\(.+?\\) returned",
        "SQ074: Line \\d+:",
        "SR185: Undefined procedure",
        "SQ200: No table ",
        "Virtuoso S0002 Error",
        "\\[(Virtuoso Driver|Virtuoso iODBC Driver)\\]\\[Virtuoso Server\\]"]

def melon_scanner(host, delay=1):
    clear()
    payload_list = []
    response_admin = 0
    response_cgi_bin = 0
    response_directory_traversal = 0
    response_env = 0
    response_git = 0
    response_the_silent_directory = 0
    response_trace = 0
    response_track = 0
    response_the_silent_method = 0
    response_command_alt_port = False
    response_command_url = False
    response_command_headers = False
    response_command_cookie = False
    response_command_method = False
    response_python_alt_port = False
    response_python_url = False
    response_python_headers = False
    response_python_cookie = False
    response_python_method = False
    response_sql_alt_port = False
    response_sql_url = False
    response_sql_headers = False
    response_sql_cookie = False
    response_sql_method = False
    response_xss_alt_port = False
    response_xss_url = False
    response_xss_headers = False
    response_xss_cookie = False
    response_xss_method = False

    clear()
    new_port_list = []
    new_host = host.replace("http://", "")
    new_host = new_host.replace("https://", "")

    
    for port in range(1,65536):
        new_port_list.append(port)

    port_list = []
    new_port_list = random.sample(new_port_list[:], len(new_port_list[:]))
    for port in new_port_list:
        print(f"checking port: {port}/tcp")
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_socket.settimeout(5)
        try:
            my_socket.connect((new_host, int(port)))
            my_socket.close()
            print(f"found port: {port}/tcp")
            port_list.append(port)

        except:
            my_socket.close()
            continue

    new_port_list = random.sample(new_port_list[:], len(new_port_list[:]))
    for port in new_port_list:
        print(f"checking port: {port}/udp")
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        my_socket.settimeout(5)
        try:
            my_socket.sendto(b"",(new_host, int(port)))
            simple_response = my_socket.recvfrom(65536)
            port_list.append(port)
            print(f"found port: {port}/udp")

        except:
            continue

    port_list = list(set(port_list[:]))

    # attempt to get banner using tcp
    print(CYAN + "attempting to get banners using tcp")
    port_list = random.sample(port_list[:], len(port_list[:]))
    for port in port_list:
        print(CYAN + f"getting banner: {new_host}:{port}/tcp")
        time.sleep(delay)
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_socket.settimeout(5)
        try:
            my_socket.connect((new_host, int(port)))
            banner = my_socket.recv(65536).decode()
            print(CYAN + f"port {port}/tcp: {banner}")
            threats.append(f"port {port}/tcp: {banner}")
            my_socket.close()

        except:
            my_socket.close()
            continue

    # attempt to get banner using udp
    print(CYAN + "attempting to get banners using udp")
    port_list = random.sample(port_list[:], len(port_list[:]))
    for port in port_list:
        print(CYAN + f"getting banner: {new_host}:{port}/udp")
        time.sleep(delay)
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        my_socket.settimeout(5)
        try:
            my_socket.sendto(b"",(new_host,port))
            banner = my_socket.recvfrom(65536).decode()
            print(CYAN + f"port {port}/udp: {banner}")
            threats.append(f"port {port}/udp: {banner}")

        except:
            continue

    print(CYAN + "checking for injection points on every port")

    # test for command injection on alt port tcp
    mal_commands = ["echo TheSilent", "ping -c 60 127.0.0.1"]
    port_list = random.sample(port_list[:], len(port_list[:]))
    for port in port_list:
        print(CYAN + f"checking for command injection on port {port}/tcp")
        for mal in mal_commands:
            time.sleep(delay)
            my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            my_socket.settimeout(5)
            try:
                my_socket.connect((new_host, int(port)))
                my_socket.send(mal.encode())
                start = time.time()
                simple_response = my_socket.recv(65536).decode()
                my_socket.close()
                end = time.time()
                if mal == "echo TheSilent" and "TheSilent" in simple_response and "echo" not in simple_response and "TheSilent" not in false_postive_check:
                    repsonse_command_alt_port = True
                    payload_list.append(f"port/tcp: {mal}")

                if mal == "ping -c 60 127.0.0.1" and end - start >= 60:
                    repsonse_command_alt_port = True
                    payload_list.append(f"{port}/tcp: {mal}")
                    my_socket.close()

            except:
                my_socket.close()
                continue

    # test for command injection on alt port udp
    mal_commands = ["echo TheSilent", "ping -c 60 127.0.0.1"]
    port_list = random.sample(port_list[:], len(port_list[:]))
    for port in port_list:
        print(CYAN + f"checking for command injection on port {port}/udp")
        for mal in mal_commands:
            time.sleep(delay)
            my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            my_socket.settimeout(5)
            try:
                my_socket.sendto(mal.encode(), (new_host,port))
                start = time.time()
                simple_response = my_socket.recvfrom(65536).decode()
                end = time.time()
                if mal == "echo TheSilent" and "TheSilent" in simple_response and "echo" not in simple_response and "TheSilent" not in false_postive_check:
                    repsonse_command_alt_port = True
                    payload_list.append(f"port/udp: {mal}")

                if mal == "ping -c 60 127.0.0.1" and end - start >= 60:
                    repsonse_command_alt_port = True
                    payload_list.append(f"{port}/udp: {mal}")

            except:
                continue

    # test for python injection on alt port tcp
    mal_python = [r'eval(compile("import sys\ndef the_silent():\n return sys.version\nprint(the_silent())", "thesilent", "exec"))', r'eval(compile("import sys\ndef the_silent():\n return sys.version\nthe_silent()", "thesilent", "exec"))', r'eval(compile("import time\ntime.sleep(60)", "thesilent", "exec"))']
    port_list = random.sample(port_list[:], len(port_list[:]))
    for port in port_list:
        print(CYAN + f"checking for python injection on port {port}/tcp")
        for mal in mal_python:
            time.sleep(delay)
            my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            my_socket.settimeout(5)
            try:
                my_socket.connect((new_host, int(port)))
                my_socket.send(mal.encode())
                start = time.time()
                simple_response = my_socket.recv(65536).decode()
                my_socket.close()
                end = time.time()
                if mal == r'eval(compile("import sys\ndef the_silent():\n return sys.version\nprint(the_silent())", "thesilent", "exec"))' and "gcc" in simple_response.lower() and "gcc" not in false_positive_check.lower():
                    response_python_alt_port = True
                    payload_list.append(f"{port}/tcp: {mal}")

                if mal == r'eval(compile("import sys\ndef the_silent():\n return sys.version\nthe_silent()", "thesilent", "exec"))' and "gcc" in simple_response.lower() and "gcc" not in false_positive_check.lower():
                    response_python_alt_port = True
                    payload_list.append(f"{port}/tcp: {mal}")
                    
                if mal == r'eval(compile("import time\ntime.sleep(60)", "thesilent", "exec"))' and end - start >= 60:
                    response_python_alt_port = True
                    payload_list.append(f"{port}/tcp: {mal}")

            except:
                my_socket.close()
                continue

    # test for python injection on alt port udp
    mal_python = [r'eval(compile("import sys\ndef the_silent():\n return sys.version\nprint(the_silent())", "thesilent", "exec"))', r'eval(compile("import sys\ndef the_silent():\n return sys.version\nthe_silent()", "thesilent", "exec"))', r'eval(compile("import time\ntime.sleep(60)", "thesilent", "exec"))']
    port_list = random.sample(port_list[:], len(port_list[:]))
    for port in port_list:
        print(CYAN + f"checking for python injection on port {port}/udp")
        for mal in mal_python:
            time.sleep(delay)
            my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            my_socket.settimeout(5)
            try:
                my_socket.sendto(mal.encode(),(new_host,port))
                start = time.time()
                simple_response = my_socket.recvfrom(65536).decode()
                end = time.time()
                if mal == r'eval(compile("import sys\ndef the_silent():\n return sys.version\nprint(the_silent())", "thesilent", "exec"))' and "gcc" in simple_response.lower() and "gcc" not in false_positive_check.lower():
                    response_python_alt_port = True
                    payload_list.append(f"{port}/udp: {mal}")

                if mal == r'eval(compile("import sys\ndef the_silent():\n return sys.version\nthe_silent()", "thesilent", "exec"))' and "gcc" in simple_response.lower() and "gcc" not in false_positive_check.lower():
                    response_python_alt_port = True
                    payload_list.append(f"{port}/udp: {mal}")
                    
                if mal == r'eval(compile("import time\ntime.sleep(60)", "thesilent", "exec"))' and end - start >= 60:
                    response_python_alt_port = True
                    payload_list.append(f"{port}/udp: {mal}")

            except:
                continue

    # test for sql injection on alt port tcp
    mal_sql = ["'", '"', "*", ";", "`", "')", '")', "*)", ";)", "`)", "'))", '"))', "*))", ";))", "`))", "')))", '")))', "*)))", ";)))", "`)))"]
    port_list = random.sample(port_list[:], len(port_list[:]))
    for port in port_list:
        print(CYAN + f"checking for sql injection on port {port}/tcp")
        for mal in mal_sql:
            time.sleep(delay)
            my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            my_socket.settimeout(5)
            try:
                my_socket.connect((new_host, int(port)))
                my_socket.send(mal.encode())
                simple_response = my_socket.recv(65536).decode()
                my_socket.close()
                for error in sql_errors:
                    result = re.search(error, simple_response)
                    if result:
                        response_sql_alt_port = True
                        payload_list.append(f"{port}/tcp: {mal}")

            except:
                my_socket.close()
                continue

    # test for sql injection on alt port udp
    mal_sql = ["'", '"', "*", ";", "`", "')", '")', "*)", ";)", "`)", "'))", '"))', "*))", ";))", "`))", "')))", '")))', "*)))", ";)))", "`)))"]
    port_list = random.sample(port_list[:], len(port_list[:]))
    for port in port_list:
        print(CYAN + f"checking for sql injection on port {port}/udp")
        for mal in mal_sql:
            time.sleep(delay)
            my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            my_socket.settimeout(5)
            try:
                my_socket.sendto(mal.encode(),(new_host,port))
                simple_response = my_socket.recvfrom(65536).decode()
                for error in sql_errors:
                    result = re.search(error, simple_response)
                    if result:
                        response_sql_alt_port = True
                        payload_list.append(f"{port}/udp: {mal}")

            except:
                continue

    # test for xss on alt port tcp
    mal_xss = ["<div>TheSilent</div>", "<em>TheSilent</em>", "<iframe>TheSilent</iframe>", "<input type='text' id='thesilent' name='TheSilent' value='TheSilent'>", "<p>TheSilent</p>", '<script>alert("TheSilent")</script>;', '<script>prompt("TheSilent")</script>;', "<strong>TheSilent</strong>"]
    port_list = random.sample(port_list[:], len(port_list[:]))
    for port in port_list:
        print(CYAN + f"checking for xss on port {port}/tcp")
        for mal in mal_xss:
            time.sleep(delay)
            my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            my_socket.settimeout(5)
            try:
                my_socket.connect((new_host, int(port)))
                my_socket.send(mal.encode())
                start = time.time()
                simple_response = my_socket.recv(65536).decode()
                my_socket.close()
                end = time.time()
                if mal in simple_response:
                    response_xss_alt_port = True
                    payload_list.append(f"{port}: {mal}")

            except:
                my_socket.close()
                continue

    # test for xss on alt port udp
    mal_xss = ["<div>TheSilent</div>", "<em>TheSilent</em>", "<iframe>TheSilent</iframe>", "<input type='text' id='thesilent' name='TheSilent' value='TheSilent'>", "<p>TheSilent</p>", '<script>alert("TheSilent")</script>;', '<script>prompt("TheSilent")</script>;', "<strong>TheSilent</strong>"]
    port_list = random.sample(port_list[:], len(port_list[:]))
    for port in port_list:
        print(CYAN + f"checking for xss on port {port}/udp")
        for mal in mal_xss:
            time.sleep(delay)
            my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            my_socket.settimeout(5)
            try:
                my_socket.sendto(mal.encode(), (new_host,port))
                simple_response = my_socket.recvfrom(65536).decode()
                if mal in simple_response:
                    response_xss_alt_port = True
                    payload_list.append(f"{port}/udp: {mal}")

            except:
                continue

    try:
        # get admin
        print(CYAN + "checking for admin")
        my_request = urllib.request.Request(host + "/admin", method="GET")
        my_request.add_header("User-Agent",return_user_agent())
        my_request.add_header("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8")
        my_request.add_header("Accept-Encoding","deflate")
        my_request.add_header("Accept-Language","en-US,en;q=0.5")
        my_request.add_header("Referer","https://www.google.com/")
        my_request.add_header("UPGRADE-INSECURE-REQUESTS","1")
        response_admin = urllib.request.urlopen(my_request, context=verify, timeout=15).status
        time.sleep(delay)
    except:
        pass

    try:
        # get cgi-bin
        print(CYAN + "checking for cgi-bin")
        my_request = urllib.request.Request(host + "/cgi-bin", method="GET")
        my_request.add_header("User-Agent",return_user_agent())
        my_request.add_header("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8")
        my_request.add_header("Accept-Encoding","deflate")
        my_request.add_header("Accept-Language","en-US,en;q=0.5")
        my_request.add_header("Referer","https://www.google.com/")
        my_request.add_header("UPGRADE-INSECURE-REQUESTS","1")
        response_cgi_bin = urllib.request.urlopen(my_request, context=verify, timeout=15).status
        time.sleep(delay)
    except:
        pass

    try:
        # test directory traversal
        print(CYAN + "checking for directory traversal using /.../")
        my_request = urllib.request.Request(host + "/.../", method="GET")
        my_request.add_header("User-Agent",return_user_agent())
        my_request.add_header("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8")
        my_request.add_header("Accept-Encoding","deflate")
        my_request.add_header("Accept-Language","en-US,en;q=0.5")
        my_request.add_header("Referer","https://www.google.com/")
        my_request.add_header("UPGRADE-INSECURE-REQUESTS","1")
        response_directory_traversal = urllib.request.urlopen(my_request, context=verify, timeout=15).status
        time.sleep(delay)
    except:
        pass

    try:
        # get .env
        print(CYAN + "checking for .env")
        my_request = urllib.request.Request(host + "/.env", method="GET")
        my_request.add_header("User-Agent",return_user_agent())
        my_request.add_header("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8")
        my_request.add_header("Accept-Encoding","deflate")
        my_request.add_header("Accept-Language","en-US,en;q=0.5")
        my_request.add_header("Referer","https://www.google.com/")
        my_request.add_header("UPGRADE-INSECURE-REQUESTS","1")
        response_env = urllib.request.urlopen(my_request, context=verify, timeout=15).status
        time.sleep(delay)
    except:
        pass

    try:
        # get .git
        print(CYAN + "checking for .git")
        my_request = urllib.request.Request(host + "/.git", method="GET")
        my_request.add_header("User-Agent",return_user_agent())
        my_request.add_header("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8")
        my_request.add_header("Accept-Encoding","deflate")
        my_request.add_header("Accept-Language","en-US,en;q=0.5")
        my_request.add_header("Referer","https://www.google.com/")
        my_request.add_header("UPGRADE-INSECURE-REQUESTS","1")
        response_admin = urllib.request.urlopen(my_request, context=verify, timeout=15).status
        time.sleep(delay)
    except:
        pass

    try:
        # get TheSilent (false positive check)
        print(CYAN + "checking for TheSilent")
        my_request = urllib.request.Request(host + "/TheSilent", method="GET")
        my_request.add_header("User-Agent",return_user_agent())
        my_request.add_header("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8")
        my_request.add_header("Accept-Encoding","deflate")
        my_request.add_header("Accept-Language","en-US,en;q=0.5")
        my_request.add_header("Referer","https://www.google.com/")
        my_request.add_header("UPGRADE-INSECURE-REQUESTS","1")
        response_the_silent_directory = urllib.request.urlopen(my_request, context=verify, timeout=15).status
        time.sleep(delay)
    except:
        pass

    try:
        # test trace method
        print(CYAN + "checking trace method")
        my_request = urllib.request.Request(host, method="TRACE")
        my_request.add_header("User-Agent",return_user_agent())
        my_request.add_header("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8")
        my_request.add_header("Accept-Encoding","deflate")
        my_request.add_header("Accept-Language","en-US,en;q=0.5")
        my_request.add_header("Referer","https://www.google.com/")
        my_request.add_header("UPGRADE-INSECURE-REQUESTS","1")
        response_trace = urllib.request.urlopen(my_request, context=verify, timeout=15).status
        time.sleep(delay)
    except:
        pass

    try:
        # test track method
        print(CYAN + "checking track method")
        my_request = urllib.request.Request(host, method="TRACK")
        my_request.add_header("User-Agent",return_user_agent())
        my_request.add_header("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8")
        my_request.add_header("Accept-Encoding","deflate")
        my_request.add_header("Accept-Language","en-US,en;q=0.5")
        my_request.add_header("Referer","https://www.google.com/")
        my_request.add_header("UPGRADE-INSECURE-REQUESTS","1")
        response_track = urllib.request.urlopen(my_request, context=verify, timeout=15).status
        time.sleep(delay)
    except:
        pass

    try:
        # test THESILENT method (false positive check)
        print(CYAN + "checking THESILENT method")
        my_request = urllib.request.Request(host, method="THESILENT")
        my_request.add_header("User-Agent",return_user_agent())
        my_request.add_header("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8")
        my_request.add_header("Accept-Encoding","deflate")
        my_request.add_header("Accept-Language","en-US,en;q=0.5")
        my_request.add_header("Referer","https://www.google.com/")
        my_request.add_header("UPGRADE-INSECURE-REQUESTS","1")
        response_trace = urllib.request.urlopen(my_request, context=verify, timeout=15).status
        time.sleep(delay)
    except:
        pass

    # test for command injection in url
    print(CYAN + "checking for command injection in url")
    mal_commands = ["/echo TheSilent", "/ping -c 60 127.0.0.1"]
    for mal in mal_commands:
        time.sleep(delay)
        start = time.time()
        try:
            my_request = urllib.request.Request(host + f"/{urllib.parse.quote(mal)}", method="GET")
            my_request.add_header("User-Agent",return_user_agent())
            my_request.add_header("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8")
            my_request.add_header("Accept-Encoding","deflate")
            my_request.add_header("Accept-Language","en-US,en;q=0.5")
            my_request.add_header("Referer","https://www.google.com/")
            my_request.add_header("UPGRADE-INSECURE-REQUESTS","1")
            simple_response = str(urllib.request.urlopen(my_request, context=verify, timeout=15).read())
            end = time.time()
            if mal == "/echo TheSilent" and "TheSilent" in simple_response and "echo" not in simple_response and "TheSilent" not in false_postive_check:
                response_command_url = True
                payload_list.append(f"url: {mal}")

            if mal == "/ping -c 60 127.0.0.1" and end - start >= 60:
                response_command_url = True
                payload_list.append(f"url: {mal}")

        except:
            continue

    # test for command injection in headers
    print(CYAN + "checking for command injection in headers")
    mal_commands = ["/echo TheSilent", "/ping -c 60 127.0.0.1"] 
    time.sleep(delay)
    for mal in mal_commands:
        time.sleep(delay)
        start = time.time()
        try:
            my_request = urllib.request.Request(host, method="GET")
            my_request.add_header("User-Agent",return_user_agent())
            my_request.add_header("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8")
            my_request.add_header("Accept-Encoding","deflate")
            my_request.add_header("Accept-Language","en-US,en;q=0.5")
            my_request.add_header("Referer",mal)
            my_request.add_header("UPGRADE-INSECURE-REQUESTS","1")
            simple_response = str(urllib.request.urlopen(my_request, context=verify, timeout=15).read())
            end = time.time()
            if mal == "/echo TheSilent" and "TheSilent" in simple_response and "echo" not in simple_response and "TheSilent" not in false_positive_check:
                response_command_headers = True
                payload_list.append(f"header: {head}:{mal}")

            if mal == "/ping -c 60 127.0.0.1" and end - start >= 60:
                response_command_headers = True

        except:
            continue

    # test for command injection in cookie
    print(CYAN + "checking for command injection in cookie")
    mal_commands = ["/echo TheSilent", "/ping -c 60 127.0.0.1"]
    for mal in mal_commands:
        time.sleep(delay)
        start = time.time()
        try:
            my_request = urllib.request.Request(host, method="GET")
            my_request.add_header("User-Agent",return_user_agent())
            my_request.add_header("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8")
            my_request.add_header("Accept-Encoding","deflate")
            my_request.add_header("Accept-Language","en-US,en;q=0.5")
            my_request.add_header("Referer","https://www.google.com/")
            my_request.add_header("UPGRADE-INSECURE-REQUESTS","1")
            my_request.add_header("Cookie",mal)
            simple_response = str(urllib.request.urlopen(my_request, context=verify, timeout=15).read())
        
            end = time.time()
            if mal == "/echo TheSilent" and "TheSilent" in simple_response and "echo" not in simple_response and "TheSilent" not in false_postive_check:
                response_command_cookie = True
                payload_list.append(f"cookie: {mal}")

            if mal == "/ping -c 60 127.0.0.1" and end - start >= 60:
                response_command_cookie = True

        except:
            continue
                
    # test for command injection in method
    print(CYAN + "checking for command injection in method")
    mal_commands = ["/echo TheSilent", "/ping -c 60 127.0.0.1"]
    for mal in mal_commands:
        time.sleep(delay)
        start = time.time()
        try:
            my_request.add_header("User-Agent",return_user_agent())
            my_request.add_header("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8")
            my_request.add_header("Accept-Encoding","deflate")
            my_request.add_header("Accept-Language","en-US,en;q=0.5")
            my_request.add_header("Referer","https://www.google.com/")
            my_request.add_header("UPGRADE-INSECURE-REQUESTS","1")
            simple_response = str(urllib.request.urlopen(my_request, context=verify, timeout=15).read())
        
            end = time.time()
            if mal == "/echo TheSilent" and "TheSilent" in simple_response and "echo" not in simple_response and "TheSilent" not in false_postive_check:
                response_command_method = True
                payload_list.append(f"method: {mal}")

            if mal == "/ping -c 60 127.0.0.1" and end - start >= 60:
                response_command_method = True
                payload_list.append(f"method: {mal}")

        except:
            continue

    # test for python injection in url
    print(CYAN + "checking for python injection in url")
    mal_python = [r'eval(compile("import sys\ndef the_silent():\n return sys.version\nprint(the_silent())", "thesilent", "exec"))', r'eval(compile("import sys\ndef the_silent():\n return sys.version\nthe_silent()", "thesilent", "exec"))', r'eval(compile("import time\ntime.sleep(60)", "thesilent", "exec"))']
    for mal in mal_python:
        time.sleep(delay)
        start = time.time()
        try:
            my_request = urllib.request.Request(host + f"/{urllib.parse.quote(mal)}", method="GET")
            my_request.add_header("User-Agent",return_user_agent())
            simple_response = str(urllib.request.urlopen(my_request, context=verify, timeout=15).read())
            end = time.time()
            if mal == r'eval(compile("import sys\ndef the_silent():\n return sys.version\nprint(the_silent())", "thesilent", "exec"))' and "gcc" in simple_response.lower() and "gcc" not in false_positive_check.lower():
                response_python_url = True
                payload_list.append(f"url: {mal}")

            if mal == r'eval(compile("import sys\ndef the_silent():\n return sys.version\nthe_silent()", "thesilent", "exec"))' and "gcc" in simple_response.lower() and "gcc" not in false_positive_check.lower():
                response_python_url = True
                payload_list.append(f"url: {mal}")
                
            if mal == r'eval(compile("import time\ntime.sleep(60)", "thesilent", "exec"))' and end - start >= 60:
                response_python_url = True
                payload_list.append(f"url: {mal}")

        except:
            continue
                
    # test for python injection in headers
    print(CYAN + "checking for python injection in headers")
    mal_python = [r'eval(compile("import sys\ndef the_silent():\n return sys.version\nprint(the_silent())", "thesilent", "exec"))', r'eval(compile("import sys\ndef the_silent():\n return sys.version\nthe_silent()", "thesilent", "exec"))', r'eval(compile("import time\ntime.sleep(60)", "thesilent", "exec"))']
    time.sleep(delay)
    for mal in mal_python:
        time.sleep(delay)
        start = time.time()
        try:
            my_request = urllib.request.Request(host, method="GET")
            my_request.add_header("User-Agent",return_user_agent())
            my_request.add_header("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8")
            my_request.add_header("Accept-Encoding","deflate")
            my_request.add_header("Accept-Language","en-US,en;q=0.5")
            my_request.add_header("Referer","https://www.google.com/")
            my_request.add_header("UPGRADE-INSECURE-REQUESTS","1")
            my_request.add_header(head,mal)
            simple_response = str(urllib.request.urlopen(my_request, context=verify, timeout=15).read())
            end = time.time()
            if mal == r'eval(compile("import sys\ndef the_silent():\n return sys.version\nprint(the_silent())", "thesilent", "exec"))' and "gcc" in simple_response.lower() and "gcc" not in false_positive_check.lower():
                response_python_headers = True
                payload_list.append(f"header: {head}:{mal}")

            if mal == r'eval(compile("import sys\ndef the_silent():\n return sys.version\nthe_silent()", "thesilent", "exec"))' and "gcc" in simple_response.lower() and "gcc" not in false_positive_check.lower():
                response_python_headers = True
                payload_list.append(f"header: {head}:{mal}")
                
            if mal == r'eval(compile("import time\ntime.sleep(60)", "thesilent", "exec"))' and end - start >= 60:
                response_python_headers = True
                payload_list.append(f"header: {head}:{mal}")

        except:
            continue

    # test for python injection in cookie
    print(CYAN + "checking for python injection in cookie")
    mal_python = [r'eval(compile("import sys\ndef the_silent():\n return sys.version\nprint(the_silent())", "thesilent", "exec"))', r'eval(compile("import sys\ndef the_silent():\n return sys.version\nthe_silent()", "thesilent", "exec"))', r'eval(compile("import time\ntime.sleep(60)", "thesilent", "exec"))']
    for mal in mal_python:
        time.sleep(delay)
        start = time.time()
        try:
            my_request = urllib.request.Request(host, method="GET")
            my_request.add_header("User-Agent",return_user_agent())
            my_request.add_header("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8")
            my_request.add_header("Accept-Encoding","deflate")
            my_request.add_header("Accept-Language","en-US,en;q=0.5")
            my_request.add_header("Referer","https://www.google.com/")
            my_request.add_header("UPGRADE-INSECURE-REQUESTS","1")
            my_request.add_header("Cookie",mal)
            simple_response = str(urllib.request.urlopen(my_request, context=verify, timeout=15).read())
            end = time.time()
            if mal == r'eval(compile("import sys\ndef the_silent():\n return sys.version\nprint(the_silent())", "thesilent", "exec"))' and "gcc" in simple_response.lower() and "gcc" not in false_positive_check.lower():
                response_python_cookie = True
                payload_list.append(f"cookie: {mal}")

            if mal == r'eval(compile("import sys\ndef the_silent():\n return sys.version\nthe_silent()", "thesilent", "exec"))' and "gcc" in simple_response.lower() and "gcc" not in false_positive_check.lower():
                response_python_cookie = True
                payload_list.append(f"cookie: {mal}")
                
            if mal == r'eval(compile("import time\ntime.sleep(60)", "thesilent", "exec"))' and end - start >= 60:
                response_python_cookie = True
                payload_list.append(f"cookie: {mal}")

        except:
            continue

    # test for python injection in method
    print(CYAN + "checking for python injection in method")
    mal_python = [r'eval(compile("import sys\ndef the_silent():\n return sys.version\nprint(the_silent())", "thesilent", "exec"))', r'eval(compile("import sys\ndef the_silent():\n return sys.version\nthe_silent()", "thesilent", "exec"))', r'eval(compile("import time\ntime.sleep(60)", "thesilent", "exec"))']
    for mal in mal_python:
        time.sleep(delay)
        start = time.time()
        try:
            my_request = urllib.request.Request(host, method=mal)
            my_request.add_header("User-Agent",return_user_agent())
            my_request.add_header("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8")
            my_request.add_header("Accept-Encoding","deflate")
            my_request.add_header("Accept-Language","en-US,en;q=0.5")
            my_request.add_header("Referer","https://www.google.com/")
            my_request.add_header("UPGRADE-INSECURE-REQUESTS","1")
            simple_response = str(urllib.request.urlopen(my_request, context=verify, timeout=15).read())
            end = time.time()
            if mal == r'eval(compile("import sys\ndef the_silent():\n return sys.version\nprint(the_silent())", "thesilent", "exec"))' and "gcc" in simple_response.lower() and "gcc" not in false_positive_check.lower():
                response_python_method = True
                payload_list.append(f"method: {mal}")

            if mal == r'eval(compile("import sys\ndef the_silent():\n return sys.version\nthe_silent()", "thesilent", "exec"))' and "gcc" in simple_response.lower() and "gcc" not in false_positive_check.lower():
                response_python_method = True
                payload_list.append(f"method: {mal}")
                
            if mal == r'eval(compile("import time\ntime.sleep(60)", "thesilent", "exec"))' and end - start >= 60:
                response_python_method = True
                payload_list.append(f"method: {mal}")

        except:
            continue

    # test for sql injection in url
    print(CYAN + "checking for sql injection in url")
    mal_sql = ["'", '"', "*", ";", "`", "')", '")', "*)", ";)", "`)", "'))", '"))', "*))", ";))", "`))", "')))", '")))', "*)))", ";)))", "`)))"]
    for mal in mal_sql:
        time.sleep(delay)
        try:
            my_request = urllib.request.Request(host + f"/{urllib.parse.quote(mal)}", method="GET")
            my_request.add_header("User-Agent",return_user_agent())
            my_request.add_header("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8")
            my_request.add_header("Accept-Encoding","deflate")
            my_request.add_header("Accept-Language","en-US,en;q=0.5")
            my_request.add_header("Referer","https://www.google.com/")
            my_request.add_header("UPGRADE-INSECURE-REQUESTS","1")
            simple_response = str(urllib.request.urlopen(my_request, context=verify, timeout=15).read())
            for error in sql_errors:
                result = re.search(error, simple_response)
                if result:
                    response_sql_url = True
                    payload_list.append(f"url: {mal}")

        except:
            continue
                
    # test for sql injection in headers
    print(CYAN + "checking for sql injection in headers")
    mal_sql = ["'", '"', "*", ";", "`", "')", '")', "*)", ";)", "`)", "'))", '"))', "*))", ";))", "`))", "')))", '")))', "*)))", ";)))", "`)))"]
    time.sleep(delay)
    for mal in mal_sql:
        time.sleep(delay)
        try:
            my_request = urllib.request.Request(host, method="GET")
            my_request.add_header("User-Agent",return_user_agent())
            my_request.add_header("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8")
            my_request.add_header("Accept-Encoding","deflate")
            my_request.add_header("Accept-Language","en-US,en;q=0.5")
            my_request.add_header("Referer","https://www.google.com/")
            my_request.add_header("UPGRADE-INSECURE-REQUESTS","1")
            my_request.add_header(head,mal)
            simple_response = str(urllib.request.urlopen(my_request, context=verify, timeout=15).read())
            for error in sql_errors:
                result = re.search(error, simple_response)
                if result:
                    response_sql_headers = True
                    payload_list.append(f"header: {head}:{mal}")

        except:
            continue

    # test for sql injection in cookie
    print(CYAN + "checking for sql injection in cookie")
    mal_sql = ["'", '"', "*", ";", "`", "')", '")', "*)", ";)", "`)", "'))", '"))', "*))", ";))", "`))", "')))", '")))', "*)))", ";)))", "`)))"]
    for mal in mal_sql:
        time.sleep(delay)
        try:
            my_request = urllib.request.Request(host, method="GET")
            my_request.add_header("User-Agent",return_user_agent())
            my_request.add_header("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8")
            my_request.add_header("Accept-Encoding","deflate")
            my_request.add_header("Accept-Language","en-US,en;q=0.5")
            my_request.add_header("Referer","https://www.google.com/")
            my_request.add_header("UPGRADE-INSECURE-REQUESTS","1")
            my_request.add_header("Cookie",mal)
            simple_response = str(urllib.request.urlopen(my_request, context=verify, timeout=15).read())
            for error in sql_errors:
                result = re.search(error, simple_response)
                if result:
                    response_sql_cookie = True
                    payload_list.append(f"cookie: {mal}")

        except:
            continue

    # test for sql injection in method
    print(CYAN + "checking for sql injection in method")
    mal_sql = ["'", '"', "*", ";", "`", "')", '")', "*)", ";)", "`)", "'))", '"))', "*))", ";))", "`))", "')))", '")))', "*)))", ";)))", "`)))"]
    for mal in mal_sql:
        time.sleep(delay)
        try:
            my_request = urllib.request.Request(host, method=mal)
            my_request.add_header("User-Agent",return_user_agent())
            my_request.add_header("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8")
            my_request.add_header("Accept-Encoding","deflate")
            my_request.add_header("Accept-Language","en-US,en;q=0.5")
            my_request.add_header("Referer","https://www.google.com/")
            my_request.add_header("UPGRADE-INSECURE-REQUESTS","1")
            simple_response = str(urllib.request.urlopen(my_request, context=verify, timeout=15).read())
            for error in sql_errors:
                result = re.search(error, simple_response)
                if result:
                    response_sql_method = True
                    payload_list.append(f"method: {mal}")

        except:
            continue
                
    # test for xss in url
    print(CYAN + "checking for xss in url")
    mal_xss = ["<div>TheSilent</div>", "<em>TheSilent</em>", "<iframe>TheSilent</iframe>", "<input type='text' id='thesilent' name='TheSilent' value='TheSilent'>", "<p>TheSilent</p>", '<script>alert("TheSilent")</script>;', '<script>prompt("TheSilent")</script>;', "<strong>TheSilent</strong>"]
    for mal in mal_xss:
        time.sleep(delay)
        try:
            my_request = urllib.request.Request(host + f"/{urllib.parse.quote(mal)}", method="GET")
            my_request.add_header()
            simple_response = str(urllib.request.urlopen(my_request, context=verify, timeout=15).read())
            if mal in simple_response:
                response_xss_url = True
                payload_list.append(f"url: {mal}")

        except:
            continue

    # test for xss in headers
    print(CYAN + "checking for xss in headers")
    mal_xss = ["<div>TheSilent</div>", "<em>TheSilent</em>", "<iframe>TheSilent</iframe>", "<input type='text' id='thesilent' name='TheSilent' value='TheSilent'>", "<p>TheSilent</p>", '<script>alert("TheSilent")</script>;', '<script>prompt("TheSilent")</script>;', "<strong>TheSilent</strong>"]    
    time.sleep(delay)
    for mal in mal_xss:
        time.sleep(delay)
        try:
            my_request = urllib.request.Request(host, method="GET")
            my_request.add_header("User-Agent",return_user_agent())
            my_request.add_header("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8")
            my_request.add_header("Accept-Encoding","deflate")
            my_request.add_header("Accept-Language","en-US,en;q=0.5")
            my_request.add_header("Referer","https://www.google.com/")
            my_request.add_header("UPGRADE-INSECURE-REQUESTS","1")
            my_request.add_header(head,mal)
            simple_response = str(urllib.request.urlopen(my_request, context=verify, timeout=15).read())
            if mal in simple_response:
                response_xss_headers = True
                payload_list.append(f"header: {head}:{mal}")

        except:
            continue

    # test for xss in cookie
    print(CYAN + "checking for xss in cookie")
    mal_xss = ["<div>TheSilent</div>", "<em>TheSilent</em>", "<iframe>TheSilent</iframe>", "<input type='text' id='thesilent' name='TheSilent' value='TheSilent'>", "<p>TheSilent</p>", '<script>alert("TheSilent")</script>;', '<script>prompt("TheSilent")</script>;', "<strong>TheSilent</strong>"]
    for mal in mal_xss:
        time.sleep(delay)
        try:
            my_request = urllib.request.Request(host, method="GET")
            my_request.add_header("User-Agent",return_user_agent())
            my_request.add_header("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8")
            my_request.add_header("Accept-Encoding","deflate")
            my_request.add_header("Accept-Language","en-US,en;q=0.5")
            my_request.add_header("Referer","https://www.google.com/")
            my_request.add_header("UPGRADE-INSECURE-REQUESTS","1")
            my_request.add_header("Cookie",mal)
            simple_response = str(urllib.request.urlopen(my_request, context=verify, timeout=15).read())        
            if mal in simple_response:
                response_xss_cookie = True
                payload_list.append(f"cookie: {mal}")

        except:
            continue

    # test for xss in method
    print(CYAN + "checking for xss in method")
    mal_xss = ["<div>TheSilent</div>", "<em>TheSilent</em>", "<iframe>TheSilent</iframe>", "<input type='text' id='thesilent' name='TheSilent' value='TheSilent'>", "<p>TheSilent</p>", '<script>alert("TheSilent")</script>;', '<script>prompt("TheSilent")</script>;', "<strong>TheSilent</strong>"]
    for mal in mal_xss:
        time.sleep(delay)
        try:
            my_request = urllib.request.Request(host, method=mal)
            my_request.add_header("User-Agent",return_user_agent())
            my_request.add_header("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8")
            my_request.add_header("Accept-Encoding","deflate")
            my_request.add_header("Accept-Language","en-US,en;q=0.5")
            my_request.add_header("Referer","https://www.google.com/")
            my_request.add_header("UPGRADE-INSECURE-REQUESTS","1")
            simple_response = str(urllib.request.urlopen(my_request, context=verify, timeout=15).read())
            if mal in simple_response:
                response_xss_method = True
                payload_list.append(f"method: {mal}")

        except:
            continue

    # test for annonymous ftp bindings
    print(CYAN + "checking for annonymous ftp bindings")
    ftp_verify = False
    new_host = host.replace("http://", "")
    new_host = new_host.replace("https://", "")
    try:
        ftp = FTP(new_host, timeout=15)
        ftp.login()
        ftp.close()
        ftp_verify = True
    except:
        pass

    time.sleep(delay)
    try:
        ftp = FTP_TLS(new_host, timeout=15)
        ftp.login()
        ftp.close()
        ftp_verify = True 
    except:
        pass

    clear()
    secure = True
    threats = []

    if response_command_alt_port:
        threats.append("Command injection in port found!")
        secure = False

    if response_python_alt_port:
        threats.append("Python injection in port found!")
        secure = False

    if response_sql_alt_port:
        threats.append("SQL injection in port found!")
        secure = False

    if response_xss_alt_port:
        threats.append("XSS in port found!")
        secure = False

    if response_admin == 200:
        threats.append("Admin page found!")
        secure = False

    if response_cgi_bin == 200:
        threats.append("CGI-BIN directory found!")
        secure = False

    if response_command_url:
        threats.append("Command injection in url found!")
        secure = False

    if response_command_headers:
        threats.append("Command injection in headers found!")
        secure = False

    if response_command_cookie:
        threats.append("Command injection in cookie found!")
        secure = False

    if response_command_method:
        threats.append("Command injection in method found!")
        secure = False

    if response_directory_traversal == 200:
        threats.append("Directory traversal using /.../ found!")
        secure = False

    if response_env == 200:
        threats.append(".ENV found!")
        secure = False

    if ftp_verify:
        threats.append("Annonymous ftp binding found!")
        secure = False

    if response_git == 200:
        threats.append(".GIT found!")
        secure = False

    if response_python_url:
        threats.append("Python injection in url found!")
        secure = False

    if response_python_headers:
        threats.append("Python injection in headers found!")
        secure = False

    if response_python_cookie:
        threats.append("Python injection in cookie found!")
        secure = False

    if response_python_method:
        threats.append("Python injection in method found!")
        secure = False

    if response_sql_url:
        threats.append("SQL injection found in url!")
        secure = False

    if response_sql_headers:
        threats.append("SQL injection found in headers!")
        secure = False

    if response_sql_cookie:
        threats.append("SQL injection found in cookie!")
        secure = False

    if response_sql_method:
        threats.append("SQL injection found in method!")
        secure = False

    if response_the_silent_directory == 200:
        threats.append("TheSilent directory found (directory traversal attempts need to be manually checked)!")
        secure = False

    if response_the_silent_method == 200:
        threats.append("THESILENT method allowed (all methods are allowed)!")
        secure = False

    if response_trace == 200:
        threats.append("TRACE method allowed!")
        secure = False

    if response_track == 200:
        threats.append("TRACK method allowed!")
        secure = False

    if response_xss_url:
        threats.append("XSS found in url!")
        secure = False

    if response_xss_headers:
        threats.append("XSS found in headers!")
        secure = False

    if response_xss_cookie:
        threats.append("XSS found in cookie!")
        secure = False

    if response_xss_method:
        threats.append("XSS found in method!")
        secure = False
        
    if secure:
        print(GREEN + "")
        clear()
        return "This server is secure!"

    else:
        print(RED + "")
        clear()

        return threats, payload_list
