from typing import Tuple, Dict
from daisyfl.common.logger import log
from logging import WARNING, ERROR

## reserved
ANCHOR = "anchor"
HANDOVER= "handover"
IS_ZONE = "is_zone"
## required
CID = "cid"
CREDENTIAL = "credential"
## else
DATASET = "dataset"
DEVICE = "device"
ROOT_CERTIFICATES = "root_certificates"

reserved = [ANCHOR, IS_ZONE, HANDOVER,]
required = [CID, CREDENTIAL]

def metadata_to_dict(
    metadata: Tuple,
    _check_reserved: bool = True,
    _check_required: bool = True,
) -> Dict:
    dict = {}
    done = []
    redundant = False
    for m in metadata:
        if m[0] in done:
            redundant = True
        dict[m[0]] = m[1]
        done.append(m[0])
    # check reserved words
    if _check_reserved:
        for word in reserved:
            if dict.__contains__(word):
                log(WARNING, "\"{}\" is a reserved word.".format(word))
    # check required words
    if _check_required:
        for word in required:
            if not dict.__contains__(word):
                if (word == CREDENTIAL) and dict.__contains__(IS_ZONE):
                    continue
                log(ERROR, "\"{}\" is a required word but isn't defined".format(word))
    if redundant:
        log(WARNING, "Some keys was redundantly defined.")
    return dict

def dict_to_metadata(dict: Dict) -> Tuple:
    l = []
    for key in dict.keys():
        l.append((key, dict[key]))
    return tuple(l)
