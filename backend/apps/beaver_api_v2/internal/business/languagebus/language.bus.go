package languagebus

import (
	"beaver-api/internal/storage/languagedb"
	"context"
)

type LangService struct {
	repo *languagedb.Queries
}

func NewLangService(r *languagedb.Queries)*LangService{
	return &LangService{
		repo: r,
	}
}

func (ls *LangService)RetrieveLanguages(ctx context.Context, offset int, size int)([]Language, error){
	qp := languagedb.ListLanguagesParams{Offset: int32(offset),Limit: int32(size)}

	langsDB, err := ls.repo.ListLanguages(ctx, qp)
	if err != nil{
		return nil, err
	}

	langsBus := make([]Language, len(langsDB))
	for i, langDB := range langsDB {
		bt, err := toLanguageBus(langDB)
		if err !=nil {
			return nil, err
		}
		langsBus[i] = bt
	}

	return langsBus, nil
}
