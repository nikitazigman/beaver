package loader

import (
	"beaver-api/internal/business/contributor"
	"beaver-api/internal/business/language"
	"beaver-api/internal/business/script"
	"beaver-api/internal/business/tag"
	"context"
	"errors"
	"fmt"
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

func (s *Service) LoadScripts(ctx context.Context, db pgx.Tx, scripts []Script, timestamp time.Time) error {
	toLoad := toEntitiesToLoad(scripts, timestamp)

	tagMap := make(map[string]uuid.UUID)
	for _, t := range toLoad.UniqueTags {
		uuid, err := s.tagService.GetOrCreate(ctx, db, t)
		if err != nil {
			return err
		}
		tagMap[t] = uuid
	}

	langMap := make(map[string]uuid.UUID)
	for _, l := range toLoad.UniqueLangs {
		uuid, err := s.langService.Upsert(ctx, db, l)
		if err != nil {
			return err
		}
		langMap[l] = uuid
	}

	contribMap := make(map[string]uuid.UUID)
	for _, c := range toLoad.UniqueContribs {
		uuid, err := s.contribService.UpsertContributors(ctx, db, c)
		if err != nil {
			return err
		}
		contribMap[c.EmailAddress] = uuid
	}

	for _, sl := range toLoad.UniqueScripts {
		lID, exist := langMap[sl.language]
		if !exist {
			return errors.New(fmt.Sprintf("language %s does not exist", sl.language))
		}

		sc := script.UpsertScript{
			Title:         sl.title,
			Code:          sl.code,
			LinkToProject: sl.linkToProject,
			LanguageID:    lID,
			CreatedAt:     timestamp,
		}
		scriptID, err := s.scriptService.Upsert(ctx, db, sc)
		if err != nil {
			return err
		}

		for _, t := range sl.tags {
			tagID, exist := tagMap[t]
			if !exist {
				return errors.New(fmt.Sprintf("tag %s does not exist", t))
			}
			l := script.TagScript{
				TagID:    tagID,
				ScriptID: scriptID,
			}
			if err := s.scriptService.LinkTag(ctx, db, l); err != nil {
				return nil
			}
		}

		for _, c := range sl.contributors {
			ctrbID, exist := contribMap[c]
			if !exist {
				return errors.New(fmt.Sprintf("contributor %s does not exist", c))
			}
			l := script.ContributorScript{
				ContributorID: ctrbID,
				ScriptID:      scriptID,
			}
			if err := s.scriptService.LinkContrib(ctx, db, l); err != nil {
				return err
			}
		}
	}
	return nil
}

func (s *Service) RemoveOldScripts(ctx context.Context, db pgx.Tx, timestamp time.Time) error {
	if err := s.scriptService.DeleteScripts(ctx, db, timestamp); err != nil {
		return err
	}

	langs, err := s.scriptService.Languages(ctx, db)
	if err != nil {
		return err
	}

	tags, err := s.scriptService.LinkedTags(ctx, db)
	if err != nil {
		return err
	}

	contribs, err := s.scriptService.LinkedContributors(ctx, db)
	if err != nil {
		return err
	}

	if err := s.langService.KeepOnly(ctx, db, langs); err != nil {
		return err
	}

	if err := s.tagService.KeepOnly(ctx, db, tags); err != nil {
		return err
	}

	if err := s.contribService.KeepOnly(ctx, db, contribs); err != nil {
		return err
	}

	return nil
}
