import logging

import yaml

from click import command, option


@command()
@option("--input_data", "-i", required=True, help="Path to a container-style LinkML data file.")
@option("--output_data", required=True, help="Path to save the first iterm from the first key in the input.")
def cli(input_data, output_data):
    """
    A CLI tool to get the first item of the (list) object of the first key in a LinkML container-like data file.
    """

    logger = logging.getLogger(__name__)

    # safely load yaml file into python dict
    with open(input_data, 'r') as file:
        try:
            yaml_data = yaml.safe_load(file)
        except yaml.YAMLError as e:
            logger.error(f"Error while loading YAML file: {e}")
            exit(1)

    # get the first key of the dict
    try:
        first_key = list(yaml_data.keys())[0]
    except IndexError as e:
        logger.error(f"Error while getting first key from YAML file: {e}")
        exit(1)

    # get the first item of the list object of the first key
    try:
        first_item = yaml_data[first_key][0]
    except IndexError as e:
        logger.error(f"Error while getting first item from list object in YAML file: {e}")
        exit(1)

    # save the first item to a yaml file
    with open(output_data, 'w') as file:
        yaml.safe_dump(first_item, file)


if __name__ == "__main__":
    cli()
