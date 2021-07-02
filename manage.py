"""
Project management module.
"""

from sys import argv
import subprocess

from settings import config


def main():
    """
    Run administrative tasks.
    """
    script, command = argv
    print(f'Start with: {script}...')
    if command == 'makecleandata':
        launcher = subprocess.call(["venv/Scripts/python", f"{config.DATA_DIRECTORY}/data_cleaning.py"])
        print("Cleaning data...", launcher)


if __name__ == '__main__':
    main()
