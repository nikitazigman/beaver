
-- name: Count :one
SELECT COUNT(*) FROM scripts_details WHERE tag_id = $1 AND contributor_id = $2 AND language_id = $3;

-- name: GetDetailedScript :one
SELECT * FROM scripts_details OFFSET $1 LIMIT 1;
