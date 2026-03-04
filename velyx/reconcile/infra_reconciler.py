def reconcile_intent_vs_infra(intent: dict, infra: dict) -> dict:
    """
    Compare expected posture vs detected posture and produce findings.
    """
    from velyx.reconcile.rules import expected_posture_from_intent

    expected = expected_posture_from_intent(intent.get("fields", {}))
    detected = infra.get("posture", {})

    findings = []

    def add_finding(severity, expectation, observed, recommendation, evidence):
        findings.append({
            "type": "infra",
            "severity": severity,
            "expectation": expectation,
            "observed": observed,
            "recommendation": recommendation,
            "evidence": evidence
        })

    # multi_az
    if expected["multi_az_required"] and not detected.get("multi_az"):
        add_finding(
            "RISK",
            "Gold-tier services should be deployed multi-AZ for resilience.",
            "multi_az=false",
            "Enable multi-AZ or deploy redundant instances across availability zones.",
            ["terraform:missing_or_disabled_multi_az"]
        )

    # autoscaling
    if expected["autoscaling_required"] and not detected.get("autoscaling"):
        add_finding(
            "ADVISORY",
            "External/partner-facing services should have autoscaling enabled.",
            "autoscaling=false",
            "Add autoscaling group/policies aligned to traffic expectations.",
            ["terraform:missing_autoscaling"]
        )

    # backups
    if expected["backups_required"] and not detected.get("backups_enabled"):
        add_finding(
            "RISK",
            "Regulated-data services should have backups enabled with retention.",
            "backups_enabled=false",
            "Enable backups (e.g., retention period > 0) and validate restore process.",
            ["terraform:missing_backup_retention"]
        )

    # Overall status
    if any(f["severity"] == "RISK" for f in findings):
        overall = "RISK"
    elif len(findings) > 0:
        overall = "ADVISORY"
    else:
        overall = "PASS"

    report = {
        "service_id": intent.get("service_id"),
        "env": intent.get("env"),
        "overall": overall,
        "expected": expected,
        "detected": detected,
        "findings": findings
    }

    return report