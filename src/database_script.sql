CREATE TABLE Customer (
    customer_id INT PRIMARY KEY, 
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(15)
);

CREATE TABLE Account (
    account_id INT PRIMARY KEY,  
    customer_id INT,
    account_type VARCHAR(50),
    balance DECIMAL(10,2),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
);

CREATE TABLE Transaction (
    transaction_id INT PRIMARY KEY,
    account_id INT NOT NULL,
    transaction_type VARCHAR(50),
    amount DECIMAL(10,2),
    transaction_date DATE,
    FOREIGN KEY (account_id) REFERENCES Account(account_id)
);


INSERT INTO Customer (customer_id, name, email, phone)
VALUES (1, 'abc', 'abc@gmail.com', '9876543210');

INSERT INTO Customer (customer_id, name, email, phone)
VALUES (2, 'rst', 'rst@gmail.com', '9123456789');


INSERT INTO Account (account_id, customer_id, account_type, balance)
VALUES 
    (101, 1, 'Savings', 5000.00),
    (102, 1, 'Current', 2000.00),
    (103, 2, 'Savings', 7000.00),
    (104, 2, 'Current', 1500.00);


INSERT INTO Transaction (transaction_id, account_id, transaction_type, amount, transaction_date) VALUES
(1001, 101, 'Deposit', 500.00, '2025-03-15'),
(1002, 101, 'Withdrawal', 200.00, '2025-02-10'),
(1003, 101, 'Deposit', 300.00, '2025-01-20'),
(1004, 101, 'Withdrawal', 150.00, '2025-04-05'),
(1005, 101, 'Deposit', 450.00, '2025-03-08');

INSERT INTO Transaction (transaction_id, account_id, transaction_type, amount, transaction_date) VALUES
(1006, 102, 'Deposit', 700.00, '2025-03-18'),
(1007, 102, 'Withdrawal', 250.00, '2025-02-28'),
(1008, 102, 'Deposit', 600.00, '2025-01-25'),
(1009, 102, 'Withdrawal', 350.00, '2025-04-01'),
(1010, 102, 'Deposit', 400.00, '2025-03-11');

INSERT INTO Transaction (transaction_id, account_id, transaction_type, amount, transaction_date) VALUES
(1011, 103, 'Deposit', 800.00, '2025-03-03'),
(1012, 103, 'Withdrawal', 300.00, '2025-02-20'),
(1013, 103, 'Deposit', 700.00, '2025-01-15'),
(1014, 103, 'Withdrawal', 250.00, '2025-04-10'),
(1015, 103, 'Deposit', 900.00, '2025-03-20');

INSERT INTO Transaction (transaction_id, account_id, transaction_type, amount, transaction_date) VALUES
(1016, 104, 'Deposit', 900.00, '2025-03-05'),
(1017, 104, 'Withdrawal', 400.00, '2025-02-14'),
(1018, 104, 'Deposit', 500.00, '2025-01-28'),
(1019, 104, 'Withdrawal', 450.00, '2025-04-07'),
(1020, 104, 'Deposit', 600.00, '2025-03-25');