
-- name: CreateScripts :batchexec
INSERT INTO scripts (title, code, link_to_project, language_id) VALUES($1, $2, $3, $4);

-- name: DeleteScripts :batchexec
DELETE FROM scripts WHERE id = $1;

-- name: AddTags :batchexec
INSERT INTO tags_scripts (tag_id, script_id) VALUES($1, $2);

-- name: RemoveTags :batchexec
DELETE FROM tags_scripts WHERE id = $1;

-- name: AddContributors :batchexec
INSERT INTO contributors_scripts (contributor_id, script_id) VALUES($1, $2);

-- name: RemoveContributors :batchexec
DELETE FROM contributors_scripts WHERE id = $1;
