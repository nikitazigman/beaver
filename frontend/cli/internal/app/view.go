package app

import (
	"fmt"

	"github.com/charmbracelet/lipgloss"
)

// View renders the UI based on current model state
func (m Model) View() string {
	if !m.ready {
		return "\n  Initializing..."
	}

	// Render based on current screen
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
	default:
		return "Unknown screen"
	}
}

// renderLoading shows loading spinner while fetching algorithm
func (m Model) renderLoading() string {
	var s string
	s += m.renderHeader()
	s += "\n\n"
	s += "  Loading algorithm...\n"
	s += "  Please wait...\n"
	s += "\n\n"
	s += m.renderFooter()
	return s
}

// renderTyping shows the main typing practice screen
func (m Model) renderTyping() string {
	var s string
	s += m.renderHeader()
	s += "\n"

	if m.algorithm != nil {
		// Algorithm metadata
		metadataStyle := lipgloss.NewStyle().Foreground(lipgloss.Color("240"))
		s += "\n"
		s += metadataStyle.Render(fmt.Sprintf("  %s", m.algorithm.Title))
		s += metadataStyle.Render(fmt.Sprintf(" • %s", m.algorithm.Language))
		if len(m.algorithm.Tags) > 0 {
			tags := ""
			for i, tag := range m.algorithm.Tags {
				if i > 0 {
					tags += ", "
				}
				tags += tag
			}
			s += metadataStyle.Render(fmt.Sprintf(" • %s", tags))
		}
		s += "\n\n"

		// Display highlighted code in viewport-like area
		codeStyle := lipgloss.NewStyle().
			Border(lipgloss.RoundedBorder()).
			BorderForeground(lipgloss.Color("238")).
			Padding(0, 1)

		codeContent := ""
		if m.highlightedCode != "" {
			codeContent = m.highlightedCode
		} else {
			codeContent = m.algorithm.Code
		}

		s += codeStyle.Render(codeContent)
		s += "\n\n"

		// Status message
		if !m.isTyping {
			statusStyle := lipgloss.NewStyle().
				Foreground(lipgloss.Color("42")).
				Bold(true)
			s += statusStyle.Render("  ▶ Start typing to begin...")
		} else {
			// Show progress
			progress := float64(m.cursorPos) / float64(len([]rune(m.algorithm.Code))) * 100
			statusStyle := lipgloss.NewStyle().Foreground(lipgloss.Color("33"))
			s += statusStyle.Render(fmt.Sprintf("  Progress: %.1f%%", progress))
		}
		s += "\n"
	} else {
		s += "\n  No algorithm loaded\n\n"
	}

	s += m.renderFooter()
	return s
}

// renderResults shows typing statistics after completion
func (m Model) renderResults() string {
	var s string
	s += m.renderHeader()
	s += "\n\n"
	s += "  Results\n"
	s += "  -------\n"
	s += "\n"
	s += "  WPM: --\n"
	s += "  Accuracy: --%\n"
	s += "  Time: --s\n"
	s += "\n"
	s += "  Press Tab/Enter/Space for next algorithm\n"
	s += "\n"
	s += m.renderFooter()
	return s
}

// renderSettings shows configuration options
func (m Model) renderSettings() string {
	var s string
	s += m.renderHeader()
	s += "\n\n"
	s += "  Settings\n"
	s += "  --------\n"
	s += "\n"

	if m.config != nil {
		s += fmt.Sprintf("  API URL: %s\n", m.config.API.BaseURL)
		s += fmt.Sprintf("  Theme: %s\n", m.config.UI.Theme)
		s += fmt.Sprintf("  Language: %s\n", m.config.Filters.Language)
		s += "\n"
	}

	s += "  Press Esc to close\n"
	s += "\n"
	s += m.renderFooter()
	return s
}

// renderHelp shows keyboard shortcuts and instructions
func (m Model) renderHelp() string {
	var s string
	s += m.renderHeader()
	s += "\n\n"

	helpContent := `  Keyboard Shortcuts
  ------------------

  Global:
    q, Ctrl+C  - Quit application
    ?          - Toggle this help screen
    s          - Open settings

  Typing Screen:
    Tab        - Skip to next algorithm (when not typing)
    Esc        - Pause/return to menu

  Results Screen:
    Tab/Enter/Space - Load next algorithm
    r               - Retry same algorithm

  Settings:
    Esc     - Close settings
    Ctrl+C  - Cancel without saving

  Error Screen:
    r  - Retry
    s  - Open settings
    c  - Clear filters
`

	s += helpContent
	s += "\n"
	s += "  Press ? or Esc to close\n"
	s += "\n"
	s += m.renderFooter()
	return s
}

// renderError shows error messages with recovery options
func (m Model) renderError() string {
	var s string
	s += m.renderHeader()
	s += "\n\n"
	s += "  Error\n"
	s += "  -----\n"
	s += "\n"

	if m.err != nil {
		s += fmt.Sprintf("  %s\n", m.err.Error())
	} else {
		s += "  An unknown error occurred\n"
	}

	s += "\n"
	s += "  Press 'r' to retry\n"
	s += "  Press 's' for settings\n"
	s += "\n"
	s += m.renderFooter()
	return s
}

// renderHeader shows the app title and current status
func (m Model) renderHeader() string {
	title := lipgloss.NewStyle().
		Bold(true).
		Foreground(lipgloss.Color("205")).
		Render("Beaver CLI - Developer Typing Practice")

	return fmt.Sprintf("\n  %s\n", title)
}

// renderFooter shows global shortcuts reminder
func (m Model) renderFooter() string {
	footer := lipgloss.NewStyle().
		Foreground(lipgloss.Color("241")).
		Render("Press ? for help • q to quit")

	return fmt.Sprintf("  %s\n", footer)
}
