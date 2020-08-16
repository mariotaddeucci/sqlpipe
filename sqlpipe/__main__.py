from os import getenv
from .SqlPipeBuilder import SqlPipeBuilder
import optparse

if __name__ == "__main__":
    parser = optparse.OptionParser()

    parser.add_option(
        '-d', '--directory',
        action="store", dest="directory",
        help="Direcotry to apply method map_directory. Is required"
    )

    parser.add_option(
        '-t', '--task',
        action="store", dest="task",
        help="Task Id to run", default=None
    )

    parser.add_option(
        '-l', '--limit',
        action="store", dest="limit",
        help="Limit connections pool.", default=20
    )

    options, args = parser.parse_args()

    if not options.directory:
        parser.error('Directory not given')

    pipe = SqlPipeBuilder(
        getenv('DATABASE_URL'),
        connections_limit=options.limit
    )
    pipe.map_directory(options.directory)
    pipe.execute(options.task)
