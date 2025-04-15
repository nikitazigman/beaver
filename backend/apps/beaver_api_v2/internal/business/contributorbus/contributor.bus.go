package contributorbus

import (
	"beaver-api/internal/storage/contributordb"
	"context"
)

type ContribService struct {
	repo *contributordb.Queries
}


func NewContribService(r *contributordb.Queries)*ContribService{
	return &ContribService{
		repo: r,
	}
}

func (cs *ContribService) RetrieveContributors(ctx context.Context, offset int, size int) ([]Contributor, error) {
	qp := contributordb.ListContributorsParams{Offset: int32(offset), Limit: int32(size)}

	contrDB, err := cs.repo.ListContributors(ctx, qp)

	if err != nil {
		return nil, err
	}

	contrsBus := make([]Contributor, len(contrDB))
	for i, contr := range contrDB {
		contrBus, err := toBusContrib(contr)
		if err != nil {
			return nil, err
		}
		contrsBus[i] = contrBus
	}

	return contrsBus, nil
}
