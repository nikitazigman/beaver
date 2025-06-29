-- +goose Up
-- +goose StatementBegin
CREATE TABLE scripts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE,

    title VARCHAR(255) UNIQUE,
    code TEXT,
    link_to_project VARCHAR(1024),
    language_id UUID REFERENCES languages(id) ON DELETE SET NULL
);

CREATE TABLE tags_scripts(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    tag_id UUID REFERENCES tags(id) ON DELETE CASCADE,
    script_id UUID REFERENCES scripts(id) ON DELETE CASCADE,

    UNIQUE(tag_id, script_id)
);

CREATE TABLE contributors_scripts(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    contributor_id UUID REFERENCES contributors(id) ON DELETE CASCADE,
    script_id UUID REFERENCES scripts(id) ON DELETE CASCADE,

    UNIQUE(contributor_id, script_id)
);
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
DROP TABLE contributors_scripts;
DROP TABLE tags_scripts;
DROP TABLE scripts;
-- +goose StatementEnd
