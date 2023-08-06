import base64
import os
import requests
import subprocess
from rich.progress import Progress, SpinnerColumn, TextColumn
from sys import platform

from snapctl.types.definitions import ResponseType
from snapctl.utils.echo import error, success, info

class ByoSnap:
  COMMANDS = ['build', 'push', 'upload-docs', 'publish']

  def __init__(self, command: str, path: str, tag: str, token: str, dockerfile: str = 'Dockerfile') -> None:
    self.command: str = command
    self.path: str = path
    self.tag: str = tag
    self.token: str = token
    self.token_parts: list = ByoSnap.get_token_values(token)
    self.dockerfile = dockerfile

  @staticmethod
  def get_token_values(token: str) -> None | list:
    try:
      input_token = base64.b64decode(token).decode('ascii')
      token_parts = input_token.split('|')
      # url|web_app_token|service_id|ecr_repo_url|ecr_repo_username|ecr_repo_token
      # url = self.token_parts[0]
      # web_app_token = self.token_parts[1]
      # service_id = self.token_parts[2]
      # ecr_repo_url = self.token_parts[3]
      # ecr_repo_username = self.token_parts[4]
      # ecr_repo_token = self.token_parts[5]
      if len(token_parts) == 6:
        return token_parts
    except Exception:
      pass
    return None

  def validate_input(self) -> ResponseType:
    response: ResponseType = {
      'error': True,
      'msg': '',
      'data': []
    }
    # Check command
    if not self.command in ByoSnap.COMMANDS:
      response['msg'] = f"Invalid command. Valid commands are {', '.join(ByoSnap.COMMANDS['byosnap'])}."
      return response
    # Check path
    if not os.path.isfile(f"{self.path}/{self.dockerfile}"):
      response['msg'] = f"Unable to find {self.dockerfile} at path {self.path}"
      return response
    # Check tag
    if len(self.tag.split()) > 1 or len(self.tag) > 25:
      response['msg'] = f"Tag should be a single word with maximum of 25 characters"
      return response
    # Check the token
    if self.token_parts is None:
      response['msg'] = 'Invalid token. Please reach out to your support team.'
      return response
    # Send success
    response['error'] = False
    return response

  def build(self) -> bool:
    # Get the data
    # url = self.token_parts[0]
    # web_app_token = self.token_parts[1]
    service_id = self.token_parts[2]
    ecr_repo_url = self.token_parts[3]
    ecr_repo_username = self.token_parts[4]
    ecr_repo_token = self.token_parts[5]
    image_tag = f'{service_id}.{self.tag}'
    full_ecr_repo_url = f'{ecr_repo_url}:{image_tag}'
    try:
      # Check dependencies
      with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
      ) as progress:
        progress.add_task(description=f'Checking dependencies...', total=None)
        try:
          subprocess.run([
            "docker", "--version"
          ], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        except:
          error('Docker not present')
          return False
      success('Dependencies Verified')

      # Login to Snapser Registry
      with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
      ) as progress:
        progress.add_task(description=f'Logging into Snapser Image Registry...', total=None)
        if platform == 'win32':
          response = subprocess.run([
            'docker', 'login', '--username', ecr_repo_username, '--password', ecr_repo_token, ecr_repo_url
          ], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        else:
          response = subprocess.run([
            f'echo "{ecr_repo_token}" | docker login --username {ecr_repo_username} --password-stdin {ecr_repo_url}'
          ], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        if response.returncode:
          error('Unable to connect to the Snapser Container Repository. Please get the latest token from the Web app.')
          return False
      success('Login Successful')

      # Build your snap
      with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
      ) as progress:
        progress.add_task(description=f'Building your snap...', total=None)
        if platform == "win32":
          response = subprocess.run([
            #f"docker build --no-cache -t {tag} {path}"
            'docker', 'build', '--platform', 'linux/arm64', '-t', image_tag, self.path
          ], shell=True, )#stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        else:
          response = subprocess.run([
            #f"docker build --no-cache -t {tag} {path}"
            f"docker build --platform linux/arm64 -t {image_tag} {self.path}"
          ], shell=True, )#stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        if response.returncode:
          error('Unable to build docker.')
          return False
      success('Build Successfull')

      # Tag the repo
      with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
      ) as progress:
        progress.add_task(description=f'Tagging your snap...', total=None)
        if platform == "win32":
           response = subprocess.run([
            'docker', 'tag', image_tag, full_ecr_repo_url
          ], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        else:
          response = subprocess.run([
            f"docker tag {image_tag} {full_ecr_repo_url}"
          ], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        if response.returncode:
          error('Unable to tag your snap.')
          return False
      success('Tag Successfull')

      return True
    except:
      error('CLI Error')
      return False

  def push(self) -> bool:
    # url = self.token_parts[0]
    # web_app_token = self.token_parts[1]
    service_id = self.token_parts[2]
    ecr_repo_url = self.token_parts[3]
    image_tag = f'{service_id}.{self.tag}'
    full_ecr_repo_url = f'{ecr_repo_url}:{image_tag}'
    # ecr_repo_username = self.token_parts[4]
    # ecr_repo_token = self.token_parts[5]

    # Push the image
    with Progress(
      SpinnerColumn(),
      TextColumn("[progress.description]{task.description}"),
      transient=True,
    ) as progress:
      progress.add_task(description=f'Pushing your snap...', total=None)
      if platform == "win32":
        response = subprocess.run([
          'docker', 'push', full_ecr_repo_url
        ], shell=True, )#stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
      else:
        response = subprocess.run([
          f"docker push {full_ecr_repo_url}"
        ], shell=True, )#stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
      if response.returncode:
        error('Unable to push your snap.')
        return False
    success('Snap Upload Successfull')
    return True

  def upload_docs(self) -> bool:
    '''
      Note this step is optional hence we always respond with a True
    '''
    url = self.token_parts[0]
    web_app_token = self.token_parts[1]
    service_id = self.token_parts[2]
    ecr_repo_url = self.token_parts[3]
    ecr_repo_username = self.token_parts[4]
    ecr_repo_token = self.token_parts[5]

    # Push the swagger.json
    with Progress(
      SpinnerColumn(),
      TextColumn("[progress.description]{task.description}"),
      transient=True,
    ) as progress:
      progress.add_task(description=f'Uploading your API Json...', total=None)
      try:
        dfile = open(f"{self.path}/swagger.json", "rb")
        test_res = requests.post(f"{url}/{self.tag}/openapispec", files = {"attachment": dfile}, headers={'Token': web_app_token})
        if test_res.ok:
          success('Uploaded Swagger.json')
        else:
          error(test_res.status_code)
          response_json = test_res.json()
          error(response_json['details'][0])
      except Exception as e:
        info('Unable to find swagger.json at ' + self.path + str(e))

    # Push the README.md
    with Progress(
      SpinnerColumn(),
      TextColumn("[progress.description]{task.description}"),
      transient=True,
    ) as progress:
      progress.add_task(description=f'Uploading your README...', total=None)
      try:
        dfile = open(f"{self.path}/README.md", "rb")
        test_res = requests.post(f"{url}/{self.tag}/markdown", files = {"attachment": dfile}, headers={'Token': web_app_token})
        if test_res.ok:
          success('Uploaded README.md')
        else:
          error('Unable to upload your README.md')
      except:
        info('Unable to find README.md at ' + self.path)
    return True

  def publish(self) -> None:
    if not self.build() or not self.push() or not self.upload_docs():
      return False
    return True
