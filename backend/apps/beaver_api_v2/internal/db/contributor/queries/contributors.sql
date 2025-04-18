
-- name: ListContributors :many
SELECT * FROM contributors OFFSET $1 LIMIT $2;

-- name: CreateContributors :batchexec
INSERT INTO contributors (name, last_name, email_address) VALUES($1, $2, $3);

-- name: DeleteContributors :batchexec
DELETE FROM contributors WHERE id = $1;
