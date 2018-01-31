"""AlayaNotes

Usage:
  main.py [run]
  main.py initdb
  main.py completed
"""
from docopt import docopt
import subprocess
import os

from alayatodo import app


def _run_sql(filename):
    try:
        subprocess.check_output(
            "sqlite3 %s < %s" % (app.config['DATABASE'], filename),
            stderr=subprocess.STDOUT,
            shell=True
        )
    except subprocess.CalledProcessError, ex:
        print ex.output


if __name__ == '__main__':
    args = docopt(__doc__)
    if args['initdb']:
        _run_sql('resources/database.sql')
        _run_sql('resources/fixtures.sql')
        print "AlayaTodo: Database initialized."
    ##Perform a migration if completed keyowrd is used
    if args['completed']:
        _run_sql('resources/completed.sql')
        print "AlayaTodo: Database migration done!."
    else:
        app.run(use_reloader=True)
