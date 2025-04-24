package script

import "beaver-api/internal/db/script"

type Service struct {
	q *script.Queries
}

func New(q *script.Queries) *Service {
	return &Service{
		q: q,
	}
}

func CreateMissingScripts(scripts []Script) error {
	return nil
}

func AddMissingTags(tagScriptLinks []TagScript) error {
	return nil
}

func AddMissingContributors(contribScriptLinks []ContributorScript) error {
	return nil
}
