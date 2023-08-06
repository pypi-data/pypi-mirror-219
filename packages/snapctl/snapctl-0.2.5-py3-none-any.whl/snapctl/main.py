import typer

from snapctl.commands.byosnap import ByoSnap
from snapctl.types.definitions import ResponseType
from snapctl.utils.echo import error, success, info

app = typer.Typer()

# Commands
@app.callback()
def callback():
  """
  Snapser CLI Tool
  """

# command: Optional[str] = typer.Argument(None)
@app.command()
def byosnap(
  command: str = typer.Argument(..., help="BYOSnap Commands: " + ", ".join(ByoSnap.COMMANDS) + "."),
  path: str = typer.Argument(..., help="Path to your snap code"),
  tag: str = typer.Argument(..., help="Tag for your snap"),
  token: str = typer.Argument(..., help="Copy the token from the Web App"),
  docker_file: str = typer.Option("Dockerfile", help="Dockerfile name to use")
) -> None:
  """
    Bring your own Snap
  """
  byosnap: ByoSnap = ByoSnap(command, path, tag, token, docker_file)
  validate_input_response: ResponseType = byosnap.validate_input()
  if validate_input_response['error']:
    return error(validate_input_response['msg'])
  command_method = command.replace('-', '_')
  method: function = getattr(byosnap, command_method)
  if not method():
    return
  success(f"BYOSnap {command} complete :oncoming_fist:")

# @app.command()
# def byow():
#   """
#   Bring your own workstation
#   """
#   typer.echo("Connecting to your cluster")