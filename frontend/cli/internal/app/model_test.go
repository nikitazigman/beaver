package app

import (
	"testing"
	"time"

	"github.com/beaver-app/beaver-cli/internal/models"
	"github.com/beaver-app/beaver-cli/internal/services"
)

func TestNewModel(t *testing.T) {
	config := models.DefaultConfig()
	apiClient := services.NewAPIClient("https://test-api.com", 5*time.Second)

	model := NewModel(config, apiClient)

	// Test initial state
	if model.currentScreen != ScreenLoading {
		t.Errorf("currentScreen = %v, want ScreenLoading", model.currentScreen)
	}

	if model.config == nil {
		t.Error("config is nil")
	}

	if model.apiClient == nil {
		t.Error("apiClient is nil")
	}

	if model.prefetchChan == nil {
		t.Error("prefetchChan is nil")
	}

	if model.prefetchStop == nil {
		t.Error("prefetchStop is nil")
	}

	if cap(model.prefetchChan) != config.Prefetch.QueueSize {
		t.Errorf("prefetchChan capacity = %v, want %v", cap(model.prefetchChan), config.Prefetch.QueueSize)
	}

	if model.typingEvents == nil {
		t.Error("typingEvents is nil")
	}

	if model.errorEvents == nil {
		t.Error("errorEvents is nil")
	}

	if model.corrections != 0 {
		t.Errorf("corrections = %v, want 0", model.corrections)
	}

	if model.isTyping {
		t.Error("isTyping should be false initially")
	}

	if model.ready {
		t.Error("ready should be false initially")
	}
}

func TestScreenConstants(t *testing.T) {
	// Test that screen constants are defined and distinct
	screens := []Screen{
		ScreenLoading,
		ScreenTyping,
		ScreenResults,
		ScreenSettings,
		ScreenHelp,
		ScreenError,
	}

	// Check they're all different
	seen := make(map[Screen]bool)
	for _, screen := range screens {
		if seen[screen] {
			t.Errorf("Duplicate screen value: %v", screen)
		}
		seen[screen] = true
	}

	// Check expected count
	if len(seen) != 6 {
		t.Errorf("Expected 6 distinct screens, got %v", len(seen))
	}
}

func TestModelInit(t *testing.T) {
	config := models.DefaultConfig()
	apiClient := services.NewAPIClient("https://test-api.com", 5*time.Second)
	model := NewModel(config, apiClient)

	cmd := model.Init()
	// For now, Init returns nil
	if cmd != nil {
		t.Logf("Init() returned cmd (expected for now)")
	}
}

func TestModelStateManagement(t *testing.T) {
	config := models.DefaultConfig()
	apiClient := services.NewAPIClient("https://test-api.com", 5*time.Second)
	model := NewModel(config, apiClient)

	// Test that we can change screens
	model.currentScreen = ScreenTyping
	if model.currentScreen != ScreenTyping {
		t.Error("Failed to update currentScreen")
	}

	// Test that we can store previous screen
	model.prevScreen = ScreenTyping
	model.currentScreen = ScreenSettings
	if model.prevScreen != ScreenTyping {
		t.Error("Failed to store prevScreen")
	}
}

func TestModelTypingState(t *testing.T) {
	config := models.DefaultConfig()
	apiClient := services.NewAPIClient("https://test-api.com", 5*time.Second)
	model := NewModel(config, apiClient)

	// Test initial typing state
	if model.isTyping {
		t.Error("isTyping should be false initially")
	}
	if model.cursorPos != 0 {
		t.Error("cursorPos should be 0 initially")
	}

	// Test that we can update typing state
	model.isTyping = true
	model.startTime = time.Now()
	model.cursorPos = 5

	if !model.isTyping {
		t.Error("Failed to update isTyping")
	}
	if model.cursorPos != 5 {
		t.Error("Failed to update cursorPos")
	}
	if model.startTime.IsZero() {
		t.Error("Failed to set startTime")
	}
}

func TestModelStatisticsTracking(t *testing.T) {
	config := models.DefaultConfig()
	apiClient := services.NewAPIClient("https://test-api.com", 5*time.Second)
	model := NewModel(config, apiClient)

	// Test adding typing events
	now := time.Now()
	model.typingEvents = append(model.typingEvents, now)
	if len(model.typingEvents) != 1 {
		t.Error("Failed to add typing event")
	}

	// Test adding error events
	model.errorEvents = append(model.errorEvents, now)
	if len(model.errorEvents) != 1 {
		t.Error("Failed to add error event")
	}

	// Test incrementing corrections
	model.corrections++
	if model.corrections != 1 {
		t.Error("Failed to increment corrections")
	}
}
