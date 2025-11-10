package config

import (
	"fmt"
	"os"
	"path/filepath"

	"github.com/beaver-app/beaver-cli/internal/models"
	"github.com/spf13/viper"
)

const (
	// ConfigFileName is the name of the config file
	ConfigFileName = "config"
	// ConfigFileType is the type of the config file
	ConfigFileType = "yaml"
	// ConfigDirName is the directory name for config
	ConfigDirName = "beaver"
)

// LoadConfig loads configuration from file and environment variables
// Priority: environment variables > config file > defaults
func LoadConfig(configPath string) (*models.Config, error) {
	// Start with defaults
	config := models.DefaultConfig()

	// Setup Viper
	v := viper.New()
	v.SetConfigType(ConfigFileType)

	// Set config file path
	if configPath != "" {
		// Use provided config path
		v.SetConfigFile(configPath)
	} else {
		// Use default config location
		configDir, err := GetConfigDir()
		if err != nil {
			return nil, fmt.Errorf("failed to get config directory: %w", err)
		}
		v.AddConfigPath(configDir)
		v.SetConfigName(ConfigFileName)
	}

	// Set environment variable prefix
	v.SetEnvPrefix("BEAVER")
	v.AutomaticEnv()

	// Map environment variables to config keys
	v.BindEnv("api.base_url", "BEAVER_API_BASE_URL")
	v.BindEnv("api.timeout", "BEAVER_API_TIMEOUT")
	v.BindEnv("filters.language", "BEAVER_FILTERS_LANGUAGE")
	v.BindEnv("filters.tags", "BEAVER_FILTERS_TAGS")
	v.BindEnv("ui.theme", "BEAVER_UI_THEME")
	v.BindEnv("ui.tab_width", "BEAVER_UI_TAB_WIDTH")
	v.BindEnv("prefetch.queue_size", "BEAVER_PREFETCH_QUEUE_SIZE")

	// Read config file (it's okay if it doesn't exist)
	if err := v.ReadInConfig(); err != nil {
		// Check if it's a "file not found" error
		if _, ok := err.(viper.ConfigFileNotFoundError); !ok {
			// Config file found but has parse/read error
			// Check if it's just that the file doesn't exist at explicit path
			if configPath != "" && os.IsNotExist(err) {
				// File doesn't exist, use defaults - this is okay
			} else {
				// Some other error occurred (e.g., parse error)
				return nil, fmt.Errorf("error reading config file: %w", err)
			}
		}
		// Config file not found - use defaults
	}

	// Unmarshal into config struct
	if err := v.Unmarshal(config); err != nil {
		return nil, fmt.Errorf("error unmarshaling config: %w", err)
	}

	// Validate config
	if err := config.Validate(); err != nil {
		return nil, fmt.Errorf("invalid configuration: %w", err)
	}

	return config, nil
}

// GetConfigDir returns the configuration directory path
func GetConfigDir() (string, error) {
	homeDir, err := os.UserHomeDir()
	if err != nil {
		return "", err
	}
	return filepath.Join(homeDir, ".config", ConfigDirName), nil
}

// GetConfigPath returns the full path to the config file
func GetConfigPath() (string, error) {
	configDir, err := GetConfigDir()
	if err != nil {
		return "", err
	}
	return filepath.Join(configDir, ConfigFileName+"."+ConfigFileType), nil
}

// ConfigExists checks if a config file exists
func ConfigExists() (bool, error) {
	configPath, err := GetConfigPath()
	if err != nil {
		return false, err
	}

	_, err = os.Stat(configPath)
	if err == nil {
		return true, nil
	}
	if os.IsNotExist(err) {
		return false, nil
	}
	return false, err
}
