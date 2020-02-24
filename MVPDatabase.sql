CREATE TABLE IF NOT EXISTS mvp_table(
    hunt_id INT PRIMARY KEY AUTO_INCREMENT,
    node_number INT NOT NULL,
    question_text VARCHAR(255),
    answer VARCHAR (25)
)

INSERT INTO mvp_table (node_number, question_text, answer)
VALUES(
    1, 'How many computers are there in the LoveLace room?','37' 

);

INSERT INTO mvp_table (node_number, question_text, answer)
VALUES(
    2, 'Which lab in the innovation center has Windows PC?','Babbage' 

);

INSERT INTO mvp_table (node_number, question_text, answer)
VALUES(
    3, 'How much are the rice dishes for students at the innovation cafe?','4.50' 

);

INSERT INTO mvp_table (node_number, question_text, answer)
VALUES(
    4, 'How many floors does the Harrison Building have?','4' 

);
