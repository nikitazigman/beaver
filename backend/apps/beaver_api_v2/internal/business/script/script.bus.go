package script

import (
	"beaver-api/internal/db/script"
	"context"

	"github.com/jackc/pgx/v5/pgtype"
)

type Service struct {
	q *script.Queries
}

func New(q *script.Queries) *Service {
	return &Service{
		q: q,
	}
}

func (s *Service) UpsertScripts(ctx context.Context, scripts []Script) error {
	qp := make([]script.UpsertScriptsParams, len(scripts))
	for i, sc := range scripts {
		qp[i] = script.UpsertScriptsParams{
			Title:         pgtype.Text{String: sc.Title, Valid: true},
			LinkToProject: pgtype.Text{String: sc.LinkToProject, Valid: true},
			Code:          pgtype.Text{String: sc.Code, Valid: true},
			LanguageID:    pgtype.UUID{Bytes: sc.LanguageID, Valid: true},
		}
	}

	var upsertErr error
	s.q.UpsertScripts(ctx, qp).Exec(func(i int, err error) {
		if err != nil {
			upsertErr = err
		}
	})

	return upsertErr
}

func (s *Service) LinkTags(ctx context.Context, tagScriptLinks []TagScript) error {
	qp := make([]script.LinkTagsParams, len(tagScriptLinks))
	for i, ts := range tagScriptLinks {
		qp[i] = script.LinkTagsParams{
			TagID:    pgtype.UUID{Bytes: ts.TagID, Valid: true},
			ScriptID: pgtype.UUID{Bytes: ts.ScriptID, Valid: true},
		}
	}
	var tErr error
	s.q.LinkTags(ctx, qp).Exec(func(i int, err error) {
		if err != nil {
			tErr = err
		}
	})
	return tErr
}

func (s *Service) LinkContributors(ctx context.Context, contribScriptLinks []ContributorScript) error {
	qp := make([]script.LinkContributorsParams, len(contribScriptLinks))
	for i, cs := range contribScriptLinks {
		qp[i] = script.LinkContributorsParams{
			ContributorID: pgtype.UUID{Bytes: cs.ContributorID, Valid: true},
			ScriptID:      pgtype.UUID{Bytes: cs.ScriptID, Valid: true},
		}
	}
	var cErr error
	s.q.LinkContributors(ctx, qp).Exec(func(i int, err error) {
		if err != nil {
			cErr = err
		}
	})
	return cErr
}
