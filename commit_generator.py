# Please Do Not Use Unethically
# Modified for https://github.com/GitByMY/verge.git

import argparse
import os
from datetime import datetime, timedelta
from random import randint
from subprocess import Popen


def main():
    args = arguments()
    curr_date = datetime.now()
    directory = 'verge-' + curr_date.strftime('%Y-%m-%d-%H-%M-%S')
    repository = "https://github.com/GitByMY/verge.git"
    no_weekends = args.no_weekends
    frequency = args.frequency
    
    os.mkdir(directory)
    os.chdir(directory)
    run(['git', 'init'])
    start_date = curr_date.replace(hour=20, minute=0) - timedelta(days=365)
    
    for day in (start_date + timedelta(n) for n in range(365)):
        if (not no_weekends or day.weekday() < 5) and randint(0, 100) < frequency:
            for commit_time in (day + timedelta(minutes=m) for m in range(contributions_per_day(args))):
                contribute(commit_time)

    run(['git', 'remote', 'add', 'origin', repository])
    run(['git', 'branch', '-M', 'main'])
    run(['git', 'push', '-u', 'origin', 'main'])

    print('\nRepository generation \x1b[6;30;42mcompleted successfully\x1b[0m!')


def contribute(date):
    with open(os.path.join(os.getcwd(), 'README.md'), 'a') as file:
        file.write(message(date) + '\n')
    run(['git', 'add', '.'])
    run(['git', 'commit', '-m', f'"{message(date)}"', '--date', date.strftime('"%Y-%m-%d %H:%M:%S"')])


def run(commands):
    Popen(commands).wait()


def message(date):
    return date.strftime('Contribution: %Y-%m-%d %H:%M')


def contributions_per_day(args):
    max_c = args.max_commits
    max_c = min(max(max_c, 1), 20)  # Ensure max commits are between 1 and 20
    return randint(1, max_c)


def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-nw', '--no_weekends', action='store_true', default=False, help="Do not commit on weekends")
    parser.add_argument('-mc', '--max_commits', type=int, default=10, help="Maximum number of commits per day (1-20)")
    parser.add_argument('-fr', '--frequency', type=int, default=80, help="Frequency of commits in percentage (1-100)")
    return parser.parse_args()


if __name__ == "__main__":
    main()
