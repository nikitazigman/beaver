package scriptdetail

import (
	"beaver-api/internal/db/scriptdetail"
	"context"

	"github.com/google/uuid"
	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgtype"
)

type Service struct{}

func New() *Service {
	return &Service{}
}

func (s *Service) GetRandomScriptDetail(ctx context.Context, db *pgx.Conn, tagIDs []uuid.UUID, contribIDs []uuid.UUID, langID uuid.UUID) (ScriptDetail, error) {
	repo := scriptdetail.New(db)
	qp := scriptdetail.RandomParams{
		TagIDs:     tagIDs,
		ContribIDs: contribIDs,
		LanguageID: pgtype.UUID{
			Bytes: langID,
			Valid: false,
		},
	}
	dbScripts, err := repo.Random(ctx, qp)

	if err != nil {
		return ScriptDetail{}, err
	}

	script := toBus(dbScripts)
	return script, nil
}
