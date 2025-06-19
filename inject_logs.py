import sqlite3
import random
import time
import sys
import os
import argparse
from datetime import datetime, timezone
from typing import Dict, List, Tuple

# Resolve base directory and set logger-data path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "mcp-toolbox/logger-data")
os.makedirs(LOG_DIR, exist_ok=True)

# Corrected DB file name to match configuration
DB_NAME = os.path.join(LOG_DIR, "database.db")

class ChaosLogger:
    def __init__(self):
        try:
            self.conn = sqlite3.connect(DB_NAME)
            self.cursor = self.conn.cursor()
            self._create_tables()
            self._init_scenarios()
            self.start_time = datetime.now(timezone.utc)
            self._log_startup_message()
        except Exception as e:
            print(f"🚨 Failed to initialize logger: {str(e)}", file=sys.stderr)
            raise

    def _create_tables(self):
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
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_health_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_timestamp TEXT,
                service_name TEXT,
                cpu_usage REAL,
                memory_usage_mb REAL,
                disk_io_mb REAL,
                response_time_ms REAL,
                status TEXT,
                region TEXT
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
        return random.choice(self.rare_scenarios) if random.random() < 0.1 else random.choice(self.scenarios)

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

    def generate_health_metrics(self, count: int = 50):
        print(f"📊 Generating {count} system health metric entries...")
        services = ["auth-api", "billing-api", "user-service", "notifications", "search-service"]
        for _ in range(count):
            try:
                data = {
                    "metric_timestamp": datetime.now(timezone.utc).isoformat(),
                    "service_name": random.choice(services),
                    "cpu_usage": round(random.uniform(5.0, 95.0), 2),
                    "memory_usage_mb": round(random.uniform(100.0, 2048.0), 2),
                    "disk_io_mb": round(random.uniform(1.0, 300.0), 2),
                    "response_time_ms": round(random.uniform(50.0, 3000.0), 2),
                    "status": random.choices(["ok", "degraded", "failed"], weights=[0.7, 0.2, 0.1])[0],
                    "region": random.choice(["us-central1", "europe-west1", "asia-northeast1"])
                }

                self.cursor.execute("""
                    INSERT INTO system_health_metrics (
                        metric_timestamp, service_name, cpu_usage, memory_usage_mb,
                        disk_io_mb, response_time_ms, status, region
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, tuple(data.values()))
                self.conn.commit()

                print(f"✅ Health Metric: {data['service_name']} - CPU: {data['cpu_usage']}% - Status: {data['status']}")
                time.sleep(random.uniform(0.05, 0.15))
            except Exception as e:
                print(f"🚨 Error inserting metric: {str(e)}", file=sys.stderr)

    def __del__(self):
        runtime = datetime.now(timezone.utc) - self.start_time
        print(f"\n🛑 Chaos Logger shut down after {runtime.total_seconds():.2f} seconds")
        self.conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate chaos logs and/or health metrics into SQLite DB.")
    parser.add_argument("--count", type=int, default=10, help="Number of chaos logs to generate.")
    parser.add_argument("--health", type=int, default=0, help="Number of system health metrics to generate.")
    args = parser.parse_args()

    logger = ChaosLogger()
    logger.generate_logs(count=args.count)

    if args.health > 0:
        logger.generate_health_metrics(count=args.health)
