import sys

from actions import action_dispatcher
from library import Library


def main():
    library = Library()
    with library.lock():
        while (action:= input('Введите команду для работы: ')) != "exit":
            if action in action_dispatcher:
                action_dispatcher[action](library)
            else:
                print('Команда не распознана.')


if __name__ == "__main__":
    sys.exit(main())
