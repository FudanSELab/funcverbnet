"""Console script for funcverbnet."""
import sys
import click


@click.command()
def main(args=None):
    """Console script for funcverbnet."""
    click.echo(
        "FuncVerbNet provides a knowledge system constructed from functionality categories, verbs, and "
        "phrase patterns, as well as functionality for fine-grained analysis of functionality descriptions "
        "based on this knowledge system."
        )
    # click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
