package loader

import (
	"beaver-api/internal/business/loader"
	"time"
)

type Contributor struct {
	Name         string `json:"name"`
	LastName     string `json:"last_name"`
	EmailAddress string `json:"address"`
}

type POSTUpdateScriptDTO struct {
	Title         string   `json:"title"`
	Code          string   `json:"code"`
	LinkToProject string   `json:"link_to_project"`
	Language      string   `json:"language"`
	Tags          []string `json:"tags"`
	Contributors  []Contributor
	LastSync      string `json:"last_synchronization"`
}

func toScriptDetail(dto []POSTUpdateScriptDTO) ([]loader.Script, time.Time, error) {
	timestamp, err := time.Parse("2006-01-02 15:04:05.999999-07:00", dto[0].LastSync)
	if err != nil {
		return nil, time.Time{}, err
	}

	sd := make([]loader.Script, len(dto))
	for i, s := range dto {
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
