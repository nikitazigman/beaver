package app

import (
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
	switch msg.String() {
	case "tab":
		if !m.isTyping {
			// Skip to next algorithm
			// TODO: Implement loadNext
			return m, nil
		}
		// During typing, tab inserts spaces (handled in character input)

	case "esc":
		// Pause or return to menu (optional)
		return m, nil
	}

	// Handle character input
	// TODO: Implement character-by-character validation
	return m, nil
}

// handleResultsKeys handles keys on results screen
func (m Model) handleResultsKeys(msg tea.KeyMsg) (tea.Model, tea.Cmd) {
	switch msg.String() {
	case "tab", "enter", " ":
		// Load next algorithm
		// TODO: Implement loadNext
		m.currentScreen = ScreenLoading
		return m, nil

	case "r":
		// Retry same algorithm (optional)
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
		// Retry
		m.currentScreen = ScreenLoading
		// TODO: Retry fetch
		return m, nil

	case "s":
		// Open settings
		m.prevScreen = ScreenError
		m.currentScreen = ScreenSettings
		return m, nil

	case "c":
		// Clear filters (optional)
		return m, nil
	}

	return m, nil
}
