from logging import INFO, WARNING, basicConfig, getLogger

# Set common logger
basicConfig(
    level=INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
# Set pyrogram LOGGER level to WARNING
getLogger("pyrogram").setLevel(WARNING)
getLogger("urllib3").setLevel(WARNING)

# Initialise LOGGER
LOGGER = getLogger(__name__)
