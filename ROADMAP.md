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

### Phase 2: Data Management & Analytics (COMPLETE)
**Goal:** Add intelligence to raw tracking data

#### Tasks:
- [x] **Categorization System** (`src/core/categorizer.py`)
  - [x] Default app categories (50+ apps)
  - [x] Productivity scoring (weighted system)
  - [x] Custom category rules
  - [x] Save user preferences to JSON

- [x] **Data Aggregation** (`src/core/aggregator.py`)
  - [x] Hourly summaries
  - [x] Daily rollups
  - [x] Weekly/monthly aggregates
  - [x] Data compression for old records

- [x] **Reporting Engine** (`src/core/reports.py`)
  - [x] Daily productivity score
  - [x] Top apps by usage
  - [x] Time distribution charts (text-based)
  - [x] Trend analysis

- [ ] **Enhanced CLI** (next phase)
  - [ ] Report commands (day/week/month)
  - [ ] Category management
  - [ ] App-specific queries

**Achievements:**
- 89% test coverage (exceeded 80% requirement)
- 51 total tests passing
- Full TDD implementation
- Smart categorization system
- Comprehensive reporting

**Deliverable:** Intelligent reports and productivity insights

---

### Phase 3: Export & Integration (COMPLETE)
**Goal:** Make data portable and integrable

#### Tasks:
- [x] **Export Module** (`src/core/export.py`)
  - [x] CSV export with filters
  - [x] JSON export for API consumption
  - [x] Backup/restore functionality
  - [x] Data anonymization option

- [x] **Configuration System** (`src/utils/config.py`)
  - [x] JSON config file
  - [x] User preferences
  - [x] App-specific settings
  - [x] Goal definitions

- [x] **CLI Export Commands**
  - [x] Export to CSV/JSON
  - [x] Date range filtering
  - [x] Database backup/restore

- [ ] **Local API Server** (`src/api/`) - Deferred to Phase 5
  - [ ] FastAPI setup
  - [ ] REST endpoints
  - [ ] Real-time data access
  - [ ] WebSocket for live updates

**Achievements:**
- DataExporter class with full export capabilities
- ConfigManager for flexible configuration
- CLI integration with all export features
- 25 new tests added
- Test coverage maintained

**Deliverable:** Full data portability and configuration system

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

## Timeline & Progress

| Phase | Duration | Status | Achievements |
|-------|----------|--------|--------------|
| Phase 1: Core Engine | 1 week | ✅ Complete | Database, Sessions, Basic CLI |
| Phase 2: Analytics | 1 week | ✅ Complete | Categorization, Aggregation, Reports |
| Phase 3: Export & CI | 1 week | ✅ Complete | CSV/JSON Export, Config, **Full CI** |
| Phase 4: GUI | 2 weeks | 🔄 Next | Dashboard, Timeline, Settings |
| Phase 5: Advanced | 1 week | ⏳ Planned | Goals, Focus Mode, Alerts |
| Phase 6: Release | 1 week | ⏳ Planned | Installers, Documentation |

**Progress: 3/6 Phases Complete (50%)**
**Test Coverage: 81% | Tests: 76 passing on Windows & Linux**

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

## Current Status: Phase 3 Complete with Full Cross-Platform CI ✅

### Major Achievements:
- **Full Windows & Linux CI Support** - All 76 tests passing on both platforms!
- **81% Code Coverage** - Comprehensive test suite
- **Cross-Platform Compatibility** - Resolved all platform-specific issues
- **6 CI Jobs Running** - Python 3.8, 3.11, 3.12 on Ubuntu & Windows

### CI/CD Milestones Completed:
1. ✅ Fixed module import issues (moved to module level)
2. ✅ Fixed dependency installation (`pip install -e ".[dev]"`)
3. ✅ Fixed Unicode encoding (UTF-8 for README)
4. ✅ Fixed SQLite database locking on Windows
5. ✅ Fixed platform-specific path validation
6. ✅ All tests passing on both platforms!

### Next Steps for Tempo:
1. Implement actual window tracking for Windows/Linux
2. Build background service for real-time monitoring
3. Add GUI interface (Phase 4)
4. Create installer packages for distribution

---

*This roadmap is a living document and will be updated as development progresses.*