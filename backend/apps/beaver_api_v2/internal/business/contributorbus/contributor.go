package busconributor

import "github.com/google/uuid"



type Contributor struct {
	ID uuid.UUID
	Name string
	LastName string
	EmailAddress string
}
