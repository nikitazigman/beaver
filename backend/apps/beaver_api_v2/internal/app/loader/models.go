package loader

import (
	"beaver-api/internal/business/loader"
	"time"
)

type Contributor struct {
	Name         string `json:"name"`
	LastName     string `json:"last_name"`
	EmailAddress string `json:"email_address"`
}

type Script struct {
	Title         string `json:"title"`
	Code          string `json:"code"`
	LinkToProject string `json:"link_to_project"`
	Contributors  []Contributor
	Tags          []string `json:"tags"`
	Language      string   `json:"language"`
}

type POSTLoadScriptsDTO struct {
	Timestamp string `json:"timestamp"`
	Scripts   []Script
}

func toScriptDetail(dto POSTLoadScriptsDTO) ([]loader.Script, time.Time, error) {
	timestamp, err := time.Parse("2006-01-02T15:04:05Z", dto.Timestamp)
	if err != nil {
		return nil, time.Time{}, err
	}

	sd := make([]loader.Script, len(dto.Scripts))
	for i, s := range dto.Scripts {
		contribs := make([]loader.Contributor, 0, len(s.Contributors))
		for _, c := range s.Contributors {
			contribs = append(contribs, loader.Contributor{Name: c.Name, LastName: c.LastName, EmailAddress: c.EmailAddress})
		}
		sd[i] = loader.Script{
			Title:         s.Title,
			Code:          s.Code,
			LinkToProject: s.LinkToProject,
			Language:      s.Language,
			Tags:          s.Tags,
			Contributors:  contribs,
		}
	}
	return sd, timestamp, nil
}
