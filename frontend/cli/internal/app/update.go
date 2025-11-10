package app

import (
	"time"

	tea "github.com/charmbracelet/bubbletea"
)

// Update handles all messages and updates the model
func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {

	// Window resize
	case tea.WindowSizeMsg:
		m.windowWidth = msg.Width
		m.windowHeight = msg.Height
		m.ready = true

		// Update viewport dimensions
		m.codeViewport.Width = msg.Width - 4
		m.codeViewport.Height = msg.Height - 10

		return m, nil

	// Algorithm loaded successfully
	case algorithmLoadedMsg:
		m.algorithm = msg.algorithm
		m.currentScreen = ScreenTyping
		m.err = nil

		// Reset typing state
		m.cursorPos = 0
		m.userInput = make([]rune, 0)
		m.isTyping = false
		m.errorPos = make(map[int]bool)
		m.typingEvents = make([]time.Time, 0)
		m.errorEvents = make([]time.Time, 0)
		m.corrections = 0
		m.startTime = time.Time{}
		m.endTime = time.Time{}

		// Highlight the code
		if m.algorithm != nil {
			highlighted, err := m.highlighter.Highlight(m.algorithm.Code, m.algorithm.Language)
			if err != nil {
				// Log error but continue with unhighlighted code
				m.highlightedCode = m.algorithm.Code
			} else {
				m.highlightedCode = highlighted
			}
		}

		return m, nil

	// Typing events
	case startTypingMsg:
		m.isTyping = true
		m.startTime = msg.timestamp
		return m, nil

	case correctCharMsg:
		m.typingEvents = append(m.typingEvents, msg.timestamp)
		return m, nil

	case errorCharMsg:
		m.errorEvents = append(m.errorEvents, msg.timestamp)
		m.errorPos[m.cursorPos] = true
		return m, nil

	case correctionMsg:
		m.corrections++
		return m, nil

	case completionMsg:
		m.endTime = msg.timestamp
		m.currentScreen = ScreenResults
		return m, nil

	// Error loading algorithm
	case algorithmErrorMsg:
		m.err = msg.err
		m.currentScreen = ScreenError
		return m, nil

	// Keyboard input
	case tea.KeyMsg:
		return m.handleKeyPress(msg)

	}

	// Update viewport
	var cmd tea.Cmd
	m.codeViewport, cmd = m.codeViewport.Update(msg)
	return m, cmd
}

// handleKeyPress handles keyboard input based on current screen
func (m Model) handleKeyPress(msg tea.KeyMsg) (tea.Model, tea.Cmd) {
	// Global shortcuts
	switch msg.String() {
	case "ctrl+c", "q":
		// Quit application
		return m, tea.Quit

	case "?":
		// Toggle help
		if m.currentScreen == ScreenHelp {
			m.currentScreen = m.prevScreen
		} else {
			m.prevScreen = m.currentScreen
			m.currentScreen = ScreenHelp
		}
		return m, nil

	case "s":
		// Show settings (only if not typing)
		if !m.isTyping {
			m.prevScreen = m.currentScreen
			m.currentScreen = ScreenSettings
			return m, nil
		}
	}

	// Screen-specific shortcuts
	switch m.currentScreen {
	case ScreenLoading:
		return m.handleLoadingKeys(msg)
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

// handleLoadingKeys handles keys on loading screen
func (m Model) handleLoadingKeys(msg tea.KeyMsg) (tea.Model, tea.Cmd) {
	// No special handling for loading screen
	return m, nil
}

// handleTypingKeys handles keys during typing practice
func (m Model) handleTypingKeys(msg tea.KeyMsg) (tea.Model, tea.Cmd) {
	// If no algorithm loaded, do nothing
	if m.algorithm == nil {
		return m, nil
	}

	codeRunes := []rune(m.algorithm.Code)

	switch msg.Type {
	case tea.KeyTab:
		if !m.isTyping {
			// Skip to next algorithm
			m.currentScreen = ScreenLoading
			return m, m.fetchAlgorithm()
		}
		// During typing, insert tab as spaces
		return m.handleCharacterInput('\t', codeRunes)

	case tea.KeyEsc:
		// Pause or return to menu
		return m, nil

	case tea.KeyBackspace:
		return m.handleBackspace(codeRunes)

	case tea.KeyEnter:
		return m.handleCharacterInput('\n', codeRunes)

	case tea.KeySpace:
		return m.handleCharacterInput(' ', codeRunes)

	case tea.KeyRunes:
		// Handle regular character input
		if len(msg.Runes) > 0 {
			return m.handleCharacterInput(msg.Runes[0], codeRunes)
		}
	}

	return m, nil
}

// handleCharacterInput processes a single character input
func (m Model) handleCharacterInput(char rune, codeRunes []rune) (tea.Model, tea.Cmd) {
	// Start typing on first character
	if !m.isTyping {
		m.isTyping = true
		m.startTime = time.Now()
	}

	// Check if we've reached the end
	if m.cursorPos >= len(codeRunes) {
		return m, nil
	}

	expected := codeRunes[m.cursorPos]

	// Handle tab as 4 spaces or actual tab
	if char == '\t' {
		char = '\t' // Keep as tab for comparison
	}

	// Compare character
	if char == expected {
		// Correct character
		m.userInput = append(m.userInput, char)
		m.cursorPos++
		m.typingEvents = append(m.typingEvents, time.Now())

		// Check if completed
		if m.cursorPos >= len(codeRunes) {
			m.endTime = time.Now()
			m.currentScreen = ScreenResults
		}

		return m, nil
	} else {
		// Incorrect character
		m.errorPos[m.cursorPos] = true
		m.errorEvents = append(m.errorEvents, time.Now())
		return m, nil
	}
}

// handleBackspace processes backspace key
func (m Model) handleBackspace(codeRunes []rune) (tea.Model, tea.Cmd) {
	if m.cursorPos > 0 {
		m.cursorPos--
		if len(m.userInput) > 0 {
			m.userInput = m.userInput[:len(m.userInput)-1]
		}
		// Clear error at this position
		delete(m.errorPos, m.cursorPos)
		m.corrections++
	}
	return m, nil
}

// handleResultsKeys handles keys on results screen
func (m Model) handleResultsKeys(msg tea.KeyMsg) (tea.Model, tea.Cmd) {
	switch msg.String() {
	case "tab", "enter", " ":
		// Load next algorithm
		m.currentScreen = ScreenLoading
		return m, m.fetchAlgorithm()

	case "r":
		// Retry same algorithm
		m.currentScreen = ScreenTyping
		m.cursorPos = 0
		m.userInput = make([]rune, 0)
		m.isTyping = false
		m.typingEvents = make([]time.Time, 0)
		m.errorEvents = make([]time.Time, 0)
		m.corrections = 0
		return m, nil
	}

	return m, nil
}

// handleSettingsKeys handles keys on settings screen
func (m Model) handleSettingsKeys(msg tea.KeyMsg) (tea.Model, tea.Cmd) {
	switch msg.String() {
	case "esc":
		// Save and close settings
		m.currentScreen = m.prevScreen
		return m, nil

	case "ctrl+c":
		// Cancel without saving
		m.currentScreen = m.prevScreen
		return m, nil
	}

	// TODO: Handle settings navigation (tab, arrows, space, enter)
	return m, nil
}

// handleHelpKeys handles keys on help screen
func (m Model) handleHelpKeys(msg tea.KeyMsg) (tea.Model, tea.Cmd) {
	switch msg.String() {
	case "esc", "?":
		// Close help
		m.currentScreen = m.prevScreen
		return m, nil

	case "up", "k":
		// Scroll up
		m.codeViewport.LineUp(1)
		return m, nil

	case "down", "j":
		// Scroll down
		m.codeViewport.LineDown(1)
		return m, nil

	case "pgup":
		// Page up
		m.codeViewport.HalfViewUp()
		return m, nil

	case "pgdown", " ":
		// Page down
		m.codeViewport.HalfViewDown()
		return m, nil
	}

	return m, nil
}

// handleErrorKeys handles keys on error screen
func (m Model) handleErrorKeys(msg tea.KeyMsg) (tea.Model, tea.Cmd) {
	switch msg.String() {
	case "r":
		// Retry fetch
		m.currentScreen = ScreenLoading
		m.err = nil
		return m, m.fetchAlgorithm()

	case "s":
		// Open settings
		m.prevScreen = ScreenError
		m.currentScreen = ScreenSettings
		return m, nil

	case "c":
		// Clear filters
		m.config.Filters.Language = ""
		m.config.Filters.Tags = []string{}
		m.currentScreen = ScreenLoading
		m.err = nil
		return m, m.fetchAlgorithm()
	}

	return m, nil
}
