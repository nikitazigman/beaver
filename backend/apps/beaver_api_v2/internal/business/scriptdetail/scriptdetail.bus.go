package scriptdetail

import (
	"beaver-api/internal/db/scriptdetail"
	"context"
	"errors"

	"github.com/jackc/pgx/v5"
)

type Service struct{}

func New() *Service {
	return &Service{}
}

func (s *Service) GetRandomScriptDetail(ctx context.Context, db pgx.Tx, tags []string, contributors []string, languages []string) (ScriptDetail, error) {
	repo := scriptdetail.New(db)
	qp := scriptdetail.RandomParams{
		Tags:     tags,
		Contribs: contributors,
		Langs:    languages,
	}

	dbScripts, err := repo.Random(ctx, qp)
	if err != nil {
		return ScriptDetail{}, err
	}
	if dbScripts == nil {
		return ScriptDetail{}, errors.New("Could not find script in the db")
	}

	script := toBus(dbScripts)

	return script, nil
}
