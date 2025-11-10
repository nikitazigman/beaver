package services

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"

	"github.com/google/uuid"

	"github.com/beaver-app/beaver-cli/internal/models"
)

func TestNewAPIClient(t *testing.T) {
	client := NewAPIClient("https://test-api.com", 5*time.Second)

	if client == nil {
		t.Fatal("NewAPIClient() returned nil")
	}
	if client.baseURL != "https://test-api.com" {
		t.Errorf("baseURL = %v, want https://test-api.com", client.baseURL)
	}
	if client.httpClient == nil {
		t.Error("httpClient is nil")
	}
	if client.httpClient.Timeout != 5*time.Second {
		t.Errorf("httpClient.Timeout = %v, want 5s", client.httpClient.Timeout)
	}
}

func TestFetchRandom(t *testing.T) {
	tests := []struct {
		name       string
		language   string
		tags       []string
		response   interface{}
		statusCode int
		wantErr    bool
	}{
		{
			name:     "successful fetch",
			language: "python",
			tags:     []string{"sort"},
			response: models.CodeDocument{
				ID:            uuid.New(),
				Title:         "Bubble Sort",
				Code:          "def bubble_sort(arr): pass",
				Language:      "python",
				Tags:          []string{"sort"},
				LinkToProject: "https://example.com",
				CreatedAt:     models.FlexibleTime{time.Now()},
				UpdatedAt:     models.FlexibleTime{time.Now()},
			},
			statusCode: http.StatusOK,
			wantErr:    false,
		},
		{
			name:       "fetch without filters",
			language:   "",
			tags:       nil,
			response: models.CodeDocument{
				ID:            uuid.New(),
				Title:         "Test Algorithm",
				Code:          "code",
				Language:      "go",
				Tags:          []string{},
				LinkToProject: "",
				CreatedAt:     models.FlexibleTime{time.Now()},
				UpdatedAt:     models.FlexibleTime{time.Now()},
			},
			statusCode: http.StatusOK,
			wantErr:    false,
		},
		{
			name:       "API returns 404",
			language:   "python",
			tags:       []string{"nonexistent"},
			response:   map[string]string{"error": "not found"},
			statusCode: http.StatusNotFound,
			wantErr:    true,
		},
		{
			name:       "API returns 500",
			language:   "",
			tags:       nil,
			response:   map[string]string{"error": "internal server error"},
			statusCode: http.StatusInternalServerError,
			wantErr:    true,
		},
		{
			name:       "invalid JSON response",
			language:   "",
			tags:       nil,
			response:   "invalid json",
			statusCode: http.StatusOK,
			wantErr:    true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Create mock server
			server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
				// Verify method
				if r.Method != http.MethodGet {
					t.Errorf("Method = %v, want GET", r.Method)
				}

				// Verify path
				if r.URL.Path != "/api/v1/code_documents/code_document/" {
					t.Errorf("Path = %v, want /api/v1/code_documents/code_document/", r.URL.Path)
				}

				// Verify query parameters
				if tt.language != "" {
					if r.URL.Query().Get("language") != tt.language {
						t.Errorf("language param = %v, want %v", r.URL.Query().Get("language"), tt.language)
					}
				}
				if len(tt.tags) > 0 {
					tags := r.URL.Query()["tags"]
					if len(tags) != len(tt.tags) {
						t.Errorf("len(tags) = %v, want %v", len(tags), len(tt.tags))
					}
				}

				// Write response
				w.WriteHeader(tt.statusCode)
				if tt.statusCode == http.StatusOK {
					json.NewEncoder(w).Encode(tt.response)
				} else {
					if str, ok := tt.response.(string); ok {
						w.Write([]byte(str))
					} else {
						json.NewEncoder(w).Encode(tt.response)
					}
				}
			}))
			defer server.Close()

			// Create client
			client := NewAPIClient(server.URL, 5*time.Second)

			// Test
			doc, err := client.FetchRandom(context.Background(), tt.language, tt.tags)
			if (err != nil) != tt.wantErr {
				t.Errorf("FetchRandom() error = %v, wantErr %v", err, tt.wantErr)
				return
			}

			if !tt.wantErr {
				if doc == nil {
					t.Error("FetchRandom() returned nil document")
					return
				}
				if doc.ID == uuid.Nil {
					t.Error("Document ID is nil")
				}
				if doc.Title == "" {
					t.Error("Document title is empty")
				}
			}
		})
	}
}

func TestListLanguages(t *testing.T) {
	tests := []struct {
		name       string
		response   interface{}
		statusCode int
		wantErr    bool
		wantCount  int
	}{
		{
			name: "successful list",
			response: []models.Language{
				{ID: uuid.New(), Name: "Python"},
				{ID: uuid.New(), Name: "Go"},
				{ID: uuid.New(), Name: "JavaScript"},
			},
			statusCode: http.StatusOK,
			wantErr:    false,
			wantCount:  3,
		},
		{
			name:       "empty list",
			response:   []models.Language{},
			statusCode: http.StatusOK,
			wantErr:    false,
			wantCount:  0,
		},
		{
			name:       "API returns 500",
			response:   map[string]string{"error": "internal server error"},
			statusCode: http.StatusInternalServerError,
			wantErr:    true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Create mock server
			server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
				if r.URL.Path != "/api/v1/languages/" {
					t.Errorf("Path = %v, want /api/v1/languages/", r.URL.Path)
				}

				w.WriteHeader(tt.statusCode)
				json.NewEncoder(w).Encode(tt.response)
			}))
			defer server.Close()

			// Create client
			client := NewAPIClient(server.URL, 5*time.Second)

			// Test
			languages, err := client.ListLanguages(context.Background())
			if (err != nil) != tt.wantErr {
				t.Errorf("ListLanguages() error = %v, wantErr %v", err, tt.wantErr)
				return
			}

			if !tt.wantErr {
				if len(languages) != tt.wantCount {
					t.Errorf("len(languages) = %v, want %v", len(languages), tt.wantCount)
				}
			}
		})
	}
}

func TestListTags(t *testing.T) {
	tests := []struct {
		name       string
		response   interface{}
		statusCode int
		wantErr    bool
		wantCount  int
	}{
		{
			name: "successful list",
			response: []models.Tag{
				{ID: uuid.New(), Name: "sort"},
				{ID: uuid.New(), Name: "search"},
				{ID: uuid.New(), Name: "graph"},
			},
			statusCode: http.StatusOK,
			wantErr:    false,
			wantCount:  3,
		},
		{
			name:       "empty list",
			response:   []models.Tag{},
			statusCode: http.StatusOK,
			wantErr:    false,
			wantCount:  0,
		},
		{
			name:       "API returns 404",
			response:   map[string]string{"error": "not found"},
			statusCode: http.StatusNotFound,
			wantErr:    true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Create mock server
			server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
				if r.URL.Path != "/api/v1/tags/" {
					t.Errorf("Path = %v, want /api/v1/tags/", r.URL.Path)
				}

				w.WriteHeader(tt.statusCode)
				json.NewEncoder(w).Encode(tt.response)
			}))
			defer server.Close()

			// Create client
			client := NewAPIClient(server.URL, 5*time.Second)

			// Test
			tags, err := client.ListTags(context.Background())
			if (err != nil) != tt.wantErr {
				t.Errorf("ListTags() error = %v, wantErr %v", err, tt.wantErr)
				return
			}

			if !tt.wantErr {
				if len(tags) != tt.wantCount {
					t.Errorf("len(tags) = %v, want %v", len(tags), tt.wantCount)
				}
			}
		})
	}
}

func TestAPIClientTimeout(t *testing.T) {
	// Create a server that delays response
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(2 * time.Second)
		w.WriteHeader(http.StatusOK)
		json.NewEncoder(w).Encode(models.CodeDocument{
			ID:       uuid.New(),
			Title:    "Test",
			Code:     "code",
			Language: "python",
		})
	}))
	defer server.Close()

	// Create client with very short timeout
	client := NewAPIClient(server.URL, 100*time.Millisecond)

	// This should timeout
	_, err := client.FetchRandom(context.Background(), "", nil)
	if err == nil {
		t.Error("FetchRandom() expected timeout error, got nil")
	}
}

func TestAPIClientContext(t *testing.T) {
	// Create a server that delays response
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(2 * time.Second)
		w.WriteHeader(http.StatusOK)
		json.NewEncoder(w).Encode(models.CodeDocument{
			ID:       uuid.New(),
			Title:    "Test",
			Code:     "code",
			Language: "python",
		})
	}))
	defer server.Close()

	// Create client
	client := NewAPIClient(server.URL, 5*time.Second)

	// Create context with timeout
	ctx, cancel := context.WithTimeout(context.Background(), 100*time.Millisecond)
	defer cancel()

	// This should be cancelled by context
	_, err := client.FetchRandom(ctx, "", nil)
	if err == nil {
		t.Error("FetchRandom() expected context cancellation error, got nil")
	}
}
