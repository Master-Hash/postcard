#!/usr/bin/env python3
# coding=utf8

# 这个文件显然不能叫做 locale.py，
# locale 是 builtin-module（

import subprocess
import typer

app = typer.Typer()


@app.command()
def extract() -> None:
    subprocess.run(
        args=[
            "pybabel",
            "-v",
            "extract",
            "-F",
            "babel-mapping.ini",
            "-o",
            "locale/messages.pot",
            ".",
        ]
    )


@app.command()
def init(locale: str) -> None:
    subprocess.run(
        args=[
            "pybabel",
            "-v",
            "init",
            "-l",
            locale,
            "-i",
            "locale/messages.pot",
            "-d",
            "locale",
        ],
    )


@app.command()
def update() -> None:
    subprocess.run(
        args=[
            "pybabel",
            "-v",
            "update",
            "-i",
            "locale/messages.pot",
            "-d",
            "locale",
        ]
    )


@app.command()
def compile() -> None:
    subprocess.run(
        args=[
            "pybabel",
            "-v",
            "compile",
            "-d",
            "locale",
        ]
    )


if __name__ == "__main__":
    app()
