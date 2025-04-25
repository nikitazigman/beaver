
-- name: ListLanguages :many
SELECT * FROM languages OFFSET $1 LIMIT $2;

-- name: UpsertLanguages :batchexec
INSERT INTO languages (name) VALUES($1) ON CONFLICT (id) DO NOTHING;

-- name: DeleteLanguages :batchexec
DELETE FROM languages WHERE id = $1;
