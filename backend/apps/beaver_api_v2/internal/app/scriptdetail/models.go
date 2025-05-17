package scriptdetail

import biz "beaver-api/internal/business/scriptdetail"

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
	Tags          []string `json:"tags"`
	Language      string   `json:"language"`
	UpdatedAt     string   `json:"updated_at"`
	CreatedAt     string   `json:"created_at"`
}

func toDTO(script biz.ScriptDetail) GetRandScriptDetailDTO {
	tags := make([]string, len(script.Tags))
	for i, t := range script.Tags {
		tags[i] = t.Name
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
		Language:      script.Language.Name,
		Contributors:  contribs,
		Tags:          tags,
		UpdatedAt:     script.UpdatedAt.Format("2006-01-02 15:04:05.999999-07:00"),
		CreatedAt:     script.CreatedAt.Format("2006-01-02 15:04:05.999999-07:00"),
	}
	return dto
}
