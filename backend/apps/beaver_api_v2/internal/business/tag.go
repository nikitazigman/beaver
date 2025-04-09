package business

import (
	"beaver-api/internal/storage"

	"github.com/google/uuid"
	"github.com/jackc/pgx/v5/pgtype"
)
type Tag struct {
	ID uuid.UUID
	Name string
}

func ToStorTag (busTug Tag)(storage.Tag, error){
	storTag := storage.Tag{
		ID: pgtype.UUID{Bytes:  ([16]byte)(busTug.ID), Valid: true},
		Name: pgtype.Text{String:  busTug.Name, Valid: true},
	}

	return storTag, nil
}

func ToBusTag (tag storage.Tag) (Tag,error){
	if !(tag.ID.Valid || tag.Name.Valid){
		return Tag{}, nil
	}

	busTug := Tag{
		ID: uuid.UUID( tag.ID.Bytes),
		Name: tag.Name.String,
	}

	return busTug, nil
}
