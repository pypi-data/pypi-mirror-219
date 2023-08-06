import click
from huhk.case_project.version import version as _version


@click.command()
@click.option('-v', '--version', help='线索版本', default="$None$")
@click.option('-i', '--init', help='创建项目，参数项目key', prompt="$None$", required=False)
@click.option('-u', '--update', help='更新项目，参数项目key', default="$None$")
def main(version, init, update):
    """Simple program that greets NAME for a total of COUNT times."""
    if version:
        click.echo('版本：' + _version)
        click.echo(type(version))
    elif init:
        click.echo('init：' + _version)
        click.echo(type(init))
    elif update:
        click.echo('update：' + _version)
        click.echo(type(update))


if __name__ == '__main__':
    main()