package models

import (
	"time"
)

// Config represents the complete application configuration
type Config struct {
	API      APIConfig      `mapstructure:"api" yaml:"api"`
	Filters  FilterConfig   `mapstructure:"filters" yaml:"filters"`
	UI       UIConfig       `mapstructure:"ui" yaml:"ui"`
	Prefetch PrefetchConfig `mapstructure:"prefetch" yaml:"prefetch"`
}

// APIConfig holds API-related configuration
type APIConfig struct {
	BaseURL string        `mapstructure:"base_url" yaml:"base_url" validate:"required,url"`
	Timeout time.Duration `mapstructure:"timeout" yaml:"timeout" validate:"required,min=1s,max=30s"`
}

// FilterConfig holds algorithm filtering configuration
type FilterConfig struct {
	Language string   `mapstructure:"language" yaml:"language"`
	Tags     []string `mapstructure:"tags" yaml:"tags"`
}

// UIConfig holds UI-related configuration
type UIConfig struct {
	Theme    string `mapstructure:"theme" yaml:"theme" validate:"required,oneof=dark light"`
	TabWidth int    `mapstructure:"tab_width" yaml:"tab_width" validate:"required,min=1,max=8"`
}

// PrefetchConfig holds prefetch service configuration
type PrefetchConfig struct {
	QueueSize int `mapstructure:"queue_size" yaml:"queue_size" validate:"required,min=1,max=20"`
}

// DefaultConfig returns a configuration with sensible defaults
func DefaultConfig() *Config {
	return &Config{
		API: APIConfig{
			BaseURL: "https://beaver-api.com",
			Timeout: 5 * time.Second,
		},
		Filters: FilterConfig{
			Language: "", // Any language
			Tags:     []string{},
		},
		UI: UIConfig{
			Theme:    "dark",
			TabWidth: 4,
		},
		Prefetch: PrefetchConfig{
			QueueSize: 5,
		},
	}
}

// Validate validates the configuration
func (c *Config) Validate() error {
	// API validation
	if c.API.BaseURL == "" {
		return &ConfigError{Field: "api.base_url", Message: "base URL is required"}
	}
	if c.API.Timeout < time.Second {
		return &ConfigError{Field: "api.timeout", Message: "timeout must be at least 1 second"}
	}
	if c.API.Timeout > 30*time.Second {
		return &ConfigError{Field: "api.timeout", Message: "timeout must be at most 30 seconds"}
	}

	// UI validation
	if c.UI.Theme != "dark" && c.UI.Theme != "light" {
		return &ConfigError{Field: "ui.theme", Message: "theme must be 'dark' or 'light'"}
	}
	if c.UI.TabWidth < 1 || c.UI.TabWidth > 8 {
		return &ConfigError{Field: "ui.tab_width", Message: "tab width must be between 1 and 8"}
	}

	// Prefetch validation
	if c.Prefetch.QueueSize < 1 {
		return &ConfigError{Field: "prefetch.queue_size", Message: "queue size must be at least 1"}
	}
	if c.Prefetch.QueueSize > 20 {
		return &ConfigError{Field: "prefetch.queue_size", Message: "queue size must be at most 20"}
	}

	return nil
}

// ConfigError represents a configuration validation error
type ConfigError struct {
	Field   string
	Message string
}

func (e *ConfigError) Error() string {
	return "config error in " + e.Field + ": " + e.Message
}
