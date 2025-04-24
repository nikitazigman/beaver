package loader

import (
	"beaver-api/internal/business/contributor"
	"beaver-api/internal/business/language"
	"beaver-api/internal/business/script"
	"beaver-api/internal/business/tag"
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

func (s *Service) LoadScripts([]ScriptDetail) error {
	// get set of tags to create
	// get set of contributors to create
	// get set of languages to create

	// load languages to db -> get map[Name]ID

	// create script models using the language mapping
	// load script models to db -> get map[Title]ID

	// load tags to db -> get map[Name]ID
	// load contributors to db -> get map[EmailAddress]ID

	//create script-tags models using the script and tags mappings
	// load the script-tags to db

	// create contrib-script models using script and contribs mappings
	// load the contrib-script to db

	return nil
}

func (s *Service) RemoveOldScripts(timestamp time.Time) error {
	return nil
}
