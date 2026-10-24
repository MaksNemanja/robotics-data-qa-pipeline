from src.readers import MCAPLogReader
from src.validator import DataQualityValidator
from src.reporter import QAReporter

def main():
    mcap_path = "data/sample.mcap"
    print(f"=== Running QA Pipeline on: {mcap_path} ===")
    
    reader = MCAPLogReader(mcap_path)
    topics = reader.inspect_channels()
    
    print("\nDiscovered Topics:")
    for topic, encoding in topics.items():
        print(f" - {topic} [{encoding}]")

    messages_by_topic = {}
    for msg in reader.read_messages():
        topic = msg["topic"]
        if topic not in messages_by_topic:
            messages_by_topic[topic] = []
        messages_by_topic[topic].append(msg)
        
    validator = DataQualityValidator(max_allowed_gap_ms=50.0)
    reporter = QAReporter(output_dir="reports")

    full_report = {}
    print("\n[2] QA Validation Report:")
    for topic, msg_lists in messages_by_topic.items():
        report = validator.analyze_topic(topic, msg_lists)
        full_report[topic] = report

        print(f"\n--- Topic: {report['topic']}")
        print(f" - Total Messages: {report['total_messages']}")
        print(f" - Duration (s): {report['duration_sec']}")
        print(f" - Avvg Frequency (FPS): {report['avg_fps']} Hz")
        print(f" - Anomalies (Gaps > 50ms): {report['anomalies_count']}")

    reporter.export_to_json(full_report)

if __name__ == "__main__":
    main()