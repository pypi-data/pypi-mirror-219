
__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

import json
import os
import sys

from datetime import datetime, timedelta

import click

from mojo.xmods.xclick import NORMALIZED_STRING

from pycis.cli.cmdtree.datastore.constants import PYCIS_DB_BYPRODUCTS

HELP_HOST = "A CouchDB host name."
HELP_PORT = "The CouchDB port number."
HELP_USERNAME = "The CouchDB username who can write to a database."
HELP_PASSWORD = "The CouchDB password for the specified user."
HELP_EXPIRY = "A number of days to persist the up uploaded results."
HELP_FILENAME = "The document to publish."

@click.command("publish")
@click.option("--host", required=True, type=NORMALIZED_STRING, help=HELP_HOST)
@click.option("--port", required=True, type=click.INT, default=5984, help=HELP_PORT)
@click.option("--username", required=False, type=NORMALIZED_STRING, help=HELP_USERNAME)
@click.option("--password", required=False, type=NORMALIZED_STRING, help=HELP_PASSWORD)
@click.option("--expiry-days", required=False, type=click.INT, default=365, help=HELP_EXPIRY)
@click.argument('filename', metavar='<document>', type=click.Path(dir_okay=False))
def command_pycis_datastore_couchdb_publish(
    host: str, port: int, username: str, password: str, expiry_days: int, filename: str):
    
    try:
        import couchdb
    except ImportError:
        print("You must install 'CouchDB' in order to be able to publish to a CouchDB data store.", file=sys.stderr)
        exit(1)

    if not os.path.exists(filename):
        errmsg = f"The specified document does not exist. filename={filename}"
        click.BadParameter(errmsg)
    
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

    expiry_date = datetime.now() + timedelta(days=expiry_days)

    docobj = None
    with open(filename, 'r') as sf:
        docobj = json.load(sf)

    docobj["expiry_date"] = expiry_date.isoformat()

    dbsvr = couchdb.Server(connection)

    pycis = dbsvr[PYCIS_DB_BYPRODUCTS]
    pycis.save(docobj)

    return