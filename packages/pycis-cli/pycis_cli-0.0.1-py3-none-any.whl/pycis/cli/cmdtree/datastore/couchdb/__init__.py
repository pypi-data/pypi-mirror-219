
__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

import click

from pycis.cli.cmdtree.datastore.couchdb.initialize \
    import command_pycis_datastore_couchdb_initialize
from pycis.cli.cmdtree.datastore.couchdb.publish \
    import command_pycis_datastore_couchdb_publish


@click.group("couchdb", help="Contains commands datastore test results to CouchDB.")
def group_pycis_datastore_couchdb():
    return

group_pycis_datastore_couchdb.add_command(command_pycis_datastore_couchdb_initialize)
group_pycis_datastore_couchdb.add_command(command_pycis_datastore_couchdb_publish)
