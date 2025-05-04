
-- name: Random :many
SELECT * FROM scripts_details
WHERE script_id = (
SELECT script_id FROM scripts_details AS sd
    WHERE
        (sd.tag_id = ANY(sqlc.narg('tagIDs')::uuid[]) OR sqlc.narg('tagIDs') IS NULL) AND
        (sd.contributor_id = ANY(sqlc.narg('contribIDs')::uuid[]) OR sqlc.narg('contribIDs') IS NULL) AND
        (sd.language_id = sqlc.narg('languageID')::uuid OR sqlc.narg('languageID') IS NULL)
    ORDER BY RANDOM()
    LIMIT 1
);
