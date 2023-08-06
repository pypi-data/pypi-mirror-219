"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """YAMET."""


if __name__ == "__main__":
    main(prog_name="yamet")  # pragma: no cover
