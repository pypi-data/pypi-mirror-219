from subprocess import Popen, PIPE, run, CalledProcessError
from pathlib import Path
from sys import stdout
from os import chmod, environ
from json import load, dumps
import yaml
from pkg_resources import resource_string


class ResourceApi:
    def read_resource(self, path: str) -> bytes:
        return resource_string("ddadevops", path)


class FileApi:
    def __init__(self):
        self.execution_api = ExecutionApi()

    def clean_dir(self, directory: str):
        self.execution_api.execute("rm -rf " + directory)
        self.execution_api.execute("mkdir -p " + directory)

    def cp(self, src: str, target_dir: str, check=True):
        self.execution_api.execute(f"cp {src} {target_dir}", check=check)

    def cp_force(self, src: str, target_dir: str, check=True):
        self.execution_api.execute(f"cp -f {src}* {target_dir}", check=check)

    def cp_recursive(self, src: str, target_dir: str, check=True):
        self.execution_api.execute(f"cp -r {src} {target_dir}", check=check)

    def write_data_to_file(self, path: Path, data: bytes):
        with open(path, "w", encoding="utf-8") as output_file:
            output_file.write(data.decode(stdout.encoding))

    def write_yaml_to_file(self, path: Path, data: map):
        with open(path, "w", encoding="utf-8") as output_file:
            yaml.dump(data, output_file)
        chmod(path, 0o600)

    def write_json_to_file(self, path: Path, data: map):
        with open(path, "w", encoding="utf-8") as output_file:
            output_file.write(dumps(data))
        chmod(path, 0o600)

    def read_json_fro_file(self, path: Path) -> map:
        with open(path, "r", encoding="utf-8") as input_file:
            return load(input_file)


class ImageApi:
    def __init__(self):
        self.execution_api = ExecutionApi()

    def image(self, name: str, path: Path):
        self.execution_api.execute_handled(
            f"docker build -t {name} --file {path}/image/Dockerfile {path}/image"
        )

    def drun(self, name: str):
        self.execution_api.execute_handled(
            f'docker run -it --entrypoint="" {name} /bin/bash'
        )

    def dockerhub_login(self, username: str, password: str):
        self.execution_api.execute_handled(
            f"docker login --username {username} --password {password}"
        )

    def dockerhub_publish(self, name: str, username: str, tag=None):
        if tag is not None:
            self.execution_api.execute_handled(
                f"docker tag {name} {username}/{name}:{tag}"
            )
            self.execution_api.execute_handled(
                f"docker push {username}/{name}:{tag}"
            )
        self.execution_api.execute_handled(
            f"docker tag {name} {username}/{name}:latest"
        )
        self.execution_api.execute_handled(
            f"docker push {username}/{name}:latest"
        )

    def test(self, name: str, path: Path):
        self.execution_api.execute_handled(
            f"docker build -t {name} -test --file {path}/test/Dockerfile {path}/test"
        )


class ExecutionApi:
    def execute(self, command: str, dry_run=False, shell=True, check=True):
        output = ""
        if dry_run:
            print(command)
        else:
            # output = check_output(command, encoding="UTF-8", shell=shell)
            output = run(
                command, encoding="UTF-8", shell=shell, stdout=PIPE, check=check
            ).stdout
            output = output.rstrip()
        return output

    def execute_live(self, command: str, dry_run=False, shell=True):
        if dry_run:
            print(command)
        else:
            process = Popen(command, stdout=PIPE, shell=shell)
            for line in iter(process.stdout.readline, b""):
                print(line.decode("utf-8"), end="")
            process.stdout.close()
            process.wait()

    def execute_handled(self, command: str, dry_run=False, shell=True, check=True):
        if dry_run:
            print(command)
        else:
            try:
                run(
                    command,
                    shell=shell,
                    check=check,
                    stderr=PIPE,
                    text=True)
            except CalledProcessError as exc:
                print("Command failed with code: ", exc.returncode, " and message:", exc.stderr)
                raise exc


class EnvironmentApi:
    def get(self, key):
        return environ.get(key)


class CredentialsApi:
    def __init__(self):
        self.execution_api = ExecutionApi()

    def gopass_field_from_path(self, path, field):
        credential = None
        if path and field:
            print("get field for: " + path + ", " + field)
            credential = self.execution_api.execute(
                ["gopass", "show", path, field], shell=False
            )
        return credential

    def gopass_password_from_path(self, path):
        credential = None
        if path:
            print("get password for: " + path)
            credential = self.execution_api.execute(
                ["gopass", "show", "--password", path], shell=False
            )
        return credential


class GitApi:
    def __init__(self):
        self.execution_api = ExecutionApi()

    # pylint: disable=invalid-name
    def get_latest_n_commits(self, n: int):
        return self.execution_api.execute(f'git log --oneline --format="%s %b" -n {n}')

    def get_latest_commit(self):
        return self.get_latest_n_commits(1)

    def tag_annotated(self, annotation: str, message: str, count: int):
        return self.execution_api.execute(
            f"git tag -a {annotation} -m '{message}' HEAD~{count}"
        )

    def tag_annotated_second_last(self, annotation: str, message: str):
        return self.tag_annotated(annotation, message, 1)

    def get_latest_tag(self):
        return self.execution_api.execute("git describe --tags --abbrev=0")

    def get_current_branch(self):
        return "".join(self.execution_api.execute("git branch --show-current")).rstrip()

    def init(self, default_branch: str = "main"):
        self.execution_api.execute("git init")
        self.execution_api.execute(f"git checkout -b {default_branch}")

    def set_user_config(self, email: str, name: str):
        self.execution_api.execute(f"git config user.email {email}")
        self.execution_api.execute(f"git config user.name {name}")

    def add_file(self, file_path: Path):
        return self.execution_api.execute(f"git add {file_path}")

    def add_remote(self, origin: str, url: str):
        return self.execution_api.execute(f"git remote add {origin} {url}")

    def commit(self, commit_message: str):
        return self.execution_api.execute(f'git commit -m "{commit_message}"')

    def push(self):
        return self.execution_api.execute("git push")

    def push_follow_tags(self):
        return self.execution_api.execute("git push --follow-tags")

    def checkout(self, branch: str):
        return self.execution_api.execute(f"git checkout {branch}")


class TerraformApi:
    pass
