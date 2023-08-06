import httpx
import typer

from .config import AUTH_PUBLIC_ENDPOINT, ZITRC_FILE, logger

auth_app = app = typer.Typer(name="auth", help="Auth commands")


def authenticate(token: str = None):
    if not token:
        if not ZITRC_FILE.exists():
            return False

        with ZITRC_FILE.open("r") as f:
            token = f.read()

    with httpx.Client() as client:
        try:
            r = client.get(
                f"{AUTH_PUBLIC_ENDPOINT}/whoami",
                headers={"Authorization": f"Bearer {token}"},
            )
        except httpx.ConnectError:
            return False

        if r.status_code != 200:
            return False

        user = r.json()
        return user


@app.command(name="login", help="Zit login")
def login():
    api_key = typer.prompt("Enter your Zit API key", hide_input=True)

    # Validate the API key
    user = authenticate(api_key)
    if not user:
        logger.info("Login failed. Please check your API key and try again.")
        return

    # Store the API key in the .zitrc file
    with ZITRC_FILE.open("w") as f:
        f.write(api_key)

    # Set the file permissions to be readable and writable only by the owner
    ZITRC_FILE.chmod(0o600)

    logger.info("Login successfully.")


@app.command(name="logout", help="Zit logout")
def logout():
    if ZITRC_FILE.exists():
        ZITRC_FILE.unlink()  # Delete the .zitrc file
        logger.info("Logout successful. Your API key has been removed.")
    else:
        logger.info("You are not currently logged in.")
