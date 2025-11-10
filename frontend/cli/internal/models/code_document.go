package models

import (
	"time"

	"github.com/google/uuid"
)

// CodeDocument represents an algorithm/code snippet for typing practice
type CodeDocument struct {
	ID            uuid.UUID     `json:"id"`
	Title         string        `json:"title"`
	Code          string        `json:"code"`
	Language      string        `json:"language"`
	Tags          []string      `json:"tags"`
	LinkToProject string        `json:"link_to_project"`
	Contributors  []Contributor `json:"contributors,omitempty"`
	CreatedAt     time.Time     `json:"created_at"`
	UpdatedAt     time.Time     `json:"updated_at"`
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
