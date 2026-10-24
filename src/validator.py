from typing import List, Dict, Any

class DataQualityValidator:
    def __init__(self, max_allowed_gap_ms: float = 50.0):
        self.max_allowed_gap_ns = max_allowed_gap_ms * 1e6

    def analyze_topic(self, topic_name: str, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not messages:
            return {"topic": topic_name, "error": "No messages found"}

        timestamps = [msg["log_time_ns"] for msg in messages]
        timestamps.sort()

        total_messages = len(timestamps)
        duration_ns = timestamps[-1] - timestamps[0] if total_messages > 1 else 0
        duration_sec = duration_ns / 1e9

        # Calcul sécurisé du FPS : évite les divisions par des durées quasi nulles
        MIN_DURATION_SEC = 0.001  # 1 ms minimum pour un calcul de fréquence pertinent
        if duration_sec >= MIN_DURATION_SEC:
            avg_fps = round(total_messages / duration_sec, 2)
        else:
            avg_fps = 0.0  # Durée trop courte pour déterminer une fréquence stable

        anomalies = []
        for i in range(1, total_messages):
            gap_ns = timestamps[i] - timestamps[i - 1]
            if gap_ns > self.max_allowed_gap_ns:
                anomalies.append({
                    "index": i,
                    "gap_ms": round(gap_ns / 1e6, 2)
                })

        return {
            "topic": topic_name,
            "total_messages": total_messages,
            "duration_sec": round(duration_sec, 4),
            "avg_fps": avg_fps,
            "anomalies_count": len(anomalies),
            "anomalies": anomalies
        }