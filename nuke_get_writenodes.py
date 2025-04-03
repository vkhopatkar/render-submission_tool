#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import nuke
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    if len(sys.argv) < 2:
        logger.error("No file path provided as argument.")
        return

    filename = sys.argv[1]
    logger.info("Opening Nuke script: %s", filename)

    try:
        nuke.scriptOpen(filename)
    except Exception as e:
        logger.error("Failed to open Nuke script: %s", e)
        return

    logger.info("Script successfully opened.")

    write_nodes_data = {}

    write_nodes = nuke.allNodes('Write')
    if write_nodes:
        logger.info("Found %d Write nodes.", len(write_nodes))
        for node in write_nodes:
            name = node['name'].value()
            filepath = node['file'].value()
            logger.info("Write node: %s --> %s", name, filepath)
            write_nodes_data[name] = filepath
    else:
        logger.warning("No Write nodes found in script.")
        write_nodes_data["none"] = "Nothing found"

    output_path = "/usr/tmp/nuke_write.json"
    try:
        with open(output_path, "w") as f:
            json.dump(write_nodes_data, f)
        logger.info("Write node data saved to: %s", output_path)
    except IOError as e:
        logger.error("Failed to write JSON file: %s", e)


if __name__ == "__main__":
    main()
