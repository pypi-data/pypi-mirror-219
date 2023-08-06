import os
import subprocess
import sys
import webbrowser
from pathlib import Path
from typing import Optional

import typer

from .config import logger
from .utils import find_zit_root

dashboard_app = app = typer.Typer(name="dashboard", help="Dashboard commands")


class SubprocessError(Exception):
    def __init__(self, returncode, stderr, cmd):
        self.returncode = returncode
        self.stderr = stderr
        self.cmd = cmd
        super().__init__(f"Error running command: {' '.join(cmd)}\n{stderr}")


def run_subprocess(command, cwd=None, capture_stdout=True, shell=False, env=None, wait=True):
    process = subprocess.Popen(
        command,
        stdout=None if capture_stdout else subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
        cwd=cwd,
        shell=shell,
        env=env,
    )

    if not wait:
        return process

    _, stderr = process.communicate()

    if process.returncode:
        raise SubprocessError(process.returncode, stderr, command)

    return process


def is_git_repo(path: Path):
    try:
        run_subprocess(["git", "-C", str(path), "rev-parse"], capture_stdout=False)
        return True
    except SubprocessError:
        return False


def clone_zlens_repo(path: Path):
    if is_git_repo(path):
        try:
            logger.info("Updating zlens repository...")
            run_subprocess(["git", "-C", str(path), "pull"])
        except SubprocessError as e:
            logger.info(f"Error updating zlens repository: {e}")
            sys.exit(1)
    else:
        try:
            logger.info("Cloning zlens repository...")
            run_subprocess(["git", "clone", "git@github.com:ZitySpace/zlens.git", str(path)])
        except SubprocessError as e:
            logger.info(f"Error cloning zlens repository: {e}")
            sys.exit(1)


def has_npm():
    try:
        run_subprocess(["npm", "-v"], capture_stdout=False)
        return True
    except FileNotFoundError:
        return False


def check_and_install_poetry():
    try:
        # Check if poetry is already installed
        run_subprocess(["poetry", "--version"], cwd=None, capture_stdout=False)
        logger.info("Poetry is already installed.")
    except FileNotFoundError:
        yes = typer.prompt("Poetry not found. Do you want to install it?", type=bool)
        if not yes:
            logger.info('Please install poetry manually and re-run "zit dashboard install".')

        # Check the Python version
        major_version = sys.version_info.major
        minor_version = sys.version_info.minor

        # Installation command for Poetry
        install_command = f"curl -sSL https://install.python-poetry.org | python{major_version}.{minor_version} -"

        try:
            # Run the installation command
            run_subprocess(install_command, cwd=None, shell=True)
            logger.info("Poetry has been installed successfully.")
        except SubprocessError as e:
            logger.error("Error installing Poetry:")
            logger.error(e.stderr)


def check_and_install_pnpm():
    if not has_npm():
        logger.info('NPM is not installed. Please install Node.js and NPM manually and re-run "zit dashboard install".')
        return

    try:
        run_subprocess(["pnpm", "--version"], cwd=None, capture_stdout=False)
        logger.info("pnpm is already installed.")
    except FileNotFoundError:
        logger.info("pnpm not found. Installing pnpm...")
        install_command = "npm install -g pnpm"

        try:
            run_subprocess(install_command, cwd=None, shell=True)
            logger.info("pnpm has been installed successfully.")
        except SubprocessError as e:
            logger.error("Error installing pnpm:")
            logger.error(e.stderr)


def install_zlens_dependencies(path: Path):
    api_path = path / "api"
    ui_path = path / "ui"

    check_and_install_poetry()
    logger.info("Installing zlens API dependencies...")
    try:
        new_env = os.environ.copy()
        new_env.pop("VIRTUAL_ENV", None)

        run_subprocess(["poetry", "install"], cwd=str(api_path), env=new_env)
    except SubprocessError as e:
        logger.error("Error installing zlens API dependencies:")
        logger.error(e.stderr)
        sys.exit(1)

    check_and_install_pnpm()
    logger.info("Installing zlens UI dependencies...")
    try:
        run_subprocess(["pnpm", "install"], cwd=str(ui_path))
    except SubprocessError as e:
        logger.error("Error installing zlens UI dependencies:")
        logger.error(e.stderr)
        sys.exit(1)


def create_database_tables(path: Path):
    api_path = path / "api"
    venv_path = api_path / ".venv"
    python_executable = (
        venv_path / "bin" / "python" if sys.platform != "win32" else venv_path / "Scripts" / "python.exe"
    )
    logger.info("Creating database tables...")
    try:
        run_subprocess(
            [str(python_executable), "-m", "alembic", "upgrade", "head"],
            cwd=str(api_path),
        )
    except SubprocessError as e:
        logger.error("Error creating database tables:")
        logger.error(e.stderr)
        sys.exit(1)


@app.command(name="install", help="Install dashboard")
def install():
    logger.info("Installing dashboard: ")

    zit_root = find_zit_root(Path.cwd())
    zlens_path = zit_root / ".zit" / "zlens"
    os.makedirs(zlens_path, exist_ok=True)

    clone_zlens_repo(zlens_path)
    install_zlens_dependencies(zlens_path)
    create_database_tables(zlens_path)


def start_api_service(api_path: Path, port: int):
    venv_path = api_path / ".venv"
    python_executable = (
        venv_path / "bin" / "python" if sys.platform != "win32" else venv_path / "Scripts" / "python.exe"
    )

    env = os.environ.copy()
    env.pop("http_proxy", None)
    env.pop("https_proxy", None)
    env.pop("all_proxy", None)
    env.pop("HTTP_PROXY", None)
    env.pop("HTTPS_PROXY", None)
    env.pop("ALL_PROXY", None)

    command = [
        str(python_executable),
        "-m",
        "uvicorn",
        "app.api.serv:app",
        "--host",
        "0.0.0.0",
        "--port",
        str(port),
        "--reload",
    ]
    return run_subprocess(command, cwd=str(api_path), capture_stdout=True, env=env, wait=False)


def start_ui_service(ui_path: Path, port: int, api_port: Optional[int] = None):
    env = os.environ.copy()
    env["PORT"] = str(port)

    if api_port:
        env["NEXT_PUBLIC_API_PORT"] = str(api_port)

    command = ["pnpm", "run", "dev"]
    return run_subprocess(command, cwd=str(ui_path), capture_stdout=True, env=env, wait=False)


def start_celery_service(api_path: Path, port: int = 5672):
    venv_path = api_path / ".venv"
    python_executable = (
        venv_path / "bin" / "python" if sys.platform != "win32" else venv_path / "Scripts" / "python.exe"
    )

    # ensure that the python executable used in the subprocess is the one from zlens api venv
    # otherwise, it will be the one from the current activated venv
    env = os.environ.copy()
    env.pop("http_proxy", None)
    env.pop("https_proxy", None)
    env.pop("all_proxy", None)
    env.pop("HTTP_PROXY", None)
    env.pop("HTTPS_PROXY", None)
    env.pop("ALL_PROXY", None)
    env["PATH"] = str(venv_path / "bin") + os.pathsep + env["PATH"]

    command = [
        str(python_executable),
        "-m",
        "celery",
        "-A",
        "app.utils.taskqueue.worker.appFormula",
        "worker",
        "--loglevel=INFO",
        "--pool=processes",
        "--hostname=formulaWorker",
        "--queues",
        "formulaQ",
    ]
    return run_subprocess(command, cwd=str(api_path), capture_stdout=True, env=env, wait=False)


@app.command(name="show", help="Open dashboard")
def show(
    api_port: int = typer.Option(60000, help="Port number for the API service"),
    ui_port: int = typer.Option(60001, help="Port number for the UI service"),
):
    zit_root = find_zit_root(Path.cwd())
    zlens_path = zit_root / ".zit" / "zlens"
    api_path = zlens_path / "api"
    ui_path = zlens_path / "ui"

    try:
        api_process = start_api_service(api_path, api_port)
        ui_process = start_ui_service(ui_path, ui_port, api_port)
        celery_process = start_celery_service(api_path)

        webbrowser.open(f"http://localhost:{ui_port}")

        api_process.wait()
        ui_process.wait()
        celery_process.wait()
    except KeyboardInterrupt:
        print("Dashboard stopped.")
    finally:
        api_process.terminate()
        ui_process.terminate()
        celery_process.terminate()
        sys.exit(0)
