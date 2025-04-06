-- create database quud;
-- use quud;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    names VARCHAR(100) NOT NULL,
    last_names VARCHAR(100) NOT NULL,
    cellphone VARCHAR(20),
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE TABLE languages (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    uuid UUID NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE TABLE language_versions (
    id SERIAL PRIMARY KEY,
    language_id INT REFERENCES languages(id) ON DELETE CASCADE,
    version TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    owner_id INT REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    url VARCHAR(255),
    language_id INT REFERENCES languages(id) ON DELETE SET NULL,
    language_version_id INT REFERENCES language_versions(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE TABLE criteria (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    params JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE TABLE quality_rules (
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE TABLE quality_rule_criteria (
    quality_rule_id INT REFERENCES quality_rules(id) ON DELETE CASCADE,
    criteria_id INT REFERENCES criteria(id) ON DELETE CASCADE,
    PRIMARY KEY (quality_rule_id, criteria_id)
);

CREATE TABLE inspections (
    id SERIAL PRIMARY KEY,
    project_id INT REFERENCES projects(id) ON DELETE CASCADE,
    branch VARCHAR(100),
    quality_rule_id INT REFERENCES quality_rules(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);


INSERT INTO languages (name, uuid) VALUES 
('Python', 'b6f7d3c7-2e44-4f4e-88d4-1b635b1e1c1f'),
('Java', '7b1a8d9a-5a43-47a6-bc9f-2fabe94c7c9f'),
('JavaScript', 'fa5f9ad7-19f4-42b7-9bde-6cf6480f243d');


INSERT INTO language_versions (language_id, version) VALUES 
(1, '3.6'),
(1, '3.7'),
(1, '3.8'),
(1, '3.9'),
(1, '3.10');


INSERT INTO language_versions (language_id, version) VALUES 
(2, '8'),
(2, '11'),
(2, '15'),
(2, '17');

INSERT INTO language_versions (language_id, version) VALUES 
(3, 'ES5'),
(3, 'ES6'),
(3, 'ES7'),
(3, 'ES8');

ALTER TABLE users ADD COLUMN profile_metadata JSONB;