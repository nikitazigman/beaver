
-- name: ListLanguages :many
SELECT * FROM languages OFFSET $1 LIMIT $2;

-- name: CreateLanguages :batchexec
INSERT INTO languages (name) VALUES($1);

-- name: DeleteLanguages :batchexec
DELETE FROM languages WHERE id = $1;
