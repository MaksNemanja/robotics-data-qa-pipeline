import json
import os
from typing import Dict, Any


class QAReporter:
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def export_to_json(self, reports_data: Dict[str, Any], filename: str = "qa_report.json") -> str:
        """Sauvegarde les résultats de validation dans un fichier JSON structuré."""
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(reports_data, f, indent=4)
        print(f"\n[+] QA Report exported to: {filepath}")
        return filepath