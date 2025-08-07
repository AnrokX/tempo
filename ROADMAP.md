# Tempo - Project Roadmap & Development Plan

```
     Finding your productivity rhythm
```

## Project Vision
**Tempo** - A lightweight, privacy-focused activity tracker that runs entirely locally, helping users find their optimal work tempo while consuming minimal system resources.

## Development Phases

### Phase 0: Project Setup (Complete)
- [x] Initialize git repository
- [x] Create project structure
- [x] Define architecture and features
- [x] Document usage examples

---

### Phase 1: Core Tracking Engine (COMPLETE)
**Goal:** Build the minimal viable tracker that captures application usage

#### Tasks:
- [x] **Platform Detection Module** (`src/utils/platform.py`)
  - [x] Detect OS (Windows/Linux/macOS)
  - [x] Import appropriate window tracking libraries
  - [x] Handle missing dependencies gracefully

- [x] **Window Tracking** (`src/core/tracker.py`)
  - [x] Get active window process name
  - [x] Get window title (optional)
  - [ ] Sample every 10-30 seconds (next phase)
  - [ ] Handle system sleep/wake events (next phase)

- [x] **Database Layer** (`src/core/database.py`)
  - [x] Create SQLite schema
  - [x] Connection management
  - [x] Basic CRUD operations
  - [x] Data integrity checks

- [x] **Session Management** (`src/core/session.py`)
  - [x] Detect app switches
  - [x] Merge consecutive same-app usage
  - [x] Calculate session duration
  - [ ] Handle idle time (next phase)

- [x] **Basic CLI** (`src/cli.py`)
  - [x] Start/stop commands
  - [x] Status command
  - [x] Today summary command

**Achievements:**
- 82% test coverage (exceeded 80% requirement)
- 29 passing tests
- Full TDD implementation
- Clean, modular architecture

**Deliverable:** Tempo v0.1 - A working tracker that logs app usage to SQLite database

---

### Phase 2: Data Management & Analytics
**Goal:** Add intelligence to raw tracking data

#### Tasks:
- [ ] **Categorization System** (`src/core/categorizer.py`)
  - [ ] Default app categories
  - [ ] Productivity scoring (1-3 scale)
  - [ ] Custom category rules
  - [ ] Save user preferences

- [ ] **Data Aggregation** (`src/core/aggregator.py`)
  - [ ] Hourly summaries
  - [ ] Daily rollups
  - [ ] Weekly/monthly aggregates
  - [ ] Data compression for old records

- [ ] **Reporting Engine** (`src/core/reports.py`)
  - [ ] Daily productivity score
  - [ ] Top apps by usage
  - [ ] Time distribution charts (text-based)
  - [ ] Trend analysis

- [ ] **Enhanced CLI** 
  - [ ] Report commands (day/week/month)
  - [ ] Category management
  - [ ] App-specific queries

**Deliverable:** Intelligent reports and productivity insights

---

### Phase 3: Export & Integration
**Goal:** Make data portable and integrable

#### Tasks:
- [ ] **Export Module** (`src/core/export.py`)
  - [ ] CSV export with filters
  - [ ] JSON export for API consumption
  - [ ] Backup/restore functionality
  - [ ] Data anonymization option

- [ ] **Configuration System** (`src/utils/config.py`)
  - [ ] JSON config file
  - [ ] User preferences
  - [ ] App-specific settings
  - [ ] Goal definitions

- [ ] **Local API Server** (`src/api/`)
  - [ ] FastAPI setup
  - [ ] REST endpoints
  - [ ] Real-time data access
  - [ ] WebSocket for live updates

**Deliverable:** Full data portability and API access

---

### Phase 4: Simple GUI
**Goal:** User-friendly interface for non-technical users

#### GUI Design Principles:
- **Minimal**: Single window, no unnecessary features
- **Fast**: Instant load, responsive updates
- **Clear**: Data visualization at a glance
- **Native**: Looks good on Windows and Linux

#### Tasks:
- [ ] **Technology Selection**
  - [ ] Evaluate: Tkinter (built-in) vs PyQt6 (modern) vs Web UI
  - [ ] Create proof of concept
  - [ ] Finalize choice

- [ ] **Main Dashboard** (`src/gui/dashboard.py`)
  - [ ] Today's summary card
  - [ ] Live activity indicator
  - [ ] Productivity score gauge
  - [ ] Top 5 apps list

- [ ] **Timeline View** (`src/gui/timeline.py`)
  - [ ] Horizontal timeline (like RescueTime)
  - [ ] Color-coded blocks by category
  - [ ] Hover for details
  - [ ] Zoom in/out for different time scales

- [ ] **Settings Panel** (`src/gui/settings.py`)
  - [ ] Category management
  - [ ] App productivity scores
  - [ ] Tracking preferences
  - [ ] Export options

- [ ] **System Tray Integration**
  - [ ] Minimize to tray
  - [ ] Quick stats on hover
  - [ ] Start/stop from tray
  - [ ] Today's time in tray icon

**Deliverable:** Simple, functional desktop GUI

---

### Phase 5: Advanced Features
**Goal:** Power user features and optimizations

#### Tasks:
- [ ] **Goals & Alerts** (`src/core/goals.py`)
  - [ ] Daily productivity goals
  - [ ] App usage limits
  - [ ] Break reminders
  - [ ] Achievement notifications

- [ ] **Focus Mode** (`src/core/focus.py`)
  - [ ] Block distracting apps
  - [ ] Pomodoro timer
  - [ ] Focus session tracking
  - [ ] Do not disturb mode

- [ ] **Advanced Analytics**
  - [ ] Pattern detection
  - [ ] Productivity trends
  - [ ] Peak hours analysis
  - [ ] Weekly comparisons

- [ ] **Performance Optimizations**
  - [ ] Reduce CPU usage to < 0.1%
  - [ ] Memory usage under 10MB
  - [ ] Database optimization
  - [ ] Efficient queries

**Deliverable:** Feature-complete tracker

---

### Phase 6: Polish & Release
**Goal:** Production-ready application

#### Tasks:
- [ ] **Installer/Packaging**
  - [ ] PyInstaller for single executable
  - [ ] Windows installer (.msi)
  - [ ] Linux packages (.deb, .rpm, AppImage)
  - [ ] Auto-update mechanism

- [ ] **Documentation**
  - [ ] User guide
  - [ ] Video tutorials
  - [ ] FAQ section
  - [ ] Troubleshooting guide

- [ ] **Testing**
  - [ ] Unit tests (pytest)
  - [ ] Integration tests
  - [ ] Performance benchmarks
  - [ ] Multi-day stress testing

- [ ] **Community**
  - [ ] GitHub releases
  - [ ] Contributing guidelines
  - [ ] Issue templates
  - [ ] Feature request process

**Deliverable:** Tempo v1.0 - Production Release

---

## Timeline Estimate

| Phase | Duration | Target Completion |
|-------|----------|------------------|
| Phase 1 | 1 week | Week 1 |
| Phase 2 | 1 week | Week 2 |
| Phase 3 | 1 week | Week 3 |
| Phase 4 | 2 weeks | Week 5 |
| Phase 5 | 1 week | Week 6 |
| Phase 6 | 1 week | Week 7 |

**Total: 7 weeks to Tempo v1.0**

## Success Metrics

### Performance Targets
- [ ] < 10MB RAM usage
- [ ] < 0.1% CPU usage
- [ ] < 50MB database for 1 year of data
- [ ] < 1 second startup time
- [ ] Zero network connections

### Feature Targets
- [ ] Track 95%+ of active computer time
- [ ] Accurate categorization for top 100 apps
- [ ] Generate reports in < 1 second
- [ ] Export 1 year of data in < 10 seconds

### User Experience Targets
- [ ] Install in < 1 minute
- [ ] Understand UI without documentation
- [ ] Access any data in < 3 clicks
- [ ] Zero configuration required to start

## Current Status: Phase 2 - Data Management & Analytics

### Next Steps for Tempo:
1. Set up Python project structure for Tempo
2. Implement basic window tracking for current OS
3. Create SQLite schema for tempo.db
4. Build Tempo CLI for start/stop/status commands

---

*This roadmap is a living document and will be updated as development progresses.*