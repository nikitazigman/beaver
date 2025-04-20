package scriptdetail

import (
	db "beaver-api/internal/db/scriptdetail"
	"context"

	"github.com/google/uuid"
	"github.com/jackc/pgx/v5/pgtype"
)

type Service struct {
	q *db.Queries
}

func New(q *db.Queries) *Service {
	return &Service{
		q: q,
	}
}

func (s *Service) GetRandomScriptDetail(ctx context.Context, tagIDs []uuid.UUID, contribIDs []uuid.UUID, langID uuid.UUID) (ScriptDetail, error) {
	qp := db.RandomParams{
		TagIDs:     tagIDs,
		ContribIDs: contribIDs,
		LanguageID: pgtype.UUID{
			Bytes: langID,
			Valid: false,
		},
	}
	dbScripts, err := s.q.Random(ctx, qp)
	if err != nil {
		return ScriptDetail{}, err
	}

	script := toBus(dbScripts)
	return script, nil
}
