import random
import time
from datetime import datetime
from google.cloud import logging_v2

client = logging_v2.Client()
logger = client.logger("chaospilot-fake-logs")

LOG_ENTRIES = {
    "INFO": [
        ("✅ 200 OK - Deployment successful", 200),
        ("🟢 200 OK - Health check passed", 200),
    ],
    "WARNING": [
        ("⚠️ 400 Bad Request - Invalid request payload", 400),
        ("🟠 400 Bad Request - Unsupported operation", 400)
    ],
    "ERROR": [
        ("🔥 500 Internal Error - CPU spike", 500),
        ("🛑 500 Internal Error - Service crashed", 500)
    ]
}

def generate_logs(n=100):
    for _ in range(n):
        severity = random.choices(["INFO", "WARNING", "ERROR"], weights=[0.6, 0.25, 0.15])[0]
        message, status_code = random.choice(LOG_ENTRIES[severity])
        
        http_request = {
            "requestMethod": random.choice(["GET", "POST"]),
            "requestUrl": random.choice(["/api/v1/deploy", "/api/v1/metrics", "/health"]),
            "status": status_code,
            "responseSize": random.randint(200, 1500),
        }

        log_data = {
            "timestamp": datetime.utcnow().isoformat(timespec="microseconds") + "Z",
            "message": message,
            "status_code": status_code,
            "agent_id": f"agent-{random.randint(1, 5)}",
            "experiment_id": f"exp{random.randint(1000, 9999)}",
            "region": random.choice(["us-central1", "europe-west1", "asia-east1"]),
            "details": {
                "duration_ms": random.randint(100, 3000),
                "component": random.choice(["scheduler", "load-balancer", "node-exporter"]),
                "user_id": f"user-{random.randint(100, 999)}"
            },
            "httpRequest": http_request
        }

        logger.log_struct(
            log_data,
            severity=severity,
            labels={
                "region": log_data["region"],
                "component": log_data["details"]["component"],
                "status": str(status_code)
            }
        )

        time.sleep(0.05)

    print(f"{n} enhanced log entries sent to Logs Explorer.")

generate_logs(20)
