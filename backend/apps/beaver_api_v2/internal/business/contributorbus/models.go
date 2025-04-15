package contributorbus

import (
	"beaver-api/internal/storage/contributordb"
	"errors"

	"github.com/google/uuid"
)

type Contributor struct {
	ID           uuid.UUID
	Name         string
	LastName     string
	EmailAddress string
}

func toBusContrib(contrib contributordb.Contributor) (Contributor, error) {
	if !(contrib.ID.Valid || contrib.Name.Valid || contrib.LastName.Valid || contrib.EmailAddress.Valid) {
		return Contributor{}, errors.New("some of the Contributor fields are not Valid")
	}

	contribBus := Contributor{
		ID:           uuid.UUID(contrib.ID.Bytes),
		Name:         contrib.Name.String,
		LastName:     contrib.LastName.String,
		EmailAddress: contrib.EmailAddress.String,
	}
	return contribBus, nil
}
