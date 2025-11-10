# Beaver Go CLI - User Flows

## Overview

This document details all user interaction flows in the Beaver CLI application, from startup to completion of typing practice sessions.

---

## Flow 1: Application Startup

### Happy Path

```
1. User launches CLI: `beaver`
   │
   ├─→ App initializes configuration
   │   ├─ Load ~/.config/beaver/config.yaml (if exists)
   │   ├─ Apply defaults for missing values
   │   └─ Validate configuration
   │
   ├─→ Start background prefetch goroutine
   │   └─ Begin fetching first algorithm from API
   │
   ├─→ Show splash/loading screen (max 1 second)
   │   "Loading algorithms..."
   │
   ├─→ Wait for first algorithm (with timeout: 3 seconds)
   │
   └─→ Display main screen with algorithm
       ├─ Show algorithm metadata (title, language, tags)
       ├─ Show code with syntax highlighting
       ├─ Show footer with keyboard shortcuts
       └─ Ready for user input
```

### Alternate Path: Network Error on Startup

```
1. User launches CLI: `beaver`
   │
   ├─→ App initializes configuration
   │
   ├─→ Start background prefetch
   │   └─ API request fails
   │
   ├─→ Show loading screen...
   │
   ├─→ Timeout waiting for first algorithm (3 seconds)
   │
   └─→ Display error screen
       ┌──────────────────────────────────────┐
       │            ⚠ Error                   │
       │                                      │
       │ Could not connect to Beaver API      │
       │ Please check your network connection │
       │                                      │
       │ [r] Retry  [s] Settings  [q] Quit    │
       └──────────────────────────────────────┘
```

**User Options**:
- Press `r`: Retry connection, restart prefetch
- Press `s`: Open settings to change API URL
- Press `q`: Quit application

### Alternate Path: Invalid Configuration

```
1. User launches CLI
   │
   ├─→ Load configuration
   │   └─ Validation fails (e.g., invalid API URL)
   │
   └─→ Display error screen with specific message
       "Invalid configuration: API URL must start with http:// or https://"

       [s] Fix Settings  [d] Use Defaults  [q] Quit
```

---

## Flow 2: First-Time User Experience

### First Launch (No Config File)

```
1. Launch beaver
   │
   ├─→ No config file found at ~/.config/beaver/config.yaml
   │
   ├─→ Create default configuration
   │   api:
   │     base_url: "https://beaver-api.com"
   │   filters:
   │     language: ""  # Any language
   │     tags: []      # All tags
   │   ui:
   │     theme: "dark"
   │     tab_width: 4
   │
   ├─→ Save default config
   │
   └─→ Continue normal startup flow
```

### Optional: Welcome Screen (Future Enhancement)

```
┌─────────────────────────────────────────────────┐
│         Welcome to Beaver!                      │
│                                                 │
│ Type algorithms to improve your coding speed    │
│                                                 │
│ Quick Tips:                                     │
│  • Press Tab to skip to next algorithm          │
│  • Press ? for help anytime                     │
│  • Press s to filter by language/tags           │
│                                                 │
│         [Press any key to start]                │
└─────────────────────────────────────────────────┘
```

---

## Flow 3: Typing Practice Session

### Main Typing Flow

```
1. Main screen displays algorithm
   │
   ├─ Algorithm metadata shown:
   │  ┌────────────────────────────────────┐
   │  │ Bubble Sort                        │
   │  │ [docs.link]                        │
   │  │ Python • sort, beginner            │
   │  └────────────────────────────────────┘
   │
   ├─ Code displayed with syntax highlighting
   │  Cursor at position [0, 0] (first character)
   │
   └─ Footer shows: "Tab: Next  ?: Help  s: Settings  q: Quit"

2. User starts typing
   │
   ├─→ First keypress detected
   │   ├─ Start timer (display in header: "00:00")
   │   ├─ Update footer: "Tab: Skip  q: Quit"
   │   └─ Begin statistics tracking
   │
   └─→ For each subsequent keypress:
       │
       ├─ IF character matches expected:
       │  ├─ Move cursor forward
       │  ├─ Mark character as typed (dim color)
       │  ├─ Record timestamp in events list
       │  └─ Update progress indicator
       │
       ├─ IF character does NOT match:
       │  ├─ Highlight error (red background)
       │  ├─ Keep cursor at same position
       │  ├─ Increment error count
       │  └─ Record error timestamp
       │
       ├─ IF backspace pressed:
       │  ├─ Move cursor back one position
       │  ├─ Clear error highlight (if any)
       │  ├─ Increment correction count
       │  └─ Allow retyping
       │
       └─ Update timer display (every 100ms)

3. User completes algorithm (last character correct)
   │
   └─→ Trigger completion flow (see Flow 4)
```

### Visual States During Typing

**Before Typing Starts**:
```python
def bubble_sort(array: list[int]) -> list[int]:
    ▊                    # Cursor at start
    n: int = len(array)
    ...
```

**During Typing (Correct)**:
```python
def bubble_sor▊(array: list[int]) -> list[int]:
    ^^^^^^^^^^^^           # Dimmed (already typed)
               ▊           # Cursor
                t(array... # Normal (upcoming)
```

**During Typing (Error)**:
```python
def bubble_sox▊(array: list[int]) -> list[int]:
    ^^^^^^^^^^^^           # Dimmed (correct)
              ▓            # Red highlight (error)
               ▊           # Cursor stays here
```

**After Backspace**:
```python
def bubble_so▊(array: list[int]) -> list[int]:
    ^^^^^^^^^^^            # Dimmed (correct)
              ▊            # Cursor moved back
               rt(array... # Normal (can retype)
```

---

## Flow 4: Typing Completion

### Completion Sequence

```
1. User types final character correctly
   │
   ├─→ Detect completion (cursor at end of code)
   │
   ├─→ Stop timer
   │
   ├─→ Calculate statistics:
   │   ├─ Total time elapsed
   │   ├─ Total characters
   │   ├─ Total errors
   │   ├─ Total corrections (backspaces)
   │   ├─ Accuracy percentage
   │   └─ Characters per minute (CPM)
   │
   ├─→ Transition to results screen (smooth fade/slide)
   │
   └─→ Display results screen:

       ┌─────────────────────────────────────┐
       │           Results                   │
       ├─────────────────────────────────────┤
       │                                     │
       │ Algorithm: Bubble Sort              │
       │                                     │
       │ Time:            01:23              │
       │ Characters:      156                │
       │ Errors:          7                  │
       │ Corrections:     3                  │
       │ Accuracy:        95.5%              │
       │ CPM:             678                │
       │                                     │
       ├─────────────────────────────────────┤
       │ Tab: Next Algorithm    q: Quit      │
       └─────────────────────────────────────┘

2. User options:
   ├─ Press Tab: Load next algorithm (Flow 5)
   ├─ Press q: Quit application
   └─ Press ?: Show help screen
```

### Accuracy Feedback (Optional Enhancement)

Show different messages based on accuracy:

- **95%+**: "Excellent accuracy! 🎯"
- **85-94%**: "Good work! Keep practicing."
- **70-84%**: "Nice try! Focus on accuracy."
- **<70%**: "Take your time. Accuracy improves with practice."

---

## Flow 5: Loading Next Algorithm

### User-Initiated Navigation

```
1. User presses Tab (from results screen or during typing)
   │
   ├─→ IF during typing:
   │   └─ Confirm skip? (Optional)
   │       ├─ Yes: Continue to step 2
   │       └─ No: Return to typing
   │
   ├─→ Clear current screen
   │
   ├─→ Show brief transition ("Loading next algorithm...")
   │
   ├─→ Attempt to get next algorithm from prefetch queue
   │   │
   │   ├─ IF queue has algorithm:
   │   │  ├─ Pop algorithm from queue
   │   │  ├─ Reset all state:
   │   │  │  ├─ Clear timer (00:00)
   │   │  │  ├─ Clear statistics
   │   │  │  ├─ Reset cursor to [0,0]
   │   │  │  └─ Clear input buffer
   │   │  └─ Display new algorithm (return to Flow 3)
   │   │
   │   └─ IF queue is empty:
   │      ├─ Show loading screen (max 3 seconds)
   │      ├─ Wait for background fetch
   │      │  │
   │      │  ├─ IF fetch succeeds:
   │      │  │  └─ Display algorithm
   │      │  │
   │      │  └─ IF fetch fails/timeout:
   │      │     └─ Show error screen (Flow 6)
   │      │
   │      └─ Background goroutine continues fetching
```

### Automatic Navigation (After Completion)

Same as above, but triggered automatically when Tab is pressed on results screen.

---

## Flow 6: Error Handling

### Network Error During Usage

```
1. Prefetch queue becomes empty
   │
   ├─→ User presses Tab for next algorithm
   │
   ├─→ No algorithms in queue
   │
   ├─→ Wait for background fetch (3 second timeout)
   │
   ├─→ Timeout expires / all retries failed
   │
   └─→ Display error screen:

       ┌─────────────────────────────────────┐
       │            ⚠ No Algorithms          │
       │                                     │
       │ Could not fetch algorithms from API │
       │                                     │
       │ Possible causes:                    │
       │  • Network connection lost          │
       │  • API server unreachable           │
       │  • Filters too restrictive          │
       │                                     │
       │ [r] Retry                           │
       │ [s] Change Settings                 │
       │ [q] Quit                            │
       └─────────────────────────────────────┘

2. User actions:
   ├─ Press r: Retry fetch immediately
   ├─ Press s: Open settings (Flow 7)
   └─ Press q: Quit application
```

### Restrictive Filters Error

```
Scenario: User selects language="Python" and tags=["graph", "advanced"]
         but no algorithms match these criteria.

1. Background fetch returns empty/404
   │
   └─→ Display error screen:

       ┌─────────────────────────────────────┐
       │     ⚠ No Matching Algorithms        │
       │                                     │
       │ No algorithms found with:           │
       │  • Language: Python                 │
       │  • Tags: graph, advanced            │
       │                                     │
       │ Try broadening your filters.        │
       │                                     │
       │ [s] Change Filters                  │
       │ [c] Clear Filters                   │
       │ [q] Quit                            │
       └─────────────────────────────────────┘
```

---

## Flow 7: Settings Management

### Opening Settings

```
1. User presses 's' (from any screen)
   │
   └─→ Display settings modal (overlay on current screen):

       ┌──────────────── Settings ───────────────────┐
       │                                             │
       │  Language:  [▼ Any         ]                │
       │             ┌──────────────┐                │
       │             │ Any          │                │
       │             │ Python       │                │
       │             │ Go           │                │
       │             │ JavaScript   │                │
       │             └──────────────┘                │
       │                                             │
       │  Tags:      [ ] sort                        │
       │             [✓] graph                       │
       │             [ ] search                      │
       │             [ ] dynamic-programming         │
       │             [ ] data-structures             │
       │                                             │
       │  Theme:     ( ) Light                       │
       │             (•) Dark                        │
       │                                             │
       │  Tab Width: [4] spaces                      │
       │                                             │
       ├─────────────────────────────────────────────┤
       │ Esc: Save & Close    Ctrl+C: Cancel         │
       └─────────────────────────────────────────────┘
```

### Changing Settings

```
2. User navigates with arrow keys / Tab
   │
   ├─ Arrow Up/Down: Move between fields
   ├─ Space: Toggle checkbox / radio button
   ├─ Enter: Open dropdown / confirm selection
   └─ Type: Edit text fields (tab width)

3. User saves settings (press Esc)
   │
   ├─→ Validate settings
   │   ├─ IF valid:
   │   │  ├─ Save to ~/.config/beaver/config.yaml
   │   │  ├─ Apply to application state
   │   │  ├─ Update background prefetch filters
   │   │  ├─ Clear prefetch queue
   │   │  └─ Start fetching with new filters
   │   │
   │   └─ IF invalid:
   │      └─ Show error message in settings modal
   │         "Tab width must be between 1 and 8"
   │
   └─→ Close modal, return to previous screen

4. User cancels (press Ctrl+C)
   │
   └─→ Discard changes, close modal
```

### Settings Application Timing

```
┌─────────────────────────────────────────────────┐
│ User Changes Filters in Settings                │
└─────────────────────────────────────────────────┘
            │
            ├─→ Settings saved
            │
            ├─→ Application state updated
            │
            ├─→ Signal background goroutine:
            │   ├─ Stop current fetch (if in progress)
            │   ├─ Clear prefetch queue (discard old algorithms)
            │   └─ Restart fetching with new filters
            │
            └─→ IF currently on results screen:
                └─ Next algorithm will use new filters
```

---

## Flow 8: Help System

### Accessing Help

```
1. User presses '?' from any screen
   │
   └─→ Display help modal (full screen overlay):

       ┌──────────────── Beaver Help ────────────────┐
       │                                             │
       │ Beaver - Typing Practice for Developers     │
       │                                             │
       │ KEYBOARD SHORTCUTS                          │
       │                                             │
       │ Global:                                     │
       │   ?         Show this help                  │
       │   s         Open settings                   │
       │   q         Quit application                │
       │   Ctrl+C    Force quit                      │
       │                                             │
       │ During Typing:                              │
       │   Tab       Skip to next algorithm          │
       │   Backspace Delete previous character       │
       │                                             │
       │ Results Screen:                             │
       │   Tab       Load next algorithm             │
       │                                             │
       │ ABOUT                                       │
       │                                             │
       │ Version: 1.0.0                              │
       │ API: beaver-api.com                         │
       │                                             │
       │ Documentation: github.com/beaver/cli        │
       │ Report issues: github.com/beaver/issues     │
       │                                             │
       ├─────────────────────────────────────────────┤
       │ Esc or ?: Close                             │
       └─────────────────────────────────────────────┘

2. User closes help (press Esc or ?)
   │
   └─→ Return to previous screen (maintain state)
```

---

## Flow 9: Theme Switching

### Toggle Theme

```
1. User presses 't' to toggle theme
   │
   ├─→ Get current theme from state
   │   ├─ IF "dark": Switch to "light"
   │   └─ IF "light": Switch to "dark"
   │
   ├─→ Update application state
   │
   ├─→ Update syntax highlighting colors (Chroma lexer style)
   │
   ├─→ Update UI component colors (Lipgloss styles)
   │
   ├─→ Re-render current screen with new theme
   │
   └─→ Save preference to config file

(No modal, instant transition)
```

---

## Flow 10: Graceful Shutdown

### Normal Quit

```
1. User presses 'q' from any screen
   │
   ├─→ IF currently typing:
   │   └─ Show confirmation (Optional):
   │      "Are you sure? Progress will be lost. (y/n)"
   │      ├─ y: Continue quit
   │      └─ n: Cancel, return to typing
   │
   ├─→ Stop background prefetch goroutine
   │   └─ Send cancellation signal via context
   │
   ├─→ Close HTTP client connections
   │
   ├─→ Save any pending config changes (if any)
   │
   ├─→ Clear screen
   │
   └─→ Exit with code 0

Output:
"Thanks for practicing! Come back soon. 👋"
```

### Force Quit

```
1. User presses Ctrl+C
   │
   ├─→ Bubble Tea captures interrupt signal
   │
   ├─→ Trigger shutdown sequence (same as normal quit)
   │   └─ Graceful cleanup with 2 second timeout
   │
   └─→ Exit with code 130 (standard for SIGINT)
```

### Crash Recovery

```
1. Panic occurs in application
   │
   ├─→ Defer recover() catches panic
   │
   ├─→ Log error to ~/.config/beaver/crash.log
   │
   ├─→ Attempt to restore terminal state
   │
   ├─→ Display error message:
   │   "Oops! Beaver crashed. Error logged to crash.log"
   │
   └─→ Exit with code 1
```

---

## Flow 11: Terminal Resize Handling

### Resize Event

```
1. User resizes terminal window
   │
   ├─→ Bubble Tea detects window size change
   │
   ├─→ Send WindowSizeMsg to Update()
   │
   ├─→ Recalculate layout:
   │   ├─ Update viewport dimensions
   │   ├─ Reflow code display
   │   ├─ Adjust header/footer widths
   │   └─ Adjust modal sizes (if open)
   │
   ├─→ Re-render screen with new dimensions
   │
   └─→ IF terminal too small (< 80x24):
       └─ Show warning overlay:
          "Terminal too small. Minimum 80x24."
```

---

## Summary of All Screens

| Screen | Trigger | Exit | State Preserved |
|--------|---------|------|-----------------|
| **Main (Typing)** | Startup, Tab from results | Completion, Tab (skip) | No |
| **Results** | Complete algorithm | Tab (next), q (quit) | No |
| **Settings** | Press 's' | Esc (save), Ctrl+C (cancel) | Yes (returns to previous) |
| **Help** | Press '?' | Esc or '?' | Yes (returns to previous) |
| **Error** | Network failure, empty queue | r (retry), s (settings), q (quit) | Context-dependent |
| **Loading** | Waiting for algorithm | Automatic (success) or Error (timeout) | N/A (transient) |

---

## Key User Experience Principles

1. **Immediate Feedback**: Every keypress should have instant visual feedback
2. **Clear Navigation**: Always show available actions in footer
3. **No Dead Ends**: Every error screen has actionable options
4. **State Preservation**: Modals (settings, help) don't disrupt main flow
5. **Graceful Degradation**: Network issues don't crash app
6. **Predictable Behavior**: Same action always does same thing
7. **Escape Hatches**: Multiple ways to exit/cancel (Esc, Ctrl+C, q)

---

**Document Status**: Draft v1.0
**Last Updated**: 2025-11-10
**Owner**: Beaver Development Team
