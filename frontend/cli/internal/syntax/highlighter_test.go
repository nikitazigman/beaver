package syntax

import (
	"strings"
	"testing"
)

func TestNewHighlighter(t *testing.T) {
	tests := []struct {
		name  string
		theme string
	}{
		{"dark theme", "dark"},
		{"light theme", "light"},
		{"invalid theme defaults to dark", "invalid"},
		{"empty theme defaults to dark", ""},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			h := NewHighlighter(tt.theme)
			if h == nil {
				t.Fatal("NewHighlighter returned nil")
			}
			if h.theme != tt.theme {
				t.Errorf("theme = %v, want %v", h.theme, tt.theme)
			}
			if h.style == nil {
				t.Error("style is nil")
			}
		})
	}
}

func TestHighlight_Go(t *testing.T) {
	h := NewHighlighter("dark")
	code := `package main

import "fmt"

func main() {
	fmt.Println("Hello, World!")
}
`

	highlighted, err := h.Highlight(code, "go")
	if err != nil {
		t.Fatalf("Highlight failed: %v", err)
	}

	// Should contain ANSI escape codes
	if !strings.Contains(highlighted, "\x1b[") {
		t.Error("Expected ANSI escape codes in highlighted output")
	}

	// Should contain the original code content (check for individual words since ANSI codes might split them)
	if !strings.Contains(highlighted, "package") || !strings.Contains(highlighted, "main") {
		t.Errorf("Highlighted output missing original code content, got: %s", highlighted)
	}
}

func TestHighlight_Python(t *testing.T) {
	h := NewHighlighter("dark")
	code := `def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
`

	highlighted, err := h.Highlight(code, "python")
	if err != nil {
		t.Fatalf("Highlight failed: %v", err)
	}

	if !strings.Contains(highlighted, "\x1b[") {
		t.Error("Expected ANSI escape codes in highlighted output")
	}
	if !strings.Contains(highlighted, "binary_search") {
		t.Error("Highlighted output missing original code content")
	}
}

func TestHighlight_JavaScript(t *testing.T) {
	h := NewHighlighter("light")
	code := `function quicksort(arr) {
    if (arr.length <= 1) {
        return arr;
    }
    const pivot = arr[0];
    const left = arr.slice(1).filter(x => x < pivot);
    const right = arr.slice(1).filter(x => x >= pivot);
    return [...quicksort(left), pivot, ...quicksort(right)];
}
`

	highlighted, err := h.Highlight(code, "javascript")
	if err != nil {
		t.Fatalf("Highlight failed: %v", err)
	}

	if !strings.Contains(highlighted, "\x1b[") {
		t.Error("Expected ANSI escape codes in highlighted output")
	}
	if !strings.Contains(highlighted, "quicksort") {
		t.Error("Highlighted output missing original code content")
	}
}

func TestHighlight_UnknownLanguage(t *testing.T) {
	h := NewHighlighter("dark")
	code := `some plain text code
with no specific language
`

	highlighted, err := h.Highlight(code, "unknownlang")
	if err != nil {
		t.Fatalf("Highlight should not fail for unknown language: %v", err)
	}

	// Should return original code when language is unknown
	if highlighted != code {
		t.Error("Expected original code for unknown language")
	}
}

func TestHighlight_EmptyCode(t *testing.T) {
	h := NewHighlighter("dark")
	code := ""

	highlighted, err := h.Highlight(code, "go")
	if err != nil {
		t.Fatalf("Highlight failed: %v", err)
	}

	if highlighted != "" {
		t.Errorf("Expected empty string, got: %q", highlighted)
	}
}

func TestGetLexer(t *testing.T) {
	h := NewHighlighter("dark")

	tests := []struct {
		language string
		wantNil  bool
	}{
		{"go", false},
		{"golang", false},
		{"python", false},
		{"py", false},
		{"javascript", false},
		{"js", false},
		{"typescript", false},
		{"ts", false},
		{"java", false},
		{"c", false},
		{"c++", false},
		{"cpp", false},
		{"rust", false},
		{"ruby", false},
		{"php", false},
		{"shell", false},
		{"bash", false},
		{"unknownlanguage", true},
		{"", true},
	}

	for _, tt := range tests {
		t.Run(tt.language, func(t *testing.T) {
			lexer := h.getLexer(tt.language)
			if tt.wantNil && lexer != nil {
				t.Errorf("Expected nil lexer for %q, got %v", tt.language, lexer)
			}
			if !tt.wantNil && lexer == nil {
				t.Errorf("Expected non-nil lexer for %q", tt.language)
			}
		})
	}
}

func TestSetTheme(t *testing.T) {
	h := NewHighlighter("dark")

	if h.GetTheme() != "dark" {
		t.Errorf("Initial theme = %v, want dark", h.GetTheme())
	}

	h.SetTheme("light")
	if h.GetTheme() != "light" {
		t.Errorf("Theme after SetTheme = %v, want light", h.GetTheme())
	}

	// Verify style changed
	if h.style == nil {
		t.Error("Style is nil after SetTheme")
	}
}

func TestHighlight_DifferentThemes(t *testing.T) {
	code := `func hello() string {
    return "world"
}
`

	darkH := NewHighlighter("dark")
	lightH := NewHighlighter("light")

	darkOutput, err := darkH.Highlight(code, "go")
	if err != nil {
		t.Fatalf("Dark highlight failed: %v", err)
	}

	lightOutput, err := lightH.Highlight(code, "go")
	if err != nil {
		t.Fatalf("Light highlight failed: %v", err)
	}

	// Both should have ANSI codes
	if !strings.Contains(darkOutput, "\x1b[") {
		t.Error("Dark output missing ANSI codes")
	}
	if !strings.Contains(lightOutput, "\x1b[") {
		t.Error("Light output missing ANSI codes")
	}

	// They might be different (different color schemes)
	// But both should contain the original content
	if !strings.Contains(darkOutput, "hello") {
		t.Error("Dark output missing code content")
	}
	if !strings.Contains(lightOutput, "hello") {
		t.Error("Light output missing code content")
	}
}

func TestHighlight_MultipleLanguages(t *testing.T) {
	h := NewHighlighter("dark")

	languages := []struct {
		lang string
		code string
	}{
		{"go", "package main\nfunc main() {}"},
		{"python", "def main():\n    pass"},
		{"rust", "fn main() {\n    println!(\"hello\");\n}"},
		{"java", "public class Main {\n    public static void main(String[] args) {}\n}"},
		{"c", "int main() {\n    return 0;\n}"},
	}

	for _, lang := range languages {
		t.Run(lang.lang, func(t *testing.T) {
			highlighted, err := h.Highlight(lang.code, lang.lang)
			if err != nil {
				t.Fatalf("Highlight failed for %s: %v", lang.lang, err)
			}
			if highlighted == "" {
				t.Errorf("Empty output for %s", lang.lang)
			}
		})
	}
}

func TestHighlight_PreservesContent(t *testing.T) {
	h := NewHighlighter("dark")
	code := `func example() {
    // This is a comment
    x := 42
    fmt.Println(x)
}
`

	highlighted, err := h.Highlight(code, "go")
	if err != nil {
		t.Fatalf("Highlight failed: %v", err)
	}

	// Strip ANSI codes to check content preservation
	stripped := stripANSI(highlighted)

	// Should contain all major elements
	mustContain := []string{"func", "example", "comment", "42", "Println"}
	for _, s := range mustContain {
		if !strings.Contains(stripped, s) {
			t.Errorf("Highlighted output missing: %s", s)
		}
	}
}

// stripANSI removes ANSI escape codes from a string
func stripANSI(s string) string {
	// Simple ANSI code stripper for testing
	result := ""
	inEscape := false
	for _, ch := range s {
		if ch == '\x1b' {
			inEscape = true
			continue
		}
		if inEscape {
			if ch == 'm' {
				inEscape = false
			}
			continue
		}
		result += string(ch)
	}
	return result
}
