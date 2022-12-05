import typer
from playwright.sync_api import sync_playwright
from rich import print

app = typer.Typer()


@app.command()
def login(
    email: str, password: str = typer.Option(..., prompt=True, hide_input=True)
) -> None:
    """
    Login to OpenAI ChatGPT and set access token
    """
    with sync_playwright() as p:
        browser = p.webkit.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://chat.openai.com/auth/login")
        page.get_by_role("button", name="Log in").click()
        page.get_by_label("Email address").fill(email)
        page.locator('button[name="action"]').click()
        page.get_by_label("Password").click()
        page.get_by_label("Password").fill(password)
        page.get_by_role("button", name="Continue").click()
        with page.expect_response("**/auth/session", timeout=3000):
            cookies = context.cookies()
            session_token = [
                cookie["value"]
                for cookie in cookies
                if cookie["name"] == "__Secure-next-auth.session-token"
            ][0]
            print(f"Session token: {session_token}")
        browser.close()


@app.command()
def reset() -> None:
    """
    Reset conversation with ChatGPT
    """


if __name__ == "__main__":
    app()
