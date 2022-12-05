import json
import uuid

import requests
import typer
from playwright.sync_api import sync_playwright
from rich import print

from chatgpt import settings

app = typer.Typer()


@app.command()
def login(
    email: str, password: str = typer.Option(..., prompt=True, hide_input=True)
) -> None:
    """
    Login to OpenAI ChatGPT and set access token

    :params email: OpenAI email
    :params password: OpenAI account password
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
            print("[green]Successfully obtained session token[/green]")
            with open(settings.SETTINGS_PATH, "w") as s:
                json.dump(
                    {
                        "sessionToken": session_token,
                        "parentId": str(uuid.uuid4()),
                        "conversationId": None,
                    },
                    s,
                )
        browser.close()


@app.command()
def prompt(prompt: str) -> None:
    """
    Get ChatGPT prompt

    :params prompt: prompt to feed OpenAI
    """
    response = requests.post(
        "https://chat.openai.com/backend-api/conversation",
        headers={
            "Authorization": f"Bearer {settings.SESSION_TOKEN}",
        },
        json={
            "action": "next",
            "messages": [
                {
                    "id": str(uuid.uuid4()),
                    "role": "user",
                    "content": {"content_type": "text", "parts": [prompt]},
                }
            ],
            "conversation_id": settings.CONVERSATION_ID,
            "parent_message_id": settings.PARENT_ID,
            "model": "text-davinci-002-render",
        },
    ).json()
    print(response)
