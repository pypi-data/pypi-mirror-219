import click
from dataclasses import dataclass

from entail import TestEnv


@dataclass
class CliCtx:
    test_home: str


@click.group()
@click.option('--test_home', envvar='ENTAIL_BASE', default='entail_tests')
@click.pass_context
def cli(ctx, test_home):
    ctx.obj = CliCtx(test_home)


@cli.command()
@click.option('--name', default=None, help='Name of the test to run')
@click.option('--file', default=None, help='Path to the test file')
@click.option('--tag', default=None, help='tag of tests')
def run(name, file, tag):
    te = TestEnv()


@cli.command()
def init():
    pass


if __name__ == '__main__':
    cli()
