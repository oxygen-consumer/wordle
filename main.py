#!/usr/bin/env python3
from Controller.cli_ui import CLI
from Logic.game_logic import WordleServ
from Repository.default_repo import DefaultRepo

repo = DefaultRepo()
serv = WordleServ(repo)
ui = CLI(serv)


def main():
    ui.run_ui()


if __name__ == "__main__":
    main()
