PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE users (
        id INTEGER NOT NULL,
        login_id VARCHAR(50),
        password VARCHAR(50),
        name VARCHAR(50),
        email VARCHAR(120),
        is_active VARCHAR(1),
        created_on DATETIME,
        created_by INTEGER,
        updated_on DATETIME,
        updated_by INTEGER,
        PRIMARY KEY (id),
        UNIQUE (login_id),
        UNIQUE (email)
);
INSERT INTO users VALUES(1,'admin','admin','admin','admin@localhost','Y','2007-01-01 10:00:00',1,'2007-01-01 10:00:00',1);
CREATE TABLE roles (
        id INTEGER NOT NULL,
        name VARCHAR(50),
        PRIMARY KEY (id),
        UNIQUE (name)
);
INSERT INTO roles VALUES(1,'admin');
INSERT INTO roles VALUES(2,'user');
CREATE TABLE user_role_maps (
        user_id INTEGER NOT NULL,
        role_id INTEGER NOT NULL,
        UNIQUE (user_id,role_id)
);
INSERT INTO user_role_maps VALUES(1,1);
CREATE TABLE modules (
        id INTEGER NOT NULL,
        name VARCHAR(50),
        PRIMARY KEY (id),
        UNIQUE (name)
);
INSERT INTO modules VALUES(1,'Users');
INSERT INTO modules VALUES(2,'Roles');
CREATE TABLE role_module_permissions (
        role_id INTEGER NOT NULL,
        module_id INTEGER NOT NULL,
        view_flag VARCHAR(1),
        create_flag VARCHAR(1),
        modify_flag VARCHAR(1),
        delete_flag VARCHAR(1),
        upload_flag VARCHAR(1),
        download_flag VARCHAR(1),
        PRIMARY KEY (role_id,module_id)
);
INSERT INTO role_module_permissions VALUES(1,1,'Y','Y','Y','Y','Y','Y');
INSERT INTO role_module_permissions VALUES(1,2,'Y','Y','Y','Y','Y','Y');
INSERT INTO role_module_permissions VALUES(2,1,'Y','Y','Y','Y','Y','Y');
COMMIT;