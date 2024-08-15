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

The main page features buttons that allow users to add new customers and invoices, making it easy to manage store transactions. Users can view all invoices, as well as filter by paid and unpaid invoices, ensuring comprehensive tracking. Additionally, the page provides options to view customer details, search for specific customer invoices, and generate reports for analysis.

## Add Customer

<img width="473" alt="image" src="https://github.com/user-attachments/assets/3265d501-de02-4bb4-a5e3-4f017def7122">

This frame prompts the user to enter customer details, including customer ID, name, phone number, address, and email. A note is prominently displayed in the frame, indicating that the customer ID should be numerical only. Input fields are provided for each detail, ensuring that users can easily fill in the required information. Validation checks are implemented to ensure that only numerical values are accepted for the customer ID, preventing errors during data entry.

<img width="479" alt="image" src="https://github.com/user-attachments/assets/55a4b02f-d386-4c1a-834f-90ab1f3c0302">

After entering the customer details, a "Customer added successfully" prompt will confirm that the information has been saved. The system then securely stores the newly entered customer details in the *Customers* database, ensuring that all relevant information is recorded. This process updates the database with the latest customer data for future reference and transactions.

## Add Invoice

<img width="543" alt="image" src="https://github.com/user-attachments/assets/2f83f878-eebe-4906-96a6-341bbdf92f97">

Once the customer details are entered, the next step is to add invoice details through the "Add Invoice" tab. This tab requires you to input the customer ID, invoice date, and payment status (paid or unpaid). You can then add items to the invoice by specifying the item name, quantity, rate, and unit type, such as piece, pair, box, or set.

<img width="479" alt="image" src="https://github.com/user-attachments/assets/d4aa2bc6-f135-4c7a-a598-d3d81ac170e6">

After entering the relevant details, a prompt will confirm "Invoice added successfully." The system then stores the invoice in the database, ensuring all information is securely saved.

## View all Invoices

<img width="949" alt="image" src="https://github.com/user-attachments/assets/1258a644-5518-4cd7-b7e7-e6f4e6c5da4e">

## View Unpaid Invoices

<img width="954" alt="image" src="https://github.com/user-attachments/assets/7510ed2b-9c4b-43ed-b807-669deee73729">

## View Paid Invoices

<img width="955" alt="image" src="https://github.com/user-attachments/assets/69dc9ffa-7e98-43f6-8f34-a1fc6029fe15">

The "View All Invoices" tab provides a comprehensive list of all invoices stored in the database. The "View Paid Invoices" tab filters and displays invoices that have been marked as paid. Conversely, the "View Unpaid Invoices" tab shows invoices with an unpaid status. This organization ensures easy access to the invoice details based on their payment status.

## Search Customer Invoices

<img width="497" alt="image" src="https://github.com/user-attachments/assets/500086db-859b-49dd-99de-39af74ff9570">

This frame allows users to search for customer invoices by entering a specific customer ID. Once the ID is provided, the frame displays all associated invoice details for that customer. This functionality ensures that users can quickly access and review invoices related to a particular customer.

## Customer Details

<img width="494" alt="image" src="https://github.com/user-attachments/assets/b0e13980-c989-461d-b552-7c8f5529c4ea">

If additional customer details are needed, this frame allows users to retrieve information by entering the customer's ID.It retrieves and displays the customer's relevant details, providing users with quick and efficient access to comprehensive information.

## View Report
## Invoice Status Count

<img width="279" alt="image" src="https://github.com/user-attachments/assets/0b5c61ea-5392-47c5-97b4-796bbe43f960">

## Sales Count by Product

<img width="281" alt="image" src="https://github.com/user-attachments/assets/eaabb77f-27b0-4611-9e03-4241465c790f">

Under the "View Report" tab, there are two analysis sections. The first tab displays a graph showing the count of invoice statuses, indicating whether invoices are paid or unpaid. The second tab features a graph of item sales by product, illustrating the total sales for each item based on the product type.




