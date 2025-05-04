package scriptdetail

import biz "beaver-api/internal/business/scriptdetail"

type Language struct {
	ID   string `json:"id"`
	Name string `json:"name"`
}

type Tag struct {
	ID   string `json:"id"`
	Name string `json:"name"`
}

type Contributor struct {
	ID           string `json:"id"`
	Name         string `json:"name"`
	LastName     string `json:"last_name"`
	EmailAddress string `json:"email_address"`
}

type GetRandScriptDetailDTO struct {
	ID            string `json:"id"`
	Title         string `json:"title"`
	Code          string `json:"code"`
	LinkToProject string `json:"link_to_project"`
	Contributors  []Contributor
	Tags          []Tag
	Language      Language
}

func toDTO(script biz.ScriptDetail) GetRandScriptDetailDTO {
	tags := make([]Tag, len(script.Tags))
	for i, t := range script.Tags {
		tags[i] = Tag{ID: t.ID.String(), Name: t.Name}
	}

	contribs := make([]Contributor, len(script.Contributors))
	for i, c := range script.Contributors {
		contribs[i] = Contributor{
			ID:           c.ID.String(),
			Name:         c.Name,
			LastName:     c.LastName,
			EmailAddress: c.EmailAddress,
		}
	}

	dto := GetRandScriptDetailDTO{
		ID:            script.ID.String(),
		Title:         script.Title,
		Code:          script.Code,
		LinkToProject: script.LinkToProject,
		Language:      Language{ID: script.Language.ID.String(), Name: script.Language.Name},
		Contributors:  contribs,
		Tags:          tags,
	}
	return dto
}
