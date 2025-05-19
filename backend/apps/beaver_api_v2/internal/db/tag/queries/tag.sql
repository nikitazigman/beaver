
-- name: List :many
SELECT * FROM tags OFFSET $1 LIMIT $2;

-- name: Upsert :exec
INSERT INTO tags (name) VALUES($1) ON CONFLICT (name) DO NOTHING;

-- name: GetID :one
SELECT id FROM tags WHERE name=$1;

-- name: KeepOnly :exec
DELETE FROM tags WHERE NOT (id = ANY(sqlc.narg('ids')::UUID[]));

-- name: Count :one
SELECT COUNT(*) FROM tags;
