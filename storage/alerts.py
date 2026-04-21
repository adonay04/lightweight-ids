def get_alerts():
    return [
        {
            "id": "A102",
            "time": "12:55",
            "severity": "HIGH",
            "type": "Port Scan",
            "source_ip": "192.168.1.23",
            "description": "Multiple connection attempts detected.",
            "recommended_action": "Check the device and update passwords",
            "status": "New"
        },
        {
            "id": "A101",
            "time": "12:01",
            "severity": "MEDIUM",
            "type": "DNS Alert",
            "source_ip": "192.168.1.11",
            "description": "Suspicious DNS query pattern detected.",
            "recommended_action": "Monitor DNS activity",
            "status": "Seen"
        },
        {
            "id": "A100",
            "time": "11:57",
            "severity": "LOW",
            "type": "New Device Seen",
            "source_ip": "192.168.1.58",
            "description": "A previously unseen device joined the network.",
            "recommended_action": "Verify the device is trusted",
            "status": "Seen"
        }
    ]


def get_dashboard_summary():
    alerts = get_alerts()

    summary = {
        "total": len(alerts),
        "high": 0,
        "medium": 0,
        "low": 0,
        "recent_alerts": alerts[:3]
    }

    for alert in alerts:
        severity = alert["severity"]
        if severity == "HIGH":
            summary["high"] += 1
        elif severity == "MEDIUM":
            summary["medium"] += 1
        elif severity == "LOW":
            summary["low"] += 1

    return summary
