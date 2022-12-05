import typer

app = typer.Typer()

@app.command()
def login() -> None:
    """
    Login to OpenAI ChatGPT and set access token
    """


@app.command()
def reset() -> None:
    """
    Reset conversation with ChatGPT
    """


if __name__ == "__main__":
    app()
