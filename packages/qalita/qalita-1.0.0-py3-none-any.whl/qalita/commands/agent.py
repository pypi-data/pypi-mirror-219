"""
# QALITA (c) COPYRIGHT 2023 - ALL RIGHTS RESERVED -
"""
import subprocess
import click
import sys
import time
from qalita.cli import pass_config, logger
from qalita.internal.utils import send_request, send_api_request
import os
import random
import string
import tarfile
from datetime import datetime
from shutil import copy2
import json
import select


@click.group()
@click.option(
    "-n",
    "--name",
    help="The name of the agent, it will be used to identify the agent in the qalita platform",
    envvar="QALITA_AGENT_NAME",
)
@click.option(
    "-m",
    "--mode",
    type=click.Choice(["job", "worker"], case_sensitive=False),
    help="The mode of the agent, <worker/job> if you run the agent in worker mode, the agent will loop until it gets a job to do, in job mode it will immediately do a job",
    envvar="QALITA_AGENT_MODE",
)
@click.option(
    "-t",
    "--token",
    help="The API token from the qalita platform, it is user scoped. Make sure you have at least the Data Engineer role to have the ability to register agents.",
    envvar="QALITA_AGENT_API_TOKEN",
)
@click.option(
    "-u",
    "--url",
    help="The URL to the qalita backend the agent have to register exemple : http://backend:3080/api/v1",
    envvar="QALITA_AGENT_URL_ENDPOINT",
)
@pass_config
def agent(config, name, mode, token, url):
    """Manage Qalita Platform Agents"""

    all_check_pass = True

    # Validation of required options
    if not name:
        logger.error("Error: Agent name is required!")
        logger.info("\tTo do so, you can set an Environment Variable : ")
        logger.info("\t\texport QALITA_AGENT_NAME='agent-1'")
        logger.info("\tor add the name as a commandline argument : ")
        logger.info("\t\tqalita agent --name 'agent-1'")
        logger.info(
            "\tthe prefered way is to create a file '.env-file' with the values : "
        )
        logger.info("\t\tQALITA_AGENT_NAME=agent-1")
        logger.info("\tand source it : ")
        logger.info("\t\texport $(xargs < .env-file)")
        all_check_pass = False
    if not mode:
        logger.error("Error: Agent Mode is required!")
        logger.info("\tTo do so, you can set an Environment Variable : ")
        logger.info("\t\texport QALITA_AGENT_MODE='job'")
        logger.info("\tor add the mode as a commandline argument : ")
        logger.info("\t\tqalita agent --mode 'job'")
        logger.info(
            "\tthe prefered way is to create a file '.env-file' with the values : "
        )
        logger.info("\t\tQALITA_AGENT_MODE=job")
        logger.info("\tand source it : ")
        logger.info("\t\texport $(xargs < .env-file)")
        all_check_pass = False
    if not token:
        logger.error("Error: API_Token is required!")
        logger.info("\tTo do so, you can set an Environment Variable : ")
        logger.info("\t\texport QALITA_AGENT_API_TOKEN='<your_api_token>'")
        logger.info("\tor add the token as a commandline argument : ")
        logger.info("\t\tqalita agent --token '<your_api_token>'")
        logger.info(
            "\tthe prefered way is to create a file '.env-file' with the values : "
        )
        logger.info("\t\tQALITA_AGENT_API_TOKEN=<your_api_token>")
        logger.info("\tand source it : ")
        logger.info("\t\texport $(xargs < .env-file)")
        all_check_pass = False
    if not url:
        logger.error("Error: API_URL is required!")
        logger.info("\tTo do so, you can set an Environment Variable : ")
        logger.info(
            "\t\texport QALITA_AGENT_URL_ENDPOINT='http://localhost:3080/api/v1'"
        )
        logger.info("\tor add the url as a commandline argument : ")
        logger.info("\t\tqalita agent --url 'agent-1'")
        logger.info(
            "\tthe prefered way is to create a file '.env-file' with the values : "
        )
        logger.info("\t\tQALITA_AGENT_URL_ENDPOINT=http://localhost:3080/api/v1")
        logger.info("\tand source it : ")
        logger.info("\t\texport $(xargs < .env-file)")
        all_check_pass = False
    if all_check_pass:
        config.name = name
        config.mode = mode
        config.token = token
        config.url = url
    else:
        return


@agent.command()
@pass_config
def info(config):
    """Display Information about the agent"""
    data = config.load_agent_config()

    logger.info("------------- Agent information -------------")
    logger.info(f"Name : {config.name}")
    logger.info(f"Mode : {config.mode}")
    logger.info(f"Backend URL : {config.url}")
    logger.info(f"Id : {data['context']['remote']['id']}")


@pass_config
def send_alive(config, config_file, mode="", status="online"):
    if mode == "":
        mode = config.mode

    """Send a keep alive to the backend"""
    r = send_api_request(
        request=f'/agents/{config_file["context"]["remote"]["id"]}/alive?name={config_file["context"]["local"]["name"]}&mode={mode}&status={status}',
        mode="put",
    )
    if r.status_code != 200:
        logger.warning(f"Agent failed to send alive {r.status_code} - {r.text}")


@pass_config
def authenticate(config):
    """Authenticate the agent to the Qalita Platform"""

    r = send_request(request=f"{config.url}/users/me", mode="get")

    if r.status_code == 200:
        logger.success("Agent Authenticated")
        config_json = {}
        config_json["user"] = r.json()
        try:
            config_json["context"]["local"] = config.json()
        except KeyError:
            config_json["context"] = {}
            config_json["context"]["local"] = config.json()

        config.save_agent_config(config_json)
    else:
        logger.error(
            f"Agent can't authenticate - HTTP Code : {r.status_code} - {r.text}"
        )
        logger.error(
            "Make sure you have generated an API TOKEN from the qalita platform backend or web app"
        )

    r = send_api_request(request=f"/agents/?name={config.name}", mode="get")

    if r.status_code == 200:
        logger.success("Agent Registered")
    elif r.status_code == 404:
        logger.info("Agent not Registered")
        try:
            logger.info("Registering agent...")
            r = send_api_request(
                request=f"/agents/register",
                mode="post",
                query_params={
                    "name": {config.name},
                    "mode": {config.mode},
                    "status": "online",
                },
            )
            if r.status_code == 201:
                logger.success("Agent Registered")
            else:
                logger.error(
                    f"Agent can't register - HTTP Code : {r.status_code} - {r.text}"
                )
        except Exception as exception:
            logger.error(f"Agent can't communicate with backend : {exception}")
            sys.exit(1)
    else:
        logger.error(
            f"Agent can't authenticate - HTTP Code : {r.status_code} - {r.text}"
        )
        logger.error(
            "Make sure you have generated an API TOKEN from the qalita platform backend or web app"
        )
    config_json = config.load_agent_config()
    config_json["context"]["remote"] = r.json()
    config.save_agent_config(config_json)

    r = send_api_request(request=f"/registries/local", mode="get")

    if r.status_code == 200:
        logger.success("Registry credentials fetched")
    elif r.status_code == 404:
        logger.info("No registry")
        sys.exit(1)
    else:
        logger.error(
            f"Agent can't fetch registry - HTTP Code : {r.status_code} - {r.text}"
        )
        logger.error(
            "Make sure you have generated an API TOKEN from the qalita platform backend or web app"
        )

    config_json = config.load_agent_config()
    config_json["registries"] = r.json()
    config.save_agent_config(config_json)


@agent.command()
@pass_config
def login(config):
    """
    Register the agent to the Qalita Platform
    """
    print("test")
    if config.verbose:
        logger.info("Verbose mode enabled")
    authenticate()


@agent.command()
@pass_config
@click.option(
    "-s",
    "--source",
    help="The source ID to run the job against, to get the source ID, run qalita source list",
    envvar="QALITA_AGENT_JOB_SOURCE",
)
@click.option(
    "-sv",
    "--source-version",
    help="The source Version to run the job against, to get the source version, run qalita source -s <source_id> versions, default to latest",
    envvar="QALITA_AGENT_JOB_SOURCE_VERSION",
)
@click.option(
    "-p",
    "--pack",
    help="The pack ID to run the job against, to get the pack ID, run qalita pack list",
    envvar="QALITA_AGENT_JOB_PACK",
)
@click.option(
    "-pv",
    "--pack-version",
    help="The pack Version to run the job against, to get the pack version, run qalita pack -p <pack_id> versions, default to latest",
    envvar="QALITA_AGENT_JOB_PACK_VERSION",
)
def run(config, source, source_version, pack, pack_version):
    """Runs de agent"""
    # Pre-checks
    if config.mode == "job":
        if source is None:
            logger.error("Agent can't run job without source")
            logger.error(
                "Please configure a source with --source or -s or QALITA_AGENT_JOB_SOURCE"
            )
            logger.error("To get the source ID, run qalita source list")
            sys.exit(1)
        if pack is None:
            logger.error("Agent can't run job without pack")
            logger.error(
                "Please configure a pack with --pack or -p or QALITA_AGENT_JOB_PACK"
            )
            logger.error("To get the pack ID, run qalita pack list")
            sys.exit(1)
    logger.info("------------- Agent Authenticate -------------")
    authenticate()
    logger.info("------------- Agent Run -------------")
    agent_conf = config.load_agent_config()
    logger.info(f"Agent ID : {agent_conf['context']['remote']['id']}")
    logger.info(f"Agent Mode : {config.mode}")

    # Create a temp folder named "agent_run_temp" if it doesn't already exist
    if not os.path.exists("agent_run_temp"):
        os.makedirs("agent_run_temp")

    if config.mode == "job":
        job_run(source, source_version, pack, pack_version)
    elif config.mode == "worker":
        try:
            logger.info(f"Worker Start at {time.strftime('%X %d-%m-%Y %Z')}")
            while True:
                send_alive(config_file=agent_conf)
                check_job = send_api_request(
                    request=f'/agents/{agent_conf["context"]["remote"]["id"]}/jobs/next',
                    mode="get",
                )
                if check_job.status_code == 200:
                    job = check_job.json()
                    source = job["source"]
                    pack = job["pack"]
                    job_run(source, pack)
                    time.sleep(10)
                else:
                    time.sleep(10)
        except KeyboardInterrupt:
            logger.warning("KILLSIG detected. Gracefully exiting the program.")
            logger.error("Set Agent OFFLINE...")
            send_alive(config_file=agent_conf, status="offline")
            logger.error("Exit")

    else:
        logger.error("Agent mode not supported : <worker/job>")
        sys.exit(1)

def pull_pack(pack_id, pack_version=None):
    # Fetch the pack data from api
    response_pack = send_api_request(f"/assets/{pack_id}", "get")
    if response_pack.status_code == 200:
        # The request was successful
        response_pack = response_pack.json()
    else:
        # The request failed
        logger.error(f"Failed to fetch pack info: {response_pack.text}")
        sys.exit(1)

    if pack_version is None:
        # Convert the 'sem_ver_id' to tuple for easy comparison
        for version in response_pack["version"]:
            version["sem_ver_id"] = tuple(map(int, version["sem_ver_id"].split(".")))

        # Sort the versions in descending order
        response_pack["version"].sort(key=lambda v: v["sem_ver_id"], reverse=True)

        # Get the highest version
        highest_version = response_pack["version"][0]

        # Convert the 'sem_ver_id' back to string
        highest_version["sem_ver_id"] = ".".join(
            map(str, highest_version["sem_ver_id"])
        )

        logger.info(f"Pack version not specified, Latest pack version is {highest_version['sem_ver_id']}")
        pack_version = highest_version["sem_ver_id"]
        pack_version_id = highest_version["id"]

    # Filter the version list for the matching version
    matching_versions = [
        v for v in response_pack["version"] if v["sem_ver_id"] == pack_version
    ]

    if not matching_versions:
        logger.error(f"Version {pack_version} not found in pack {pack_id}")
        sys.exit(1)

    # Get the URL from the matching version
    pack_url = matching_versions[0]["url"]

    # Système de caching, on regarde si le pack est déjà présent dans le cache sinon on le télécharge
    file_name = pack_url.split("/")[-1]
    bucket_name = pack_url.split("/")[3]
    s3_folder = "/".join(pack_url.split("/")[4:-1])
    local_path = f"./agent_run_temp/{bucket_name}/{s3_folder}/{file_name}"

    if os.path.exists(local_path):
        return local_path
    if not os.path.exists(f"./agent_run_temp/{bucket_name}/{s3_folder}"):
        os.makedirs(f"./agent_run_temp/{bucket_name}/{s3_folder}")

    # Fetch the pack from api
    response = send_api_request(f"/assets/{pack_id}/fetch/{pack_version_id}", "get")

    if response.status_code == 200:
        # The request was successful
        with open(local_path, "wb") as file:
            file.write(response.content)
        logger.info(f"Pack fetched successfully")
        return local_path
    else:
        logger.error(f"Failed to fetch pack. Status code: {response.status_code}")


def run_pack(pack_file_path):
    logger.info("------------- Pack Run -------------")
    # Check if the run.sh file exists
    run_script = "run.sh"  # Only the script name is needed now
    if not os.path.isfile(os.path.join(pack_file_path, run_script)):
        logger.error(
            f"run.sh script does not exist in the package folder {pack_file_path}"
        )
        return

    # Run the run.sh script and get the output
    process = subprocess.Popen(
        ["sh", run_script],
        cwd=pack_file_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=1,
        universal_newlines=True,
    )

    while process.poll() is None:
        reads = [process.stdout.fileno(), process.stderr.fileno()]
        ret = select.select(reads, [], [])

        for fd in ret[0]:
            if fd == process.stdout.fileno():
                read = process.stdout.readline().strip()
                if read:  # Only print if there's output
                    logger.info(read)
            if fd == process.stderr.fileno():
                read = process.stderr.readline().strip()
                if read:  # Only print if there's output
                    logger.error(read)

    process.stdout.close()
    process.stderr.close()
    logger.success("Pack run completed")


@pass_config
def job_run(config, source_id, source_version, pack_id, pack_version):
    logger.info("------------- Job Run -------------")

    """Runs a job"""
    agent_conf = config.load_agent_config()
    send_alive(config_file=agent_conf, mode="job", status="starting")

    pack_file_path = pull_pack(pack_id, pack_version)
    pack_folder = f"{pack_file_path.split('/')[-1].split('.')[0]}_pack"

    # Create a sub folder named with the current datetime and random generated seed
    datetime_string = datetime.now().strftime("%Y%m%d%H%M%S")
    random_seed = "".join(
        random.choice(string.ascii_lowercase + string.digits) for _ in range(5)
    )
    temp_folder_name = f"./agent_run_temp/{datetime_string}_{random_seed}"
    os.makedirs(temp_folder_name)

    # Copy the downloaded pack to the temp folder
    copy2(pack_file_path, temp_folder_name)

    # Uncompress the pack
    with tarfile.open(
        os.path.join(temp_folder_name, pack_file_path.split("/")[-1]), "r:gz"
    ) as tar:
        tar.extractall(path=temp_folder_name)

    # Delete the compressed pack
    os.remove(os.path.join(temp_folder_name, pack_file_path.split("/")[-1]))

    # Load the source configuration
    source_conf = config.load_source_config()

    # Find the matching source_id
    matching_sources = [
        s for s in source_conf["sources"] if str(s.get("id")) == str(source_id)
    ]

    if matching_sources:
        # If there is a match, get the first one (there should only be one match anyway)
        source = matching_sources[0]
    else:
        logger.error(f"No source found with id {source_id}")
        sys.exit(1)

    # save the source conf as a json file in the temp folder
    with open(os.path.join(temp_folder_name,pack_folder, "source_conf.json"), "w") as file:
        json.dump(source, file, indent=4)

    # run the job
    run_pack(os.path.join(temp_folder_name,pack_folder))

    logger.info(f"Sending data to Qalita Platform...")
    # todo send the data to the qalita platform

    logger.success(f"Job run finished")


@agent.group(help="Manage Agent Jobs")
def jobs():
    """Jobs are the tasks that the agent will execute"""
