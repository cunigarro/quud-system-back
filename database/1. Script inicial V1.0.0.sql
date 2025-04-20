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


CREATE TABLE rule_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE TABLE rules (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL, 
    description TEXT NOT NULL,
    rule_type_id INT REFERENCES rule_types(id) ON DELETE SET NULL,
    execution_params JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE TABLE rule_groups (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    owner_id INT REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE TABLE rule_group_rules (
    id SERIAL PRIMARY KEY,
    rule_id INT NOT NULL REFERENCES rules(id) ON DELETE CASCADE,
    group_id INT NOT NULL REFERENCES rule_groups(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE inspection_status (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) not null
);

CREATE TABLE inspections (
    id SERIAL PRIMARY KEY,
    branch VARCHAR(100),
    project_id INT REFERENCES projects(id) ON DELETE CASCADE,
    rule_group_id INT REFERENCES rule_groups(id) ON DELETE SET NULL,
    inspection_status_id INT REFERENCES rule_groups(id) ON DELETE SET NULL,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    result JSONB,
    execute_steps JSONB,
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

INSERT INTO rule_types (name) VALUES 
('readability'),
('maintainability'),
('adherence_to_paradigm'),
('adherence_to_standards'),
('efficiency');

INSERT INTO rules (name, description, rule_type_id, execution_params) VALUES 
('Required Classes', 'At least one class is required in the project', 3, '{}'),
('Implementation of all clasess', 'The classes that are defined must be used', 3, '{}');


INSERT INTO inspection_status (name) VALUES
('init'),
('processing'),
('completed'),
('error');

ALTER TABLE rules
RENAME COLUMN execution_params TO flow_config;

ALTER TABLE rule_groups
ADD COLUMN flow_config JSON;

update rules set flow_config = '{
    "init_flow": [
        {
            "name": "required_classes",
            "settings": {}
        }
    ]
}' where id = 1;


update rules set flow_config = '{
    "init_flow": [
        {
            "name": "implementation_all_classes",
            "settings": {}
        }
    ]
}' where id = 2;


ALTER TABLE inspections
ADD COLUMN history_status JSON;


ALTER TABLE inspections
RENAME COLUMN execute_steps TO execution_info;

ALTER TABLE inspections
ADD COLUMN notification_info JSON;


ALTER TABLE inspections
ADD COLUMN owner_id INT REFERENCES users(id) ON DELETE CASCADE;

ALTER TABLE inspections
ADD COLUMN error TEXT;

update rule_types set name = 'portability' where id = 4;

ALTER TABLE rule_groups
ADD COLUMN attributes_weights JSON;

ALTER TABLE rule_groups
ADD COLUMN paradigm_weights JSON;




CREATE TYPE rule_dimension AS ENUM ('attribute', 'paradigm');
ALTER TABLE rule_types ADD COLUMN dimension rule_dimension;

update rule_types set dimension = 'attribute' where id in (1,2,4,5);
update rule_types set dimension = 'paradigm', name = 'POO_inheritance' where id in (3);


INSERT INTO rule_types (name, dimension) VALUES 
('POO_polimorfism', 'paradigm'),
('POO_encapsulation', 'paradigm'),
('POO_abstraction', 'paradigm');

ALTER TABLE rule_groups
ADD COLUMN alfa REAL;

ALTER TABLE inspections
ADD COLUMN total_score REAL;

ALTER TABLE inspections
ADD COLUMN total_paradigm REAL;

ALTER TABLE inspections
ADD COLUMN total_attributes REAL;


CREATE TABLE inspection_rule (
    id SERIAL PRIMARY KEY,
    inspection_id INT REFERENCES inspections(id) ON DELETE CASCADE,
    rule_id INT REFERENCES rules(id) ON DELETE SET NULL,
    calification REAL,
    comment JSON
);