#!/usr/bin/env python
# encoding: utf-8

import argparse
import datetime

from launchpadlib.launchpad import Launchpad
from launchpadlib.uris import LPNET_SERVICE_ROOT


def get_all_bugs(project, use_edge):
    service_root = 'edge' if use_edge else LPNET_SERVICE_ROOT
    lp = Launchpad.login_anonymously('lpbugs2githubissues', service_root)
    project = lp.projects[project]

    states = [
        "Won't Fix",
        'Confirmed',
        'Expired',
        'Fix Committed',
        'Fix Released',
        'In Progress',
        'Incomplete (with response)',
        'Incomplete (without response)',
        'Incomplete',
        'Invalid',
        'New',
        'Opinion',
        'Triaged',
    ]

    tasks = project.searchTasks(search_text='', status=states)
    from IPython import embed; embed()
    print '#sirver len(tasks): %r\n' % (len(tasks))

    # return {
    # "New": stats[0],
    # "Incomplete": sum(stats[1:4]),
    # "Invalid": stats[4],
    # "Won't Fix": stats[5],
    # "Confirmed": stats[6],
    # "Triaged": stats[7],
    # "In Progress": stats[8],
    # "Fix Committed": stats[9],
    # "Fix Released": stats[10],
    # }


def parse_args():
    p = argparse.ArgumentParser(description='Download bugs from launchpad and saves them to JSON files.'
                                )

    p.add_argument('-e', '--edge', action='store_true',
                   default=False, help='Use launchpad edge instead.')
    p.add_argument(
        '-p', '--project', type=str, help='Project to fetch bugs for.')

    args = p.parse_args()
    if args.project is None:
        p.error('Need --project.')

    return args


def main():
    args = parse_args()

    s = get_all_bugs(args.project, args.edge)
    f = open('stats.db', 'a')
    f.write('%s,%i,%i,%i,%i,%i,%i,%i,%i,%i\n' % (
        datetime.date.today().strftime('%d.%m.%Y'),
        s['New'],
        s['Incomplete'],
        s['Invalid'],
        s["Won't Fix"],
        s['Confirmed'],
        s['Triaged'],
        s['In Progress'],
        s['Fix Committed'],
        s['Fix Released'],)
    )
    f.close()


if __name__ == '__main__':
    import sys
    sys.exit(main())
