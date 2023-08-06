
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

import click

from mojo.xmods.jsos import load_jsos_stream_from_file

HELP_RESULTS = "A folder containing test results to publish"
HELP_EXPIRY = "A number of days to persist the up uploaded results."

@click.command("create")
@click.option("--results", required=True, type=click.Path(exists=True, file_okay=False), help=HELP_RESULTS)
@click.argument('filename', metavar='<testrun document>', type=click.Path(dir_okay=False))
def command_pycis_document_testrun_create(results: str, filename: str):

    # Make sure the summary document and the tests document exists
    summary_file = os.path.join(results, "testrun_summary.json")
    testresults_file = os.path.join(results, "testrun_results.jsos")

    summary = None
    with open(summary_file, 'r') as sf:
        summary = json.load(sf)

    trstream = load_jsos_stream_from_file(testresults_file)

    document = {
        "dversion": "1.0",
        "dtype": "testrun",
        "resultitems": trstream
    }

    document.update(summary)


    with open(filename, 'w') as of:
        json.dump(document, of, indent=4)

    return