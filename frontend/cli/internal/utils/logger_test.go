package utils

import (
	"os"
	"path/filepath"
	"testing"

	"github.com/rs/zerolog"
)

func TestParseLogLevel(t *testing.T) {
	tests := []struct {
		name     string
		level    LogLevel
		expected zerolog.Level
	}{
		{"debug level", LogLevelDebug, zerolog.DebugLevel},
		{"info level", LogLevelInfo, zerolog.InfoLevel},
		{"warn level", LogLevelWarn, zerolog.WarnLevel},
		{"error level", LogLevelError, zerolog.ErrorLevel},
		{"invalid defaults to info", LogLevel("invalid"), zerolog.InfoLevel},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := parseLogLevel(tt.level)
			if result != tt.expected {
				t.Errorf("parseLogLevel(%v) = %v, want %v", tt.level, result, tt.expected)
			}
		})
	}
}

func TestGetLogLevelFromEnv(t *testing.T) {
	tests := []struct {
		name     string
		envValue string
		expected LogLevel
	}{
		{"debug from env", "debug", LogLevelDebug},
		{"info from env", "info", LogLevelInfo},
		{"warn from env", "warn", LogLevelWarn},
		{"error from env", "error", LogLevelError},
		{"invalid defaults to info", "invalid", LogLevelInfo},
		{"empty defaults to info", "", LogLevelInfo},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Set env var
			if tt.envValue != "" {
				os.Setenv("BEAVER_LOG_LEVEL", tt.envValue)
			} else {
				os.Unsetenv("BEAVER_LOG_LEVEL")
			}
			defer os.Unsetenv("BEAVER_LOG_LEVEL")

			result := GetLogLevelFromEnv()
			if result != tt.expected {
				t.Errorf("GetLogLevelFromEnv() = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestGetDefaultLogPath(t *testing.T) {
	path := GetDefaultLogPath()

	if path == "" {
		t.Error("GetDefaultLogPath() returned empty string")
	}

	// Should end with .config/beaver/beaver.log or be ./beaver.log (fallback)
	if path != "./beaver.log" {
		expected := filepath.Join(".config", "beaver", "beaver.log")
		if !filepath.IsAbs(path) {
			t.Errorf("GetDefaultLogPath() should return absolute path, got %v", path)
		}
		if filepath.Base(path) != "beaver.log" {
			t.Errorf("GetDefaultLogPath() should end with beaver.log, got %v", path)
		}
		if !filepath.IsAbs(path) && path != expected {
			t.Errorf("GetDefaultLogPath() = %v, want to contain %v", path, expected)
		}
	}
}

func TestInitLogger(t *testing.T) {
	t.Run("console only", func(t *testing.T) {
		config := LoggerConfig{
			Level:      LogLevelInfo,
			EnableFile: false,
			Pretty:     false,
		}

		err := InitLogger(config)
		if err != nil {
			t.Errorf("InitLogger() error = %v, want nil", err)
		}
	})

	t.Run("with file output", func(t *testing.T) {
		tmpDir := t.TempDir()
		logPath := filepath.Join(tmpDir, "test.log")

		config := LoggerConfig{
			Level:      LogLevelDebug,
			EnableFile: true,
			FilePath:   logPath,
			Pretty:     false,
		}

		err := InitLogger(config)
		if err != nil {
			t.Errorf("InitLogger() error = %v, want nil", err)
		}

		// Check log file was created
		if _, err := os.Stat(logPath); os.IsNotExist(err) {
			t.Errorf("Log file was not created at %v", logPath)
		}
	})

	t.Run("pretty console", func(t *testing.T) {
		config := LoggerConfig{
			Level:      LogLevelWarn,
			EnableFile: false,
			Pretty:     true,
		}

		err := InitLogger(config)
		if err != nil {
			t.Errorf("InitLogger() error = %v, want nil", err)
		}
	})

	t.Run("creates log directory", func(t *testing.T) {
		tmpDir := t.TempDir()
		logPath := filepath.Join(tmpDir, "nested", "dir", "test.log")

		config := LoggerConfig{
			Level:      LogLevelInfo,
			EnableFile: true,
			FilePath:   logPath,
			Pretty:     false,
		}

		err := InitLogger(config)
		if err != nil {
			t.Errorf("InitLogger() error = %v, want nil", err)
		}

		// Check nested directories were created
		logDir := filepath.Dir(logPath)
		if _, err := os.Stat(logDir); os.IsNotExist(err) {
			t.Errorf("Log directory was not created at %v", logDir)
		}
	})
}
