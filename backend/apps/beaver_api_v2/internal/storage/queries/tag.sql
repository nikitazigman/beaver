
-- name: ListTags :many
SELECT * FROM tags OFFSET $1 LIMIT $2;

-- name: CreateTags :batchexec
INSERT INTO tags (name) VALUES($1);

-- name: DeleteTags :batchexec
DELETE FROM tags WHERE id = $1;
