ALTER TABLE todos RENAME TO temp_table;

CREATE TABLE todos (id INTEGER PRIMARY KEY, user_id INT (11) NOT NULL, description VARCHAR (255), completed BOOLEAN, FOREIGN KEY (user_id) REFERENCES users (id));

INSERT INTO todos (id, user_id, description) SELECT id, user_id, description FROM temp_table;

DROP TABLE temp_table;
