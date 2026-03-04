def extract_posture(tfplan, service_id, env):

    posture = {
        "service_id": service_id,
        "env": env,
        "posture": {
            "multi_az": False,
            "autoscaling": False,
            "backups_enabled": False
        }
    }

    for r in tfplan.get("resource_changes", []):

        rtype = r.get("type")
        after = r.get("change", {}).get("after", {})

        # Multi AZ (RDS)
        if rtype == "aws_db_instance":
            if after.get("multi_az"):
                posture["posture"]["multi_az"] = True

            if after.get("backup_retention_period", 0) > 0:
                posture["posture"]["backups_enabled"] = True

        # Autoscaling
        if rtype == "aws_autoscaling_group":
            posture["posture"]["autoscaling"] = True

    return posture