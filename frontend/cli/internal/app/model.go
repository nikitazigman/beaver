package app

import (
	"context"
	"time"

	"github.com/charmbracelet/bubbles/viewport"
	tea "github.com/charmbracelet/bubbletea"

	"github.com/beaver-app/beaver-cli/internal/models"
	"github.com/beaver-app/beaver-cli/internal/services"
	"github.com/beaver-app/beaver-cli/internal/syntax"
)

// Custom messages for algorithm loading
type algorithmLoadedMsg struct {
	algorithm *models.CodeDocument
}

type algorithmErrorMsg struct {
	err error
}

// Typing messages
type startTypingMsg struct {
	timestamp time.Time
}

type correctCharMsg struct {
	char      rune
	timestamp time.Time
}

type errorCharMsg struct {
	expected  rune
	actual    rune
	timestamp time.Time
}

type correctionMsg struct {
	timestamp time.Time
}

type completionMsg struct {
	timestamp time.Time
}

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

// Model is the main application state for Bubble Tea
type Model struct {
	// Screen management
	currentScreen Screen
	prevScreen    Screen // For modal return

	// Current algorithm
	algorithm       *models.CodeDocument
	highlightedCode string // Pre-highlighted code

	// Typing state
	userInput   []rune
	cursorPos   int       // Current position in code
	isTyping    bool      // Whether user has started typing
	startTime   time.Time
	endTime     time.Time
	errorPos    map[int]bool // Positions where errors occurred

	// Statistics tracking
	typingEvents []time.Time // Timestamps of correct keypresses
	errorEvents  []time.Time // Timestamps of errors
	corrections  int         // Number of backspaces

	// Services
	apiClient    *services.APIClient
	highlighter  *syntax.Highlighter
	prefetchChan chan *models.CodeDocument
	prefetchStop chan struct{}

	// Components
	codeViewport viewport.Model

	// Configuration
	config *models.Config

	// UI state
	windowWidth  int
	windowHeight int
	ready        bool
	err          error

	// Key bindings
	// keys KeyMap // TODO: Implement in keys.go
}

// NewModel creates a new application model
func NewModel(config *models.Config, apiClient *services.APIClient) Model {
	// Create highlighter with configured theme
	highlighter := syntax.NewHighlighter(config.UI.Theme)

	return Model{
		currentScreen: ScreenLoading,
		config:        config,
		apiClient:     apiClient,
		highlighter:   highlighter,
		prefetchChan:  make(chan *models.CodeDocument, config.Prefetch.QueueSize),
		prefetchStop:  make(chan struct{}),
		codeViewport:  viewport.New(80, 24),
		typingEvents:  make([]time.Time, 0),
		errorEvents:   make([]time.Time, 0),
		corrections:   0,
		errorPos:      make(map[int]bool),
		userInput:     make([]rune, 0),
	}
}

// Init initializes the Bubble Tea application
func (m Model) Init() tea.Cmd {
	// Fetch the first algorithm on startup
	return m.fetchAlgorithm()
}

// fetchAlgorithm creates a command to fetch an algorithm from the API
func (m Model) fetchAlgorithm() tea.Cmd {
	return func() tea.Msg {
		ctx := context.Background()

		// Use configured language filter, or empty for random
		language := m.config.Filters.Language
		tags := m.config.Filters.Tags

		doc, err := m.apiClient.FetchRandom(ctx, language, tags)
		if err != nil {
			return algorithmErrorMsg{err: err}
		}

		return algorithmLoadedMsg{algorithm: doc}
	}
}

// rehighlightCode re-applies syntax highlighting to the current algorithm
// This is useful when the theme changes
func (m *Model) rehighlightCode() {
	if m.algorithm != nil {
		highlighted, err := m.highlighter.Highlight(m.algorithm.Code, m.algorithm.Language)
		if err != nil {
			m.highlightedCode = m.algorithm.Code
		} else {
			m.highlightedCode = highlighted
		}
	}
}
