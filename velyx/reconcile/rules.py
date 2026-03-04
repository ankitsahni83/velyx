def expected_posture_from_intent(intent_fields: dict) -> dict:
    """
    Compute expected posture (requirements) from inferred intent.
    Keep it small and explicit for MVP.
    """
    tier = intent_fields.get("service_tier", {}).get("value")
    exposure = intent_fields.get("customer_exposure", {}).get("value")
    sensitivity = intent_fields.get("data_sensitivity", {}).get("value")

    expected = {
        "multi_az_required": False,
        "autoscaling_required": False,
        "backups_required": False
    }

    if tier == "gold":
        expected["multi_az_required"] = True

    if exposure in ("external", "partner"):
        expected["autoscaling_required"] = True

    if sensitivity == "regulated":
        expected["backups_required"] = True

    return expected