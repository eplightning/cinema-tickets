from flask import g
from cinema_tickets.app import app
from cassandra.cluster import Cluster
from werkzeug.local import LocalProxy

def get_cassandra_session():
    sess = getattr(g, '_cass_session', None)

    if sess is None:
        cl = Cluster([app.config['CASSANDRA_CLUSTER']])
        sess = g._cass_session = cl.connect(app.config['CASSANDRA_KEYSPACE'])
    
    return sess

@app.teardown_appcontext
def teardown_cass(exception):
    sess = getattr(g, '_cass_session', None)

    if sess is not None:
        sess.shutdown()

db_session = LocalProxy(get_cassandra_session)
