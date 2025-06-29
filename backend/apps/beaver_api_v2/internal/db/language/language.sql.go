// Code generated by sqlc. DO NOT EDIT.
// versions:
//   sqlc v1.28.0
// source: language.sql

package language

import (
	"context"

	"github.com/google/uuid"
	"github.com/jackc/pgx/v5/pgtype"
)

const count = `-- name: Count :one
SELECT COUNT(*) FROM languages
`

func (q *Queries) Count(ctx context.Context) (int64, error) {
	row := q.db.QueryRow(ctx, count)
	var count int64
	err := row.Scan(&count)
	return count, err
}

const getID = `-- name: GetID :one
SELECT id FROM languages WHERE name=$1
`

func (q *Queries) GetID(ctx context.Context, name pgtype.Text) (uuid.UUID, error) {
	row := q.db.QueryRow(ctx, getID, name)
	var id uuid.UUID
	err := row.Scan(&id)
	return id, err
}

const keepOnly = `-- name: KeepOnly :exec
DELETE FROM languages WHERE NOT (id = ANY($1::UUID[]))
`

func (q *Queries) KeepOnly(ctx context.Context, ids []uuid.UUID) error {
	_, err := q.db.Exec(ctx, keepOnly, ids)
	return err
}

const list = `-- name: List :many
SELECT id, created_at, updated_at, name FROM languages OFFSET $1 LIMIT $2
`

type ListParams struct {
	Offset int32
	Limit  int32
}

func (q *Queries) List(ctx context.Context, arg ListParams) ([]Language, error) {
	rows, err := q.db.Query(ctx, list, arg.Offset, arg.Limit)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var items []Language
	for rows.Next() {
		var i Language
		if err := rows.Scan(
			&i.ID,
			&i.CreatedAt,
			&i.UpdatedAt,
			&i.Name,
		); err != nil {
			return nil, err
		}
		items = append(items, i)
	}
	if err := rows.Err(); err != nil {
		return nil, err
	}
	return items, nil
}

const upsert = `-- name: Upsert :exec
INSERT INTO languages (name) VALUES($1) ON CONFLICT (name) DO NOTHING
`

func (q *Queries) Upsert(ctx context.Context, name pgtype.Text) error {
	_, err := q.db.Exec(ctx, upsert, name)
	return err
}
