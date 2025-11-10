# Beaver Go CLI - Technology Stack

## Overview

This document outlines all technology choices, libraries, and tools for building the Beaver Go CLI application. Each choice is justified based on project requirements, community support, and production readiness.

---

## Core Technology

### Go 1.21+

**Chosen Version**: Go 1.21 or later

**Justification**:
- Modern language features (generics, improved error handling)
- Excellent standard library for networking, concurrency, file I/O
- Single binary distribution (no runtime dependencies)
- Fast compilation and execution
- Strong typing with excellent tooling
- Native concurrency with goroutines and channels
- Cross-platform support (macOS, Linux, Windows)

**Why Go over Python**:
- Better performance (startup time, memory usage, CPU)
- Easier distribution (single binary vs Python + dependencies)
- Better concurrency primitives (goroutines vs threads)
- Stronger type safety at compile time
- No runtime version conflicts

---

## TUI Framework

### Bubble Tea

**Package**: `github.com/charmbracelet/bubbletea`
**Latest Version**: v0.27.x (check for latest)
**License**: MIT

**Description**:
Bubble Tea is a Go framework for building terminal applications based on The Elm Architecture (TEA). It provides a clean, functional approach to TUI development with a strong focus on composability and testability.

**Key Features**:
- Model-Update-View architecture (predictable state management)
- Event-driven message passing
- Built-in support for keyboard, mouse, window resize events
- No global state (all state in model)
- Composable components
- Active development and strong community
- Production-ready (used by GitHub, Charm, and many others)

**Why Bubble Tea**:
- ✅ De facto standard for Go TUI apps (most popular)
- ✅ Clean architecture that scales well
- ✅ Excellent documentation and examples
- ✅ Rich ecosystem (Bubbles, Lipgloss, Glamour)
- ✅ Active maintenance by Charm (funded company)
- ✅ Handles all low-level terminal interactions

**Alternatives Considered**:
- **tview**: More traditional widget-based approach, less flexible
- **termui**: More focused on dashboards/visualizations
- **gocui**: Lower-level, requires more manual work

**Decision**: Bubble Tea offers the best balance of power, simplicity, and community support.

---

## UI Components & Styling

### Bubbles (Component Library)

**Package**: `github.com/charmbracelet/bubbles`
**Latest Version**: v0.18.x
**License**: MIT

**Description**:
Ready-made Bubble Tea components for common UI patterns.

**Components We'll Use**:

1. **Viewport** (`bubbles/viewport`)
   - Scrollable content area
   - Use for: Code display, help screen
   - Features: Keyboard/mouse scrolling, percentage tracking

2. **Spinner** (`bubbles/spinner`)
   - Loading indicator
   - Use for: Fetching algorithms, waiting states
   - Features: Multiple spinner styles, customizable

3. **Help** (`bubbles/help`)
   - Keyboard shortcut display
   - Use for: Footer shortcuts, help screen
   - Features: Full/short modes, key binding management

4. **Text Input** (`bubbles/textinput`)
   - Single-line text input
   - Use for: Settings (tab width, API URL)
   - Features: Placeholder, validation, cursor

**Why Bubbles**:
- ✅ Officially maintained by Charm
- ✅ Consistent with Bubble Tea patterns
- ✅ Well-tested in production
- ✅ Saves development time on common patterns

### Lipgloss (Styling Library)

**Package**: `github.com/charmbracelet/lipgloss`
**Latest Version**: v0.13.x
**License**: MIT

**Description**:
Style definitions for terminal output. Think of it as "CSS for the terminal."

**Features**:
- Colors (ANSI, hex, RGB)
- Text formatting (bold, italic, underline)
- Borders and boxes
- Padding and margins
- Width and height constraints
- Alignment (left, center, right)
- Composable styles

**Usage Examples**:

```go
// Title style
titleStyle := lipgloss.NewStyle().
    Bold(true).
    Foreground(lipgloss.Color("#FAFAFA")).
    Background(lipgloss.Color("#7D56F4")).
    Padding(0, 1)

// Error text style
errorStyle := lipgloss.NewStyle().
    Foreground(lipgloss.Color("#FF0000")).
    Bold(true)

// Box with border
box := lipgloss.NewStyle().
    Border(lipgloss.RoundedBorder()).
    BorderForeground(lipgloss.Color("#7D56F4")).
    Padding(1, 2)
```

**Why Lipgloss**:
- ✅ Declarative styling (easy to maintain)
- ✅ Handles terminal color capabilities automatically
- ✅ Consistent rendering across terminals
- ✅ Composable and reusable styles
- ✅ Part of Charm ecosystem (works seamlessly with Bubble Tea)

---

## Syntax Highlighting

### Chroma

**Package**: `github.com/alecthomas/chroma/v2`
**Latest Version**: v2.14.x
**License**: MIT

**Description**:
Pure Go syntax highlighting library supporting 200+ languages.

**Key Features**:
- Lexers for all major programming languages
- Multiple built-in styles (Monokai, VS Code Dark, GitHub, etc.)
- ANSI/terminal output formatters
- Fast and memory-efficient
- No external dependencies (pure Go)
- Used by many projects (Hugo, GitHub CLI, etc.)

**Languages Supported** (relevant to Beaver):
- Python ✅
- Go ✅
- JavaScript/TypeScript ✅
- Java ✅
- C/C++ ✅
- Rust ✅
- Ruby ✅
- PHP ✅
- ...and 200+ more

**Usage Example**:

```go
import (
    "github.com/alecthomas/chroma/v2/quick"
    "github.com/alecthomas/chroma/v2/formatters"
    "github.com/alecthomas/chroma/v2/styles"
)

// Highlight code
var buf bytes.Buffer
err := quick.Highlight(&buf, code, "python", "terminal16m", "monokai")

// More control
lexer := lexers.Get("python")
style := styles.Get("monokai")
formatter := formatters.Get("terminal16m")
iterator, _ := lexer.Tokenise(nil, code)
formatter.Format(&buf, style, iterator)
```

**Integration with Bubble Tea**:
- Highlight code in model initialization
- Store highlighted output as styled string
- Render in view using Lipgloss

**Styles We'll Use**:
- **Dark theme**: `monokai` or `dracula`
- **Light theme**: `github` or `xcode`

**Why Chroma**:
- ✅ Most comprehensive language support
- ✅ Pure Go (no C dependencies)
- ✅ Battle-tested in production
- ✅ Easy to integrate with terminal output
- ✅ Customizable and extensible

**Alternatives Considered**:
- **go-tree-sitter**: More accurate, but overkill for display-only highlighting
- **regexp-based**: Too limited, hard to maintain

---

## HTTP Client

### Standard Library (`net/http`)

**Package**: Built-in `net/http`
**Go Version**: Included in Go 1.21+

**Description**:
Go's standard HTTP client is production-ready and feature-complete.

**Features**:
- Connection pooling (via `http.Transport`)
- Timeout control (per request, connection, TLS handshake)
- Automatic redirect handling
- HTTP/2 support
- Cookie management
- TLS/SSL support

**Configuration**:

```go
client := &http.Client{
    Timeout: 5 * time.Second,
    Transport: &http.Transport{
        MaxIdleConns:        10,
        MaxIdleConnsPerHost: 5,
        IdleConnTimeout:     30 * time.Second,
    },
}
```

**Why Standard Library**:
- ✅ No external dependencies
- ✅ Well-documented and understood
- ✅ Sufficient for our needs
- ✅ Connection pooling built-in
- ✅ Easy timeout management

**Optional Enhancement**: `github.com/hashicorp/go-retryablehttp`
- Automatic retry with exponential backoff
- Wraps `net/http.Client`
- Only add if we need sophisticated retry logic

---

## Configuration Management

### Viper

**Package**: `github.com/spf13/viper`
**Latest Version**: v1.18.x
**License**: MIT

**Description**:
Complete configuration solution for Go applications.

**Features**:
- Multiple config formats (YAML, JSON, TOML, env vars)
- Environment variable support with prefixes
- Config file watching (hot reload)
- Defaults and validation
- Nested configuration
- Remote config support (optional)

**Usage Example**:

```go
import "github.com/spf13/viper"

// Set defaults
viper.SetDefault("api.base_url", "https://beaver-api.com")
viper.SetDefault("api.timeout", "5s")

// Read config file
viper.SetConfigName("config")
viper.SetConfigType("yaml")
viper.AddConfigPath("$HOME/.config/beaver")
viper.ReadInConfig()

// Environment variables
viper.SetEnvPrefix("BEAVER")
viper.AutomaticEnv()

// Get values
apiURL := viper.GetString("api.base_url")
timeout := viper.GetDuration("api.timeout")
```

**Config File Structure**:

```yaml
# ~/.config/beaver/config.yaml
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

**Why Viper**:
- ✅ Industry standard (used by Kubernetes, Hugo, etc.)
- ✅ Handles all config scenarios
- ✅ Environment variable overrides (good for Docker)
- ✅ Type-safe getters
- ✅ Default values built-in

**Alternative**: `github.com/kelseyhightower/envconfig` (simpler, env-only)
- Already used in backend API
- Lighter weight if we only need env vars
- **Decision**: Use Viper for flexibility (config file + env vars)

---

## Data Validation

### Go Playground Validator

**Package**: `github.com/go-playground/validator/v10`
**Latest Version**: v10.22.x
**License**: MIT

**Description**:
Struct and field validation using tags.

**Usage Example**:

```go
type Config struct {
    APIBaseURL string        `validate:"required,url"`
    Timeout    time.Duration `validate:"required,min=1s,max=30s"`
    TabWidth   int           `validate:"min=1,max=8"`
}

validate := validator.New()
err := validate.Struct(config)
```

**Why Validator**:
- ✅ Declarative validation (tags)
- ✅ Extensive built-in rules
- ✅ Custom validators supported
- ✅ Used in many Go projects

**Alternative**: Manual validation
- Simpler, no dependencies
- More verbose
- **Decision**: Use validator for complex validation, manual for simple checks

---

## Logging

### Zerolog

**Package**: `github.com/rs/zerolog`
**Latest Version**: v1.33.x
**License**: MIT

**Description**:
Zero-allocation JSON logger optimized for speed.

**Features**:
- Structured logging (JSON output)
- Zero-allocation design (fast)
- Log levels (Debug, Info, Warn, Error, Fatal)
- Context-aware logging
- Pretty console output (for development)

**Usage Example**:

```go
import "github.com/rs/zerolog/log"

// Development: pretty console output
log.Logger = log.Output(zerolog.ConsoleWriter{Out: os.Stderr})

// Production: JSON to file
file, _ := os.OpenFile("~/.config/beaver/beaver.log", os.O_CREATE|os.O_APPEND|os.O_WRONLY, 0644)
log.Logger = zerolog.New(file).With().Timestamp().Logger()

// Usage
log.Info().Str("algorithm", "bubble_sort").Msg("Loaded algorithm")
log.Error().Err(err).Msg("Failed to fetch from API")
```

**Why Zerolog**:
- ✅ Very fast (important for TUI, no lag)
- ✅ Structured output (easy to parse)
- ✅ Nice console output for debugging
- ✅ Zero allocations (GC-friendly)

**Alternative**: `go.uber.org/zap`
- Already used in backend API
- Slightly more features, but heavier
- **Decision**: Use zerolog for CLI (lighter, faster)

---

## CLI Argument Parsing

### Cobra

**Package**: `github.com/spf13/cobra`
**Latest Version**: v1.8.x
**License**: Apache 2.0

**Description**:
Modern CLI framework for Go, used by Kubernetes, Docker, GitHub CLI, etc.

**Features**:
- Subcommands (`beaver practice`, `beaver config`, etc.)
- Flags (global, persistent, local)
- Auto-generated help
- Shell completion (bash, zsh, fish)
- Flag aliases and shortcuts

**Usage Example**:

```go
var rootCmd = &cobra.Command{
    Use:   "beaver",
    Short: "Typing practice for developers",
    Run: func(cmd *cobra.Command, args []string) {
        // Start TUI
        runApp()
    },
}

var configCmd = &cobra.Command{
    Use:   "config",
    Short: "Show current configuration",
    Run: func(cmd *cobra.Command, args []string) {
        showConfig()
    },
}

func main() {
    rootCmd.AddCommand(configCmd)
    rootCmd.Execute()
}
```

**Commands We'll Support**:

```bash
beaver                    # Start TUI (default)
beaver --version          # Show version
beaver --config <path>    # Use custom config file
beaver config             # Show current config
beaver config reset       # Reset to defaults
```

**Why Cobra**:
- ✅ Industry standard (kubectl, docker, gh all use it)
- ✅ Excellent documentation
- ✅ Auto-generated help and docs
- ✅ Shell completion
- ✅ Works well with Viper (same author)

**Alternative**: `github.com/urfave/cli`
- Simpler, but less powerful
- **Decision**: Use Cobra for future extensibility

---

## Testing

### Standard Library (`testing`)

**Package**: Built-in `testing`
**Go Version**: Included in Go 1.21+

**Tools**:
- `go test` - Test runner
- `testing.T` - Test framework
- `testing.B` - Benchmarking

**Additional Testing Libraries**:

#### Testify (Assertions)

**Package**: `github.com/stretchr/testify`
**License**: MIT

```go
import "github.com/stretchr/testify/assert"

func TestStatistics(t *testing.T) {
    stats := calculateStats(events)
    assert.Equal(t, 95.5, stats.Accuracy)
    assert.Greater(t, stats.CPM, 600)
}
```

#### Mockery (Mocking)

**Package**: `github.com/vektra/mockery`
**License**: BSD-3

Generate mocks from interfaces:

```go
//go:generate mockery --name=APIClient
type APIClient interface {
    FetchCodeDocument(filters Filters) (*CodeDocument, error)
}
```

**Why Standard Library + Testify**:
- ✅ Testing built into Go
- ✅ Testify adds convenience without complexity
- ✅ Table-driven tests easy to write
- ✅ Mockery generates clean mocks

---

## Build and Tooling

### Go Modules

**Tool**: `go mod`
**Go Version**: Built-in

For dependency management:

```bash
go mod init github.com/yourorg/beaver-cli
go mod tidy
go mod vendor  # Optional: vendor dependencies
```

### Makefile

For common tasks:

```makefile
.PHONY: build test run clean install

build:
    go build -o bin/beaver cmd/beaver/main.go

test:
    go test ./...

run:
    go run cmd/beaver/main.go

install:
    go install cmd/beaver/main.go

clean:
    rm -rf bin/
```

### GoReleaser

**Package**: `github.com/goreleaser/goreleaser`
**License**: MIT

For building multi-platform binaries and releases:

```yaml
# .goreleaser.yaml
builds:
  - main: ./cmd/beaver
    binary: beaver
    goos:
      - linux
      - darwin
      - windows
    goarch:
      - amd64
      - arm64
```

---

## Full Dependency List

### Direct Dependencies

```go
// go.mod
module github.com/yourorg/beaver-cli

go 1.21

require (
    github.com/charmbracelet/bubbletea v0.27.0
    github.com/charmbracelet/bubbles v0.18.0
    github.com/charmbracelet/lipgloss v0.13.0
    github.com/alecthomas/chroma/v2 v2.14.0
    github.com/spf13/cobra v1.8.0
    github.com/spf13/viper v1.18.0
    github.com/rs/zerolog v1.33.0
    github.com/go-playground/validator/v10 v10.22.0
)

require (
    // Test dependencies
    github.com/stretchr/testify v1.9.0
)
```

### Approximate Binary Size

Estimated final binary size (with all dependencies):
- **macOS/Linux**: ~15-20 MB
- **Windows**: ~15-20 MB

Compressed (gzip):
- **All platforms**: ~5-7 MB

---

## Development Environment

### Required Tools

1. **Go 1.21+**: Language runtime and toolchain
2. **Make**: Build automation (optional but recommended)
3. **Git**: Version control
4. **Modern Terminal**: iTerm2, Alacritty, Kitty, Windows Terminal

### Recommended Tools

1. **GoLand / VS Code**: IDE with Go support
2. **golangci-lint**: Linting (catches common issues)
3. **gopls**: Language server (for IDE features)
4. **delve**: Debugger (for debugging)

### Editor Setup

**VS Code Extensions**:
- Go (official)
- Error Lens
- GitLens

**Linting Configuration** (`.golangci.yml`):

```yaml
linters:
  enable:
    - gofmt
    - govet
    - errcheck
    - staticcheck
    - unused
    - gosimple
    - ineffassign
```

---

## Platform Support

### Supported Platforms

| OS | Architecture | Status |
|----|--------------|--------|
| **macOS** | Intel (amd64) | ✅ Primary |
| **macOS** | Apple Silicon (arm64) | ✅ Primary |
| **Linux** | amd64 | ✅ Primary |
| **Linux** | arm64 | ✅ Secondary |
| **Windows** | amd64 | ✅ Secondary |

### Terminal Compatibility

**Tested Terminals**:
- iTerm2 (macOS) ✅
- Terminal.app (macOS) ✅
- Alacritty (cross-platform) ✅
- Kitty (cross-platform) ✅
- Windows Terminal (Windows) ✅

**Minimum Requirements**:
- 256-color support (for syntax highlighting)
- UTF-8 support (for box drawing characters)
- Minimum size: 80x24

---

## Summary Table

| Category | Choice | Reason |
|----------|--------|--------|
| **Language** | Go 1.21+ | Performance, single binary, strong typing |
| **TUI Framework** | Bubble Tea | Industry standard, Elm architecture, great ecosystem |
| **Components** | Bubbles | Official components, well-tested |
| **Styling** | Lipgloss | CSS-like styling for terminals |
| **Syntax Highlighting** | Chroma | 200+ languages, pure Go, fast |
| **HTTP Client** | net/http | Built-in, sufficient for our needs |
| **Configuration** | Viper | Flexible, supports files + env vars |
| **Validation** | go-playground/validator | Declarative, extensive rules |
| **Logging** | Zerolog | Fast, zero-allocation, structured |
| **CLI Framework** | Cobra | Industry standard, great for extensibility |
| **Testing** | testing + Testify | Built-in + convenient assertions |

---

**Document Status**: Draft v1.0
**Last Updated**: 2025-11-10
**Owner**: Beaver Development Team
