
-- name: List :many
SELECT * FROM languages OFFSET $1 LIMIT $2;

-- name: Upsert :exec
INSERT INTO languages (name) VALUES($1) ON CONFLICT (name) DO NOTHING;

-- name: GetID :one
SELECT id FROM languages WHERE name=$1;

-- name: KeepOnly :exec
DELETE FROM languages WHERE NOT (id = ANY(sqlc.narg('ids')::UUID[])) ;

-- name: Count :one
SELECT COUNT(*) FROM languages;
