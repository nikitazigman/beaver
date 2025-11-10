package app

import (
	"time"

	"github.com/charmbracelet/bubbles/viewport"
	tea "github.com/charmbracelet/bubbletea"

	"github.com/beaver-app/beaver-cli/internal/models"
	"github.com/beaver-app/beaver-cli/internal/services"
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

	// Statistics tracking
	typingEvents []time.Time // Timestamps of correct keypresses
	errorEvents  []time.Time // Timestamps of errors
	corrections  int         // Number of backspaces

	// Services
	apiClient    *services.APIClient
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
	return Model{
		currentScreen: ScreenLoading,
		config:        config,
		apiClient:     apiClient,
		prefetchChan:  make(chan *models.CodeDocument, config.Prefetch.QueueSize),
		prefetchStop:  make(chan struct{}),
		codeViewport:  viewport.New(80, 24),
		typingEvents:  make([]time.Time, 0),
		errorEvents:   make([]time.Time, 0),
		corrections:   0,
	}
}

// Init initializes the Bubble Tea application
func (m Model) Init() tea.Cmd {
	// Start prefetch service (will be implemented later)
	// For now, just return nil
	return nil
}
