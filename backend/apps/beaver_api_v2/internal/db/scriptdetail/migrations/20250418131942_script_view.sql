-- +goose Up
-- +goose StatementBegin
CREATE OR REPLACE VIEW scripts_details AS
SELECT
    scripts.id as script_id,
    scripts.title as script_title,
    scripts.code as script_code ,
    scripts.link_to_project as script_link_to_project,
    languages.id as language_id,
    languages.name as language_name,
    tags.id as tag_id,
    tags.name as tag_name,
    contributors.id as contributor_id,
    contributors.name as contributor_name,
    contributors.last_name as contributor_last_name,
    contributors.email_address as contributor_email_address
FROM scripts
JOIN languages ON languages.id = scripts.language_id
JOIN tags_scripts ON tags_scripts.script_id = scripts.id
JOIN tags ON tags.id = tags_scripts.tag_id
JOIN contributors_scripts ON contributors_scripts.script_id = scripts.id
JOIN contributors ON contributors.id = contributors_scripts.contributor_id;
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
DROP VIEW scripts_detail;
-- +goose StatementEnd
