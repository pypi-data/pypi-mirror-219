from rich import print
import typer

app = typer.Typer()


@app.command()
def main() -> None:
    print(
        "",
        "Mike Moran",
        "Data Scientist at [bold green]Duo Security[/bold green]",
        "",
        "Email :incoming_envelope-emoji:       mike@mkmrn.dev",
        "Gitlab :fox_face-emoji:      @mmoran0032",
        "Most socials:  @mmoran0032",
        "",
        sep="\n",
    )


if __name__ == "__main__":
    app()
