package services

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"time"

	"github.com/beaver-app/beaver-cli/internal/models"
)

// APIClient handles communication with the Beaver API
type APIClient struct {
	baseURL    string
	httpClient *http.Client
}

// NewAPIClient creates a new API client
func NewAPIClient(baseURL string, timeout time.Duration) *APIClient {
	return &APIClient{
		baseURL: baseURL,
		httpClient: &http.Client{
			Timeout: timeout,
			Transport: &http.Transport{
				MaxIdleConns:        10,
				MaxIdleConnsPerHost: 5,
				IdleConnTimeout:     30 * time.Second,
			},
		},
	}
}

// FetchRandom fetches a random code document with optional filters
func (c *APIClient) FetchRandom(ctx context.Context, language string, tags []string) (*models.CodeDocument, error) {
	// Build URL
	u, err := url.Parse(c.baseURL + "/api/v1/code_documents/code_document/")
	if err != nil {
		return nil, fmt.Errorf("failed to parse URL: %w", err)
	}

	// Add query parameters
	q := u.Query()
	if language != "" {
		q.Set("language", language)
	}
	for _, tag := range tags {
		q.Add("tags", tag)
	}
	u.RawQuery = q.Encode()

	// Create request
	req, err := http.NewRequestWithContext(ctx, http.MethodGet, u.String(), nil)
	if err != nil {
		return nil, fmt.Errorf("failed to create request: %w", err)
	}

	// Make request
	resp, err := c.httpClient.Do(req)
	if err != nil {
		return nil, fmt.Errorf("request failed: %w", err)
	}
	defer resp.Body.Close()

	// Check status code
	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("API returned status %d: %s", resp.StatusCode, string(body))
	}

	// Parse response
	var doc models.CodeDocument
	if err := json.NewDecoder(resp.Body).Decode(&doc); err != nil {
		return nil, fmt.Errorf("failed to parse response: %w", err)
	}

	// Validate
	if err := doc.Validate(); err != nil {
		return nil, fmt.Errorf("invalid code document: %w", err)
	}

	return &doc, nil
}

// ListLanguages fetches all available languages
func (c *APIClient) ListLanguages(ctx context.Context) ([]models.Language, error) {
	// Build URL
	u := c.baseURL + "/api/v1/languages/"

	// Create request
	req, err := http.NewRequestWithContext(ctx, http.MethodGet, u, nil)
	if err != nil {
		return nil, fmt.Errorf("failed to create request: %w", err)
	}

	// Make request
	resp, err := c.httpClient.Do(req)
	if err != nil {
		return nil, fmt.Errorf("request failed: %w", err)
	}
	defer resp.Body.Close()

	// Check status code
	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("API returned status %d: %s", resp.StatusCode, string(body))
	}

	// Parse response
	var languages []models.Language
	if err := json.NewDecoder(resp.Body).Decode(&languages); err != nil {
		return nil, fmt.Errorf("failed to parse response: %w", err)
	}

	return languages, nil
}

// ListTags fetches all available tags
func (c *APIClient) ListTags(ctx context.Context) ([]models.Tag, error) {
	// Build URL
	u := c.baseURL + "/api/v1/tags/"

	// Create request
	req, err := http.NewRequestWithContext(ctx, http.MethodGet, u, nil)
	if err != nil {
		return nil, fmt.Errorf("failed to create request: %w", err)
	}

	// Make request
	resp, err := c.httpClient.Do(req)
	if err != nil {
		return nil, fmt.Errorf("request failed: %w", err)
	}
	defer resp.Body.Close()

	// Check status code
	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("API returned status %d: %s", resp.StatusCode, string(body))
	}

	// Parse response
	var tags []models.Tag
	if err := json.NewDecoder(resp.Body).Decode(&tags); err != nil {
		return nil, fmt.Errorf("failed to parse response: %w", err)
	}

	return tags, nil
}
