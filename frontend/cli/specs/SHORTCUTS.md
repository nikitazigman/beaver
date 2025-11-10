# Beaver Go CLI - Keyboard Shortcuts Specification

## Overview

This document defines all keyboard shortcuts for the Beaver CLI. The shortcuts are designed to be:

- **Intuitive**: Common keys for common actions
- **Memorable**: Mnemonics where possible (s = settings, ? = help)
- **Terminal-friendly**: Avoid conflicts with terminal emulator shortcuts
- **Context-aware**: Different behaviors based on current screen

---

## Design Principles

### 1. Conflict Avoidance
Avoid shortcuts that conflict with:
- Terminal emulators (Ctrl+T for new tab, Ctrl+W for close, etc.)
- Shell commands (Ctrl+Z, Ctrl+D, etc.)
- Text editors (for familiarity)

### 2. Discoverability
- Always show available shortcuts in footer
- Use standard conventions (? for help, q for quit)
- Single-key shortcuts for frequent actions

### 3. Consistency
- Same key does similar things across contexts
- Escape always closes modal/cancels
- Ctrl+C always quits (emergency exit)

### 4. Efficiency
- Most common actions have single-key shortcuts
- No complex chords for basic functionality
- Typing flow is never interrupted by accidental shortcuts

---

## Global Shortcuts

These shortcuts work from **any screen** in the application.

| Key | Action | Description | Notes |
|-----|--------|-------------|-------|
| `?` | Show Help | Opens help modal with all shortcuts and info | Modal overlay |
| `s` | Open Settings | Opens settings screen to configure filters/preferences | Modal overlay |
| `q` | Quit | Exit application (may prompt if typing in progress) | Confirmation optional |
| `Ctrl+C` | Force Quit | Immediate exit, no confirmation | Standard interrupt |

---

## Main Screen (Typing Mode) Shortcuts

Active when the user is **viewing or typing an algorithm**.

### Before Typing Starts

| Key | Action | Description |
|-----|--------|-------------|
| `Tab` | Next Algorithm | Skip current algorithm, load next from queue |
| Any printable key | Start Typing | Begin typing practice, start timer |

### During Active Typing

| Key | Action | Description | Implementation Notes |
|-----|--------|-------------|----------------------|
| Printable chars | Type character | Input character for validation | a-z, A-Z, 0-9, symbols, space |
| `Backspace` | Delete character | Remove previous character, allow correction | Move cursor back |
| `Tab` | Insert spaces | Convert to 4 spaces (configurable) | Matches code indentation |
| `Enter` | New line | Move to next line in code | Validate newline character |
| `Tab` (hold for 2s) | Skip Algorithm | Load next algorithm (with confirmation) | Optional: prevent accidents |
| `Esc` | Pause/Stop | Pause timer, show menu (optional feature) | Future enhancement |

**Ignored Keys** (no action):
- Arrow keys
- Home/End/PgUp/PgDn
- Function keys (F1-F12) except those bound globally
- Ctrl/Alt/Cmd combinations (except Ctrl+C)
- Delete (forward delete)
- Insert

### After Completion

After user types the last character, immediately transition to Results screen (see below).

---

## Results Screen Shortcuts

Active when **viewing statistics** after completing an algorithm.

| Key | Action | Description |
|-----|--------|-------------|
| `Tab` | Next Algorithm | Load next algorithm, reset state, start new session |
| `r` | Retry | Restart same algorithm (optional feature) |
| `Space` | Next Algorithm | Alternative to Tab (common expectation) |
| `Enter` | Next Algorithm | Another alternative |

**Design Note**: Multiple keys for "next" to match user expectations. Most users will naturally press Tab, Space, or Enter.

---

## Settings Screen Shortcuts

Active when the **settings modal is open**.

### Navigation

| Key | Action | Description |
|-----|--------|-------------|
| `Tab` | Next field | Move focus to next setting |
| `Shift+Tab` | Previous field | Move focus to previous setting |
| `Arrow Up` | Previous field | Alternative navigation |
| `Arrow Down` | Next field | Alternative navigation |
| `Esc` | Save & Close | Apply settings and close modal |
| `Ctrl+C` | Cancel | Discard changes and close modal |

### Interaction

| Key | Action | Context | Description |
|-----|--------|---------|-------------|
| `Space` | Toggle | Checkboxes, radio buttons | Select/deselect option |
| `Enter` | Activate | Dropdowns | Open dropdown menu |
| `Arrow Up/Down` | Navigate | Open dropdown | Select option in list |
| `Enter` | Confirm | Open dropdown | Close dropdown with selection |
| `Type` | Edit | Text fields | Edit numeric/text values |

### Settings Fields

**Language Dropdown**:
```
Language: [▼ Any         ]
          ┌──────────────┐
          │ Any          │ ← Arrow keys to navigate
          │ Python       │
          │ Go           │
          └──────────────┘
```
- Arrow Up/Down: Navigate options
- Enter: Confirm selection
- Esc: Cancel dropdown

**Tags Checkboxes**:
```
Tags: [ ] sort            ← Space to toggle
      [✓] graph           ← Space to toggle
      [ ] search
```
- Space: Toggle checkbox
- Tab/Arrow: Move to next tag

**Theme Radio Buttons**:
```
Theme: ( ) Light          ← Space to select
       (•) Dark
```
- Space: Select option
- Only one can be selected

**Tab Width Input**:
```
Tab Width: [4_] spaces    ← Type numbers
```
- Type: Enter number (1-8)
- Backspace: Delete digit

---

## Help Screen Shortcuts

Active when the **help modal is open**.

| Key | Action | Description |
|-----|--------|-------------|
| `?` | Close Help | Toggle help (same key opens/closes) |
| `Esc` | Close Help | Standard close modal key |
| `Arrow Up` | Scroll up | If help content exceeds screen height |
| `Arrow Down` | Scroll down | If help content exceeds screen height |
| `PgUp` | Page up | Scroll one page up |
| `PgDn` | Page down | Scroll one page down |
| `Space` | Page down | Alternative to PgDn |

---

## Error Screen Shortcuts

Active when an **error screen is displayed**.

The shortcuts vary based on error type:

### Network Error

| Key | Action | Description |
|-----|--------|-------------|
| `r` | Retry | Attempt to reconnect/fetch again |
| `s` | Open Settings | Change API URL or filters |
| `q` | Quit | Exit application |

### No Algorithms Available (Restrictive Filters)

| Key | Action | Description |
|-----|--------|-------------|
| `s` | Open Settings | Modify filters to broaden search |
| `c` | Clear Filters | Reset to "Any" language and all tags |
| `r` | Retry | Try fetching again with current filters |
| `q` | Quit | Exit application |

---

## Loading Screen Shortcuts

Active during **loading/fetching** algorithms.

| Key | Action | Description |
|-----|--------|-------------|
| `Esc` | Cancel | Stop waiting, show error screen or previous screen |
| `Ctrl+C` | Force Quit | Exit application immediately |

---

## Special Key Behaviors

### Tab Key

The `Tab` key has context-specific behavior:

| Context | Behavior |
|---------|----------|
| Typing code | Insert 4 spaces (tab character) |
| Results screen | Load next algorithm |
| Settings screen | Navigate to next field |
| Help screen | (No action) |

**Implementation**: Check current screen/mode to determine action.

### Escape Key

The `Esc` key always means "go back" or "cancel":

| Context | Behavior |
|---------|----------|
| Settings modal | Save and close |
| Help modal | Close |
| Error screen | (No standard action, depends on options) |
| Typing | (Optional) Pause or return to main menu |
| Loading | Cancel wait, go back |

### Enter Key

| Context | Behavior |
|---------|----------|
| Typing code | Insert newline character |
| Results screen | Load next algorithm |
| Settings dropdown | Confirm selection |
| Settings field | Move to next field or save |

---

## Shortcut Quick Reference

### Visual Footer Examples

**Main Screen (Before Typing)**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tab: Next  ?: Help  s: Settings  q: Quit
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Main Screen (During Typing)**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tab: Skip  Backspace: Correct  q: Quit
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Results Screen**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tab: Next Algorithm  r: Retry  q: Quit
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Settings Screen**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tab: Navigate  Space: Toggle  Esc: Save  Ctrl+C: Cancel
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Help Screen**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Arrow Keys: Scroll  Esc or ?: Close
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Error Screen**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
r: Retry  s: Settings  q: Quit
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Shortcut Cheat Sheet

Print-friendly quick reference for users:

```
┌────────────────────────────────────────────────┐
│         BEAVER KEYBOARD SHORTCUTS              │
├────────────────────────────────────────────────┤
│ GLOBAL                                         │
│  ?         Help                                │
│  s         Settings                            │
│  q         Quit                                │
│  Ctrl+C    Force quit                          │
├────────────────────────────────────────────────┤
│ TYPING                                         │
│  Tab       Next algorithm / Insert spaces      │
│  Backspace Delete & correct                    │
│  Enter     New line                            │
├────────────────────────────────────────────────┤
│ RESULTS                                        │
│  Tab       Next algorithm                      │
│  Space     Next algorithm                      │
│  Enter     Next algorithm                      │
│  r         Retry same algorithm                │
├────────────────────────────────────────────────┤
│ SETTINGS                                       │
│  Tab       Next field                          │
│  Space     Toggle checkbox/radio               │
│  Arrows    Navigate                            │
│  Esc       Save & close                        │
├────────────────────────────────────────────────┤
│ HELP                                           │
│  Esc or ?  Close                               │
│  Arrows    Scroll                              │
└────────────────────────────────────────────────┘
```

---

## Implementation Notes

### Bubble Tea Key Handling

In Bubble Tea, keyboard input is handled in the `Update()` function via `tea.KeyMsg`:

```go
func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.String() {
        case "ctrl+c", "q":
            return m, tea.Quit
        case "?":
            return m.showHelp(), nil
        case "s":
            return m.showSettings(), nil
        case "tab":
            return m.handleTab(), nil
        // ... more cases
        }
    }
    return m, nil
}
```

### Context-Aware Handling

Use model state to determine behavior:

```go
func (m Model) handleTab() (Model, tea.Cmd) {
    switch m.currentScreen {
    case ScreenTyping:
        if m.isTyping {
            // Insert 4 spaces
            return m.insertSpaces(), nil
        } else {
            // Skip to next algorithm
            return m.loadNext(), nil
        }
    case ScreenResults:
        // Load next algorithm
        return m.loadNext(), nil
    case ScreenSettings:
        // Navigate to next field
        return m.focusNextField(), nil
    }
    return m, nil
}
```

### Modifier Keys

Bubble Tea provides helpers for checking modifiers:

```go
case tea.KeyMsg:
    switch {
    case key.Matches(msg, m.keyMap.Quit): // Handles q, Q, Ctrl+Q, etc.
        return m, tea.Quit
    }
```

### Configurable Key Bindings (Future)

Allow users to customize shortcuts via config file:

```yaml
keybindings:
  quit: "q"
  help: "?"
  settings: "s"
  next_algorithm: "tab"
  skip_algorithm: "ctrl+n"
```

---

## Accessibility Considerations

### Terminal Compatibility

Some terminals may intercept certain key combinations:

| Key Combo | Potential Issue | Workaround |
|-----------|----------------|------------|
| `Ctrl+S` | Terminal freeze (XOFF) | Use `s` instead |
| `Ctrl+Q` | Resume from freeze (XON) | Use `q` instead |
| `Ctrl+Z` | Suspend process | Don't use |
| `Ctrl+D` | EOF / close terminal | Don't use |

### Alternative Shortcuts

Always provide multiple ways to perform common actions:
- Next algorithm: Tab, Space, Enter
- Close modal: Esc, q, ?
- Quit: q, Ctrl+C

### Help Discoverability

- Show `?: Help` in footer on every screen
- Help screen lists all available shortcuts
- Context-specific shortcuts shown in footer

---

## Testing Checklist

- [ ] All global shortcuts work from every screen
- [ ] Tab key behaves correctly in each context
- [ ] Escape key closes modals and cancels operations
- [ ] Ctrl+C always force quits
- [ ] Backspace works during typing (allows corrections)
- [ ] Settings navigation (Tab, arrows) works smoothly
- [ ] Help screen scrolls correctly with arrow keys
- [ ] No conflict with terminal emulator shortcuts
- [ ] Footer always shows available shortcuts for current context
- [ ] Shortcuts are case-insensitive where appropriate (q vs Q)

---

**Document Status**: Draft v1.0
**Last Updated**: 2025-11-10
**Owner**: Beaver Development Team
