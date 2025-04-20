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
-- scripts
INSERT INTO scripts (title, code, link_to_project, language_id) VALUES('script sort python Zigman', 'print("hello world")', 'test.com', (SELECT id FROM languages WHERE name = 'python' LIMIT 1));
INSERT INTO scripts (title, code, link_to_project, language_id) VALUES('script sort hash search python Zigman Smirnov', 'print("hello world")', 'test.com', (SELECT id FROM languages WHERE name = 'python' LIMIT 1));
INSERT INTO scripts (title, code, link_to_project, language_id) VALUES('script sort go Zigman', 'print("hello world")', 'test.com', (SELECT id FROM languages WHERE name = 'go' LIMIT 1));
-- tags scripts python
INSERT INTO tags_scripts (tag_id, script_id) VALUES((SELECT id FROM tags WHERE name = 'sort' LIMIT 1), (SELECT id FROM scripts WHERE title = 'script sort python Zigman' LIMIT 1));
INSERT INTO tags_scripts (tag_id, script_id) VALUES((SELECT id FROM tags WHERE name = 'sort' LIMIT 1), (SELECT id FROM scripts WHERE title = 'script sort hash search python Zigman Smirnov' LIMIT 1));
INSERT INTO tags_scripts (tag_id, script_id) VALUES((SELECT id FROM tags WHERE name = 'hash' LIMIT 1), (SELECT id FROM scripts WHERE title = 'script sort hash search python Zigman Smirnov' LIMIT 1));
INSERT INTO tags_scripts (tag_id, script_id) VALUES((SELECT id FROM tags WHERE name = 'search' LIMIT 1), (SELECT id FROM scripts WHERE title = 'script sort hash search python Zigman Smirnov' LIMIT 1));
INSERT INTO tags_scripts (tag_id, script_id) VALUES((SELECT id FROM tags WHERE name = 'sort' LIMIT 1), (SELECT id FROM scripts WHERE title = 'script sort go Zigman' LIMIT 1));
-- contributors scripts
INSERT INTO contributors_scripts (contributor_id, script_id) VALUES((SELECT id FROM contributors WHERE last_name = 'Zigman' LIMIT 1), (SELECT id FROM scripts WHERE title = 'script sort python Zigman' LIMIT 1));
INSERT INTO contributors_scripts (contributor_id, script_id) VALUES((SELECT id FROM contributors WHERE last_name = 'Zigman' LIMIT 1), (SELECT id FROM scripts WHERE title = 'script sort hash search python Zigman Smirnov' LIMIT 1));
INSERT INTO contributors_scripts (contributor_id, script_id) VALUES((SELECT id FROM contributors WHERE last_name = 'Smirnov' LIMIT 1), (SELECT id FROM scripts WHERE title = 'script sort hash search python Zigman Smirnov' LIMIT 1));
INSERT INTO contributors_scripts (contributor_id, script_id) VALUES((SELECT id FROM contributors WHERE last_name = 'Zigman' LIMIT 1), (SELECT id FROM scripts WHERE title = 'script sort go Zigman' LIMIT 1));
