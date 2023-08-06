"""
This file should be split into environment and config files
"""

PREFIX = "prod"
DB_NAME = PREFIX + "-db"
API_NAME = PREFIX + "-api"
UTILS_NAME = PREFIX + "-utils"
SLACK_NAME = PREFIX + "-slack"
BOT_TOKEN_NAME = PREFIX + "-bot-token"
if PREFIX == "prod":
    BOT_TOKEN_NAME = "bot-token"
SWEEP_LOGIN = "sweep-ai[bot]"

if PREFIX == "prod":
    APP_ID = 307814
    ENV = PREFIX
elif PREFIX == "dev2":
    APP_ID = 327588
    ENV = PREFIX
    SWEEP_LOGIN = "sweep-canary[bot]"
elif PREFIX == "dev":
    APP_ID = 324098
    ENV = PREFIX
    SWEEP_LOGIN = "sweep-nightly[bot]"
LABEL_NAME = "sweep"
LABEL_COLOR = "9400D3"
LABEL_DESCRIPTION = "Sweep your software chores"

SWEEP_CONFIG_BRANCH = "sweep/add-sweep-config"
DEFAULT_CONFIG = """# Sweep AI turns bug fixes & feature requests into code changes (https://sweep.dev)
# For details on our config file, check out our docs at https://docs.sweep.dev
# Reference: https://github.com/sweepai/sweep/blob/main/.github/sweep.yaml.

# If you use this be sure to frequently sync your default branch(main, master) to dev.
branch: '{branch}'
"""

SECONDARY_MODEL = "gpt-3.5-turbo-16k-0613"