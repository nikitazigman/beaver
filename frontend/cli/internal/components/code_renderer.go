package components

import (
	"strings"

	"github.com/charmbracelet/lipgloss"
)

// RenderCodeWithCursor renders code with cursor position highlighted
func RenderCodeWithCursor(code string, cursorPos int, typed []rune, errors map[int]bool) string {
	runes := []rune(code)
	if len(runes) == 0 {
		return ""
	}

	var result strings.Builder

	// Styles
	typedStyle := lipgloss.NewStyle().Foreground(lipgloss.Color("240")).Faint(true)
	cursorStyle := lipgloss.NewStyle().
		Background(lipgloss.Color("33")).
		Foreground(lipgloss.Color("0")).
		Bold(true)
	errorStyle := lipgloss.NewStyle().
		Background(lipgloss.Color("196")).
		Foreground(lipgloss.Color("255"))
	upcomingStyle := lipgloss.NewStyle() // Normal style

	for i, r := range runes {
		var styled string
		char := string(r)

		if i < len(typed) {
			// Already typed
			if errors[i] {
				// Error at this position
				styled = errorStyle.Render(char)
			} else {
				// Correctly typed
				styled = typedStyle.Render(char)
			}
		} else if i == cursorPos {
			// Current cursor position
			styled = cursorStyle.Render(char)
		} else {
			// Upcoming characters
			styled = upcomingStyle.Render(char)
		}

		result.WriteString(styled)
	}

	return result.String()
}

// StripANSI removes ANSI escape codes (for testing)
func StripANSI(s string) string {
	result := ""
	inEscape := false
	for _, ch := range s {
		if ch == '\x1b' {
			inEscape = true
			continue
		}
		if inEscape {
			if ch == 'm' {
				inEscape = false
			}
			continue
		}
		result += string(ch)
	}
	return result
}
