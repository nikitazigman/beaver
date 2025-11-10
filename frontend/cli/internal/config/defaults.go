package config

import (
	"fmt"
	"os"

	"gopkg.in/yaml.v3"

	"github.com/beaver-app/beaver-cli/internal/models"
)

// CreateDefaultConfig creates a default configuration file
func CreateDefaultConfig() error {
	// Get config path
	configPath, err := GetConfigPath()
	if err != nil {
		return fmt.Errorf("failed to get config path: %w", err)
	}

	// Check if config already exists
	if _, err := os.Stat(configPath); err == nil {
		// Config already exists, don't overwrite
		return nil
	}

	// Create config directory
	configDir, err := GetConfigDir()
	if err != nil {
		return fmt.Errorf("failed to get config directory: %w", err)
	}

	if err := os.MkdirAll(configDir, 0755); err != nil {
		return fmt.Errorf("failed to create config directory: %w", err)
	}

	// Get default config
	config := models.DefaultConfig()

	// Create file
	file, err := os.Create(configPath)
	if err != nil {
		return fmt.Errorf("failed to create config file: %w", err)
	}
	defer file.Close()

	// Write header comment
	header := `# Beaver CLI Configuration
# This file contains configuration for the Beaver typing practice CLI.
#
# You can also override these settings using environment variables:
#   BEAVER_API_BASE_URL
#   BEAVER_API_TIMEOUT
#   BEAVER_FILTERS_LANGUAGE
#   BEAVER_FILTERS_TAGS
#   BEAVER_UI_THEME
#   BEAVER_UI_TAB_WIDTH
#   BEAVER_PREFETCH_QUEUE_SIZE

`
	if _, err := file.WriteString(header); err != nil {
		return fmt.Errorf("failed to write config header: %w", err)
	}

	// Marshal config to YAML
	encoder := yaml.NewEncoder(file)
	encoder.SetIndent(2)
	if err := encoder.Encode(config); err != nil {
		return fmt.Errorf("failed to encode config: %w", err)
	}

	if err := encoder.Close(); err != nil {
		return fmt.Errorf("failed to close encoder: %w", err)
	}

	return nil
}

// EnsureConfigExists creates default config if it doesn't exist
func EnsureConfigExists() error {
	exists, err := ConfigExists()
	if err != nil {
		return err
	}

	if !exists {
		return CreateDefaultConfig()
	}

	return nil
}
