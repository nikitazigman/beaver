
-- name: ListContributors :many
SELECT * FROM contributors OFFSET $1 LIMIT $2;

-- name: UpsertContributors :batchexec
INSERT INTO contributors (name, last_name, email_address) VALUES($1, $2, $3) ON CONFLICT (id) DO NOTHING;

-- name: DeleteContributors :batchexec
DELETE FROM contributors WHERE id = $1;
