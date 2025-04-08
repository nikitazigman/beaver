package business

import "github.com/google/uuid"



type Contributor struct {
	ID uuid.UUID
	Name string
	LastName string
	EmailAddress string
}
