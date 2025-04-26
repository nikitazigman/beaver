package script

import (
	"beaver-api/internal/db/script"
	"context"

	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgtype"
)

type Service struct{}

func New(q *script.Queries) *Service {
	return &Service{}
}

func (s *Service) UpsertScripts(ctx context.Context, db *pgx.Conn, scripts []Script) error {
	repo := script.New(db)
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
	repo.UpsertScripts(ctx, qp).Exec(func(i int, err error) {
		if err != nil {
			upsertErr = err
		}
	})

	return upsertErr
}

func (s *Service) LinkTags(ctx context.Context, db *pgx.Conn, tagScriptLinks []TagScript) error {
	repo := script.New(db)
	qp := make([]script.LinkTagsParams, len(tagScriptLinks))
	for i, ts := range tagScriptLinks {
		qp[i] = script.LinkTagsParams{
			TagID:    pgtype.UUID{Bytes: ts.TagID, Valid: true},
			ScriptID: pgtype.UUID{Bytes: ts.ScriptID, Valid: true},
		}
	}
	var tErr error
	repo.LinkTags(ctx, qp).Exec(func(i int, err error) {
		if err != nil {
			tErr = err
		}
	})
	return tErr
}

func (s *Service) LinkContributors(ctx context.Context, db *pgx.Conn, contribScriptLinks []ContributorScript) error {
	repo := script.New(db)
	qp := make([]script.LinkContributorsParams, len(contribScriptLinks))
	for i, cs := range contribScriptLinks {
		qp[i] = script.LinkContributorsParams{
			ContributorID: pgtype.UUID{Bytes: cs.ContributorID, Valid: true},
			ScriptID:      pgtype.UUID{Bytes: cs.ScriptID, Valid: true},
		}
	}
	var cErr error
	repo.LinkContributors(ctx, qp).Exec(func(i int, err error) {
		if err != nil {
			cErr = err
		}
	})
	return cErr
}
