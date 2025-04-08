package business

import (
	"beaver-api/internal/storage"

	"github.com/google/uuid"
)
type Tag struct {
	ID uuid.UUID
	Name string
}

func ToStorTag (busTug Tag)storage.Tag{
	storTag := storage.Tag{
		ID: busTug.ID,
		Name: busTug.Name,
	}

	return storTag
}

func ToBusTag (tag storage.Tag) Tag{
	busTug := Tag{
		ID: tag.ID,
		Name: tag.Name,
	}

	return busTug
}
