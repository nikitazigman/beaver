package app

import (
	"errors"
	"strings"
	"testing"
	"time"

	tea "github.com/charmbracelet/bubbletea"
	"github.com/beaver-app/beaver-cli/internal/models"
	"github.com/beaver-app/beaver-cli/internal/services"
	"github.com/google/uuid"
)

func TestView_NotReady(t *testing.T) {
	config := models.DefaultConfig()
	apiClient := services.NewAPIClient("https://test-api.com", 5*time.Second)
	model := NewModel(config, apiClient)
	model.ready = false

	view := model.View()
	if !strings.Contains(view, "Initializing") {
		t.Errorf("Expected 'Initializing' in view, got: %s", view)
	}
}

func TestView_Ready(t *testing.T) {
	config := models.DefaultConfig()
	apiClient := services.NewAPIClient("https://test-api.com", 5*time.Second)
	model := NewModel(config, apiClient)

	// Simulate window size message to mark as ready
	msg := tea.WindowSizeMsg{Width: 100, Height: 50}
	newModel, _ := model.Update(msg)
	model = newModel.(Model)

	if !model.ready {
		t.Fatal("Model should be ready after WindowSizeMsg")
	}

	view := model.View()
	if strings.Contains(view, "Initializing") {
		t.Error("Should not show 'Initializing' when ready")
	}
}

func TestRenderLoading(t *testing.T) {
	config := models.DefaultConfig()
	apiClient := services.NewAPIClient("https://test-api.com", 5*time.Second)
	model := NewModel(config, apiClient)
	model.ready = true
	model.currentScreen = ScreenLoading

	view := model.View()

	expectedStrings := []string{
		"Beaver CLI",
		"Loading algorithm",
		"Please wait",
		"Press ? for help",
	}

	for _, expected := range expectedStrings {
		if !strings.Contains(view, expected) {
			t.Errorf("Expected '%s' in loading view, got:\n%s", expected, view)
		}
	}
}

func TestRenderTyping_NoAlgorithm(t *testing.T) {
	config := models.DefaultConfig()
	apiClient := services.NewAPIClient("https://test-api.com", 5*time.Second)
	model := NewModel(config, apiClient)
	model.ready = true
	model.currentScreen = ScreenTyping
	model.algorithm = nil

	view := model.View()

	if !strings.Contains(view, "No algorithm loaded") {
		t.Errorf("Expected 'No algorithm loaded' when algorithm is nil, got:\n%s", view)
	}
}

func TestRenderTyping_WithAlgorithm(t *testing.T) {
	config := models.DefaultConfig()
	apiClient := services.NewAPIClient("https://test-api.com", 5*time.Second)
	model := NewModel(config, apiClient)
	model.ready = true
	model.currentScreen = ScreenTyping
	model.algorithm = &models.CodeDocument{
		ID:       uuid.New(),
		Title:    "Binary Search",
		Code:     "func binarySearch() {}",
		Language: "Go",
		Tags:     []string{"searching", "arrays"},
	}

	view := model.View()

	expectedStrings := []string{
		"Binary Search",
		"Go",
		"Start typing to begin",
		"Beaver CLI",
	}

	for _, expected := range expectedStrings {
		if !strings.Contains(view, expected) {
			t.Errorf("Expected '%s' in typing view, got:\n%s", expected, view)
		}
	}
}

func TestRenderResults(t *testing.T) {
	config := models.DefaultConfig()
	apiClient := services.NewAPIClient("https://test-api.com", 5*time.Second)
	model := NewModel(config, apiClient)
	model.ready = true
	model.currentScreen = ScreenResults

	view := model.View()

	expectedStrings := []string{
		"Results",
		"WPM",
		"Accuracy",
		"Time",
		"Press Tab/Enter/Space",
	}

	for _, expected := range expectedStrings {
		if !strings.Contains(view, expected) {
			t.Errorf("Expected '%s' in results view, got:\n%s", expected, view)
		}
	}
}

func TestRenderSettings(t *testing.T) {
	config := models.DefaultConfig()
	apiClient := services.NewAPIClient("https://test-api.com", 5*time.Second)
	model := NewModel(config, apiClient)
	model.ready = true
	model.currentScreen = ScreenSettings

	view := model.View()

	expectedStrings := []string{
		"Settings",
		"API URL",
		"Theme",
		"Language",
		"Press Esc to close",
	}

	for _, expected := range expectedStrings {
		if !strings.Contains(view, expected) {
			t.Errorf("Expected '%s' in settings view, got:\n%s", expected, view)
		}
	}

	// Check config values are displayed
	if !strings.Contains(view, config.API.BaseURL) {
		t.Errorf("Expected API URL '%s' in settings view", config.API.BaseURL)
	}
	if !strings.Contains(view, config.UI.Theme) {
		t.Errorf("Expected theme '%s' in settings view", config.UI.Theme)
	}
}

func TestRenderHelp(t *testing.T) {
	config := models.DefaultConfig()
	apiClient := services.NewAPIClient("https://test-api.com", 5*time.Second)
	model := NewModel(config, apiClient)
	model.ready = true
	model.currentScreen = ScreenHelp

	view := model.View()

	expectedStrings := []string{
		"Keyboard Shortcuts",
		"Global:",
		"q, Ctrl+C",
		"Quit application",
		"?",
		"Toggle this help screen",
		"Typing Screen:",
		"Tab",
		"Results Screen:",
		"Settings:",
		"Error Screen:",
	}

	for _, expected := range expectedStrings {
		if !strings.Contains(view, expected) {
			t.Errorf("Expected '%s' in help view, got:\n%s", expected, view)
		}
	}
}

func TestRenderError_WithError(t *testing.T) {
	config := models.DefaultConfig()
	apiClient := services.NewAPIClient("https://test-api.com", 5*time.Second)
	model := NewModel(config, apiClient)
	model.ready = true
	model.currentScreen = ScreenError
	model.err = errors.New("API connection failed")

	view := model.View()

	expectedStrings := []string{
		"Error",
		"API connection failed",
		"Press 'r' to retry",
		"Press 's' for settings",
	}

	for _, expected := range expectedStrings {
		if !strings.Contains(view, expected) {
			t.Errorf("Expected '%s' in error view, got:\n%s", expected, view)
		}
	}
}

func TestRenderError_NoError(t *testing.T) {
	config := models.DefaultConfig()
	apiClient := services.NewAPIClient("https://test-api.com", 5*time.Second)
	model := NewModel(config, apiClient)
	model.ready = true
	model.currentScreen = ScreenError
	model.err = nil

	view := model.View()

	if !strings.Contains(view, "unknown error") {
		t.Errorf("Expected 'unknown error' when err is nil, got:\n%s", view)
	}
}

func TestRenderHeader(t *testing.T) {
	config := models.DefaultConfig()
	apiClient := services.NewAPIClient("https://test-api.com", 5*time.Second)
	model := NewModel(config, apiClient)

	header := model.renderHeader()

	if !strings.Contains(header, "Beaver CLI") {
		t.Errorf("Expected 'Beaver CLI' in header, got: %s", header)
	}
	if !strings.Contains(header, "Developer Typing Practice") {
		t.Errorf("Expected 'Developer Typing Practice' in header, got: %s", header)
	}
}

func TestRenderFooter(t *testing.T) {
	config := models.DefaultConfig()
	apiClient := services.NewAPIClient("https://test-api.com", 5*time.Second)
	model := NewModel(config, apiClient)

	footer := model.renderFooter()

	expectedStrings := []string{
		"Press ? for help",
		"q to quit",
	}

	for _, expected := range expectedStrings {
		if !strings.Contains(footer, expected) {
			t.Errorf("Expected '%s' in footer, got: %s", expected, footer)
		}
	}
}

func TestView_AllScreens(t *testing.T) {
	config := models.DefaultConfig()
	apiClient := services.NewAPIClient("https://test-api.com", 5*time.Second)
	model := NewModel(config, apiClient)
	model.ready = true

	// Set up a sample algorithm for typing screen
	model.algorithm = &models.CodeDocument{
		ID:       uuid.New(),
		Title:    "Test Algorithm",
		Code:     "func test() {}",
		Language: "Go",
	}

	screens := []struct {
		screen   Screen
		expected string
	}{
		{ScreenLoading, "Loading algorithm"},
		{ScreenTyping, "Start typing"},
		{ScreenResults, "Results"},
		{ScreenSettings, "Settings"},
		{ScreenHelp, "Keyboard Shortcuts"},
		{ScreenError, "Error"},
	}

	for _, tc := range screens {
		t.Run(tc.expected, func(t *testing.T) {
			model.currentScreen = tc.screen
			view := model.View()

			if !strings.Contains(view, tc.expected) {
				t.Errorf("Expected '%s' in view for screen %v, got:\n%s", tc.expected, tc.screen, view)
			}

			// All screens should have header and footer
			if !strings.Contains(view, "Beaver CLI") {
				t.Errorf("Expected header in view for screen %v", tc.screen)
			}
			if !strings.Contains(view, "Press ? for help") {
				t.Errorf("Expected footer in view for screen %v", tc.screen)
			}
		})
	}
}

func TestView_ScreenResizing(t *testing.T) {
	config := models.DefaultConfig()
	apiClient := services.NewAPIClient("https://test-api.com", 5*time.Second)
	model := NewModel(config, apiClient)

	// Test different window sizes
	sizes := []struct {
		width  int
		height int
	}{
		{80, 24},
		{100, 50},
		{120, 40},
		{200, 60},
	}

	for _, size := range sizes {
		t.Run("", func(t *testing.T) {
			msg := tea.WindowSizeMsg{Width: size.width, Height: size.height}
			newModel, _ := model.Update(msg)
			m := newModel.(Model)

			if m.windowWidth != size.width {
				t.Errorf("Expected windowWidth %d, got %d", size.width, m.windowWidth)
			}
			if m.windowHeight != size.height {
				t.Errorf("Expected windowHeight %d, got %d", size.height, m.windowHeight)
			}

			// View should render without errors
			view := m.View()
			if len(view) == 0 {
				t.Error("View should not be empty")
			}
		})
	}
}
