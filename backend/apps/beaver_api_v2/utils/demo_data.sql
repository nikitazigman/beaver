-- tags
INSERT INTO tags (name) VALUES('sort');
INSERT INTO tags (name) VALUES('hash');
INSERT INTO tags (name) VALUES('search');
-- languages
INSERT INTO languages (name) VALUES('python');
INSERT INTO languages (name) VALUES('go');
-- contributors
INSERT INTO contributors (name, last_name, email_address) VALUES('Nikita', 'Smirnov', 'smirnov@test.com');
INSERT INTO contributors (name, last_name, email_address) VALUES('Nikita', 'Zigman', 'zigman@test.com');
-- scripts python
INSERT INTO scripts (title, code, link_to_project, language_id) VALUES('test sort zigman python', 'print("hello world")', 'test.com', (SELECT id FROM languages WHERE name = 'python' LIMIT 1));
INSERT INTO scripts (title, code, link_to_project, language_id) VALUES('test hash zigman python', 'print("hello world")', 'test.com', (SELECT id FROM languages WHERE name = 'python' LIMIT 1));
INSERT INTO scripts (title, code, link_to_project, language_id) VALUES('test search zigman python', 'print("hello world")', 'test.com', (SELECT id FROM languages WHERE name = 'python' LIMIT 1));
INSERT INTO scripts (title, code, link_to_project, language_id) VALUES('test sort smirnov python', 'print("hello world")', 'test.com', (SELECT id FROM languages WHERE name = 'python' LIMIT 1));
INSERT INTO scripts (title, code, link_to_project, language_id) VALUES('test hash smirnov python', 'print("hello world")', 'test.com', (SELECT id FROM languages WHERE name = 'python' LIMIT 1));
INSERT INTO scripts (title, code, link_to_project, language_id) VALUES('test search smirnov python', 'print("hello world")', 'test.com', (SELECT id FROM languages WHERE name = 'python' LIMIT 1));
-- scripts go
INSERT INTO scripts (title, code, link_to_project, language_id) VALUES('test sort zigman go', 'print("hello world")', 'test.com', (SELECT id FROM languages WHERE name = 'go' LIMIT 1));
INSERT INTO scripts (title, code, link_to_project, language_id) VALUES('test hash zigman go', 'print("hello world")', 'test.com', (SELECT id FROM languages WHERE name = 'go' LIMIT 1));
INSERT INTO scripts (title, code, link_to_project, language_id) VALUES('test search zigman go', 'print("hello world")', 'test.com', (SELECT id FROM languages WHERE name = 'go' LIMIT 1));
INSERT INTO scripts (title, code, link_to_project, language_id) VALUES('test sort smirnov go', 'print("hello world")', 'test.com', (SELECT id FROM languages WHERE name = 'go' LIMIT 1));
INSERT INTO scripts (title, code, link_to_project, language_id) VALUES('test hash smirnov go', 'print("hello world")', 'test.com', (SELECT id FROM languages WHERE name = 'go' LIMIT 1));
INSERT INTO scripts (title, code, link_to_project, language_id) VALUES('test search smirnov go', 'print("hello world")', 'test.com', (SELECT id FROM languages WHERE name = 'go' LIMIT 1));
-- tags scripts python
INSERT INTO tags_scripts (tag_id, script_id) VALUES((SELECT id FROM tags WHERE name = 'sort' LIMIT 1), (SELECT id FROM scripts WHERE title = 'test sort zigman python' LIMIT 1));
INSERT INTO tags_scripts (tag_id, script_id) VALUES((SELECT id FROM tags WHERE name = 'hash' LIMIT 1), (SELECT id FROM scripts WHERE title = 'test hash zigman python' LIMIT 1));
INSERT INTO tags_scripts (tag_id, script_id) VALUES((SELECT id FROM tags WHERE name = 'search' LIMIT 1), (SELECT id FROM scripts WHERE title = 'test search zigman python' LIMIT 1));
INSERT INTO tags_scripts (tag_id, script_id) VALUES((SELECT id FROM tags WHERE name = 'sort' LIMIT 1), (SELECT id FROM scripts WHERE title = 'test sort smirnov python' LIMIT 1));
INSERT INTO tags_scripts (tag_id, script_id) VALUES((SELECT id FROM tags WHERE name = 'hash' LIMIT 1), (SELECT id FROM scripts WHERE title = 'test hash smirnov python' LIMIT 1));
INSERT INTO tags_scripts (tag_id, script_id) VALUES((SELECT id FROM tags WHERE name = 'search' LIMIT 1), (SELECT id FROM scripts WHERE title = 'test search smirnov python' LIMIT 1));
-- tags scripts go
INSERT INTO tags_scripts (tag_id, script_id) VALUES((SELECT id FROM tags WHERE name = 'sort' LIMIT 1), (SELECT id FROM scripts WHERE title = 'test sort zigman go' LIMIT 1));
INSERT INTO tags_scripts (tag_id, script_id) VALUES((SELECT id FROM tags WHERE name = 'hash' LIMIT 1), (SELECT id FROM scripts WHERE title = 'test hash zigman go' LIMIT 1));
INSERT INTO tags_scripts (tag_id, script_id) VALUES((SELECT id FROM tags WHERE name = 'search' LIMIT 1), (SELECT id FROM scripts WHERE title = 'test search zigman go' LIMIT 1));
INSERT INTO tags_scripts (tag_id, script_id) VALUES((SELECT id FROM tags WHERE name = 'sort' LIMIT 1), (SELECT id FROM scripts WHERE title = 'test sort smirnov go' LIMIT 1));
INSERT INTO tags_scripts (tag_id, script_id) VALUES((SELECT id FROM tags WHERE name = 'hash' LIMIT 1), (SELECT id FROM scripts WHERE title = 'test hash smirnov go' LIMIT 1));
INSERT INTO tags_scripts (tag_id, script_id) VALUES((SELECT id FROM tags WHERE name = 'search' LIMIT 1), (SELECT id FROM scripts WHERE title = 'test search smirnov go' LIMIT 1));
-- contributors scripts
INSERT INTO contributors_scripts (contributor_id, script_id) VALUES((SELECT id FROM contributors WHERE last_name = 'Zigman' LIMIT 1), (SELECT id FROM scripts WHERE title = 'test sort zigman go' LIMIT 1));
INSERT INTO contributors_scripts (contributor_id, script_id) VALUES((SELECT id FROM contributors WHERE last_name = 'Zigman' LIMIT 1), (SELECT id FROM scripts WHERE title = 'test hash zigman go' LIMIT 1));
INSERT INTO contributors_scripts (contributor_id, script_id) VALUES((SELECT id FROM contributors WHERE last_name = 'Zigman' LIMIT 1), (SELECT id FROM scripts WHERE title = 'test search zigman go' LIMIT 1));
INSERT INTO contributors_scripts (contributor_id, script_id) VALUES((SELECT id FROM contributors WHERE last_name = 'Zigman' LIMIT 1), (SELECT id FROM scripts WHERE title = 'test sort zigman python' LIMIT 1));
INSERT INTO contributors_scripts (contributor_id, script_id) VALUES((SELECT id FROM contributors WHERE last_name = 'Zigman' LIMIT 1), (SELECT id FROM scripts WHERE title = 'test hash zigman python' LIMIT 1));
INSERT INTO contributors_scripts (contributor_id, script_id) VALUES((SELECT id FROM contributors WHERE last_name = 'Zigman' LIMIT 1), (SELECT id FROM scripts WHERE title = 'test search zigman python' LIMIT 1));
INSERT INTO contributors_scripts (contributor_id, script_id) VALUES((SELECT id FROM contributors WHERE last_name = 'Smirnov' LIMIT 1), (SELECT id FROM scripts WHERE title = 'test sort smirnov go' LIMIT 1));
INSERT INTO contributors_scripts (contributor_id, script_id) VALUES((SELECT id FROM contributors WHERE last_name = 'Smirnov' LIMIT 1), (SELECT id FROM scripts WHERE title = 'test hash smirnov go' LIMIT 1));
INSERT INTO contributors_scripts (contributor_id, script_id) VALUES((SELECT id FROM contributors WHERE last_name = 'Smirnov' LIMIT 1), (SELECT id FROM scripts WHERE title = 'test search smirnov go' LIMIT 1));
INSERT INTO contributors_scripts (contributor_id, script_id) VALUES((SELECT id FROM contributors WHERE last_name = 'Smirnov' LIMIT 1), (SELECT id FROM scripts WHERE title = 'test sort smirnov python' LIMIT 1));
INSERT INTO contributors_scripts (contributor_id, script_id) VALUES((SELECT id FROM contributors WHERE last_name = 'Smirnov' LIMIT 1), (SELECT id FROM scripts WHERE title = 'test hash smirnov python' LIMIT 1));
INSERT INTO contributors_scripts (contributor_id, script_id) VALUES((SELECT id FROM contributors WHERE last_name = 'Smirnov' LIMIT 1), (SELECT id FROM scripts WHERE title = 'test search smirnov python' LIMIT 1));
