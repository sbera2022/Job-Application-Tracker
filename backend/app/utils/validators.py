VALID_STATUSES = {
    "Saved",
    "Applied",
    "Assessment",
    "Interview",
    "Offer",
    "Rejected",
    "Withdrawn",
}

VALID_WORK_LOCATIONS = {
    "On-site",
    "Remote",
    "Hybrid",
}


def validate_application(data):
    status = data.get("status")
    work_location = data.get("work_location")

    if status is not None and status not in VALID_STATUSES:
        return {
            "error": "Invalid application status",
            "allowed_values": sorted(VALID_STATUSES),
        }

    if (
        work_location is not None
        and work_location not in VALID_WORK_LOCATIONS
    ):
        return {
            "error": "Invalid work location",
            "allowed_values": sorted(
                VALID_WORK_LOCATIONS
            ),
        }

    return None