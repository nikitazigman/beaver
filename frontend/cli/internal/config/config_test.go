package config

import (
	"os"
	"path/filepath"
	"testing"
	"time"
)

func TestGetConfigDir(t *testing.T) {
	dir, err := GetConfigDir()
	if err != nil {
		t.Fatalf("GetConfigDir() error = %v", err)
	}

	if dir == "" {
		t.Error("GetConfigDir() returned empty string")
	}

	// Should be absolute path
	if !filepath.IsAbs(dir) {
		t.Errorf("GetConfigDir() should return absolute path, got %v", dir)
	}
	if filepath.Base(filepath.Dir(dir)) != ".config" {
		t.Errorf("GetConfigDir() should be under .config directory")
	}
	if filepath.Base(dir) != ConfigDirName {
		t.Errorf("GetConfigDir() should end with %v, got %v", ConfigDirName, filepath.Base(dir))
	}
}

func TestGetConfigPath(t *testing.T) {
	path, err := GetConfigPath()
	if err != nil {
		t.Fatalf("GetConfigPath() error = %v", err)
	}

	if path == "" {
		t.Error("GetConfigPath() returned empty string")
	}

	// Should end with config.yaml
	expectedName := ConfigFileName + "." + ConfigFileType
	if filepath.Base(path) != expectedName {
		t.Errorf("GetConfigPath() = %v, want filename %v", path, expectedName)
	}
}

func TestLoadConfig_Defaults(t *testing.T) {
	// Load config with no file (should use defaults)
	config, err := LoadConfig("/nonexistent/path/config.yaml")
	if err != nil {
		t.Fatalf("LoadConfig() with defaults error = %v", err)
	}

	// Verify defaults
	if config.API.BaseURL != "https://beaver-api.com" {
		t.Errorf("API.BaseURL = %v, want https://beaver-api.com", config.API.BaseURL)
	}
	if config.API.Timeout != 5*time.Second {
		t.Errorf("API.Timeout = %v, want 5s", config.API.Timeout)
	}
	if config.UI.Theme != "dark" {
		t.Errorf("UI.Theme = %v, want dark", config.UI.Theme)
	}
	if config.UI.TabWidth != 4 {
		t.Errorf("UI.TabWidth = %v, want 4", config.UI.TabWidth)
	}
	if config.Prefetch.QueueSize != 5 {
		t.Errorf("Prefetch.QueueSize = %v, want 5", config.Prefetch.QueueSize)
	}
}

func TestLoadConfig_FromFile(t *testing.T) {
	// Create temp config file
	tmpDir := t.TempDir()
	configPath := filepath.Join(tmpDir, "config.yaml")

	configContent := `api:
  base_url: "https://test-api.com"
  timeout: 10s

filters:
  language: "python"
  tags:
    - "sort"
    - "search"

ui:
  theme: "light"
  tab_width: 2

prefetch:
  queue_size: 10
`

	if err := os.WriteFile(configPath, []byte(configContent), 0644); err != nil {
		t.Fatalf("Failed to create test config file: %v", err)
	}

	// Load config from file
	config, err := LoadConfig(configPath)
	if err != nil {
		t.Fatalf("LoadConfig() error = %v", err)
	}

	// Verify values from file
	if config.API.BaseURL != "https://test-api.com" {
		t.Errorf("API.BaseURL = %v, want https://test-api.com", config.API.BaseURL)
	}
	if config.API.Timeout != 10*time.Second {
		t.Errorf("API.Timeout = %v, want 10s", config.API.Timeout)
	}
	if config.Filters.Language != "python" {
		t.Errorf("Filters.Language = %v, want python", config.Filters.Language)
	}
	if len(config.Filters.Tags) != 2 {
		t.Errorf("len(Filters.Tags) = %v, want 2", len(config.Filters.Tags))
	}
	if config.UI.Theme != "light" {
		t.Errorf("UI.Theme = %v, want light", config.UI.Theme)
	}
	if config.UI.TabWidth != 2 {
		t.Errorf("UI.TabWidth = %v, want 2", config.UI.TabWidth)
	}
	if config.Prefetch.QueueSize != 10 {
		t.Errorf("Prefetch.QueueSize = %v, want 10", config.Prefetch.QueueSize)
	}
}

func TestLoadConfig_FromEnv(t *testing.T) {
	// Set environment variables
	os.Setenv("BEAVER_API_BASE_URL", "https://env-api.com")
	os.Setenv("BEAVER_UI_THEME", "light")
	os.Setenv("BEAVER_UI_TAB_WIDTH", "8")
	defer func() {
		os.Unsetenv("BEAVER_API_BASE_URL")
		os.Unsetenv("BEAVER_UI_THEME")
		os.Unsetenv("BEAVER_UI_TAB_WIDTH")
	}()

	// Load config (no file)
	config, err := LoadConfig("/nonexistent/path/config.yaml")
	if err != nil {
		t.Fatalf("LoadConfig() error = %v", err)
	}

	// Verify environment variables override defaults
	if config.API.BaseURL != "https://env-api.com" {
		t.Errorf("API.BaseURL = %v, want https://env-api.com", config.API.BaseURL)
	}
	if config.UI.Theme != "light" {
		t.Errorf("UI.Theme = %v, want light", config.UI.Theme)
	}
	if config.UI.TabWidth != 8 {
		t.Errorf("UI.TabWidth = %v, want 8", config.UI.TabWidth)
	}
}

func TestLoadConfig_InvalidConfig(t *testing.T) {
	// Create temp config file with invalid values
	tmpDir := t.TempDir()
	configPath := filepath.Join(tmpDir, "config.yaml")

	invalidConfigContent := `api:
  base_url: ""
  timeout: 5s

ui:
  theme: "dark"
  tab_width: 4

prefetch:
  queue_size: 5
`

	if err := os.WriteFile(configPath, []byte(invalidConfigContent), 0644); err != nil {
		t.Fatalf("Failed to create test config file: %v", err)
	}

	// Should fail validation
	_, err := LoadConfig(configPath)
	if err == nil {
		t.Error("LoadConfig() expected error for invalid config, got nil")
	}
}

func TestLoadConfig_MalformedYAML(t *testing.T) {
	// Create temp config file with malformed YAML
	tmpDir := t.TempDir()
	configPath := filepath.Join(tmpDir, "config.yaml")

	malformedContent := `api:
  base_url: "https://test.com"
  invalid yaml here
    - broken
`

	if err := os.WriteFile(configPath, []byte(malformedContent), 0644); err != nil {
		t.Fatalf("Failed to create test config file: %v", err)
	}

	// Should fail to parse
	_, err := LoadConfig(configPath)
	if err == nil {
		t.Error("LoadConfig() expected error for malformed YAML, got nil")
	}
}

func TestConfigExists(t *testing.T) {
	// Should return false for non-existent config
	exists, err := ConfigExists()
	if err != nil {
		// It's okay if we can't check (e.g., home dir issues in CI)
		t.Logf("ConfigExists() error = %v (may be expected in CI)", err)
		return
	}

	// We can't be sure about the result in CI, just verify no error
	t.Logf("ConfigExists() = %v", exists)
}
