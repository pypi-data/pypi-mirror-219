
__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

import click


from pycis.cli.cmdtree.document.testrun.create \
    import command_pycis_document_testrun_create


@click.group("testrun", help="Contains commands for creating a pycis 'testrun' document.")
def group_pycis_document_testrun():
    return

group_pycis_document_testrun.add_command(
    command_pycis_document_testrun_create
)