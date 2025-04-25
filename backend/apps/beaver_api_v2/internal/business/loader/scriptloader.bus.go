package loader

import (
	"beaver-api/internal/business/contributor"
	"beaver-api/internal/business/language"
	"beaver-api/internal/business/script"
	"beaver-api/internal/business/tag"
	"context"
	"time"
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

// TODO: transaction
func (s *Service) LoadScripts(ctx context.Context, scripts []ScriptDetail, timestamp time.Time) error {
	loader := toEntities(scripts, timestamp)

	if err := s.langService.UpsertLanguages(ctx, loader.langs); err != nil {
		return err
	}
	if err := s.contribService.UpsertContributors(ctx, loader.contributors); err != nil {
		return err
	}
	if err := s.tagService.CreateTags(ctx, loader.tags); err != nil {
		return err
	}
	if err := s.scriptService.UpsertScripts(ctx, loader.scripts); err != nil {
		return err
	}
	if err := s.scriptService.LinkTags(ctx, loader.tagScript); err != nil {
		return err
	}
	if err := s.scriptService.LinkContributors(ctx, loader.contribScript); err != nil {
		return err
	}
	return nil
}

func (s *Service) RemoveOldScripts(ctx context.Context, timestamp time.Time) error {
	return nil
}
