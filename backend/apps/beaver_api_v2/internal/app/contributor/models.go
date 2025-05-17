package contributor

import biz "beaver-api/internal/business/contributor"

type GetContribDTO struct {
	ID           string `json:"id"`
	Name         string `json:"name"`
	LastName     string `json:"last_name"`
	EmailAddress string `json:"email_address"`
}

type GetContribsDTO struct {
	Offset int `json:"offset"`
	Size   int `json:"size"`
	Value  []GetContribDTO
}

func contribBusToGetContribsDTO(bcs []biz.Contributor, offset int, size int) GetContribsDTO {
	v := make([]GetContribDTO, len(bcs))
	for i, bc := range bcs {
		v[i] = GetContribDTO{
			ID:           bc.ID.String(),
			Name:         bc.Name,
			LastName:     bc.LastName,
			EmailAddress: bc.EmailAddress,
		}
	}

	return GetContribsDTO{
		Offset: offset,
		Size:   size,
		Value:  v,
	}
}
