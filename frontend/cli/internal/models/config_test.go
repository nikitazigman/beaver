package models

import (
	"testing"
	"time"
)

func TestDefaultConfig(t *testing.T) {
	config := DefaultConfig()

	// Test API defaults
	if config.API.BaseURL != "https://beaver-api.com" {
		t.Errorf("API.BaseURL = %v, want https://beaver-api.com", config.API.BaseURL)
	}
	if config.API.Timeout != 5*time.Second {
		t.Errorf("API.Timeout = %v, want 5s", config.API.Timeout)
	}

	// Test Filters defaults
	if config.Filters.Language != "" {
		t.Errorf("Filters.Language = %v, want empty string", config.Filters.Language)
	}
	if len(config.Filters.Tags) != 0 {
		t.Errorf("Filters.Tags = %v, want empty slice", config.Filters.Tags)
	}

	// Test UI defaults
	if config.UI.Theme != "dark" {
		t.Errorf("UI.Theme = %v, want dark", config.UI.Theme)
	}
	if config.UI.TabWidth != 4 {
		t.Errorf("UI.TabWidth = %v, want 4", config.UI.TabWidth)
	}

	// Test Prefetch defaults
	if config.Prefetch.QueueSize != 5 {
		t.Errorf("Prefetch.QueueSize = %v, want 5", config.Prefetch.QueueSize)
	}
}

func TestConfigValidate(t *testing.T) {
	tests := []struct {
		name    string
		config  *Config
		wantErr bool
		errMsg  string
	}{
		{
			name:    "valid default config",
			config:  DefaultConfig(),
			wantErr: false,
		},
		{
			name: "empty base URL",
			config: &Config{
				API: APIConfig{
					BaseURL: "",
					Timeout: 5 * time.Second,
				},
				UI: UIConfig{
					Theme:    "dark",
					TabWidth: 4,
				},
				Prefetch: PrefetchConfig{
					QueueSize: 5,
				},
			},
			wantErr: true,
			errMsg:  "api.base_url",
		},
		{
			name: "timeout too short",
			config: &Config{
				API: APIConfig{
					BaseURL: "https://beaver-api.com",
					Timeout: 500 * time.Millisecond,
				},
				UI: UIConfig{
					Theme:    "dark",
					TabWidth: 4,
				},
				Prefetch: PrefetchConfig{
					QueueSize: 5,
				},
			},
			wantErr: true,
			errMsg:  "api.timeout",
		},
		{
			name: "timeout too long",
			config: &Config{
				API: APIConfig{
					BaseURL: "https://beaver-api.com",
					Timeout: 31 * time.Second,
				},
				UI: UIConfig{
					Theme:    "dark",
					TabWidth: 4,
				},
				Prefetch: PrefetchConfig{
					QueueSize: 5,
				},
			},
			wantErr: true,
			errMsg:  "api.timeout",
		},
		{
			name: "invalid theme",
			config: &Config{
				API: APIConfig{
					BaseURL: "https://beaver-api.com",
					Timeout: 5 * time.Second,
				},
				UI: UIConfig{
					Theme:    "blue",
					TabWidth: 4,
				},
				Prefetch: PrefetchConfig{
					QueueSize: 5,
				},
			},
			wantErr: true,
			errMsg:  "ui.theme",
		},
		{
			name: "tab width too small",
			config: &Config{
				API: APIConfig{
					BaseURL: "https://beaver-api.com",
					Timeout: 5 * time.Second,
				},
				UI: UIConfig{
					Theme:    "dark",
					TabWidth: 0,
				},
				Prefetch: PrefetchConfig{
					QueueSize: 5,
				},
			},
			wantErr: true,
			errMsg:  "ui.tab_width",
		},
		{
			name: "tab width too large",
			config: &Config{
				API: APIConfig{
					BaseURL: "https://beaver-api.com",
					Timeout: 5 * time.Second,
				},
				UI: UIConfig{
					Theme:    "dark",
					TabWidth: 9,
				},
				Prefetch: PrefetchConfig{
					QueueSize: 5,
				},
			},
			wantErr: true,
			errMsg:  "ui.tab_width",
		},
		{
			name: "queue size too small",
			config: &Config{
				API: APIConfig{
					BaseURL: "https://beaver-api.com",
					Timeout: 5 * time.Second,
				},
				UI: UIConfig{
					Theme:    "dark",
					TabWidth: 4,
				},
				Prefetch: PrefetchConfig{
					QueueSize: 0,
				},
			},
			wantErr: true,
			errMsg:  "prefetch.queue_size",
		},
		{
			name: "queue size too large",
			config: &Config{
				API: APIConfig{
					BaseURL: "https://beaver-api.com",
					Timeout: 5 * time.Second,
				},
				UI: UIConfig{
					Theme:    "dark",
					TabWidth: 4,
				},
				Prefetch: PrefetchConfig{
					QueueSize: 21,
				},
			},
			wantErr: true,
			errMsg:  "prefetch.queue_size",
		},
		{
			name: "valid with light theme",
			config: &Config{
				API: APIConfig{
					BaseURL: "https://beaver-api.com",
					Timeout: 5 * time.Second,
				},
				Filters: FilterConfig{
					Language: "python",
					Tags:     []string{"sort", "search"},
				},
				UI: UIConfig{
					Theme:    "light",
					TabWidth: 2,
				},
				Prefetch: PrefetchConfig{
					QueueSize: 10,
				},
			},
			wantErr: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			err := tt.config.Validate()
			if (err != nil) != tt.wantErr {
				t.Errorf("Config.Validate() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if tt.wantErr && err != nil {
				configErr, ok := err.(*ConfigError)
				if !ok {
					t.Errorf("expected ConfigError, got %T", err)
					return
				}
				if configErr.Field != tt.errMsg {
					t.Errorf("ConfigError.Field = %v, want %v", configErr.Field, tt.errMsg)
				}
			}
		})
	}
}

func TestConfigError(t *testing.T) {
	err := &ConfigError{
		Field:   "test.field",
		Message: "test message",
	}

	expected := "config error in test.field: test message"
	if err.Error() != expected {
		t.Errorf("ConfigError.Error() = %v, want %v", err.Error(), expected)
	}
}
