#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hou
import sys
import os
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    if len(sys.argv) < 2:
        logger.error("No file path provided.")
        return

    file_path = sys.argv[1]
    logger.info("Opening Houdini file: %s", file_path)

    json_path = "/usr/tmp/hou_vars.json"

    # Delete old JSON if exists
    if os.path.exists(json_path):
        os.remove(json_path)
        logger.info("Removed old JSON file: %s", json_path)
    else:
        logger.info("JSON file does not exist, nothing to remove.")

    # Load .hip file
    try:
        hou.hipFile.load(file_path)
    except hou.LoadWarning:
        logger.warning("Load warning encountered while opening HIP file.")

    # Get render nodes
    node_types = ['mantra', 'ifd', 'arnold']
    render_nodes = [
        x for x in hou.node('/out').allSubChildren()
        if x.type().name() in node_types
    ]

    if not render_nodes:
        logger.warning("No render nodes found.")
        return

    # Use first render node to get resolution
    first_render = render_nodes[0]
    width = first_render.parm('res_overridex').eval()
    height = first_render.parm('res_overridey').eval()
    logger.info("Render resolution: %dx%d", width, height)

    # Get all cameras
    cameras = hou.root().recursiveGlob('*', hou.nodeTypeFilter.ObjCamera)
    cams = [i.name() for i in cameras if i.type().name() == 'cam']
    logger.info("Found cameras: %s", cams)

    # Get enabled render layers
    render_layers = hou.node('/out').allSubChildren()
    enabled_layers = [each.name() for each in render_layers if not each.isBypassed()]
    logger.info("Enabled render layers: %s", enabled_layers)

    # Store all data in dictionary
    dat_dict = {
        "width": width,
        "height": height,
        "cams": cams,
        "renderlayer": enabled_layers
    }

    # Dump to JSON
    with open(json_path, "w") as f:
        json.dump(dat_dict, f)

    logger.info("Data saved to JSON: %s", json_path)


if __name__ == "__main__":
    main()
