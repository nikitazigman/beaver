// Code generated by sqlc. DO NOT EDIT.
// versions:
//   sqlc v1.28.0

package contributor

import (
	"github.com/google/uuid"
	"github.com/jackc/pgx/v5/pgtype"
)

type Contributor struct {
	ID           uuid.UUID
	CreatedAt    pgtype.Timestamptz
	UpdatedAt    pgtype.Timestamptz
	Name         pgtype.Text
	LastName     pgtype.Text
	EmailAddress pgtype.Text
}
