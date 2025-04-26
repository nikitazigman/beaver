package loader

import (
	"beaver-api/internal/business/contributor"
	"beaver-api/internal/business/language"
	"beaver-api/internal/business/script"
	"beaver-api/internal/business/tag"
	"context"
	"time"

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

func (s *Service) LoadScripts(ctx context.Context, db *pgx.Conn, scripts []ScriptDetail, timestamp time.Time) error {
	loader := toEntities(scripts, timestamp)

	if err := s.langService.UpsertLanguages(ctx, db, loader.langs); err != nil {
		return err
	}
	if err := s.contribService.UpsertContributors(ctx, db, loader.contributors); err != nil {
		return err
	}
	if err := s.tagService.CreateTags(ctx, db, loader.tags); err != nil {
		return err
	}
	if err := s.scriptService.UpsertScripts(ctx, db, loader.scripts); err != nil {
		return err
	}
	if err := s.scriptService.LinkTags(ctx, db, loader.tagScript); err != nil {
		return err
	}
	if err := s.scriptService.LinkContributors(ctx, db, loader.contribScript); err != nil {
		return err
	}
	return nil
}

func (s *Service) RemoveOldScripts(ctx context.Context, timestamp time.Time) error {
	return nil
}
