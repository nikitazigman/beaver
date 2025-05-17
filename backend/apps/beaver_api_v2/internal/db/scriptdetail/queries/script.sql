
-- name: Random :many
SELECT * FROM scripts_details
WHERE script_id = (
SELECT script_id FROM scripts_details AS sd
    WHERE
        (sd.tag_name = ANY(sqlc.narg('tags')::varchar[]) OR sqlc.narg('tags') IS NULL) AND
        (sd.contributor_email_address = ANY(sqlc.narg('contribs')::varchar[]) OR sqlc.narg('contribs') IS NULL) AND
        (sd.language_name = ANY(sqlc.narg('langs')::varchar[]) OR sqlc.narg('langs') IS NULL)
    ORDER BY RANDOM()
    LIMIT 1
);
