"""
# QALITA (c) COPYRIGHT 2023 - ALL RIGHTS RESERVED -
"""
import sys
import os
import json
import base64
import yaml
import click

from qalita.internal.logger import init_logging

logger = init_logging()


class CustomContext(click.Context):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.help_option_names = ["-h", "--help"]


# Config to pass to the commands
class Config(object):
    agent_data_file_name = ".agent"

    def save_source_config(self):
        with open("qalita-conf.yaml", "w") as file:
            yaml.dump(self.config, file)

    def load_source_config(self):
        try:
            with open("qalita-conf.yaml", "r") as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            logger.warning("Configuration file not found, creating a new one.")
            self.config = {"version": 1, "sources": []}
            self.save_source_config()
            return self.config
        except Exception as e:
            logger.warning(
                f"An unexpected error occurred while loading the configuration: {e}"
            )
            self.config = {"version": 1, "sources": []}
            self.save_source_config()
            return self.config

    def save_agent_config(self, data):
        """Save the agent config in file to persist between context"""
        with open(self.agent_data_file_name, "wb") as file:  # open in binary mode
            json_str = json.dumps(data, indent=4)  # convert to json string
            json_bytes = json_str.encode("utf-8")  # convert to bytes
            base64_bytes = base64.b64encode(json_bytes)  # encode to base64
            file.write(base64_bytes)

    def load_agent_config(self):
        try:
            with open(self.agent_data_file_name, "rb") as file:  # open in binary mode
                base64_bytes = file.read()  # read base64
                json_bytes = base64.b64decode(base64_bytes)  # decode from base64
                json_str = json_bytes.decode("utf-8")  # convert to string
                return json.loads(json_str)  # parse json
        except FileNotFoundError as exception:
            logger.error(f"Agent can't load data file : {exception}")
            logger.error("Make sure you have logged in before > qalita agent login")
            sys.exit(1)

    def set_agent_id(self, agent_id):
        self.agent_id = agent_id

    def json(self):
        data = {
            "name": self.name,
            "mode": self.mode,
            "token": self.token,
            "url": self.url,
            "verbose": self.verbose,
        }
        return data

    def __init__(self):
        self.name = ""
        self.mode = ""
        self.token = ""
        self.url = ""
        self.verbose = False
        self.agent_id = None
        self.config = self.load_source_config()

        # con = sqlite3.connect("agent.db")


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
def cli():
    """
    ------------------ Qalita Platform Command Line Interface ------------------\n\r
    Hello and thanks for using Qalita Platform to monitor and ensure the quality of your data. \n\r
    ----------------------------------------------------------------------------\n\r
    Please, Help us improve our service by reporting any bug by filing a bug report, Thanks ! \n\r
    mail : contact-project+qalita-platform-toolset-cli-bug@incoming.gitlab.com \n\r
    ----------------------------------------------------------------------------"""
    pass


def fetch_package_version(filename):
    """
    Fetch the version from the package.
    """
    # Open the file
    with open(filename, 'r') as f:
        data = json.load(f)

    # Retrieve the version
    version = data.get('version', 'Version not found')

    return version

@cli.command(context_settings=dict(help_option_names=["-h", "--help"]))
@pass_config
def version(config):
    """
    Display the version of the cli
    """
    logger.info("------------- QALITA CLI Version -------------")

    # Assuming that your json file is named 'version.json' and located in the same directory as this file
    file_path = os.path.join(os.path.dirname(__file__), 'version.json')
    version = fetch_package_version(file_path)

    logger.info(f"Version : {version}")

from qalita.commands import agent, source, pack

# Add pack command group to cli
cli.add_command(pack.pack)
cli.add_command(agent.agent)
cli.add_command(source.source)

if __name__ == "__main__":
    cli(context_class=CustomContext, auto_envvar_prefix="QALITA")
