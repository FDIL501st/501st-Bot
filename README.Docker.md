## Building and running your Bot

All the command used assume you are currently at the top level directory of this project. This is where the `Dockerfile`, `compose.yaml` and `__main__.py` is.

### Environment variables
This application requires some environment variables.

#### The following is mandatory
- TOKEN="The discord bot token"

#### The following are not needed (as they have default values)
- DEV=False
- SINGLE_SERVER=False
- GUILD_ID="111111111"

These environment variables can be overridden if wanted.
Set `SINGLE_SERVER=True` and `GUILD_ID` to whatever is ID of the server you want the slash command to work in.

The default option means the slash commands will work in all the servers it is in.
The downside of the default option is that it will take a few hours before slash commands are available 
if you are planning on only using the bot within a single server.

`DEV=True` only makes the bot print information about the type of error when handling them.

### Using docker compose

The docker compose yaml file expects an .env file in the top level directory of the project (same directory as the yaml file found).

Ensure .env exists before using the docker compose command.

`docker compose up`

This is a simple single container python application that doesn't expose ports.

### Using docker run

If you want to run the single container with docker run, then you will first need to build the image.

##### No need to run the following command if you have already the image locally

You can run `docker images` to check if you already have the image. If the bot shows up, you can skip to running the bot.

`docker build -t 501st-Bot .`

#### Run command
As previously mentioned, you will need to at least pass `TOKEN` environment variable. Simpliest way is to have a .env file in the same directory as the Dockerfile.

##### docker run using .env file
`docker run --env-file ./.env 501st-Bot`

The option is passing the environment variables by command line is also available. 
Here is an example of passing all the environment variables. Any you don't wish to pass can simply be ommited from the command (including the -e flag that comes before the key/value pair)

##### docker run without .env file
`docker run -e TOKEN=BOT_TOKEN -e DEV=False -e SINGLE_SERVER=False -e GUILD_ID=111111111 501st-501st-Bot:latest`
