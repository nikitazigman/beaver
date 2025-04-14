-- +goose Up
-- +goose StatementBegin
CREATE TABLE contributors(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE,

    name VARCHAR(255),
    last_name VARCHAR(255),
    email_address VARCHAR(1024)
);
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
DROP TABLE contributors;
-- +goose StatementEnd
