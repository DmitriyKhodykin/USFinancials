"""
Project management module.
"""

from sys import argv

from data import data_cleaning as makecleandata


def main():
    """
    Run administrative tasks.
    """
    script, command = argv
    print(f'Start with: {script}...')
    if command == 'makecleandata':
        makecleandata.main()


if __name__ == '__main__':
    main()
