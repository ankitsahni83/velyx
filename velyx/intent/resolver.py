from datetime import datetime, timezone
import json

def resolve_intent(service_id, env, catalog_path):

    with open(catalog_path) as f:
        catalog = json.load(f)

    record = None
    for svc in catalog["services"]:
        if svc["service_id"] == service_id:
            record = svc

    if not record:
        raise Exception("service not found")

    intent = {
        "service_id": service_id,
        "env": env,
        "snapshot_version": datetime.now(timezone.utc).isoformat(),
        "fields": {}
    }

    intent["fields"]["service_tier"] = {
        "value": record["tier"],
        "confidence": 0.95,
        "evidence": [f"catalog.tier={record['tier']}"]
    }

    intent["fields"]["customer_exposure"] = {
        "value": record["exposure"],
        "confidence": 0.9,
        "evidence": [f"catalog.exposure={record['exposure']}"]
    }

    intent["fields"]["journey_type"] = {
        "value": record["journey"],
        "confidence": 0.8,
        "evidence": [f"catalog.journey={record['journey']}"]
    }

    intent["fields"]["traffic_class"] = {
        "value": record["traffic_class"],
        "confidence": 0.75,
        "evidence": [f"catalog.traffic_class={record['traffic_class']}"]
    }

    data_class = record["data_class"]

    if data_class in ["pii", "pci", "phi"]:
        value = "regulated"
    else:
        value = "internal"

    intent["fields"]["data_sensitivity"] = {
        "value": value,
        "confidence": 0.7,
        "evidence": [f"catalog.data_class={data_class}"]
    }

    return intent