"""
Project management module.
"""

from sys import argv

from data import data_cleaning as makecleandata
from features import features_engineering as makefeatures


def main():
    """
    Run administrative tasks.
    """
    script, command = argv
    print(f'Start with: {script}...')

    if command == 'makecleandata':
        makecleandata.main()
    elif command == 'makefeatures':
        makefeatures.main()


if __name__ == '__main__':
    main()
