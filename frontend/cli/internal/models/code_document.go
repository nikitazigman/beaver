package models

import (
	"strings"
	"time"

	"github.com/google/uuid"
)

// FlexibleTime is a custom time type that can parse multiple datetime formats
type FlexibleTime struct {
	time.Time
}

// UnmarshalJSON implements custom JSON unmarshaling for flexible datetime parsing
func (ft *FlexibleTime) UnmarshalJSON(b []byte) error {
	s := strings.Trim(string(b), "\"")

	// Try multiple datetime formats
	formats := []string{
		time.RFC3339,                    // "2006-01-02T15:04:05Z07:00"
		"2006-01-02 15:04:05-07:00",     // "2006-01-02 15:04:05-07:00"
		"2006-01-02 15:04:05+00:00",     // "2006-01-02 15:04:05+00:00"
		"2006-01-02T15:04:05.999999Z",   // With microseconds
		"2006-01-02 15:04:05",           // Without timezone
	}

	var err error
	for _, format := range formats {
		ft.Time, err = time.Parse(format, s)
		if err == nil {
			return nil
		}
	}

	// If all formats fail, set to zero time
	ft.Time = time.Time{}
	return nil // Don't error on parse failure, just use zero time
}

// CodeDocument represents an algorithm/code snippet for typing practice
type CodeDocument struct {
	ID            uuid.UUID     `json:"id"`
	Title         string        `json:"title"`
	Code          string        `json:"code"`
	Language      string        `json:"language"`
	Tags          []string      `json:"tags"`
	LinkToProject string        `json:"link_to_project"`
	Contributors  []Contributor `json:"contributors,omitempty"`
	CreatedAt     FlexibleTime  `json:"created_at"`
	UpdatedAt     FlexibleTime  `json:"updated_at"`
}

// Contributor represents a contributor to an algorithm
type Contributor struct {
	Name     string `json:"name"`
	LastName string `json:"last_name"`
	Email    string `json:"email"`
}

// Language represents a programming language
type Language struct {
	ID   uuid.UUID `json:"id"`
	Name string    `json:"name"`
}

// Tag represents a tag/category for algorithms
type Tag struct {
	ID   uuid.UUID `json:"id"`
	Name string    `json:"name"`
}

// Validate validates the CodeDocument
func (c *CodeDocument) Validate() error {
	if c.ID == uuid.Nil {
		return &ValidationError{Field: "id", Message: "ID is required"}
	}
	if c.Title == "" {
		return &ValidationError{Field: "title", Message: "title is required"}
	}
	if c.Code == "" {
		return &ValidationError{Field: "code", Message: "code is required"}
	}
	if c.Language == "" {
		return &ValidationError{Field: "language", Message: "language is required"}
	}
	return nil
}

// Validate validates the Language
func (l *Language) Validate() error {
	if l.ID == uuid.Nil {
		return &ValidationError{Field: "id", Message: "ID is required"}
	}
	if l.Name == "" {
		return &ValidationError{Field: "name", Message: "name is required"}
	}
	return nil
}

// Validate validates the Tag
func (t *Tag) Validate() error {
	if t.ID == uuid.Nil {
		return &ValidationError{Field: "id", Message: "ID is required"}
	}
	if t.Name == "" {
		return &ValidationError{Field: "name", Message: "name is required"}
	}
	return nil
}

// ValidationError represents a validation error
type ValidationError struct {
	Field   string
	Message string
}

func (e *ValidationError) Error() string {
	return "validation error in " + e.Field + ": " + e.Message
}
