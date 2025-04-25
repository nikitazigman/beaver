package loader

import (
	"beaver-api/internal/business/loader"
	"time"
)

type Language struct {
	Name string `json:"name"`
}

type Tag struct {
	Name string `json:"name"`
}

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
	Tags          []Tag
	Language      Language
}

type POSTLoadScriptsDTO struct {
	Timestamp string `json:"timestamp"`
	Scripts   []Script
}

func toScriptDetail(dto POSTLoadScriptsDTO) ([]loader.ScriptDetail, time.Time, error) {
	timestamp, err := time.Parse("2006-01-02 15-04-05", dto.Timestamp)
	if err != nil {
		return nil, time.Time{}, err
	}

	sd := make([]loader.ScriptDetail, len(dto.Scripts))
	for i, s := range dto.Scripts {
		ts := make([]loader.Tag, len(s.Tags))
		for i, t := range s.Tags {
			ts[i] = loader.Tag{Name: t.Name}
		}

		cs := make([]loader.Contributor, len(s.Contributors))
		for i, c := range s.Contributors {
			cs[i] = loader.Contributor{Name: c.Name, LastName: c.LastName, EmailAddress: c.EmailAddress}
		}

		sd[i] = loader.ScriptDetail{
			Title:         s.Title,
			Code:          s.Code,
			LinkToProject: s.LinkToProject,
			Language:      loader.Language{Name: s.Language.Name},
			Contributors:  cs,
			Tags:          ts,
		}
	}
	return sd, timestamp, nil
}
