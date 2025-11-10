# Beaver CLI

Beaver is a MonkeyType-inspired typing practice application for developers. Improve your typing speed while practicing well-known algorithms and data structures.

## Features

- Type real algorithm implementations with syntax highlighting
- Character-by-character validation with backspace support
- Real-time statistics tracking (CPM, accuracy, errors)
- Filter algorithms by language and tags
- Background prefetching for smooth experience
- Dark and light themes

## Installation

```bash
# Build from source
make build

# Install to $GOPATH/bin
make install
```

## Usage

```bash
# Start the CLI
beaver

# Show version
beaver --version

# Use custom config file
beaver --config /path/to/config.yaml
```

## Keyboard Shortcuts

- `?` - Show help
- `s` - Open settings
- `Tab` - Next algorithm / Insert spaces
- `Backspace` - Delete and correct
- `q` - Quit

## Configuration

Configuration is stored at `~/.config/beaver/config.yaml`. See documentation for full details.

## Development

```bash
# Run tests
make test

# Run locally
make run

# Build binary
make build
```

## Documentation

See the `docs/` directory for comprehensive documentation:
- [Overview](OVERVIEW.md)
- [Features](FEATURES.md)
- [User Flows](USER_FLOWS.md)
- [Keyboard Shortcuts](SHORTCUTS.md)
- [Tech Stack](TECH_STACK.md)
- [Architecture](ARCHITECTURE.md)
- [Roadmap](ROADMAP.md)

## License

MIT License

## Contributing

Contributions welcome! Please read CONTRIBUTING.md for guidelines.
