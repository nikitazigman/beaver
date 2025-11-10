package models

import (
	"encoding/json"
	"testing"
	"time"

	"github.com/google/uuid"
)

func TestCodeDocumentValidate(t *testing.T) {
	tests := []struct {
		name    string
		doc     *CodeDocument
		wantErr bool
		errMsg  string
	}{
		{
			name: "valid code document",
			doc: &CodeDocument{
				ID:            uuid.New(),
				Title:         "Bubble Sort",
				Code:          "def bubble_sort(arr): pass",
				Language:      "python",
				Tags:          []string{"sort"},
				LinkToProject: "https://example.com",
				CreatedAt:     FlexibleTime{time.Now()},
				UpdatedAt:     FlexibleTime{time.Now()},
			},
			wantErr: false,
		},
		{
			name: "missing ID",
			doc: &CodeDocument{
				ID:       uuid.Nil,
				Title:    "Test",
				Code:     "code",
				Language: "python",
			},
			wantErr: true,
			errMsg:  "id",
		},
		{
			name: "missing title",
			doc: &CodeDocument{
				ID:       uuid.New(),
				Title:    "",
				Code:     "code",
				Language: "python",
			},
			wantErr: true,
			errMsg:  "title",
		},
		{
			name: "missing code",
			doc: &CodeDocument{
				ID:       uuid.New(),
				Title:    "Test",
				Code:     "",
				Language: "python",
			},
			wantErr: true,
			errMsg:  "code",
		},
		{
			name: "missing language",
			doc: &CodeDocument{
				ID:       uuid.New(),
				Title:    "Test",
				Code:     "code",
				Language: "",
			},
			wantErr: true,
			errMsg:  "language",
		},
		{
			name: "valid with contributors",
			doc: &CodeDocument{
				ID:       uuid.New(),
				Title:    "Test",
				Code:     "code",
				Language: "python",
				Contributors: []Contributor{
					{Name: "John", LastName: "Doe", Email: "john@example.com"},
				},
			},
			wantErr: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			err := tt.doc.Validate()
			if (err != nil) != tt.wantErr {
				t.Errorf("CodeDocument.Validate() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if tt.wantErr && err != nil {
				validationErr, ok := err.(*ValidationError)
				if !ok {
					t.Errorf("expected ValidationError, got %T", err)
					return
				}
				if validationErr.Field != tt.errMsg {
					t.Errorf("ValidationError.Field = %v, want %v", validationErr.Field, tt.errMsg)
				}
			}
		})
	}
}

func TestLanguageValidate(t *testing.T) {
	tests := []struct {
		name     string
		language *Language
		wantErr  bool
		errMsg   string
	}{
		{
			name: "valid language",
			language: &Language{
				ID:   uuid.New(),
				Name: "Python",
			},
			wantErr: false,
		},
		{
			name: "missing ID",
			language: &Language{
				ID:   uuid.Nil,
				Name: "Python",
			},
			wantErr: true,
			errMsg:  "id",
		},
		{
			name: "missing name",
			language: &Language{
				ID:   uuid.New(),
				Name: "",
			},
			wantErr: true,
			errMsg:  "name",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			err := tt.language.Validate()
			if (err != nil) != tt.wantErr {
				t.Errorf("Language.Validate() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if tt.wantErr && err != nil {
				validationErr, ok := err.(*ValidationError)
				if !ok {
					t.Errorf("expected ValidationError, got %T", err)
					return
				}
				if validationErr.Field != tt.errMsg {
					t.Errorf("ValidationError.Field = %v, want %v", validationErr.Field, tt.errMsg)
				}
			}
		})
	}
}

func TestTagValidate(t *testing.T) {
	tests := []struct {
		name    string
		tag     *Tag
		wantErr bool
		errMsg  string
	}{
		{
			name: "valid tag",
			tag: &Tag{
				ID:   uuid.New(),
				Name: "sort",
			},
			wantErr: false,
		},
		{
			name: "missing ID",
			tag: &Tag{
				ID:   uuid.Nil,
				Name: "sort",
			},
			wantErr: true,
			errMsg:  "id",
		},
		{
			name: "missing name",
			tag: &Tag{
				ID:   uuid.New(),
				Name: "",
			},
			wantErr: true,
			errMsg:  "name",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			err := tt.tag.Validate()
			if (err != nil) != tt.wantErr {
				t.Errorf("Tag.Validate() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if tt.wantErr && err != nil {
				validationErr, ok := err.(*ValidationError)
				if !ok {
					t.Errorf("expected ValidationError, got %T", err)
					return
				}
				if validationErr.Field != tt.errMsg {
					t.Errorf("ValidationError.Field = %v, want %v", validationErr.Field, tt.errMsg)
				}
			}
		})
	}
}

func TestCodeDocumentJSON(t *testing.T) {
	// Test JSON marshaling and unmarshaling
	doc := &CodeDocument{
		ID:            uuid.New(),
		Title:         "Test Algorithm",
		Code:          "def test(): pass",
		Language:      "python",
		Tags:          []string{"test", "example"},
		LinkToProject: "https://example.com",
		Contributors: []Contributor{
			{Name: "John", LastName: "Doe", Email: "john@example.com"},
		},
		CreatedAt: FlexibleTime{time.Now().UTC().Truncate(time.Second)},
		UpdatedAt: FlexibleTime{time.Now().UTC().Truncate(time.Second)},
	}

	// Marshal to JSON
	data, err := json.Marshal(doc)
	if err != nil {
		t.Fatalf("json.Marshal() error = %v", err)
	}

	// Unmarshal back
	var decoded CodeDocument
	if err := json.Unmarshal(data, &decoded); err != nil {
		t.Fatalf("json.Unmarshal() error = %v", err)
	}

	// Verify
	if decoded.ID != doc.ID {
		t.Errorf("ID = %v, want %v", decoded.ID, doc.ID)
	}
	if decoded.Title != doc.Title {
		t.Errorf("Title = %v, want %v", decoded.Title, doc.Title)
	}
	if decoded.Code != doc.Code {
		t.Errorf("Code = %v, want %v", decoded.Code, doc.Code)
	}
	if decoded.Language != doc.Language {
		t.Errorf("Language = %v, want %v", decoded.Language, doc.Language)
	}
	if len(decoded.Tags) != len(doc.Tags) {
		t.Errorf("len(Tags) = %v, want %v", len(decoded.Tags), len(doc.Tags))
	}
	if len(decoded.Contributors) != len(doc.Contributors) {
		t.Errorf("len(Contributors) = %v, want %v", len(decoded.Contributors), len(doc.Contributors))
	}
}

func TestLanguageJSON(t *testing.T) {
	lang := &Language{
		ID:   uuid.New(),
		Name: "Python",
	}

	data, err := json.Marshal(lang)
	if err != nil {
		t.Fatalf("json.Marshal() error = %v", err)
	}

	var decoded Language
	if err := json.Unmarshal(data, &decoded); err != nil {
		t.Fatalf("json.Unmarshal() error = %v", err)
	}

	if decoded.ID != lang.ID {
		t.Errorf("ID = %v, want %v", decoded.ID, lang.ID)
	}
	if decoded.Name != lang.Name {
		t.Errorf("Name = %v, want %v", decoded.Name, lang.Name)
	}
}

func TestTagJSON(t *testing.T) {
	tag := &Tag{
		ID:   uuid.New(),
		Name: "sort",
	}

	data, err := json.Marshal(tag)
	if err != nil {
		t.Fatalf("json.Marshal() error = %v", err)
	}

	var decoded Tag
	if err := json.Unmarshal(data, &decoded); err != nil {
		t.Fatalf("json.Unmarshal() error = %v", err)
	}

	if decoded.ID != tag.ID {
		t.Errorf("ID = %v, want %v", decoded.ID, tag.ID)
	}
	if decoded.Name != tag.Name {
		t.Errorf("Name = %v, want %v", decoded.Name, tag.Name)
	}
}

func TestValidationError(t *testing.T) {
	err := &ValidationError{
		Field:   "test_field",
		Message: "test message",
	}

	expected := "validation error in test_field: test message"
	if err.Error() != expected {
		t.Errorf("ValidationError.Error() = %v, want %v", err.Error(), expected)
	}
}
