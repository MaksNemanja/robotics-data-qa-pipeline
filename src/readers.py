from typing import Dict, Any, List, Optional
from mcap.reader import make_reader
from mcap_ros2.decoder import DecoderFactory


class MCAPLogReader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def inspect_channels(self) -> Dict[str, Any]:
        """Lit les métadonnées du fichier MCAP et liste les topics disponibles."""
        topics_info = {}
        with open(self.file_path, "rb") as f:
            reader = make_reader(f)
            summary = reader.get_summary()

            if summary and hasattr(summary, "channels") and summary.channels:
                for channel in summary.channels.values():
                    topics_info[channel.topic] = channel.message_encoding

        return topics_info

    def read_messages(self, target_topics: Optional[List[str]] = None):
        """Générateur qui extrait les messages (décodés ou bruts) des topics ciblés."""
        with open(self.file_path, "rb") as f:
            reader = make_reader(f, decoder_factories=[DecoderFactory()])
            
            for schema, channel, message in reader.iter_messages(topics=target_topics):
                yield {
                    "topic": channel.topic,
                    "log_time_ns": message.log_time,
                    "publish_time_ns": message.publish_time,
                    "sequence": message.sequence,
                    "data_size": len(message.data),
                    "schema_name": schema.name if schema else "Unknown"
                }