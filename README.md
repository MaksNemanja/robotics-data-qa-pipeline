# Robotics Data QA Pipeline (`robotics-data-qa-pipeline`)

A lightweight, modular Python pipeline designed to ingest, inspect, and validate robotic log files (`.mcap`), ensuring data integrity for Machine Learning and Embodied AI workflows.

## 🚀 Features
- **Multi-Middleware Support**: Parses MCAP logs (compatible with ROS 1 / ROS 2 data structures) without requiring a full local ROS installation.
- **Temporal Quality Assurance**: Computes precise message frequencies (FPS) and detects frame drops or time gaps exceeding configurable thresholds.
- **Structured Reporting**: Exports automated validation metrics into JSON reports for CI/CD or downstream ML datasets ingestion.

## 🛠️ Tech Stack
- **Language**: Python 3.10+
- **Libraries**: `mcap`, `mcap-ros2`
- **Testing**: Pytest / Unit-testing suite

