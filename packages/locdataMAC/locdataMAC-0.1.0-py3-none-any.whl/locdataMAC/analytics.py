from locdataMAC.logger import logger
from locdataMAC.cutom_exception import InvalidpathException
from ensure import ensure_annotations
import os
import json

@ensure_annotations
def json_data(path:str):
    if not os.path.exists(path):
        raise InvalidpathException(f"json file not found.")
    try:
        f = open(path)
        data = json.load(f)
        # Closing file
        f.close()
        json_object = json.dumps(data['activities'], indent=4)
        logger.info(f"json file saved at: {path}")
        with open("data.json", "w") as outfile:
            outfile.write(json_object)
        return open("data.json", mode='r')
    except Exception:
        raise InvalidpathException

    
