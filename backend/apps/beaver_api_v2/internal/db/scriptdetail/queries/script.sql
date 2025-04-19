
-- name: Count :one
SELECT COUNT(*) FROM scripts_details
WHERE
    (tag_id = sqlc.narg('tagID') OR sqlc.narg('tagID') IS NULL) AND
    (contributor_id = sqlc.narg('contributorID') OR sqlc.narg('contributorID') IS NULL) AND
    (language_id = sqlc.narg('languageID') OR sqlc.narg('languageID') IS NULL);


-- name: GetDetailedScript :one
SELECT * FROM scripts_details OFFSET $1 LIMIT 1;
