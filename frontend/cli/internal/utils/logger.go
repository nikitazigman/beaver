package utils

import (
	"io"
	"os"
	"path/filepath"
	"time"

	"github.com/rs/zerolog"
	"github.com/rs/zerolog/log"
)

// LogLevel represents the logging level
type LogLevel string

const (
	LogLevelDebug LogLevel = "debug"
	LogLevelInfo  LogLevel = "info"
	LogLevelWarn  LogLevel = "warn"
	LogLevelError LogLevel = "error"
)

// LoggerConfig holds logger configuration
type LoggerConfig struct {
	Level      LogLevel
	EnableFile bool
	FilePath   string
	Pretty     bool // Pretty console output for development
}

// InitLogger initializes the global logger with the provided configuration
func InitLogger(config LoggerConfig) error {
	// Set global log level
	level := parseLogLevel(config.Level)
	zerolog.SetGlobalLevel(level)

	// Configure time format
	zerolog.TimeFieldFormat = time.RFC3339

	var writers []io.Writer

	// Console output (pretty if enabled)
	if config.Pretty {
		consoleWriter := zerolog.ConsoleWriter{
			Out:        os.Stderr,
			TimeFormat: time.RFC3339,
		}
		writers = append(writers, consoleWriter)
	} else {
		writers = append(writers, os.Stderr)
	}

	// File output (if enabled)
	if config.EnableFile && config.FilePath != "" {
		// Ensure log directory exists
		logDir := filepath.Dir(config.FilePath)
		if err := os.MkdirAll(logDir, 0755); err != nil {
			return err
		}

		// Open log file
		file, err := os.OpenFile(
			config.FilePath,
			os.O_CREATE|os.O_APPEND|os.O_WRONLY,
			0644,
		)
		if err != nil {
			return err
		}

		writers = append(writers, file)
	}

	// Create multi-writer
	multi := io.MultiWriter(writers...)

	// Set global logger
	log.Logger = zerolog.New(multi).With().
		Timestamp().
		Caller().
		Logger()

	return nil
}

// parseLogLevel converts string to zerolog level
func parseLogLevel(level LogLevel) zerolog.Level {
	switch level {
	case LogLevelDebug:
		return zerolog.DebugLevel
	case LogLevelInfo:
		return zerolog.InfoLevel
	case LogLevelWarn:
		return zerolog.WarnLevel
	case LogLevelError:
		return zerolog.ErrorLevel
	default:
		return zerolog.InfoLevel
	}
}

// GetDefaultLogPath returns the default log file path
func GetDefaultLogPath() string {
	homeDir, err := os.UserHomeDir()
	if err != nil {
		return "./beaver.log"
	}
	return filepath.Join(homeDir, ".config", "beaver", "beaver.log")
}

// GetLogLevelFromEnv reads log level from environment variable
func GetLogLevelFromEnv() LogLevel {
	level := os.Getenv("BEAVER_LOG_LEVEL")
	switch level {
	case "debug":
		return LogLevelDebug
	case "info":
		return LogLevelInfo
	case "warn":
		return LogLevelWarn
	case "error":
		return LogLevelError
	default:
		return LogLevelInfo
	}
}
