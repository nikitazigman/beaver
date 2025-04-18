package contributor

import (
	db "beaver-api/internal/db/contributor"
	"errors"

	"github.com/google/uuid"
)

type Contributor struct {
	ID           uuid.UUID
	Name         string
	LastName     string
	EmailAddress string
}

func toBusContrib(cd db.Contributor) (Contributor, error) {
	if !(cd.Name.Valid || cd.LastName.Valid || cd.EmailAddress.Valid) {
		return Contributor{}, errors.New("some of the Contributor fields are not Valid")
	}

	cb := Contributor{
		ID:           cd.ID,
		Name:         cd.Name.String,
		LastName:     cd.LastName.String,
		EmailAddress: cd.EmailAddress.String,
	}
	return cb, nil
}
