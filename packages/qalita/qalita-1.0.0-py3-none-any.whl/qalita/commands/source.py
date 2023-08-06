"""
# QALITA (c) COPYRIGHT 2023 - ALL RIGHTS RESERVED -
"""
import os
import click
from tabulate import tabulate
from qalita.cli import pass_config, logger
from qalita.internal.utils import send_api_request


@click.group()
@click.option("-s", "--source", type=int, help="Source ID")
@click.pass_context
def source(ctx, source):
    """Manage Qalita Platform Sources"""
    ctx.ensure_object(dict)
    ctx.obj["SOURCE"] = source


@source.command()
@click.pass_context
def versions(ctx):
    """Print the versions of the source"""
    source = ctx.obj.get("SOURCE")
    logger.info("------------- Source Versions -------------")
    logger.info(f"Fetching versions for source [{source}]")
    logger.warning("Not Yet Implemented")


@source.command()
@pass_config
def list(config):
    """List sources that are accessible to the agent"""

    sources = []
    headers = ["ID", "Name", "Type", "Description", "Validity"]
    for source in config.config["sources"]:
        sources.append(
            [
                source.get("id", ""),
                source.get("name", ""),
                source.get("type", ""),
                source.get("description", ""),
                source.get("validate", ""),
            ]
        )

    print(tabulate(sources, headers, tablefmt="simple"))


@pass_config
def validate_source(config):
    """Validate a source configuration"""
    logger.info("------------- Source Validation -------------")
    agent_conf = config.load_agent_config()

    total_sources = 0
    error_count = 0

    source_names = []

    for i, source in enumerate(config.config["sources"]):
        total_sources += 1
        is_source_valid = True  # Assuming the source is valid initially

        # check for name
        if "name" not in source:
            logger.error(f"Source number [{total_sources}] has no name")
            is_source_valid = False
        else:
            # Check for duplicate names
            if source["name"] in source_names:
                logger.error(f"Duplicate source name: [{source['name']}]")
                is_source_valid = False
            else:
                source_names.append(source["name"])

            # check for description
            if "description" not in source:
                logger.warning(f"Source [{source['name']}] has no description")
                is_source_valid = False

            # check for owner
            if "owner" not in source:
                logger.warning(
                    f"Source [{source['name']}] must have a owner, if you publish without owner, it will be published under your name"
                )
                logger.warning(
                    f"Source defaulting to owner: {agent_conf['user']['login']}"
                )
                source["owner"] = agent_conf["user"]["login"]

        # check type
        if source["type"] == "database":
            if "config" in source:
                for key, value in source["config"].items():
                    # If the value starts with '$', assume it's an environment variable
                    if str(value).startswith("$"):
                        env_var = value[1:]
                        # Get the value of the environment variable
                        env_value = os.getenv(env_var)
                        if env_value is None:
                            logger.warning(
                                f"The environment variable [{env_var}] for the source [{source['name']}] is not set"
                            )
                            is_source_valid = False
        elif source["type"] == "file":
            # check for path in config
            if "path" not in source["config"]:
                logger.error(
                    f"Source [{source['name']}] is of type file but has no path in config"
                )
                is_source_valid = False

            # check for read access to path
            path = source["config"]["path"]
            if not os.access(path, os.R_OK):
                logger.error(
                    f"Source [{source['name']}] has a path in config, but it cannot be accessed"
                )
                is_source_valid = False

        # If all checks pass, mark the source as valid
        if is_source_valid:
            source["validate"] = "valid"
            logger.success(f"Source [{source['name']}] validated")
        else:
            source["validate"] = "invalid"
            logger.error(f"Source [{source['name']}] is invalid")
            error_count += 1

    if error_count == 0:
        logger.success("All sources validated")
    else:
        logger.error(f"{error_count} out of {total_sources} sources are invalid")

    # Write the config file
    config.save_source_config()


@source.command()
def validate():
    """Validate a source configuration"""
    validate_source()


@source.command()
@pass_config
def push(config):
    """Publish a source to the Qalita Platform"""
    validate_source()
    logger.info("------------- Source Publishing -------------")
    logger.info("Publishing sources to the Qalita Platform...")
    invalid_count = 0  # to count failed publishing sources
    agent_conf = config.load_agent_config()

    for i, source in enumerate(config.config["sources"]):
        if source["validate"] == "valid":
            owner_id = agent_conf["user"]["id"]
            if "id" in source:
                # Try to get source info from name, type and owner_id
                r = send_api_request(
                    request="/sources/",
                    mode="get",
                    query_params={
                        "name": source["name"],
                        "type": source["type"],
                        "user_id": agent_conf["user"]["id"],
                    },
                )
                if r.status_code != 200:
                    logger.warning(
                        f"Agent failed to get source info {r.status_code} - {r.text}"
                    )
                    invalid_count += 1
                else:
                    # On essaye de matcher les valeurs
                    response_data = r.json()

                    # Check if name, type and user_id match with the response data
                    if (
                        source["name"] == response_data["name"]
                        and source["type"] == response_data["type"]
                        and owner_id == response_data["user_id"]
                    ):
                        # If they match, this source is already published, skip to the next source

                        if source["description"] == response_data["description"]:
                            logger.info(
                                f"Source [{source['name']}] already published with id [{source['id']}] and no updates detected. Skipping..."
                            )
                        else:
                            r = send_api_request(
                                request=f"/sources/{response_data['id']}",
                                mode="put",
                                query_params={"description": source["description"]},
                            )
                        continue
                    else:
                        # If they don't match, continue with the publishing process
                        pass

            logger.info(f"Publishing source [{source['name']}] ...")
            # test if the owner is the same as the agent user
            if source["owner"] != agent_conf["user"]["login"]:
                # if the owner is different, we need to fetch the owner-id
                # from the Qalita Platform
                r = send_api_request(
                    request=f"/users/?name={source['owner']}", mode="get"
                )
                if r.status_code != 200:
                    logger.warning(
                        f"Agent failed to get user info {r.status_code} - {r.text}"
                    )
                    invalid_count += 1
                else:
                    owner_id = r.json()["id"]
            else:
                pass
            # send the request to the Qalita Platform
            r = send_api_request(
                request=f"/sources/publish",
                mode="post",
                query_params={
                    "name": source["name"],
                    "type": source["type"],
                    "description": source["description"],
                    "agent_id": agent_conf["context"]["remote"]["id"],
                    "user_id": owner_id,
                },
            )
            if r.status_code != 200:
                logger.warning(
                    f"Agent failed to publish source [{source['name']}] {r.status_code} - {r.text}"
                )
                invalid_count += 1
            else:
                source_id = r.json()["id"]
                logger.success(f"Source published with id [{source_id}]")
                # Add the id to the corresponding source in config.config["sources"]
                config.config["sources"][i]["id"] = source_id
                # Save the updated configuration
                config.save_source_config()

    # after all sources have been processed, print a warning if there were any invalid sources
    if invalid_count > 0:
        logger.warning(f"{invalid_count} source(s) skipped due to validation errors.")
