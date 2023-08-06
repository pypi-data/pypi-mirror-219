
__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

import click

from pycis.cli.cmdtree.document.build \
    import group_pycis_document_build
from pycis.cli.cmdtree.document.testrun \
    import group_pycis_document_testrun


@click.group("document", help="Contains commands for writing data to a pycis document.")
def group_pycis_document():
    return

group_pycis_document.add_command(
    group_pycis_document_build
)
group_pycis_document.add_command(
    group_pycis_document_testrun
)