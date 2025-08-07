# Tempo

```
╔════════════════════════════════════════╗
║  _____ _____ __  __ ____   ___         ║
║ |_   _| ____|  \/  |  _ \ / _ \        ║
║   | | |  _| | |\/| | |_) | | | |       ║
║   | | | |___| |  | |  __/| |_| |       ║
║   |_| |_____|_|  |_|_|    \___/        ║
║                                        ║
║   Your time. Your data. Your rhythm.   ║
╚════════════════════════════════════════╝
```

[![Tests](https://github.com/AnrokX/tempo/actions/workflows/test.yml/badge.svg)](https://github.com/AnrokX/tempo/actions/workflows/test.yml)
[![Test Coverage](https://img.shields.io/badge/coverage-89%25-brightgreen)](https://github.com/AnrokX/tempo)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](https://github.com/AnrokX/tempo/blob/main/LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey)](https://github.com/AnrokX/tempo)

A 100% open-source, lightweight desktop application for tracking computer activity and managing time. Built with privacy, security, and performance as core principles.

## Core Principles

- **100% Open Source**: Complete transparency in how your data is collected and processed
- **100% Local**: All data stays on your machine - no cloud, no external servers, no telemetry
- **Secure**: Your activity data is private and protected
- **Lightweight**: Minimal resource usage, runs quietly in the background
- **Cross-Platform**: Full support for Windows and Linux

## Features

### Core Tracking
- **Application Monitoring**: Track application usage with intelligent sampling (5-30 second intervals)
- **Smart Aggregation**: Combine consecutive same-app usage to reduce data redundancy
- **Idle Detection**: Automatically pause tracking during inactivity
- **Minimal Resource Usage**: < 10MB RAM, < 0.1% CPU usage

### Data Management
- **Local SQLite Database**: All data stored locally in a single, portable database file
- **Efficient Storage**: Smart compression keeps database small (< 50MB for a year of data)
- **Data Retention**: Configurable data retention policies (keep raw data for X days, aggregated forever)

### Categorization System
- **Productivity Scoring**: Three-tier system (Productive, Neutral, Distracting)
- **Auto-Categorization**: Common apps pre-categorized based on community data
- **Custom Rules**: Override categories per application
- **Category Groups**: Group similar apps together (e.g., all browsers, all IDEs)

### Analytics & Reports
- **Daily Summary**: See today's application usage at a glance
- **Weekly/Monthly Reports**: Track productivity trends over time
- **Productivity Score**: 0-100 daily score based on time in productive vs distracting apps
- **Focus Time**: Track uninterrupted productive work sessions

### Export & Integration
- **CSV Export**: Full data export for external analysis
- **JSON API**: Local REST API for third-party integrations
- **PDF Reports**: Generate professional time reports
- **Backup/Restore**: Easy data backup and migration

### Future Features
- **Goals & Limits**: Set daily goals for productive time or limits on distracting apps
- **Notifications**: Gentle reminders when spending too much time on distracting apps
- **Focus Mode**: Block distracting apps during focus sessions
- **Multi-Device Sync**: Optional encrypted sync between devices (fully local network)

## Architecture

### Backend Components
```
src/
├── core/
│   ├── tracker.py       # Main application tracking loop
│   ├── database.py      # SQLite database interface
│   ├── aggregator.py    # Data aggregation and compression
│   └── categorizer.py   # Application categorization logic
├── api/
│   ├── server.py        # Local REST API server
│   └── endpoints.py     # API endpoint definitions
├── utils/
│   ├── platform.py      # OS-specific window tracking
│   └── config.py        # Configuration management
└── cli.py               # Command-line interface
```

### Database Schema
- **applications**: Store unique applications (id, name, category, productivity_score)
- **sessions**: Track usage sessions (id, app_id, start_time, end_time, idle_time)
- **daily_stats**: Aggregated daily statistics for performance
- **categories**: Custom category definitions
- **goals**: User-defined goals and limits

### Technology Stack

- **Language**: Python 3.8+ (maximum compatibility, minimal dependencies)
- **Database**: SQLite 3 (zero-configuration, portable)
- **GUI Framework**: (Future) PyQt6 or Tkinter for native feel
- **Web Dashboard**: (Future) FastAPI + vanilla JS for lightweight web UI
- **Platform APIs**:
  - Windows: `pywin32` for window tracking
  - Linux: `python-xlib` or `subprocess` with `xdotool`

## Quick Start

```bash
# Clone the repository
git clone https://github.com/AnrokX/tempo.git
cd tempo

# Install Tempo (coming soon)
python setup.py install

# Start tracking
tempo start

# Check your daily rhythm
tempo today

# See your productivity tempo
tempo report
```

## Why Tempo?

**Tempo** helps you understand and optimize your work rhythm. Unlike cloud-based trackers, Tempo respects your privacy by keeping all data local. It's not about tracking every second - it's about finding your optimal productivity tempo.

## Privacy & Security

- All data is stored locally on your machine
- No network connections required for core functionality
- No telemetry, analytics, or data collection
- You own and control 100% of your data
- Open source code for full transparency

## Development

This project is in early development. Contributions are welcome!

## License

MIT License - See LICENSE file for details
