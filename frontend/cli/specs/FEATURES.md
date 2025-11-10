# Beaver Go CLI - Features Specification

## Feature Overview

This document provides a comprehensive specification of all features in the Beaver Go CLI, organized by functional area.

---

## 1. Core Typing Practice

### 1.1 Code Display

**Description**: Display algorithm code with proper syntax highlighting and metadata.

**Requirements**:
- Display complete algorithm code in a scrollable viewport
- Apply language-specific syntax highlighting (Chroma lexer)
- Show algorithm metadata above code:
  - Title (clickable/copyable link to documentation)
  - Programming language
  - Tags (e.g., "sort", "graph", "dynamic-programming")
- Support for multiple programming languages (Python initially, extensible)
- Code should be properly indented and formatted as-is from source
- Viewport should auto-scroll to show current typing position

**Technical Notes**:
- Use Chroma lexer matching the language specified in metadata
- Code should be rendered in a fixed-width font
- Minimum viewport height: 10 lines, expands based on terminal size

### 1.2 Typing Input System

**Description**: Character-by-character typing with real-time validation and feedback.

**Requirements**:

**Input Handling**:
- Accept printable characters, Tab, Enter, Backspace
- Tab converts to 4 spaces (configurable)
- Enter moves to next line
- Backspace allows deletion of previous character
- No clipboard paste allowed (or treat as invalid input)

**Validation**:
- Compare each typed character against expected source code
- Track correct vs incorrect characters
- Track corrections (backspace + retype) separately
- Highlight errors visually in the display

**Visual Feedback**:
- Correct characters: Normal highlighted syntax color
- Incorrect characters: Red background or red text
- Cursor position: Visible block or underline cursor
- Already-typed text: Slightly dimmed or different shade
- Upcoming text: Normal brightness

**Tracking**:
- Record timestamp for each keypress event
- Track typing events: correct character, error, correction (backspace)
- Store events in memory for statistics calculation
- Start timer on first keypress
- Stop timer on last character completion

**Edge Cases**:
- Ignore non-printable characters (F-keys, Alt, etc. unless bound)
- Handle rapid keypresses without dropping events
- Prevent input after code completion

### 1.3 Progress Tracking

**Description**: Visual indication of typing progress through the algorithm.

**Requirements**:
- Display progress indicator showing position in code
- Examples: "Line 15/42" or "65% complete" or progress bar
- Update in real-time as user types
- Show total characters typed vs total characters

**Visual Design**:
- Subtle, non-distracting placement (footer or header)
- No animation, just state updates

### 1.4 Statistics Calculation

**Description**: Real-time calculation and display of typing statistics.

**Metrics to Track**:

1. **Time Elapsed**
   - Start: First keypress
   - End: Last character typed correctly
   - Display: MM:SS format
   - Update frequency: 100ms

2. **Total Characters**
   - Count all characters in source code (including whitespace)
   - Display after completion

3. **Total Errors**
   - Count of incorrect keypresses
   - Does NOT include corrections (backspace + fix)
   - Increment on each non-matching character

4. **Corrections**
   - Count of backspace usages
   - Separate metric from errors
   - Shows how many times user self-corrected

5. **Accuracy Percentage**
   - Formula: `(Total Characters - Errors) / Total Characters * 100`
   - Display: "95.5%" format (one decimal place)

6. **Characters Per Minute (CPM)**
   - Formula: `Total Characters / (Time in Seconds / 60)`
   - Display: "450 CPM" format (integer)
   - More stable metric than WPM for code

**Statistics Display**:
- Show statistics immediately after code completion
- Simple table format, no charts
- Clear, readable presentation
- Option to show statistics during typing (footer?) or only after

### 1.5 Completion Handling

**Description**: Actions and display when user completes typing an algorithm.

**Flow**:
1. Detect when last character is typed correctly
2. Stop timer
3. Calculate all statistics
4. Transition to results screen
5. Show "Press Tab to continue" or similar prompt

**Results Screen**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
          Results
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Algorithm: Bubble Sort

Time:           01:23
Characters:     156
Errors:         7
Corrections:    3
Accuracy:       95.5%
CPM:            678

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tab - Next Algorithm    q - Quit
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 2. Algorithm Management

### 2.1 Background Prefetching

**Description**: Fetch algorithms from API in background to ensure smooth UX.

**Requirements**:
- Run background goroutine that fetches algorithms
- Maintain buffered channel (capacity: 5 algorithms)
- Start fetching on app startup
- Continue fetching as user consumes from queue
- Apply current filters (language, tags) to fetch requests

**Behavior**:
- Non-blocking: UI never waits for fetch
- Retry logic: Exponential backoff on failure (1s, 2s, 4s, 8s, max 30s)
- Error handling: Log errors but don't crash app
- On empty queue: Show cached error screen, allow retry

**Technical**:
- Use `context.Context` for cancellation
- Use buffered channel: `make(chan *CodeDocument, 5)`
- Worker goroutine with `select` for shutdown
- HTTP client with timeout (5s per request)

### 2.2 Algorithm Navigation

**Description**: Move between algorithms efficiently.

**Requirements**:

**Next Algorithm**:
- Keyboard shortcut to load next algorithm
- Pop from prefetch queue
- If queue empty: Show error, prompt to retry or change filters
- Reset all typing state (timer, input buffer, statistics)
- Transition smoothly (no flicker)

**Automatic Next** (Optional Enhancement):
- After viewing results, Tab loads next automatically
- Seamless transition from results to new algorithm

**Behavior**:
- Clear previous algorithm completely
- Reset cursor to start position
- Clear any error highlights
- Start fresh with timer at 0:00

### 2.3 Filtering

**Description**: Filter available algorithms by language and tags.

**Requirements**:

**Filter Options**:
- Language: Single selection (e.g., "Python", "Go", "Java")
- Tags: Multiple selection (e.g., ["sort", "graph"])

**Filter Application**:
- Filters apply to API requests for random code documents
- Backend handles filter logic
- CLI sends query parameters: `?language=python&tags=sort&tags=graph`

**Filter Persistence**:
- Filters remain active until changed
- Stored in application state
- Applied to background prefetch goroutine

**Special Cases**:
- No filters: Fetch any algorithm (most variety)
- Invalid filter combination (no results): API returns error, show message
- Filter change: Clear prefetch queue, restart with new filters

---

## 3. Settings Management

### 3.1 Settings Screen

**Description**: Modal screen for configuring application behavior.

**Available Settings**:

1. **Language Filter**
   - Dropdown/select menu
   - Options: "Any", "Python", "Go", "JavaScript", etc.
   - Default: "Any"

2. **Tags Filter**
   - Multi-select checkboxes
   - Options: All available tags from API (sort, graph, search, etc.)
   - Default: None selected (all tags allowed)

3. **Theme** (Optional)
   - Options: "Dark", "Light"
   - Affects syntax highlighting and UI colors

4. **Tab Width** (Optional)
   - Options: 2, 4, 8 spaces
   - Default: 4

**UI Behavior**:
- Modal overlay on top of main screen
- Escape or Save button to close
- Changes apply immediately on save
- Cancel option to discard changes

**Persistence**:
- Settings stored in config file (`~/.config/beaver/config.yaml`)
- Load on startup
- Save on change

### 3.2 Configuration File

**Location**: `~/.config/beaver/config.yaml`

**Format**:
```yaml
api:
  base_url: "https://beaver-api.com"
  timeout: 5s

filters:
  language: "python"
  tags:
    - "sort"
    - "graph"

ui:
  theme: "dark"
  tab_width: 4

prefetch:
  queue_size: 5
```

**Behavior**:
- Create default config on first run
- Validate on load, use defaults for invalid values
- Allow environment variable overrides (e.g., `BEAVER_API_URL`)

---

## 4. User Interface Components

### 4.1 Header

**Content**:
- App title and version: "Beaver v1.0.0"
- Current time elapsed (during typing)
- Progress indicator

**Layout**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Beaver v1.0.0                      Time: 00:45
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 4.2 Footer

**Content**:
- Available keyboard shortcuts for current context
- Status messages (e.g., "Loading...", "Error: ...")

**Layout**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tab: Next  ?:Help  s:Settings  q:Quit
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Context-Aware**:
- Typing mode: Show "Tab: Skip" or minimal shortcuts
- Results mode: Show "Tab: Next"
- Settings mode: Show "Esc: Save" or "q: Cancel"

### 4.3 Algorithm Metadata Panel

**Content**:
- Algorithm title with link to documentation
- Language badge
- Tags (comma-separated or as badges)

**Layout**:
```
┌─────────────────────────────────────────────┐
│ Bubble Sort Algorithm                       │
│ [docs: geeksforgeeks.org/bubble-sort]       │
│                                             │
│ Language: Python    Tags: sort, beginner   │
└─────────────────────────────────────────────┘
```

### 4.4 Code Viewport

**Description**: Main area displaying the algorithm code.

**Features**:
- Syntax highlighting
- Line numbers (optional)
- Current typing position highlighted
- Scrollable if code exceeds viewport height
- Auto-scroll to keep cursor in view

**Dimensions**:
- Full width of terminal minus padding
- Height: Terminal height minus header/footer/metadata (minimum 10 lines)

### 4.5 Help Screen

**Description**: Modal screen showing keyboard shortcuts and usage info.

**Content**:
- Keyboard shortcuts reference
- Quick start guide
- Link to documentation
- Version info
- Contributors/credits

**Format**:
- Markdown rendered as styled text
- Scrollable if content exceeds screen
- Escape to close

### 4.6 Error Screen

**Description**: Full-screen or modal display for errors.

**Triggers**:
- No algorithms available (queue empty, all retries failed)
- API unreachable
- Invalid configuration
- Network timeout

**Content**:
- Error icon/symbol
- Brief error message
- Suggested action (e.g., "Check your network connection")
- Options: Retry, Change Settings, Quit

**Example**:
```
┌─────────────────────────────────────────────┐
│                    ⚠                        │
│                                             │
│   No algorithms available                   │
│                                             │
│   The API could not be reached.             │
│   Please check your connection.             │
│                                             │
│   [r] Retry   [s] Settings   [q] Quit       │
└─────────────────────────────────────────────┘
```

---

## 5. Theme Support

### 5.1 Color Schemes

**Dark Theme** (Default):
- Background: Dark gray (#1e1e1e)
- Text: Light gray (#d4d4d4)
- Syntax highlighting: VS Code Dark+ style
- Error text: Red (#f44747)
- Correct text: Green (#4ec9b0)
- UI borders: Gray (#404040)

**Light Theme**:
- Background: White (#ffffff)
- Text: Dark gray (#000000)
- Syntax highlighting: GitHub light style
- Error text: Red (#d73a49)
- Correct text: Green (#22863a)
- UI borders: Light gray (#e1e4e8)

### 5.2 Syntax Highlighting

**Integration**: Use Chroma with Bubble Tea's Lipgloss

**Supported Languages** (Initial):
- Python
- Go
- JavaScript/TypeScript
- Java
- C/C++
- Rust

**Extensibility**: Chroma supports 200+ languages, easy to add more

---

## 6. Error Handling & Edge Cases

### 6.1 Network Errors

**Scenarios**:
- API unreachable on startup
- Network drops during usage
- API returns error responses (4xx, 5xx)

**Handling**:
- Show error screen with clear message
- Allow retry with exponential backoff
- Don't crash the app
- Log errors for debugging

### 6.2 Invalid Data

**Scenarios**:
- API returns malformed JSON
- Missing required fields in response
- Empty code document

**Handling**:
- Validate responses against expected schema
- Log validation errors
- Skip invalid documents
- Fetch next document automatically

### 6.3 Terminal Size Changes

**Scenarios**:
- User resizes terminal during typing
- Terminal too small to display UI

**Handling**:
- Listen for resize events (Bubble Tea handles this)
- Reflow UI to fit new dimensions
- Minimum terminal size: 80x24
- Show warning if terminal too small

### 6.4 Empty Queue

**Scenarios**:
- Prefetch queue empty (slow network)
- User navigates faster than fetch rate
- All retries failed

**Handling**:
- Show loading screen if temporary
- Show error screen if prolonged
- Allow manual retry
- Suggest changing filters (may be too restrictive)

### 6.5 Rapid Input

**Scenarios**:
- User types extremely fast
- Multiple keys pressed simultaneously

**Handling**:
- Process events in order (queue if needed)
- Don't drop keypress events
- Maintain accurate statistics

---

## 7. Performance Requirements

### 7.1 Startup Time
- Target: < 500ms from launch to first screen
- Acceptable: < 1s

### 7.2 Response Time
- Keystroke latency: < 50ms
- Screen transitions: < 100ms
- Network requests: 5s timeout

### 7.3 Memory Usage
- Target: < 50MB RAM
- Acceptable: < 100MB

### 7.4 CPU Usage
- Idle: < 1%
- During typing: < 5%

---

## 8. Accessibility

### 8.1 Terminal Compatibility
- Support major terminal emulators: iTerm2, Terminal.app, Alacritty, Kitty, Windows Terminal
- Graceful degradation for limited terminals

### 8.2 Color Blindness
- Don't rely solely on color for error indication
- Use symbols/styling in addition to color (e.g., underline errors)

### 8.3 Screen Readers
- Not applicable for TUI (screen readers don't work well with complex TUI apps)

---

## 9. Future Enhancements (Out of Scope)

These features are explicitly NOT included in v1.0 but documented for future consideration:

- User authentication and accounts
- Cloud statistics storage
- Historical statistics and trends
- Leaderboards
- Custom algorithm uploads
- Practice mode vs test mode
- Configurable difficulty levels
- Sound effects toggle
- Export statistics to CSV/JSON
- Integration with coding platforms
- Multiplayer/competitive mode
- Algorithm difficulty ratings
- Estimated completion time
- Pause/resume functionality
- Multiple syntax highlighting themes beyond dark/light

---

**Document Status**: Draft v1.0
**Last Updated**: 2025-11-10
**Owner**: Beaver Development Team
