from src.validator import DataQualityValidator

def test_anomaly_detection():
    validator = DataQualityValidator(max_allowed_gap_ms=50.0)
    
    # Simulation de messages : 100ms = 100 000 000 ns
    # On simule un saut de 150ms entre le message 2 et 3 (anomalie !)
    mock_messages = [
        {"log_time_ns": 1_000_000_000},
        {"log_time_ns": 1_020_000_000},  # +20ms (Normal)
        {"log_time_ns": 1_040_000_000},  # +20ms (Normal)
        {"log_time_ns": 1_200_000_000},  # +160ms (ANOMALIE > 50ms)
        {"log_time_ns": 1_220_000_000},  # +20ms (Normal)
    ]

    report = validator.analyze_topic("/test_camera", mock_messages)
    
    print(f"--- Test Report for {report['topic']} ---")
    print(f"Total Messages : {report['total_messages']}")
    print(f"Duration       : {report['duration_sec']} s")
    print(f"Avg Frequency  : {report['avg_fps']} Hz")
    print(f"Anomalies      : {report['anomalies_count']}")
    
    for a in report["anomalies"]:
        print(f" -> Gap detected: {a['gap_ms']:.2f} ms at index {a['index']}")

if __name__ == "__main__":
    test_anomaly_detection()