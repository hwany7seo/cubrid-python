"""
This module contains tests specifically focused on testing CUBRID database connections.
These tests verify various connection scenarios, error cases, and connection properties.
"""
import pytest
import _cubrid
import CUBRIDdb

def _get_connect_args():
    ip = "test-db-server"
    port = "33000"
    dbname = "demodb"
    user = "dba"
    password = ""

    return {
        'dsn': f"CUBRID:{ip}:{port}:{dbname}:::",
        'user': user,
        'password': password,
    }

@pytest.fixture
def cubrid_connection():
    conn = _cubrid.connect(_get_connect_args()['dsn'])
    yield conn

    conn.close()

@pytest.fixture
def cubrid_db_connection():
    args = _get_connect_args()
    conn = CUBRIDdb.connect(args['dsn'], args['user'], args['password'])
    yield conn
    conn.close()

def test_CUBRIDdb_connection(cubrid_db_connection):
    print(cubrid_db_connection)

    
def test_connection_args(cubrid_connection):
    print(cubrid_connection)

def test_connection_with_dsn_only():
    """Test that connection with only DSN should fail without user credentials"""
    with pytest.raises(Error):
        _cubrid.connect("CUBRID:localhost:33000:demodb:::")

def test_connection_with_invalid_user():
    """Test connection with invalid user credentials"""
    with pytest.raises(OperationalError):
        _cubrid.connect(
            "CUBRID:localhost:33000:demodb:::",
            "invalid_user",
            "invalid_password"
        )

def test_connection_with_empty_user():
    """Test that connection with empty user string should fail"""
    with pytest.raises(Error):
        _cubrid.connect(
            "CUBRID:localhost:33000:demodb:::",
            "",
            ""
        )

def test_connection_with_valid_credentials():
    """Test connection with valid credentials"""
    conn = _cubrid.connect(
        "CUBRID:localhost:33000:demodb:::",
        "dba",
        ""
    )
    assert conn is not None
    conn.close()

def test_connection_properties():
    """Test connection object properties after successful connection"""
    conn = _cubrid.connect(
        "CUBRID:localhost:33000:demodb:::",
        "dba",
        ""
    )
    try:
        # Test autocommit property
        assert hasattr(conn, 'autocommit')
        assert isinstance(conn.autocommit, bool)

        # Test isolation_level property
        assert hasattr(conn, 'isolation_level')
        assert isinstance(conn.isolation_level, str)

        # Test connection is active
        assert conn.ping() == 1
    finally:
        conn.close()

def test_multiple_connections():
    """Test creating multiple connections simultaneously"""
    conn1 = _cubrid.connect(
        "CUBRID:localhost:33000:demodb:::",
        "dba",
        ""
    )
    conn2 = _cubrid.connect(
        "CUBRID:localhost:33000:demodb:::",
        "dba",
        ""
    )
    try:
        assert conn1 is not None
        assert conn2 is not None
        assert conn1 != conn2
    finally:
        conn1.close()
        conn2.close()

def test_connection_close():
    """Test connection close behavior"""
    conn = _cubrid.connect(
        "CUBRID:localhost:33000:demodb:::",
        "dba",
        ""
    )
    conn.close()
    
    # Verify operations on closed connection raise exceptions
    with pytest.raises(Error):
        conn.ping()

def test_connection_context():
    """Test connection state and context"""
    conn = _cubrid.connect(
        "CUBRID:localhost:33000:demodb:::",
        "dba",
        ""
    )
    try:
        # Test initial connection state
        assert conn.ping() == 1
        
        # Test transaction state
        conn.set_autocommit(False)
        assert not conn.autocommit
        
        # Test isolation level setting
        conn.set_isolation_level(_cubrid.CUBRID_SERIALIZABLE)
        assert conn.isolation_level == "CUBRID_SERIALIZABLE"
    finally:
        conn.close()

def test_connection_with_invalid_dsn():
    """Test connection with invalid DSN formats"""
    invalid_dsns = [
        "",  # Empty DSN
        "CUBRID:localhost",  # Incomplete DSN
        "INVALID:localhost:33000:demodb:::",  # Wrong protocol
        "CUBRID:localhost:invalid_port:demodb:::",  # Invalid port
        "CUBRID:nonexistent_host:33000:demodb:::"  # Non-existent host
    ]
    
    for dsn in invalid_dsns:
        with pytest.raises(Error):
            _cubrid.connect(dsn, "dba", "")

def test_connection_server_info():
    """Test server information after connection"""
    conn = _cubrid.connect(
        "CUBRID:localhost:33000:demodb:::",
        "dba",
        ""
    )
    try:
        # Test server version format
        version = conn.server_version()
        assert version is not None
        assert isinstance(version, str)
        assert len(version.split('.')) == 4  # major.minor.patch.build
        
        # Test client version format
        client_version = conn.client_version()
        assert client_version is not None
        assert isinstance(client_version, str)
        assert len(client_version.split('.')) == 4
    finally:
        conn.close()
