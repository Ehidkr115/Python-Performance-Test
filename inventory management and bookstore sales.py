# Bookstore Management System
# This system allows registering books, managing stock, recording sales,
# and generating reports such as top 3 best-selling books, sales by author, and income summary.

library = []  # List to store all registered books
sales = []    # List to store all completed sales

# Validates that the user enters a positive integer (e.g., for quantity or ID)
def validate_positive_integer(message):
    entry = input(message).strip()
    if entry.isdigit():
        number = int(entry)
        if number > 0:
            return number
        print("[ERROR] Invalid number. Must be greater than 0.")
    else:
        print("[ERROR] Invalid input. Please enter numbers only.")
    return validate_positive_integer(message)

# Validates that the input is a valid name (letters and spaces only)
def validate_name(message):
    entry = input(message).strip()
    if entry and entry.replace(" ", "").isalpha():
        return entry
    print("[ERROR] Name must contain only letters and spaces.")
    return validate_name(message)

# Validates that the input is a positive float (e.g., for price)
def validate_positive_float(message):
    entry = input(message).strip()
    try:
        value = float(entry)
        if value > 0:
            return value
        print("[ERROR] Value must be greater than 0.")
    except ValueError:
        print("[ERROR] Invalid input. Please enter a valid number.")
    return validate_positive_float(message)

# Calculates total price (price * quantity)
def calculate_total(price, quantity):
    return price * quantity

# Registers a new book with ID, title, author, quantity and price
def register_book():
    book_id = str(validate_positive_integer("Enter Book ID: "))
    if any(book['id'] == book_id for book in library):
        print("[ERROR] Book with this ID already exists.")
        return

    title = validate_name("Enter book title: ")
    author = validate_name("Enter author: ")
    quantity = validate_positive_integer("Enter available quantity: ")
    price = validate_positive_float("Price: $")

    # Add book to library
    library.append({
        "id": book_id,
        "title": title,
        "author": author,
        "quantity": quantity,
        "price": price
    })

    print("[OK] Book successfully registered.")

# Checks if at least one book exists in the library
def is_library_ready():
    if not library:
        print("[WARNING] Please register at least one book first.")
        return False
    return True

# Searches a book in the library by its ID
def find_book(book_id):
    for book in library:
        if book['id'] == book_id:
            return book
    return None

# Allows user to consult a specific book's information
def consult_book():
    if not is_library_ready(): return
    book_id = str(validate_positive_integer("Enter Book ID: "))
    book = find_book(book_id)
    if book:
        print(f"\nTitle: {book['title']}\nAuthor: {book['author']}\nAvailable Quantity: {book['quantity']}\nPrice: ${book['price']:.2f}")
    else:
        print("[ERROR] Book not found.")

# Updates the quantity (stock) of an existing book
def update_stock():
    if not is_library_ready(): return
    book_id = str(validate_positive_integer("Enter Book ID: "))
    book = find_book(book_id)
    if book:
        new_quantity = validate_positive_integer("New available quantity: ")
        book['quantity'] = new_quantity
        print("[OK] Stock updated.")
    else:
        print("[ERROR] Book not found.")

# Deletes a book from the library by ID
def delete_book():
    if not is_library_ready(): return
    book_id = str(validate_positive_integer("Enter Book ID: "))
    book = find_book(book_id)
    if book:
        library.remove(book)
        print("[OK] Book deleted.")
    else:
        print("[ERROR] Book not found.")

# Displays all books currently registered in the library
def view_library():
    if not is_library_ready(): return
    print("\n--- Full Library ---")
    for book in library:
        print(f"\nID: {book['id']}\nTitle: {book['title']}\nAuthor: {book['author']}\nQuantity: {book['quantity']}\nPrice: ${book['price']:.2f}")

# Registers a sale, updates book quantity, and adds sale to history
def register_sale():
    if not is_library_ready(): return
    customer = validate_name("Customer name: ")
    book_id = str(validate_positive_integer("Enter Book ID: "))
    book = find_book(book_id)

    if not book:
        print("[ERROR] Book not found.")
        return

    print(f"Available quantity: {book['quantity']}")
    quantity_sold = validate_positive_integer("Quantity to purchase: ")

    if quantity_sold > book['quantity']:
        print("[ERROR] Not enough stock.")
        return

    total = calculate_total(book['price'], quantity_sold)
    book['quantity'] -= quantity_sold

    # Add sale record
    sales.append({
        "customer": customer,
        "book_id": book['id'],
        "title": book['title'],
        "quantity": quantity_sold,
        "total": total
    })

    print(f"[OK] Sale recorded. Total: ${total:.2f}")

# Displays all registered sales
def view_sales():
    if not sales:
        print("[WARNING] No sales recorded yet.")
        return
    print("\n--- Sales History ---")
    for sale in sales:
        print(f"\nCustomer: {sale['customer']}\nBook: {sale['title']}\nQuantity: {sale['quantity']}\nTotal: ${sale['total']:.2f}")

# Shows the top 3 books with highest quantity sold
def top_best_selling_books():
    if not sales:
        print("[WARNING] No sales recorded yet.")
        return

    count = {}
    for sale in sales:
        title = sale['title']
        count[title] = count.get(title, 0) + sale['quantity']

    top_3 = sorted(count.items(), key=lambda x: x[1], reverse=True)[:3]

    print("\n--- Top 3 Best-Selling Books ---")
    for i, (title, quantity) in enumerate(top_3, start=1):
        print(f"{i}. {title} - {quantity} units")

# Summarizes total sales value grouped by author
def sales_report_by_author():
    if not sales:
        print("[WARNING] No sales recorded yet.")
        return

    summary = {}
    for sale in sales:
        book = find_book(sale['book_id'])
        if book:
            author = book['author']
            summary[author] = summary.get(author, 0) + sale['total']

    print("\n--- Sales Report by Author ---")
    for author, total in summary.items():
        print(f"{author}: ${total:.2f}")

# Calculates and displays gross and net income (after discount)
def calculate_income(discount=0.10):
    if not sales:
        print("[WARNING] No sales recorded yet.")
        return

    gross_income = sum(sale['total'] for sale in sales)
    net_income = gross_income * (1 - discount)

    print("\n--- Income Summary ---")
    print(f"Gross Income (no discount): ${gross_income:.2f}")
    print(f"Net Income (with {int(discount * 100)}% discount): ${net_income:.2f}")

# Main menu that provides all available options to the user
def menu():
    options = {
        "1": register_book,
        "2": consult_book,
        "3": update_stock,
        "4": delete_book,
        "5": view_library,
        "6": register_sale,
        "7": view_sales,
        "8": top_best_selling_books,
        "9": sales_report_by_author,
        "10": calculate_income
    }

    selection = None
    while selection != "11":
        print("\n--- MENU ---")
        print("1. Register Book")
        print("2. Consult Book")
        print("3. Update Stock")
        print("4. Delete Book")
        print("5. View Full Library")
        print("6. Register Sale")
        print("7. View Sales")
        print("8. Top  Best-Selling Books")
        print("9. Sales Report by Author")
        print("10. Calculate Gross and Net Income")
        print("11. Exit")

        selection = input("Choose an option (1-11): ").strip()
        action = options.get(selection)

        if selection == "11":
            print("Exiting... Goodbye!   :D ")
        elif action:
            action()
        else:
            print("[ERROR] Invalid option. Please choose between 1 and 11.")

# Entry point for the script
if __name__ == '__main__':
    menu()
