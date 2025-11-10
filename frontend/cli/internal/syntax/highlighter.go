package syntax

import (
	"bytes"
	"strings"

	"github.com/alecthomas/chroma/v2"
	"github.com/alecthomas/chroma/v2/formatters"
	"github.com/alecthomas/chroma/v2/lexers"
	"github.com/alecthomas/chroma/v2/styles"
)

// Highlighter provides syntax highlighting for code
type Highlighter struct {
	theme string
	style *chroma.Style
}

// NewHighlighter creates a new syntax highlighter with the given theme
func NewHighlighter(theme string) *Highlighter {
	// Map theme names to Chroma styles
	var styleName string
	switch theme {
	case "dark":
		styleName = "monokai"
	case "light":
		styleName = "github"
	default:
		styleName = "monokai"
	}

	style := styles.Get(styleName)
	if style == nil {
		style = styles.Fallback
	}

	return &Highlighter{
		theme: theme,
		style: style,
	}
}

// Highlight applies syntax highlighting to code and returns ANSI-colored string
func (h *Highlighter) Highlight(code, language string) (string, error) {
	// Get lexer for the language
	lexer := h.getLexer(language)
	if lexer == nil {
		// Fallback to plain text
		return code, nil
	}

	// Create terminal 256 formatter
	formatter := formatters.Get("terminal256")
	if formatter == nil {
		formatter = formatters.Fallback
	}

	// Tokenize the code
	iterator, err := lexer.Tokenise(nil, code)
	if err != nil {
		return code, err
	}

	// Format to string with ANSI codes
	var buf bytes.Buffer
	err = formatter.Format(&buf, h.style, iterator)
	if err != nil {
		return code, err
	}

	return buf.String(), nil
}

// getLexer maps language names to Chroma lexers
func (h *Highlighter) getLexer(language string) chroma.Lexer {
	// Normalize language name
	lang := strings.ToLower(strings.TrimSpace(language))

	// Map common language names to Chroma lexers
	var lexer chroma.Lexer

	switch lang {
	case "go", "golang":
		lexer = lexers.Get("go")
	case "python", "py":
		lexer = lexers.Get("python")
	case "javascript", "js":
		lexer = lexers.Get("javascript")
	case "typescript", "ts":
		lexer = lexers.Get("typescript")
	case "java":
		lexer = lexers.Get("java")
	case "c":
		lexer = lexers.Get("c")
	case "c++", "cpp":
		lexer = lexers.Get("cpp")
	case "c#", "csharp":
		lexer = lexers.Get("csharp")
	case "rust", "rs":
		lexer = lexers.Get("rust")
	case "ruby", "rb":
		lexer = lexers.Get("ruby")
	case "php":
		lexer = lexers.Get("php")
	case "swift":
		lexer = lexers.Get("swift")
	case "kotlin", "kt":
		lexer = lexers.Get("kotlin")
	case "scala":
		lexer = lexers.Get("scala")
	case "r":
		lexer = lexers.Get("r")
	case "matlab":
		lexer = lexers.Get("matlab")
	case "sql":
		lexer = lexers.Get("sql")
	case "shell", "bash", "sh":
		lexer = lexers.Get("bash")
	case "html":
		lexer = lexers.Get("html")
	case "css":
		lexer = lexers.Get("css")
	case "json":
		lexer = lexers.Get("json")
	case "yaml", "yml":
		lexer = lexers.Get("yaml")
	case "xml":
		lexer = lexers.Get("xml")
	case "markdown", "md":
		lexer = lexers.Get("markdown")
	default:
		// Try to get lexer by name
		lexer = lexers.Get(lang)
	}

	// If still no lexer, try to analyze the code
	if lexer == nil {
		lexer = lexers.Analyse(language)
	}

	return lexer
}

// SetTheme changes the theme and updates the style
func (h *Highlighter) SetTheme(theme string) {
	h.theme = theme

	var styleName string
	switch theme {
	case "dark":
		styleName = "monokai"
	case "light":
		styleName = "github"
	default:
		styleName = "monokai"
	}

	style := styles.Get(styleName)
	if style == nil {
		style = styles.Fallback
	}

	h.style = style
}

// GetTheme returns the current theme name
func (h *Highlighter) GetTheme() string {
	return h.theme
}
