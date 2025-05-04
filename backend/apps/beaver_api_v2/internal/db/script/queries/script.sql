-- name: Upsert :exec
INSERT INTO scripts (title, code, link_to_project, language_id) VALUES($1, $2, $3, $4) ON CONFLICT (title) DO NOTHING;

-- name: GetID :one
SELECT id FROM scripts WHERE title=$1;

-- name: Delete :batchexec
DELETE FROM scripts WHERE id = $1;

-- name: LinkTag :exec
INSERT INTO tags_scripts (tag_id, script_id) VALUES($1, $2) ON CONFLICT (tag_id, script_id) DO NOTHING;

-- name: UnlinkTags :batchexec
DELETE FROM tags_scripts WHERE id = $1;

-- name: LinkContrib :exec
INSERT INTO contributors_scripts (contributor_id, script_id) VALUES($1, $2) ON CONFLICT (contributor_id, script_id) DO NOTHING;

-- name: UnlinkContributors :batchexec
DELETE FROM contributors_scripts WHERE id = $1;
