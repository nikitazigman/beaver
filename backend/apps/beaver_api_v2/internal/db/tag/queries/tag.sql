
-- name: ListTags :many
SELECT * FROM tags OFFSET $1 LIMIT $2;


-- name: UpsertTags :batchexec
INSERT INTO tags (name) VALUES($1) ON CONFLICT (id) DO NOTHING;

-- name: DeleteTags :batchexec
DELETE FROM tags WHERE id = $1;
