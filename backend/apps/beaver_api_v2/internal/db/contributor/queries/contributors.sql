
-- name: List :many
SELECT * FROM contributors OFFSET $1 LIMIT $2;

-- name: Upsert :exec
INSERT INTO contributors (name, last_name, email_address) VALUES($1, $2, $3) ON CONFLICT (email_address) DO NOTHING;

-- name: GetID :one
SELECT id FROM contributors WHERE email_address=$1;

-- name: Delete :batchexec
DELETE FROM contributors WHERE id = $1;
