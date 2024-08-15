import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Database connection
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="username",
        password="password",
        database="db name"
    )

# Main application class
class InvoiceManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Invoice Management System")

        self.home_frame = tk.Frame(self.root)
        self.home_frame.pack(fill="both", expand=True)

        tk.Label(self.home_frame, text="Invoice Management System", font=("Arial", 24)).pack(pady=20)

        # Buttons for various functions
        buttons = [
            ("Add Customer", self.open_add_customer),
            ("Add Invoice", self.open_add_invoice),
            ("View All Invoices", self.open_view_all_invoices),
            ("View Unpaid Invoices", self.open_view_unpaid_invoices),
            ("View Paid Invoices", self.open_view_paid_invoices),
            ("Search Customer Invoices", self.open_search_customer),
            ("View Customer Details", self.open_view_customer_details),
            ("View Reports", self.open_view_reports)
        ]
        for text, command in buttons:
            tk.Button(self.home_frame, text=text, command=command).pack(pady=10)

    def clear_frame(self):
        """Clear all widgets from the root frame."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def back_to_home(self):
        """Return to the home frame."""
        self.clear_frame()
        self.__init__(self.root)

    def open_add_customer(self):
        """Open the Add Customer window."""
        self.clear_frame()
        add_customer_frame = tk.Frame(self.root)
        add_customer_frame.pack(fill="both", expand=True)

        tk.Label(add_customer_frame, text="Add Customer", font=("Arial", 24)).pack(pady=20)

        # Customer form entries
        form_labels = ["Customer ID", "Customer Name", "Contact Number", "Email", "Address"]
        self.customer_entries = {}
        for label in form_labels:
            tk.Label(add_customer_frame, text=label).pack(pady=5)
            entry = tk.Entry(add_customer_frame)
            entry.pack(pady=5)
            self.customer_entries[label] = entry

        # Red note for Customer ID
        tk.Label(add_customer_frame, text="* Customer ID should be numerical", fg="red", font=("Arial", 12)).pack(pady=5)

        tk.Button(add_customer_frame, text="Add Customer", command=self.add_customer).pack(pady=20)
        tk.Button(add_customer_frame, text="Back to Home", command=self.back_to_home).pack(pady=10)

    def add_customer(self):
        """Add a new customer to the database."""
        customer_data = {label: entry.get() for label, entry in self.customer_entries.items()}

        # Validate form fields
        if not all(customer_data.values()):
            messagebox.showerror("Error", "All fields are required")
            return

        if not customer_data["Customer ID"].isdigit():
            messagebox.showerror("Error", "Customer ID should be numerical")
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Customers (customer_id, customer_name, contact_number, email, address)
                VALUES (%s, %s, %s, %s, %s)
            """, tuple(customer_data.values()))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Customer added successfully")
            self.back_to_home()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def open_add_invoice(self):
        """Open the Add Invoice window."""
        self.clear_frame()
        add_invoice_frame = tk.Frame(self.root)
        add_invoice_frame.pack(fill="both", expand=True)

        tk.Label(add_invoice_frame, text="Add Invoice", font=("Arial", 24)).pack(pady=20)

        # Invoice form entries
        form_labels = ["Customer ID", "Invoice Date (YYYY-MM-DD)"]
        self.invoice_entries = {}
        for label in form_labels:
            tk.Label(add_invoice_frame, text=label).pack(pady=5)
            entry = tk.Entry(add_invoice_frame)
            entry.pack(pady=5)
            self.invoice_entries[label] = entry

        tk.Label(add_invoice_frame, text="Status").pack(pady=5)
        self.status_var = tk.StringVar(value="Unpaid")
        tk.Radiobutton(add_invoice_frame, text="Paid", variable=self.status_var, value="Paid").pack(pady=5)
        tk.Radiobutton(add_invoice_frame, text="Unpaid", variable=self.status_var, value="Unpaid").pack(pady=5)

        tk.Button(add_invoice_frame, text="Add Item", command=self.add_item).pack(pady=10)
        self.item_frame = tk.Frame(add_invoice_frame)
        self.item_frame.pack(pady=10)
        self.item_frame.item_frames = []

        tk.Button(add_invoice_frame, text="Save Invoice", command=self.save_invoice).pack(pady=20)
        tk.Button(add_invoice_frame, text="Back to Home", command=self.back_to_home).pack(pady=10)

    def add_item(self):
        """Add an item entry frame for the invoice."""
        item_frame = tk.Frame(self.item_frame)
        item_frame.pack(pady=5)

        labels = ["Item Name", "Quantity", "Rate", "Unit"]
        entries = {}
        for idx, label in enumerate(labels):
            tk.Label(item_frame, text=label).grid(row=0, column=idx * 2)
            entry = tk.Entry(item_frame)
            entry.grid(row=0, column=(idx * 2) + 1)
            entries[label] = entry

        self.item_frame.item_frames.append(entries)

    def save_invoice(self):
        """Save the invoice and its items to the database."""
        invoice_data = {label: entry.get() for label, entry in self.invoice_entries.items()}
        items = self.item_frame.item_frames
        status = self.status_var.get()

        if not invoice_data["Customer ID"] or not invoice_data["Invoice Date (YYYY-MM-DD)"] or not items:
            messagebox.showerror("Error", "Please fill all fields and add at least one item")
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()

            # Check if customer exists
            cursor.execute("SELECT customer_id FROM Customers WHERE customer_id = %s", (invoice_data["Customer ID"],))
            if cursor.fetchone() is None:
                messagebox.showinfo("Info", "Customer ID does not exist")
                conn.close()
                return

            total_amount = 0
            for item in items:
                quantity_text = item["Quantity"].get()
                rate_text = item["Rate"].get()

                try:
                    quantity = float(quantity_text)
                    rate = float(rate_text)
                except ValueError:
                    messagebox.showerror("Error", "Quantity and Rate must be numeric values")
                    return

                total_amount += quantity * rate

            discount_amount = total_amount * 0.10
            final_amount = total_amount - discount_amount

            cursor.execute("""
                INSERT INTO Invoices (customer_id, invoice_date, total_amount, discount_amount, final_amount, status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (invoice_data["Customer ID"], invoice_data["Invoice Date (YYYY-MM-DD)"], total_amount, discount_amount, final_amount, status))

            invoice_id = cursor.lastrowid

            for item in items:
                cursor.execute("""
                    INSERT INTO Invoice_Items (invoice_id, item_name, quantity, rate, unit)
                    VALUES (%s, %s, %s, %s, %s)
                """, (invoice_id, item["Item Name"].get(), float(item["Quantity"].get()), float(item["Rate"].get()), item["Unit"].get()))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Invoice added successfully")
            self.back_to_home()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def load_invoices(self, filter_by_status=None):
        """Load invoices from the database, optionally filtering by status."""
        try:
            conn = connect_db()
            cursor = conn.cursor()

            query = "SELECT invoice_id, customer_id, invoice_date, total_amount, discount_amount, final_amount, status FROM Invoices"
            if filter_by_status:
                query += " WHERE status = %s"
                cursor.execute(query, (filter_by_status,))
            else:
                cursor.execute(query)

            rows = cursor.fetchall()
            conn.close()

            return rows
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            return []

    def open_view_all_invoices(self):
        """Open the window to view all invoices."""
        self.clear_frame()
        self._create_invoice_view("All Invoices", self.load_invoices())

    def open_view_unpaid_invoices(self):
        """Open the window to view unpaid invoices."""
        self.clear_frame()
        self._create_invoice_view("Unpaid Invoices", self.load_invoices(filter_by_status="Unpaid"))

    def open_view_paid_invoices(self):
        """Open the window to view paid invoices."""
        self.clear_frame()
        self._create_invoice_view("Paid Invoices", self.load_invoices(filter_by_status="Paid"))

    def _create_invoice_view(self, title, invoice_data):
        """Helper method to create invoice view UI."""
        view_invoices_frame = tk.Frame(self.root)
        view_invoices_frame.pack(fill="both", expand=True)

        tk.Label(view_invoices_frame, text=title, font=("Arial", 24)).pack(pady=20)

        tree = ttk.Treeview(view_invoices_frame, columns=("invoice_id", "customer_id", "invoice_date", "total_amount", "discount_amount", "final_amount", "status"), show="headings")
        tree.pack(fill="both", expand=True)

        columns = ["Invoice ID", "Customer ID", "Invoice Date", "Total Amount", "Discount", "Final Amount", "Status"]
        for idx, col in enumerate(columns):
            tree.heading(idx, text=col)

        for row in invoice_data:
            tree.insert("", "end", values=row)

        tk.Button(view_invoices_frame, text="Back to Home", command=self.back_to_home).pack(pady=10)

    def open_search_customer(self):
        """Open the window to search customer invoices."""
        self.clear_frame()
        search_frame = tk.Frame(self.root)
        search_frame.pack(fill="both", expand=True)

        tk.Label(search_frame, text="Search Customer Invoices", font=("Arial", 24)).pack(pady=20)

        tk.Label(search_frame, text="Customer ID").pack(pady=5)
        customer_id_entry = tk.Entry(search_frame)
        customer_id_entry.pack(pady=5)

        def search_customer_invoices():
            customer_id = customer_id_entry.get()
            if not customer_id.isdigit():
                messagebox.showerror("Error", "Customer ID should be numerical")
                return

            self.clear_frame()
            self._create_invoice_view(f"Invoices for Customer ID: {customer_id}", self._search_customer_invoices(customer_id))

        tk.Button(search_frame, text="Search", command=search_customer_invoices).pack(pady=20)
        tk.Button(search_frame, text="Back to Home", command=self.back_to_home).pack(pady=10)

    def _search_customer_invoices(self, customer_id):
        """Search for invoices by customer ID."""
        try:
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM Invoices WHERE customer_id = %s", (customer_id,))
            rows = cursor.fetchall()

            conn.close()

            return rows
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            return []

    def open_view_customer_details(self):
        """Open the window to view customer details."""
        self.clear_frame()
        customer_details_frame = tk.Frame(self.root)
        customer_details_frame.pack(fill="both", expand=True)

        tk.Label(customer_details_frame, text="Customer Details", font=("Arial", 24)).pack(pady=20)

        tk.Label(customer_details_frame, text="Customer ID").pack(pady=5)
        customer_id_entry = tk.Entry(customer_details_frame)
        customer_id_entry.pack(pady=5)

        def search_customer():
            customer_id = customer_id_entry.get()
            if not customer_id.isdigit():
                messagebox.showerror("Error", "Customer ID should be numerical")
                return

            self._view_customer_details(customer_id)

        tk.Button(customer_details_frame, text="Search", command=search_customer).pack(pady=20)
        tk.Button(customer_details_frame, text="Back to Home", command=self.back_to_home).pack(pady=10)

    def _view_customer_details(self, customer_id):
        """View customer details by customer ID."""
        try:
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM Customers WHERE customer_id = %s", (customer_id,))
            customer = cursor.fetchone()

            if customer:
                tk.Label(self.root, text=f"Customer ID: {customer[0]}").pack()
                tk.Label(self.root, text=f"Customer Name: {customer[1]}").pack()
                tk.Label(self.root, text=f"Contact Number: {customer[2]}").pack()
                tk.Label(self.root, text=f"Email: {customer[3]}").pack()
                tk.Label(self.root, text=f"Address: {customer[4]}").pack()
            else:
                messagebox.showinfo("Info", "Customer ID does not exist")

            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def open_view_reports(self):
        """Open the window to view reports with graphs on separate pages within the same tab."""
        self.clear_frame()
        reports_frame = tk.Frame(self.root)
        reports_frame.pack(fill="both", expand=True)

        tk.Label(reports_frame, text="Sales Reports", font=("Arial", 24)).pack(pady=20)

        # Create a Notebook widget for tabs
        notebook = ttk.Notebook(reports_frame)
        notebook.pack(fill="both", expand=True)

        # Create tab for the first graph
        invoice_status_tab = tk.Frame(notebook)
        notebook.add(invoice_status_tab, text="Invoice Status Count")
        self._generate_invoice_status_count_graph(invoice_status_tab)

        # Create tab for the second graph
        sales_count_tab = tk.Frame(notebook)
        notebook.add(sales_count_tab, text="Sales Count by Product")
        self._generate_sales_count_graph(sales_count_tab)

        tk.Button(reports_frame, text="Back to Home", command=self.back_to_home).pack(pady=10)

    def _generate_invoice_status_count_graph(self, parent_frame):
        """Generate and display the graph showing count of paid and unpaid invoices in the specified parent frame."""
        try:
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT status, COUNT(*)
                FROM Invoices
                GROUP BY status
            """)
            report_data = cursor.fetchall()
            conn.close()

            statuses = [row[0] for row in report_data]
            counts = [row[1] for row in report_data]

            fig, ax = plt.subplots()
            ax.bar(statuses, counts)
            ax.set_xlabel("Invoice Status")
            ax.set_ylabel("Count")
            ax.set_title("Count of Paid and Unpaid Invoices")

            canvas = FigureCanvasTkAgg(fig, master=parent_frame)
            canvas.draw()
            canvas.get_tk_widget().pack()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def _generate_sales_count_graph(self, parent_frame):
        """Generate and display the graph showing count of sales for each product in the specified parent frame."""
        try:
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT item_name, SUM(quantity)
                FROM Invoice_Items
                GROUP BY item_name
            """)
            report_data = cursor.fetchall()
            conn.close()

            items = [row[0] for row in report_data]
            quantities = [row[1] for row in report_data]

            fig, ax = plt.subplots()
            ax.bar(items, quantities)
            ax.set_xlabel("Product")
            ax.set_ylabel("Total Quantity Sold")
            ax.set_title("Sales Count by Product")

            canvas = FigureCanvasTkAgg(fig, master=parent_frame)
            canvas.draw()
            canvas.get_tk_widget().pack()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = InvoiceManagementApp(root)
    root.mainloop()
