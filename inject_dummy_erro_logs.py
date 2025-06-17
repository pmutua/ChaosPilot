import sqlite3
import random
import time
import sys
import os
import argparse
from datetime import datetime, timezone
from typing import Dict, List, Tuple

# Dynamically resolve the path to logger-data/logger-db.sql inside the mcp-toolbox
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "mcp-toolbox/logger-data")
os.makedirs(LOG_DIR, exist_ok=True)
DB_NAME = os.path.join(LOG_DIR, "logger-db.sql")

class ChaosLogger:
    def __init__(self):
        try:
            self.conn = sqlite3.connect(DB_NAME)
            self.cursor = self.conn.cursor()
            self._create_table()
            self._init_scenarios()
            self.start_time = datetime.now(timezone.utc)
            self._log_startup_message()
        except Exception as e:
            print(f"🚨 Failed to initialize logger: {str(e)}", file=sys.stderr)
            raise

    def _create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS chaos_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                experiment_id TEXT,
                message TEXT,
                failure_type TEXT,
                severity TEXT,
                impact_level TEXT,
                environment TEXT,
                release_version TEXT,
                chaos_agent TEXT,
                session_id TEXT,
                region TEXT,
                timestamp TEXT,
                scenario_metadata TEXT,
                secondary_effect TEXT,
                injected INTEGER,
                log_sequence INTEGER
            )
        """)
        self.conn.commit()

    def _init_scenarios(self):
        self.scenarios = [
            ("🔥 CPU spike to 99%", "ERROR", "cpu_spike", {"duration": random.randint(30, 300)}),
            ("❄️ Memory leak simulation", "ERROR", "memory_leak", {"leak_rate": f"{random.uniform(0.1, 5.0):.1f} MB/s"}),
            ("🌐 Network partition simulated", "WARNING", "network_partition", {"partition_duration": random.randint(10, 600)}),
            ("🛑 DB read timeout triggered", "ERROR", "db_timeout", {"timeout_ms": random.randint(1000, 30000)}),
            ("🔁 Infinite loop in API service", "CRITICAL", "infinite_loop", {"service": "auth-service"}),
            ("⛔ Disk I/O stall", "ERROR", "disk_stall", {"duration": random.randint(10, 120)}),
            ("⚠️ Throttling detected on GKE pod", "WARNING", "gke_throttle", {"pod_name": "pod-1337"}),
            ("💀 CrashLoopBackOff on pod", "CRITICAL", "crashloop", {"restart_count": random.randint(3, 20)}),
            ("🕒 Latency > 10s on user login", "WARNING", "high_latency", {"endpoint": "/api/v1/login"}),
            ("💣 Forced panic in backend service", "CRITICAL", "forced_panic", {"stack_trace": "panic at chaos.go:42"})
        ]
        self.rare_scenarios = [
            ("☢️ Full cluster outage", "EMERGENCY", "full_outage", {"duration_min": random.randint(5, 60)}),
            ("🦠 Data corruption detected", "ALERT", "data_corruption", {"backup_status": "none"})
        ]

    def _log_startup_message(self):
        print(f"📢 Chaos logger initialized. Database: {DB_NAME}")

    def _generate_metadata(self) -> Dict:
        return {
            "environment": random.choice(["prod", "staging", "dev"]),
            "release_version": f"v{random.randint(1, 10)}.{random.randint(0, 20)}.{random.randint(0, 5)}",
            "chaos_agent": f"simulator-bot-{random.randint(1, 10)}",
            "session_id": f"session-{random.getrandbits(64):016x}",
            "region": random.choice(["us-central1", "europe-west1", "asia-northeast1"]),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def _select_scenario(self) -> Tuple[str, str, str, Dict]:
        if random.random() < 0.1:
            return random.choice(self.rare_scenarios)
        return random.choice(self.scenarios)

    def generate_logs(self, count: int = 10):
        print(f"🔧 Generating {count} chaos logs...")
        for i in range(1, count + 1):
            try:
                msg, severity, failure_type, scenario_metadata = self._select_scenario()
                metadata = self._generate_metadata()
                log_data = {
                    "experiment_id": f"exp{i:04}",
                    "message": f"{msg} during chaos experiment #{i}",
                    "failure_type": failure_type,
                    "severity": severity,
                    "impact_level": random.choice(["low", "medium", "high", "critical"]),
                    "environment": metadata["environment"],
                    "release_version": metadata["release_version"],
                    "chaos_agent": metadata["chaos_agent"],
                    "session_id": metadata["session_id"],
                    "region": metadata["region"],
                    "timestamp": metadata["timestamp"],
                    "scenario_metadata": str(scenario_metadata),
                    "secondary_effect": None,
                    "injected": 1,
                    "log_sequence": i
                }

                if random.random() < 0.05:
                    sec_msg, _, sec_type, _ = random.choice(self.scenarios)
                    log_data["secondary_effect"] = f"Concurrent issue: {sec_msg} ({sec_type})"

                self.cursor.execute("""
                    INSERT INTO chaos_logs (
                        experiment_id, message, failure_type, severity, impact_level,
                        environment, release_version, chaos_agent, session_id, region,
                        timestamp, scenario_metadata, secondary_effect, injected, log_sequence
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, tuple(log_data.values()))
                self.conn.commit()

                print(f"✅ [{severity}] Log #{i}: {msg}")
                time.sleep(random.uniform(0.05, 0.2))
            except Exception as e:
                print(f"🚨 Error on log #{i}: {str(e)}", file=sys.stderr)

    def __del__(self):
        runtime = datetime.now(timezone.utc) - self.start_time
        print(f"\n🛑 Chaos Logger shut down after {runtime.total_seconds():.2f} seconds")
        self.conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate chaos logs into SQLite DB.")
    parser.add_argument("--count", type=int, default=10, help="Number of logs to generate.")
    args = parser.parse_args()

    logger = ChaosLogger()
    logger.generate_logs(count=args.count)
