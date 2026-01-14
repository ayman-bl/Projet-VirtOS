import json
import hashlib

def verify_message(data: dict, received_hash: str) -> bool:
    canonical = json.dumps(data, sort_keys=True)
    computed_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return computed_hash == received_hash
