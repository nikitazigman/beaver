package tag

import (
	db "beaver-api/internal/db/tag"
	"errors"

	"github.com/google/uuid"
)

type Tag struct {
	ID   uuid.UUID
	Name string
}

func toBusTag(dbTag db.Tag) (Tag, error) {
	if !dbTag.Name.Valid {
		return Tag{}, errors.New("ID or Name is not Valid")
	}

	busTug := Tag{
		ID:   dbTag.ID,
		Name: dbTag.Name.String,
	}

	return busTug, nil
}
