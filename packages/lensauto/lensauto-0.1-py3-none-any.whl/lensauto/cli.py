# lensauto/cli.py
import click


@click.group()
def main():
    pass


@main.command()
def sayhi():
    print("hello world")


if __name__ == "__main__":
    main()
