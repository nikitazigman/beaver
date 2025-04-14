package tagbus

import (
	"beaver-api/internal/storage/tagdb"
	"errors"

	"github.com/google/uuid"
	"github.com/jackc/pgx/v5/pgtype"
)

type Tag struct {
	ID   uuid.UUID
	Name string
}

func toDbTag(busTug Tag) (tagdb.Tag) {
	dbTag := tagdb.Tag{
		ID:   pgtype.UUID{Bytes: ([16]byte)(busTug.ID), Valid: true},
		Name: pgtype.Text{String: busTug.Name, Valid: true},
	}

	return dbTag
}

func toBusTag(dbTag tagdb.Tag) (Tag, error) {
	if !(dbTag.ID.Valid || dbTag.Name.Valid) {
		return Tag{}, errors.New("ID or Name is not Valid")
	}

	busTug := Tag{
		ID:   uuid.UUID(dbTag.ID.Bytes),
		Name: dbTag.Name.String,
	}

	return busTug, nil
}
