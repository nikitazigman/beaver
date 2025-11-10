package app

import (
	"testing"
	"time"

	tea "github.com/charmbracelet/bubbletea"
	"github.com/beaver-app/beaver-cli/internal/models"
	"github.com/beaver-app/beaver-cli/internal/services"
	"github.com/google/uuid"
)

func TestUpdate_WindowSizeMsg(t *testing.T) {
	config := models.DefaultConfig()
	apiClient := services.NewAPIClient("https://test-api.com", 5*time.Second)
	model := NewModel(config, apiClient)

	msg := tea.WindowSizeMsg{
		Width:  100,
		Height: 50,
	}

	newModel, cmd := model.Update(msg)
	m := newModel.(Model)

	if m.windowWidth != 100 {
		t.Errorf("windowWidth = %v, want 100", m.windowWidth)
	}
	if m.windowHeight != 50 {
		t.Errorf("windowHeight = %v, want 50", m.windowHeight)
	}
	if !m.ready {
		t.Error("ready should be true after WindowSizeMsg")
	}
	if m.codeViewport.Width != 96 { // 100 - 4
		t.Errorf("codeViewport.Width = %v, want 96", m.codeViewport.Width)
	}
	if m.codeViewport.Height != 40 { // 50 - 10
		t.Errorf("codeViewport.Height = %v, want 40", m.codeViewport.Height)
	}
	if cmd != nil {
		t.Error("WindowSizeMsg should return nil cmd")
	}
}

func TestUpdate_QuitKeys(t *testing.T) {
	config := models.DefaultConfig()
	apiClient := services.NewAPIClient("https://test-api.com", 5*time.Second)
	model := NewModel(config, apiClient)

	tests := []struct {
		name string
		key  string
	}{
		{"ctrl+c", "ctrl+c"},
		{"q key", "q"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			msg := tea.KeyMsg{Type: tea.KeyRunes, Runes: []rune(tt.key)}
			if tt.key == "ctrl+c" {
				msg = tea.KeyMsg{Type: tea.KeyCtrlC}
			}

			_, cmd := model.Update(msg)
			if cmd == nil {
				t.Error("quit key should return tea.Quit command")
			}
		})
	}
}

func TestUpdate_HelpKey(t *testing.T) {
	config := models.DefaultConfig()
	apiClient := services.NewAPIClient("https://test-api.com", 5*time.Second)
	model := NewModel(config, apiClient)
	model.currentScreen = ScreenTyping

	msg := tea.KeyMsg{Type: tea.KeyRunes, Runes: []rune("?")}
	newModel, _ := model.Update(msg)
	m := newModel.(Model)

	if m.currentScreen != ScreenHelp {
		t.Errorf("currentScreen = %v, want ScreenHelp", m.currentScreen)
	}
	if m.prevScreen != ScreenTyping {
		t.Errorf("prevScreen = %v, want ScreenTyping", m.prevScreen)
	}
}

func TestUpdate_SettingsKey(t *testing.T) {
	config := models.DefaultConfig()
	apiClient := services.NewAPIClient("https://test-api.com", 5*time.Second)
	model := NewModel(config, apiClient)
	model.currentScreen = ScreenResults
	model.isTyping = false // Not typing, so 's' should work

	msg := tea.KeyMsg{Type: tea.KeyRunes, Runes: []rune("s")}
	newModel, _ := model.Update(msg)
	m := newModel.(Model)

	if m.currentScreen != ScreenSettings {
		t.Errorf("currentScreen = %v, want ScreenSettings", m.currentScreen)
	}
	if m.prevScreen != ScreenResults {
		t.Errorf("prevScreen = %v, want ScreenResults", m.prevScreen)
	}
}

func TestUpdate_SettingsKeyWhileTyping(t *testing.T) {
	config := models.DefaultConfig()
	apiClient := services.NewAPIClient("https://test-api.com", 5*time.Second)
	model := NewModel(config, apiClient)
	model.currentScreen = ScreenTyping
	model.isTyping = true // Typing, so 's' should be ignored

	msg := tea.KeyMsg{Type: tea.KeyRunes, Runes: []rune("s")}
	newModel, _ := model.Update(msg)
	m := newModel.(Model)

	if m.currentScreen != ScreenTyping {
		t.Errorf("currentScreen = %v, want ScreenTyping (should not change)", m.currentScreen)
	}
}

func TestHandleSettingsKeys_Escape(t *testing.T) {
	config := models.DefaultConfig()
	apiClient := services.NewAPIClient("https://test-api.com", 5*time.Second)
	model := NewModel(config, apiClient)
	model.currentScreen = ScreenSettings
	model.prevScreen = ScreenTyping

	msg := tea.KeyMsg{Type: tea.KeyEsc}
	newModel, _ := model.Update(msg)
	m := newModel.(Model)

	if m.currentScreen != ScreenTyping {
		t.Errorf("currentScreen = %v, want ScreenTyping", m.currentScreen)
	}
}

func TestHandleHelpKeys_Escape(t *testing.T) {
	config := models.DefaultConfig()
	apiClient := services.NewAPIClient("https://test-api.com", 5*time.Second)
	model := NewModel(config, apiClient)
	model.currentScreen = ScreenHelp
	model.prevScreen = ScreenResults

	msg := tea.KeyMsg{Type: tea.KeyEsc}
	newModel, _ := model.Update(msg)
	m := newModel.(Model)

	if m.currentScreen != ScreenResults {
		t.Errorf("currentScreen = %v, want ScreenResults", m.currentScreen)
	}
}

func TestHandleHelpKeys_QuestionMark(t *testing.T) {
	config := models.DefaultConfig()
	apiClient := services.NewAPIClient("https://test-api.com", 5*time.Second)
	model := NewModel(config, apiClient)
	model.currentScreen = ScreenHelp
	model.prevScreen = ScreenTyping

	msg := tea.KeyMsg{Type: tea.KeyRunes, Runes: []rune("?")}
	newModel, _ := model.Update(msg)
	m := newModel.(Model)

	if m.currentScreen != ScreenTyping {
		t.Errorf("currentScreen = %v, want ScreenTyping (help closed)", m.currentScreen)
	}
}

func TestHandleResultsKeys_Tab(t *testing.T) {
	config := models.DefaultConfig()
	apiClient := services.NewAPIClient("https://test-api.com", 5*time.Second)
	model := NewModel(config, apiClient)
	model.currentScreen = ScreenResults

	msg := tea.KeyMsg{Type: tea.KeyTab}
	newModel, _ := model.Update(msg)
	m := newModel.(Model)

	if m.currentScreen != ScreenLoading {
		t.Errorf("currentScreen = %v, want ScreenLoading", m.currentScreen)
	}
}

func TestHandleResultsKeys_Enter(t *testing.T) {
	config := models.DefaultConfig()
	apiClient := services.NewAPIClient("https://test-api.com", 5*time.Second)
	model := NewModel(config, apiClient)
	model.currentScreen = ScreenResults

	msg := tea.KeyMsg{Type: tea.KeyEnter}
	newModel, _ := model.Update(msg)
	m := newModel.(Model)

	if m.currentScreen != ScreenLoading {
		t.Errorf("currentScreen = %v, want ScreenLoading", m.currentScreen)
	}
}

func TestHandleResultsKeys_Space(t *testing.T) {
	config := models.DefaultConfig()
	apiClient := services.NewAPIClient("https://test-api.com", 5*time.Second)
	model := NewModel(config, apiClient)
	model.currentScreen = ScreenResults

	msg := tea.KeyMsg{Type: tea.KeySpace}
	newModel, _ := model.Update(msg)
	m := newModel.(Model)

	if m.currentScreen != ScreenLoading {
		t.Errorf("currentScreen = %v, want ScreenLoading", m.currentScreen)
	}
}

func TestHandleErrorKeys_Retry(t *testing.T) {
	config := models.DefaultConfig()
	apiClient := services.NewAPIClient("https://test-api.com", 5*time.Second)
	model := NewModel(config, apiClient)
	model.currentScreen = ScreenError

	msg := tea.KeyMsg{Type: tea.KeyRunes, Runes: []rune("r")}
	newModel, _ := model.Update(msg)
	m := newModel.(Model)

	if m.currentScreen != ScreenLoading {
		t.Errorf("currentScreen = %v, want ScreenLoading", m.currentScreen)
	}
}

func TestHandleErrorKeys_Settings(t *testing.T) {
	config := models.DefaultConfig()
	apiClient := services.NewAPIClient("https://test-api.com", 5*time.Second)
	model := NewModel(config, apiClient)
	model.currentScreen = ScreenError

	msg := tea.KeyMsg{Type: tea.KeyRunes, Runes: []rune("s")}
	newModel, _ := model.Update(msg)
	m := newModel.(Model)

	if m.currentScreen != ScreenSettings {
		t.Errorf("currentScreen = %v, want ScreenSettings", m.currentScreen)
	}
	if m.prevScreen != ScreenError {
		t.Errorf("prevScreen = %v, want ScreenError", m.prevScreen)
	}
}

func TestHandleTypingKeys_Tab(t *testing.T) {
	config := models.DefaultConfig()
	apiClient := services.NewAPIClient("https://test-api.com", 5*time.Second)
	model := NewModel(config, apiClient)
	model.currentScreen = ScreenTyping
	model.isTyping = false // Not started typing
	// Need an algorithm for the handler to work
	model.algorithm = &models.CodeDocument{
		ID:       uuid.New(),
		Title:    "Test",
		Code:     "test code",
		Language: "go",
	}

	msg := tea.KeyMsg{Type: tea.KeyTab}
	newModel, cmd := model.Update(msg)
	m := newModel.(Model)

	// Should transition to loading screen when Tab is pressed (skip to next)
	if m.currentScreen != ScreenLoading {
		t.Errorf("currentScreen = %v, want ScreenLoading", m.currentScreen)
	}
	// Should return a command to fetch algorithm
	if cmd == nil {
		t.Error("Expected cmd to fetch algorithm, got nil")
	}
}

func TestUpdate_ScreenTransitions(t *testing.T) {
	config := models.DefaultConfig()
	apiClient := services.NewAPIClient("https://test-api.com", 5*time.Second)
	model := NewModel(config, apiClient)

	tests := []struct {
		name           string
		startScreen    Screen
		key            tea.KeyMsg
		expectedScreen Screen
		expectedPrev   Screen
	}{
		{
			"Help from typing",
			ScreenTyping,
			tea.KeyMsg{Type: tea.KeyRunes, Runes: []rune("?")},
			ScreenHelp,
			ScreenTyping,
		},
		{
			"Settings from results",
			ScreenResults,
			tea.KeyMsg{Type: tea.KeyRunes, Runes: []rune("s")},
			ScreenSettings,
			ScreenResults,
		},
		{
			"Close help with esc",
			ScreenHelp,
			tea.KeyMsg{Type: tea.KeyEsc},
			ScreenLoading, // prevScreen defaults to ScreenLoading
			ScreenLoading,
		},
		{
			"Retry from error",
			ScreenError,
			tea.KeyMsg{Type: tea.KeyRunes, Runes: []rune("r")},
			ScreenLoading,
			ScreenLoading,
		},
		{
			"Next from results",
			ScreenResults,
			tea.KeyMsg{Type: tea.KeyTab},
			ScreenLoading,
			ScreenLoading,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			model.currentScreen = tt.startScreen
			newModel, _ := model.Update(tt.key)
			m := newModel.(Model)

			if m.currentScreen != tt.expectedScreen {
				t.Errorf("currentScreen = %v, want %v", m.currentScreen, tt.expectedScreen)
			}
		})
	}
}
