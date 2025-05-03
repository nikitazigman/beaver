package loader

import (
	"beaver-api/internal/business/contributor"
	"beaver-api/internal/business/language"
	"beaver-api/internal/business/script"
	"beaver-api/internal/business/tag"
	"context"
	"time"

	"github.com/google/uuid"
	"github.com/jackc/pgx/v5"
)

type Service struct {
	scriptService  *script.Service
	tagService     *tag.Service
	contribService *contributor.Service
	langService    *language.Service
}

func New(
	scriptService *script.Service,
	tagService *tag.Service,
	contribService *contributor.Service,
	langService *language.Service,
) *Service {
	return &Service{
		scriptService:  scriptService,
		tagService:     tagService,
		contribService: contribService,
		langService:    langService,
	}
}

func (s *Service) LoadScripts(ctx context.Context, db *pgx.Conn, scripts []Script, timestamp time.Time) error {
	toLoad := toEntitiesToLoad(scripts, timestamp)
	tagMap := make(map[string]uuid.UUID)

	for _, t := range toLoad.UniqueTags {
		uuid, err := s.tagService.GetOrCreate(ctx, db, t)
		if err != nil {
			return err
		}
		tagMap[t] = uuid
	}

	return nil
}

func (s *Service) RemoveOldScripts(ctx context.Context, timestamp time.Time) error {
	return nil
}
