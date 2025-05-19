-- name: Upsert :exec
INSERT INTO scripts (title, code, link_to_project, language_id, created_at) VALUES($1, $2, $3, $4, $5)
ON CONFLICT (title) DO UPDATE SET created_at = EXCLUDED.created_at;

-- name: GetID :one
SELECT id FROM scripts WHERE title=$1;

-- name: Languages :many
SELECT DISTINCT(language_id) from scripts;

-- name: Delete :exec
DELETE FROM scripts WHERE created_at < $1;

-- name: LinkTag :exec
INSERT INTO tags_scripts (tag_id, script_id) VALUES($1, $2) ON CONFLICT (tag_id, script_id) DO NOTHING;

-- name: LinkedTags :many
SELECT DISTINCT(tag_id) FROM tags_scripts;

-- name: LinkContrib :exec
INSERT INTO contributors_scripts (contributor_id, script_id) VALUES($1, $2) ON CONFLICT (contributor_id, script_id) DO NOTHING;

-- name: LinkedContributors :many
SELECT DISTINCT(contributor_id) FROM contributors_scripts;
