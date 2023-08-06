
__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

import sys

import click

from mojo.xmods.xclick import NORMALIZED_STRING

from pycis.cli.cmdtree.datastore.constants import PYCIS_DB_BYPRODUCTS

HELP_HOST = "A CouchDB host name."
HELP_PORT = "The CouchDB port number."
HELP_USERNAME = "The CouchDB username who can create a database."
HELP_PASSWORD = "The CouchDB password for the specified user."

MAP_TESTRUN_BY_BRANCH = """
function (doc) {
    if (doc.dtype == 'testrun') {
        if (doc.summary.build.branch && doc.summary.build.build)
        {
            key = doc.summary.build.branch
            value = { id: doc._id, summary: doc}
            emit(key, value);
        }
    }
}
"""

MAP_TESTRUN_BY_PIPELINE = """
function (doc) {
    if (doc.dtype == 'testrun') {
        if (doc.summary.pipeline.name && doc.summary.pipeline.id)
        {
            key = doc.summary.pipeline.id
            value = { id: doc._id, result: doc}
            emit(key, value);
        }
    }
}
"""

@click.command("initialize")
@click.option("--host", required=True, type=NORMALIZED_STRING, help=HELP_HOST)
@click.option("--port", required=True, type=click.INT, default=5984, help=HELP_PORT)
@click.option("--username", required=False, type=NORMALIZED_STRING, help=HELP_USERNAME)
@click.option("--password", required=False, type=NORMALIZED_STRING, help=HELP_PASSWORD)
def command_pycis_datastore_couchdb_initialize(
    host: str, port: int, username: str, password: str):
    
    try:
        import couchdb
    except ImportError:
        print("You must install 'CouchDB in order to be able to publish to a CouchDB data store.", file=sys.stderr)
        exit(1)
    
    protocol = "http"
    if host.find("http://") > -1 or host.find("https://") > -1:
        protocol, host = host.split("://", 1)

    connection = f"{host}:{port}"
    if username is not None:
        if password is None:
            errmsg = "A 'password' parameter must be specified if a username is provided."
            click.BadArgumentUsage(errmsg)
        connection = f"{username}:{password}@{connection}"
    
    connection = f"{protocol}://{connection}"

    dbsvr = couchdb.Server(connection)

    if 'testresults' not in dbsvr:

        database = dbsvr.create(PYCIS_DB_BYPRODUCTS)

        data = {
            "_id": f"_design/default",
            "views": {
                "testrun_by_branch": {
                    "map": MAP_TESTRUN_BY_BRANCH
                },
                "testrun_by_pipeline": {
                    "map": MAP_TESTRUN_BY_PIPELINE
                }
            },
            "language": "javascript",
            "options": {"partitioned": False }
        }

        database.save( data )

    return