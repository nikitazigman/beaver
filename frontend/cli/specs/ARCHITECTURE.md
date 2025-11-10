# Beaver Go CLI - Architecture Design

## Overview

This document details the technical architecture of the Beaver Go CLI, including the application structure, state management, concurrency model, and component design.

---

## Architectural Pattern: The Elm Architecture (TEA)

Bubble Tea implements The Elm Architecture, which consists of three core concepts:

### 1. Model (State)
The single source of truth for application state.

### 2. Update (State Transitions)
Pure functions that handle messages and return new state.

### 3. View (Rendering)
Pure functions that render UI from state.

### Data Flow

```
┌─────────────────────────────────────────────┐
│                                             │
│  ┌──────────┐      ┌──────────┐            │
│  │  Model   │─────▶│   View   │───────┐    │
│  │ (State)  │      │(Render)  │       │    │
│  └──────────┘      └──────────┘       │    │
│       ▲                                │    │
│       │                                ▼    │
│       │            ┌───────────────────┐    │
│  ┌────┴─────┐      │   User Events     │    │
│  │  Update  │◀─────│   (Keyboard)      │    │
│  │(Messages)│      └───────────────────┘    │
│  └──────────┘                               │
│                                             │
└─────────────────────────────────────────────┘
```

**Key Principles**:
- Immutable state (return new model, don't mutate)
- No side effects in View
- All state transitions through Update
- Single model struct holds all application state

---

## Project Structure

```
beaver-cli/
├── cmd/
│   └── beaver/
│       └── main.go              # Entry point
├── internal/
│   ├── app/
│   │   ├── model.go            # Main Bubble Tea model
│   │   ├── update.go           # Update function (message handling)
│   │   ├── view.go             # View function (rendering)
│   │   └── keys.go             # Keybinding definitions
│   ├── components/
│   │   ├── code_display.go     # Code viewport component
│   │   ├── results.go          # Statistics display component
│   │   ├── settings.go         # Settings modal component
│   │   ├── help.go             # Help screen component
│   │   └── error.go            # Error screen component
│   ├── services/
│   │   ├── api.go              # HTTP API client
│   │   └── prefetch.go         # Background prefetch service
│   ├── models/
│   │   ├── code_document.go    # CodeDocument struct
│   │   ├── statistics.go       # Statistics struct
│   │   └── config.go           # Configuration struct
│   ├── syntax/
│   │   └── highlighter.go      # Chroma integration
│   ├── config/
│   │   ├── config.go           # Viper configuration
│   │   └── defaults.go         # Default values
│   └── utils/
│       ├── logger.go           # Logging setup
│       └── helpers.go          # Utility functions
├── pkg/                        # Public packages (if any)
├── go.mod
├── go.sum
├── Makefile
└── README.md
```

### Directory Responsibilities

**`cmd/`**: Application entry points (main.go)
**`internal/app/`**: Bubble Tea application (model, update, view)
**`internal/components/`**: Reusable UI components
**`internal/services/`**: External integrations (API, background jobs)
**`internal/models/`**: Data structures and business logic
**`internal/syntax/`**: Syntax highlighting logic
**`internal/config/`**: Configuration management
**`internal/utils/`**: Shared utilities

---

## Core Model Structure

### Main Application Model

```go
package app

import (
    tea "github.com/charmbracelet/bubbletea"
    "github.com/charmbracelet/bubbles/viewport"
    "github.com/yourorg/beaver-cli/internal/models"
    "github.com/yourorg/beaver-cli/internal/components"
)

// Screen represents the current active screen
type Screen int

const (
    ScreenLoading Screen = iota
    ScreenTyping
    ScreenResults
    ScreenSettings
    ScreenHelp
    ScreenError
)

// Model is the main application state
type Model struct {
    // Screen management
    currentScreen Screen
    prevScreen    Screen  // For modal return

    // Current algorithm
    algorithm     *models.CodeDocument
    highlightedCode string  // Pre-highlighted code

    // Typing state
    userInput     []rune
    cursorPos     int      // Current position in code
    isTyping      bool     // Whether user has started typing
    startTime     time.Time

    // Statistics tracking
    typingEvents  []time.Time  // Timestamps of correct keypresses
    errorEvents   []time.Time  // Timestamps of errors
    corrections   int          // Number of backspaces

    // Services
    apiClient     *services.APIClient
    prefetchChan  chan *models.CodeDocument
    prefetchStop  chan struct{}

    // Components
    codeViewport  viewport.Model
    resultsView   components.Results
    settingsView  components.Settings
    helpView      components.Help
    errorView     components.Error

    // Configuration
    config        *models.Config

    // UI state
    windowWidth   int
    windowHeight  int
    ready         bool
    err           error

    // Key bindings
    keys          KeyMap
}
```

### Supporting Models

#### CodeDocument

```go
package models

import (
    "time"
    "github.com/google/uuid"
)

type CodeDocument struct {
    ID            uuid.UUID
    Title         string
    Code          string
    Language      string
    Tags          []string
    LinkToProject string
    CreatedAt     time.Time
    UpdatedAt     time.Time
}
```

#### Statistics

```go
package models

import "time"

type Statistics struct {
    TimeElapsed   time.Duration
    TotalChars    int
    TotalErrors   int
    Corrections   int
    Accuracy      float64  // Percentage
    CPM           int      // Characters per minute
}

// Calculate computes statistics from events
func (s *Statistics) Calculate(
    code string,
    typingEvents []time.Time,
    errorEvents []time.Time,
    corrections int,
    startTime time.Time,
    endTime time.Time,
) {
    s.TimeElapsed = endTime.Sub(startTime)
    s.TotalChars = len(code)
    s.TotalErrors = len(errorEvents)
    s.Corrections = corrections

    // Accuracy = (correct chars / total chars) * 100
    s.Accuracy = float64(s.TotalChars-s.TotalErrors) / float64(s.TotalChars) * 100

    // CPM = total chars / (seconds / 60)
    seconds := s.TimeElapsed.Seconds()
    s.CPM = int(float64(s.TotalChars) / (seconds / 60))
}
```

#### Configuration

```go
package models

import "time"

type Config struct {
    API      APIConfig
    Filters  FilterConfig
    UI       UIConfig
    Prefetch PrefetchConfig
}

type APIConfig struct {
    BaseURL string
    Timeout time.Duration
}

type FilterConfig struct {
    Language string
    Tags     []string
}

type UIConfig struct {
    Theme    string  // "dark" or "light"
    TabWidth int
}

type PrefetchConfig struct {
    QueueSize int
}
```

---

## Message Types

Bubble Tea applications communicate via messages. Here are the custom messages for Beaver:

```go
package app

import (
    "github.com/yourorg/beaver-cli/internal/models"
)

// Algorithm fetching messages
type algorithmFetchedMsg struct {
    algorithm *models.CodeDocument
}

type algorithmErrorMsg struct {
    err error
}

// Typing event messages
type startTypingMsg struct{}

type correctCharMsg struct {
    char rune
    timestamp time.Time
}

type errorCharMsg struct {
    char rune
    timestamp time.Time
}

type correctionMsg struct {
    timestamp time.Time
}

type completionMsg struct {
    endTime time.Time
}

// Timer messages
type timerTickMsg time.Time

// Settings messages
type settingsSavedMsg struct {
    config *models.Config
}

// Navigation messages
type loadNextMsg struct{}

type showHelpMsg struct{}

type showSettingsMsg struct{}

type closeModalMsg struct{}
```

---

## Update Function Flow

The Update function is the heart of the application. It receives messages and returns updated state.

```go
package app

import tea "github.com/charmbracelet/bubbletea"

func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {

    // Window resize
    case tea.WindowSizeMsg:
        m.windowWidth = msg.Width
        m.windowHeight = msg.Height
        m.codeViewport.Width = msg.Width - 4
        m.codeViewport.Height = msg.Height - 10
        return m, nil

    // Keyboard input
    case tea.KeyMsg:
        return m.handleKeyPress(msg)

    // Algorithm fetched
    case algorithmFetchedMsg:
        m.algorithm = msg.algorithm
        m.highlightedCode = highlightCode(msg.algorithm)
        m.currentScreen = ScreenTyping
        return m, nil

    // Typing events
    case correctCharMsg:
        m.typingEvents = append(m.typingEvents, msg.timestamp)
        m.cursorPos++

        // Check for completion
        if m.cursorPos >= len(m.algorithm.Code) {
            return m, func() tea.Msg {
                return completionMsg{endTime: time.Now()}
            }
        }
        return m, nil

    case errorCharMsg:
        m.errorEvents = append(m.errorEvents, msg.timestamp)
        // Don't move cursor on error
        return m, nil

    case correctionMsg:
        m.corrections++
        if m.cursorPos > 0 {
            m.cursorPos--
        }
        return m, nil

    // Completion
    case completionMsg:
        m.isTyping = false
        stats := m.calculateStatistics(msg.endTime)
        m.resultsView = components.NewResults(stats, m.algorithm)
        m.currentScreen = ScreenResults
        return m, nil

    // Timer tick
    case timerTickMsg:
        if m.isTyping {
            return m, m.tickTimer()
        }
        return m, nil

    // Navigation
    case loadNextMsg:
        return m.loadNextAlgorithm()

    case showHelpMsg:
        m.prevScreen = m.currentScreen
        m.currentScreen = ScreenHelp
        return m, nil

    case showSettingsMsg:
        m.prevScreen = m.currentScreen
        m.currentScreen = ScreenSettings
        return m, nil

    case closeModalMsg:
        m.currentScreen = m.prevScreen
        return m, nil
    }

    return m, nil
}
```

### Key Press Handling

```go
func (m Model) handleKeyPress(msg tea.KeyMsg) (tea.Model, tea.Cmd) {
    // Global shortcuts
    switch msg.String() {
    case "ctrl+c", "q":
        if m.currentScreen == ScreenTyping && m.isTyping {
            // Optional: confirm quit
            return m, tea.Quit
        }
        return m, tea.Quit

    case "?":
        return m, func() tea.Msg { return showHelpMsg{} }

    case "s":
        return m, func() tea.Msg { return showSettingsMsg{} }
    }

    // Screen-specific shortcuts
    switch m.currentScreen {
    case ScreenTyping:
        return m.handleTypingKeys(msg)
    case ScreenResults:
        return m.handleResultsKeys(msg)
    case ScreenSettings:
        return m.handleSettingsKeys(msg)
    case ScreenHelp:
        return m.handleHelpKeys(msg)
    case ScreenError:
        return m.handleErrorKeys(msg)
    }

    return m, nil
}

func (m Model) handleTypingKeys(msg tea.KeyMsg) (tea.Model, tea.Cmd) {
    switch msg.String() {
    case "tab":
        if !m.isTyping {
            // Skip to next algorithm
            return m, func() tea.Msg { return loadNextMsg{} }
        } else {
            // Insert 4 spaces
            return m.handleCharInput('\t')
        }

    case "backspace":
        if m.isTyping {
            return m, func() tea.Msg {
                return correctionMsg{timestamp: time.Now()}
            }
        }
        return m, nil

    case "enter":
        return m.handleCharInput('\n')

    default:
        // Handle printable characters
        if len(msg.String()) == 1 {
            return m.handleCharInput(rune(msg.String()[0]))
        }
    }

    return m, nil
}

func (m Model) handleCharInput(char rune) (Model, tea.Cmd) {
    // Start typing on first character
    if !m.isTyping {
        m.isTyping = true
        m.startTime = time.Now()
        // Start timer
        return m, m.tickTimer()
    }

    // Get expected character
    expected := rune(m.algorithm.Code[m.cursorPos])

    // Handle tab as 4 spaces
    if char == '\t' {
        char = ' '
        // TODO: Handle multi-space insertion
    }

    // Validate character
    if char == expected {
        return m, func() tea.Msg {
            return correctCharMsg{
                char: char,
                timestamp: time.Now(),
            }
        }
    } else {
        return m, func() tea.Msg {
            return errorCharMsg{
                char: char,
                timestamp: time.Now(),
            }
        }
    }
}
```

---

## View Function

The View function renders the UI based on current state.

```go
package app

import (
    "github.com/charmbracelet/lipgloss"
)

func (m Model) View() string {
    if !m.ready {
        return "Initializing..."
    }

    switch m.currentScreen {
    case ScreenLoading:
        return m.renderLoading()
    case ScreenTyping:
        return m.renderTyping()
    case ScreenResults:
        return m.renderResults()
    case ScreenSettings:
        return m.renderSettings()
    case ScreenHelp:
        return m.renderHelp()
    case ScreenError:
        return m.renderError()
    }

    return ""
}

func (m Model) renderTyping() string {
    // Header
    header := m.renderHeader()

    // Algorithm metadata
    metadata := m.renderMetadata()

    // Code viewport
    code := m.renderCode()

    // Footer
    footer := m.renderFooter()

    // Combine vertically
    return lipgloss.JoinVertical(
        lipgloss.Left,
        header,
        metadata,
        code,
        footer,
    )
}

func (m Model) renderCode() string {
    // Split code into lines
    lines := strings.Split(m.algorithm.Code, "\n")

    var renderedLines []string
    for i, line := range lines {
        renderedLine := m.renderLine(i, line)
        renderedLines = append(renderedLines, renderedLine)
    }

    // Put in viewport
    m.codeViewport.SetContent(strings.Join(renderedLines, "\n"))
    return m.codeViewport.View()
}

func (m Model) renderLine(lineNum int, line string) string {
    // Calculate line start/end positions in overall code
    lineStart := /* calculate */
    lineEnd := lineStart + len(line)

    var styledLine string
    for i, char := range line {
        charPos := lineStart + i

        if charPos < m.cursorPos {
            // Already typed - dim color
            styledLine += dimStyle.Render(string(char))
        } else if charPos == m.cursorPos {
            // Current cursor position
            if m.hasError(charPos) {
                styledLine += errorStyle.Render(string(char))
            } else {
                styledLine += cursorStyle.Render(string(char))
            }
        } else {
            // Upcoming - normal highlight
            styledLine += string(char)  // Already highlighted by Chroma
        }
    }

    return styledLine
}
```

---

## Concurrency Model

### Background Prefetch Goroutine

```go
package services

import (
    "context"
    "time"
    tea "github.com/charmbracelet/bubbletea"
)

// StartPrefetch starts the background goroutine
func StartPrefetch(
    ctx context.Context,
    client *APIClient,
    filters FilterConfig,
    queueSize int,
) (chan *CodeDocument, error) {

    queue := make(chan *CodeDocument, queueSize)

    go func() {
        backoff := 1 * time.Second
        maxBackoff := 30 * time.Second

        for {
            select {
            case <-ctx.Done():
                close(queue)
                return

            default:
                // Fetch algorithm
                doc, err := client.FetchRandom(filters)

                if err != nil {
                    // Log error
                    log.Error().Err(err).Msg("Failed to fetch algorithm")

                    // Exponential backoff
                    time.Sleep(backoff)
                    backoff *= 2
                    if backoff > maxBackoff {
                        backoff = maxBackoff
                    }
                    continue
                }

                // Reset backoff on success
                backoff = 1 * time.Second

                // Try to send to queue (blocks if full)
                select {
                case queue <- doc:
                    log.Debug().Str("title", doc.Title).Msg("Prefetched algorithm")
                case <-ctx.Done():
                    close(queue)
                    return
                }
            }
        }
    }()

    return queue, nil
}

// PopFromQueue gets next algorithm from queue
func PopFromQueue(queue chan *CodeDocument, timeout time.Duration) tea.Cmd {
    return func() tea.Msg {
        select {
        case doc := <-queue:
            if doc != nil {
                return algorithmFetchedMsg{algorithm: doc}
            }
            return algorithmErrorMsg{err: errors.New("queue closed")}

        case <-time.After(timeout):
            return algorithmErrorMsg{err: errors.New("timeout waiting for algorithm")}
        }
    }
}
```

### Integration with Bubble Tea

```go
// In main.go Init function
func (m Model) Init() tea.Cmd {
    // Start prefetch goroutine
    ctx, cancel := context.WithCancel(context.Background())
    m.prefetchCancel = cancel

    queue, err := services.StartPrefetch(
        ctx,
        m.apiClient,
        m.config.Filters,
        m.config.Prefetch.QueueSize,
    )

    if err != nil {
        return func() tea.Msg {
            return algorithmErrorMsg{err: err}
        }
    }

    m.prefetchChan = queue

    // Pop first algorithm
    return services.PopFromQueue(queue, 3*time.Second)
}
```

---

## Component Architecture

### Component Interface Pattern

```go
package components

import tea "github.com/charmbracelet/bubbletea"

// Component is a reusable UI component
type Component interface {
    Update(msg tea.Msg) (Component, tea.Cmd)
    View() string
}
```

### Example: Results Component

```go
package components

import (
    "github.com/charmbracelet/lipgloss"
    "github.com/yourorg/beaver-cli/internal/models"
)

type Results struct {
    statistics *models.Statistics
    algorithm  *models.CodeDocument
    width      int
    height     int
}

func NewResults(stats *models.Statistics, algo *models.CodeDocument) Results {
    return Results{
        statistics: stats,
        algorithm:  algo,
    }
}

func (r Results) Update(msg tea.Msg) (Results, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.WindowSizeMsg:
        r.width = msg.Width
        r.height = msg.Height
    }
    return r, nil
}

func (r Results) View() string {
    title := titleStyle.Render("Results")

    content := lipgloss.JoinVertical(
        lipgloss.Left,
        "",
        labelStyle.Render("Algorithm: ")+r.algorithm.Title,
        "",
        labelStyle.Render("Time:        ")+valueStyle.Render(formatDuration(r.statistics.TimeElapsed)),
        labelStyle.Render("Characters:  ")+valueStyle.Render(fmt.Sprintf("%d", r.statistics.TotalChars)),
        labelStyle.Render("Errors:      ")+valueStyle.Render(fmt.Sprintf("%d", r.statistics.TotalErrors)),
        labelStyle.Render("Corrections: ")+valueStyle.Render(fmt.Sprintf("%d", r.statistics.Corrections)),
        labelStyle.Render("Accuracy:    ")+valueStyle.Render(fmt.Sprintf("%.1f%%", r.statistics.Accuracy)),
        labelStyle.Render("CPM:         ")+valueStyle.Render(fmt.Sprintf("%d", r.statistics.CPM)),
        "",
    )

    box := boxStyle.Render(
        lipgloss.JoinVertical(lipgloss.Center, title, content),
    )

    return lipgloss.Place(r.width, r.height, lipgloss.Center, lipgloss.Center, box)
}
```

---

## API Client

### HTTP Client Structure

```go
package services

import (
    "context"
    "encoding/json"
    "fmt"
    "net/http"
    "net/url"
    "time"
)

type APIClient struct {
    baseURL    string
    httpClient *http.Client
}

func NewAPIClient(baseURL string, timeout time.Duration) *APIClient {
    return &APIClient{
        baseURL: baseURL,
        httpClient: &http.Client{
            Timeout: timeout,
            Transport: &http.Transport{
                MaxIdleConns:        10,
                MaxIdleConnsPerHost: 5,
                IdleConnTimeout:     30 * time.Second,
            },
        },
    }
}

func (c *APIClient) FetchRandom(filters FilterConfig) (*CodeDocument, error) {
    // Build URL with query params
    u, _ := url.Parse(c.baseURL + "/api/v1/code_documents/code_document/")
    q := u.Query()

    if filters.Language != "" {
        q.Set("language", filters.Language)
    }

    for _, tag := range filters.Tags {
        q.Add("tags", tag)
    }

    u.RawQuery = q.Encode()

    // Make request
    resp, err := c.httpClient.Get(u.String())
    if err != nil {
        return nil, fmt.Errorf("request failed: %w", err)
    }
    defer resp.Body.Close()

    if resp.StatusCode != http.StatusOK {
        return nil, fmt.Errorf("API returned %d", resp.StatusCode)
    }

    // Parse response
    var doc CodeDocument
    if err := json.NewDecoder(resp.Body).Decode(&doc); err != nil {
        return nil, fmt.Errorf("failed to parse response: %w", err)
    }

    return &doc, nil
}

func (c *APIClient) ListLanguages() ([]Language, error) {
    // Similar implementation
}

func (c *APIClient) ListTags() ([]Tag, error) {
    // Similar implementation
}
```

---

## Syntax Highlighting Integration

```go
package syntax

import (
    "bytes"
    "github.com/alecthomas/chroma/v2"
    "github.com/alecthomas/chroma/v2/formatters"
    "github.com/alecthomas/chroma/v2/lexers"
    "github.com/alecthomas/chroma/v2/styles"
)

type Highlighter struct {
    style string  // "monokai" or "github"
}

func NewHighlighter(theme string) *Highlighter {
    style := "monokai"
    if theme == "light" {
        style = "github"
    }
    return &Highlighter{style: style}
}

func (h *Highlighter) Highlight(code string, language string) (string, error) {
    // Get lexer for language
    lexer := lexers.Get(language)
    if lexer == nil {
        lexer = lexers.Fallback
    }

    // Get style
    style := styles.Get(h.style)
    if style == nil {
        style = styles.Fallback
    }

    // Get formatter (terminal with 24-bit color)
    formatter := formatters.Get("terminal16m")
    if formatter == nil {
        formatter = formatters.Fallback
    }

    // Tokenize code
    iterator, err := lexer.Tokenise(nil, code)
    if err != nil {
        return "", err
    }

    // Format to buffer
    var buf bytes.Buffer
    err = formatter.Format(&buf, style, iterator)
    if err != nil {
        return "", err
    }

    return buf.String(), nil
}
```

---

## Error Handling Strategy

### Error Types

```go
package app

type ErrorType int

const (
    ErrorNetwork ErrorType = iota
    ErrorAPIUnavailable
    ErrorNoAlgorithms
    ErrorConfiguration
)

type AppError struct {
    Type    ErrorType
    Message string
    Err     error
}

func (e *AppError) Error() string {
    if e.Err != nil {
        return fmt.Sprintf("%s: %v", e.Message, e.Err)
    }
    return e.Message
}
```

### Error Handling in Update

```go
func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case algorithmErrorMsg:
        m.err = msg.err
        m.currentScreen = ScreenError

        // Determine error type and set appropriate message
        if isNetworkError(msg.err) {
            m.errorView = components.NewError(
                "Network Error",
                "Could not connect to Beaver API",
                []ErrorAction{
                    {Key: "r", Label: "Retry"},
                    {Key: "s", Label: "Settings"},
                    {Key: "q", Label: "Quit"},
                },
            )
        }

        return m, nil
    }
}
```

---

## Testing Strategy

### Unit Tests

Test pure functions (statistics calculation, validation, etc.):

```go
package models_test

import (
    "testing"
    "time"
    "github.com/stretchr/testify/assert"
)

func TestStatisticsCalculation(t *testing.T) {
    tests := []struct {
        name        string
        code        string
        errors      int
        corrections int
        duration    time.Duration
        wantAccuracy float64
        wantCPM     int
    }{
        {
            name:        "perfect typing",
            code:        "hello world",
            errors:      0,
            corrections: 0,
            duration:    10 * time.Second,
            wantAccuracy: 100.0,
            wantCPM:     66,  // 11 chars / (10s / 60) = 66
        },
        // More test cases...
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            stats := &Statistics{}
            stats.Calculate(
                tt.code,
                makeEvents(len(tt.code)),
                makeEvents(tt.errors),
                tt.corrections,
                time.Now(),
                time.Now().Add(tt.duration),
            )

            assert.InDelta(t, tt.wantAccuracy, stats.Accuracy, 0.1)
            assert.InDelta(t, tt.wantCPM, stats.CPM, 5)
        })
    }
}
```

### Integration Tests

Test API client with mock server:

```go
func TestAPIClient(t *testing.T) {
    // Start mock HTTP server
    server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.WriteHeader(http.StatusOK)
        json.NewEncoder(w).Encode(CodeDocument{
            Title: "Test Algorithm",
            Code:  "def test(): pass",
        })
    }))
    defer server.Close()

    client := NewAPIClient(server.URL, 5*time.Second)
    doc, err := client.FetchRandom(FilterConfig{})

    assert.NoError(t, err)
    assert.Equal(t, "Test Algorithm", doc.Title)
}
```

### Bubble Tea Component Tests

Test Update and View functions:

```go
func TestResultsComponent(t *testing.T) {
    stats := &Statistics{
        TimeElapsed: 60 * time.Second,
        TotalChars:  100,
        TotalErrors: 5,
        Accuracy:    95.0,
        CPM:         100,
    }

    results := NewResults(stats, &CodeDocument{Title: "Test"})
    view := results.View()

    assert.Contains(t, view, "Test")
    assert.Contains(t, view, "95.0%")
    assert.Contains(t, view, "100")
}
```

---

## Performance Considerations

### Memory Management

1. **Reuse Buffers**: Use `bytes.Buffer` for string building
2. **Avoid Allocations**: Pre-allocate slices with known capacity
3. **Clear Unused Data**: Clear previous algorithm data when loading next

### Rendering Optimization

1. **Cache Highlighted Code**: Highlight once, render many times
2. **Minimize Redraws**: Only update changed regions
3. **Viewport Clipping**: Only render visible lines

### Concurrency Safety

1. **Channel Communication**: Use channels for goroutine communication
2. **No Shared State**: Each component owns its state
3. **Context Cancellation**: Graceful shutdown of background goroutines

---

## Summary Diagram

```
┌─────────────────────────────────────────────────────────┐
│                       User                              │
└────────────────────┬────────────────────────────────────┘
                     │ Keyboard Input
                     ▼
┌─────────────────────────────────────────────────────────┐
│                 Bubble Tea Runtime                      │
│  ┌──────────┐     ┌──────────┐      ┌──────────┐       │
│  │  Model   │────▶│  Update  │─────▶│   View   │       │
│  │ (State)  │◀────│(Messages)│      │ (Render) │       │
│  └──────────┘     └──────────┘      └──────────┘       │
│       │                                    │            │
│       │                                    │            │
│       ▼                                    ▼            │
│  ┌────────────────────────────────────────────────┐    │
│  │            Components                          │    │
│  │  • CodeDisplay  • Results  • Settings          │    │
│  └────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
                     │
                     │ API Calls
                     ▼
┌─────────────────────────────────────────────────────────┐
│                 Background Services                     │
│  ┌─────────────────┐         ┌──────────────────┐      │
│  │  Prefetch       │────────▶│   API Client     │      │
│  │  Goroutine      │         │  (HTTP)          │      │
│  │  (Channel)      │         │                  │      │
│  └─────────────────┘         └──────────────────┘      │
└─────────────────────────────────────────────────────────┘
                     │
                     ▼
           ┌──────────────────┐
           │   Beaver API     │
           │  (Backend Go)    │
           └──────────────────┘
```

---

**Document Status**: Draft v1.0
**Last Updated**: 2025-11-10
**Owner**: Beaver Development Team
