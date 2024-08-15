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

<img width="467" alt="image" src="https://github.com/user-attachments/assets/f0ca14c7-65fb-4c06-a2f2-b8d4f7626c28">

## Items Table

| Column Name | Type |
| :---: | :---: | 
| item_id | INT auto_increment KEY |
| item_name | VARCHAR(255) NOT NULL |
| unit | VARCHAR(50) |
| rate | DECIMAL(10, 2) NOT NULL |

<img width="179" alt="image" src="https://github.com/user-attachments/assets/f78f7f48-828a-4f3e-a45d-1c7354ab16f7">

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

<img width="405" alt="image" src="https://github.com/user-attachments/assets/6647d6de-fed3-492c-aab9-e50482b96d4e">

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

<img width="306" alt="image" src="https://github.com/user-attachments/assets/1746a9e7-dbfe-4d25-b8c7-2a1f54a65a0c">

# Implementation Details
## Main Page

<img width="479" alt="image" src="https://github.com/user-attachments/assets/7b476da0-dc65-4ab6-af5f-861a37bfa9fd">

This main page consists of buttons for adding a customer, adding an invoice, viewing all invoices, viewing paid and unpaid invoices, viewing customer details, searching customer invoices, and viewing reports

## Add Customer

<img width="473" alt="image" src="https://github.com/user-attachments/assets/3265d501-de02-4bb4-a5e3-4f017def7122">
<img width="479" alt="image" src="https://github.com/user-attachments/assets/55a4b02f-d386-4c1a-834f-90ab1f3c0302">

## Add Invoice

<img width="543" alt="image" src="https://github.com/user-attachments/assets/2f83f878-eebe-4906-96a6-341bbdf92f97">
<img width="479" alt="image" src="https://github.com/user-attachments/assets/d4aa2bc6-f135-4c7a-a598-d3d81ac170e6">

## View all Invoices

<img width="949" alt="image" src="https://github.com/user-attachments/assets/1258a644-5518-4cd7-b7e7-e6f4e6c5da4e">

## View Unpaid Invoices

<img width="954" alt="image" src="https://github.com/user-attachments/assets/7510ed2b-9c4b-43ed-b807-669deee73729">

## View Paid Invoices

<img width="955" alt="image" src="https://github.com/user-attachments/assets/69dc9ffa-7e98-43f6-8f34-a1fc6029fe15">

## Search Customer Invoices

<img width="497" alt="image" src="https://github.com/user-attachments/assets/500086db-859b-49dd-99de-39af74ff9570">

## Customer Details

<img width="494" alt="image" src="https://github.com/user-attachments/assets/b0e13980-c989-461d-b552-7c8f5529c4ea">

## View Report
## Invoice Status Count

<img width="279" alt="image" src="https://github.com/user-attachments/assets/0b5c61ea-5392-47c5-97b4-796bbe43f960">

## Sales Count by Product

<img width="281" alt="image" src="https://github.com/user-attachments/assets/eaabb77f-27b0-4611-9e03-4241465c790f">






