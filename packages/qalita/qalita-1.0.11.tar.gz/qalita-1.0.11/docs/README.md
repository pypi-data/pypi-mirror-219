# QALITA Command Line Interface (CLI)

![logo](https://app.prod.qalita.io/logo.svg)

QALITA Command Line Interface (CLI) is a tool intended to be used by Data Engineers who setup's QALITA Platform's agents, sources and assets.

It gives easy to use command to help them make an up & running qalita platform's environment in no time.

# Quick Start

## Installation

As simple as :

`pip install qalita`

## Usage

If you want to have more detailed and contextual help, type

`qalita COMMAND -h`

```bash
Usage: qalita [OPTIONS] COMMAND [ARGS]...

  QALITA Command Line Interface
```

### Setup

This CLI command communicates with the QALITA Platform API backend.

There are several layers of configuration depending of your needs :

#### Minimal Config

* QALITA_AGENT_NAME=<agent_name>

The agent will help you identify it in the frontend interface, there are no restrictions on the name.

* QALITA_AGENT_MODE=<job/worker>

The mode of the agent :

**Job** : In job mode, when you use the command `qalita agent run`, it will immediately try to run a job on the local current context.

**Worker** : In worker mode, when you use the command `qalita agent run` it will wait for the backend to gives him jobs to run. It is simmilar to a scheduler.

> Note that the command `qalita agent run` needs more configuration to run correctly, it will displays error otherwise.

#### Linked Config

* QALITA_AGENT_URL_ENDPOINT=<backend_api_url>

***Example : http://localhost:3080/api/v1***

The agent url endpoint gives the ability for the agent to communicate with the qalita's platform endpoints, it enables :

    * Listing packs
    * Running Jobs
    * Publishing sources
    * Publishing packs

* QALITA_AGENT_API_TOKEN=<api_token>

The token is provided while doing the quickstart steps in the frontend app. It is associated with your user and your role.

> Note that you need to have at least the **[Data Engineer]** role to use the QALITA CLI

