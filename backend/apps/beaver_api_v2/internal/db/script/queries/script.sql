-- name: UpsertScripts :batchexec
INSERT INTO scripts (title, code, link_to_project, language_id) VALUES($1, $2, $3, $4) ON CONFLICT (id) DO NOTHING;

-- name: DeleteScripts :batchexec
DELETE FROM scripts WHERE id = $1;

-- name: GetTagScriptIDs :many
SELECT id from tags_scripts WHERE id = ANY(sqlc.arg('ids')::UUID[]);

-- name: LinkTags :batchexec
INSERT INTO tags_scripts (tag_id, script_id) VALUES($1, $2) ON CONFLICT (id) DO NOTHING;

-- name: UnlinkTags :batchexec
DELETE FROM tags_scripts WHERE id = $1;

-- name: LinkContributors :batchexec
INSERT INTO contributors_scripts (contributor_id, script_id) VALUES($1, $2) ON CONFLICT (id) DO NOTHING;

-- name: UnlinkContributors :batchexec
DELETE FROM contributors_scripts WHERE id = $1;
