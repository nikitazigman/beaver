package main

import (
	"fmt"
	"os"
	"time"

	tea "github.com/charmbracelet/bubbletea"
	"github.com/rs/zerolog/log"
	"github.com/spf13/cobra"

	"github.com/beaver-app/beaver-cli/internal/app"
	"github.com/beaver-app/beaver-cli/internal/config"
	"github.com/beaver-app/beaver-cli/internal/services"
	"github.com/beaver-app/beaver-cli/internal/utils"
)

var (
	version    = "1.0.0"
	configPath string
)

var rootCmd = &cobra.Command{
	Use:   "beaver",
	Short: "Beaver - Typing practice for developers",
	Long: `Beaver is a MonkeyType-inspired typing practice application for developers.
Improve your typing speed while practicing well-known algorithms and data structures.`,
	Version: version,
	Run: func(cmd *cobra.Command, args []string) {
		// Initialize logger
		logLevel := utils.GetLogLevelFromEnv()
		logConfig := utils.LoggerConfig{
			Level:      logLevel,
			Pretty:     true,
			EnableFile: true,
			FilePath:   utils.GetDefaultLogPath(),
		}
		if err := utils.InitLogger(logConfig); err != nil {
			fmt.Fprintf(os.Stderr, "Failed to initialize logger: %v\n", err)
			os.Exit(1)
		}

		log.Info().Str("version", version).Msg("Starting Beaver CLI")

		// Load configuration
		cfg, err := config.LoadConfig(configPath)
		if err != nil {
			log.Error().Err(err).Msg("Failed to load configuration")
			fmt.Fprintf(os.Stderr, "Configuration error: %v\n", err)
			fmt.Fprintln(os.Stderr, "Using default configuration...")
		}

		// Create API client
		timeout := time.Duration(cfg.API.Timeout) * time.Second
		apiClient := services.NewAPIClient(cfg.API.BaseURL, timeout)
		log.Info().Str("api_url", cfg.API.BaseURL).Msg("Initialized API client")

		// Create and start Bubble Tea app
		model := app.NewModel(cfg, apiClient)
		p := tea.NewProgram(model, tea.WithAltScreen())

		log.Info().Msg("Starting TUI application")
		if _, err := p.Run(); err != nil {
			log.Error().Err(err).Msg("Application error")
			fmt.Fprintf(os.Stderr, "Error running application: %v\n", err)
			os.Exit(1)
		}

		log.Info().Msg("Application exited normally")
	},
}

var configCmd = &cobra.Command{
	Use:   "config",
	Short: "Show current configuration",
	Long:  "Display the current Beaver configuration loaded from file and environment variables.",
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("Configuration command - Coming soon!")
		// TODO: Load and display config
	},
}

var versionCmd = &cobra.Command{
	Use:   "version",
	Short: "Print version information",
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Printf("Beaver CLI v%s\n", version)
	},
}

func init() {
	// Add persistent flags
	rootCmd.PersistentFlags().StringVar(&configPath, "config", "", "config file path (default is $HOME/.config/beaver/config.yaml)")

	// Add subcommands
	rootCmd.AddCommand(configCmd)
	rootCmd.AddCommand(versionCmd)
}

func main() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		os.Exit(1)
	}
}
