package main

import (
	"fmt"
	"os"

	"github.com/spf13/cobra"
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
		// This will be replaced with the actual Bubble Tea app
		fmt.Println("Beaver CLI v" + version)
		fmt.Println("Starting TUI application...")
		fmt.Println("\nPress Ctrl+C to quit")

		// TODO: Start Bubble Tea app here
		// For now, just show placeholder
		fmt.Println("\n[Bubble Tea app will start here]")
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
