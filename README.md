# Invoice-Management
This application generates invoices for a store with item details like name, quantity, unit, rate, and price, applying a 10% discount on the total price. It supports multiple customers and invoices, allowing searches by customer ID to display all associated invoices. Additionally, it provides features to view all invoices, paid invoices, customer balances, invoice details, and item sales.

## Database Schema
## Customer Table

| Column Name | Type |
| :---: | :---: | 
| customer_id | INT PRIMARY KEY |
| customer_name | VARCHAR(255) NOT NULL |
| contact_number | VARCHAR(20) |
| email | VARCHAR(255) |
| address | TEXT |

## Items Table

| Column Name | Type |
| :---: | :---: | 
| item_id | INT auto_increment KEY |
| item_name | VARCHAR(255) NOT NULL |
| unit | VARCHAR(50) |
| rate | DECIMAL(10, 2) NOT NULL |

## Invoices Table

| Column Name| Type |
| :---: | :---: | 
| invoice_id | INT auto_increment PRIMARY KEY |
| customer_id | INT |
| invoice_date | DATE |
| total_amount | DECIMAL(10, 2) |
| discount_amount | DECIMAL(10, 2) |
| final_amount | DECIMAL(10, 2) |
| status | ENUM('Paid', 'Unpaid') NOT NULL |
| FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) | 

## Invoice Items

| Column Name | Type |
| :---: | :---: | 
| invoice_item_id | INT AUTO_INCREMENT PRIMARY KEY |
| invoice_id | INT |
| item_name | VARCHAR(255) NOT NULL |
| quantity | INT |
| rate | DECIMAL(10, 2) |
| unit| VARCHAR(50) |
| FOREIGN KEY (invoice_id) REFERENCES Invoices(invoice_id) | 

# Implementation Details
## Main Page

<img width="479" alt="image" src="https://github.com/user-attachments/assets/7b476da0-dc65-4ab6-af5f-861a37bfa9fd">

