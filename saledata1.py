def main():
    sales_data = []

    print("Salutations, insignificant human! Ready to enter some sales data?")
    
    while True:
        print("\nMenu:")
        print("1. Enter a sales person's data")
        print("2. View sales summary")
        print("3. Save data to text file")
        print("4. Exit")
        
        choice = input("Choose an option (1-4): ").strip()

        if choice == '1':
            name = input("Enter the sales person's name: ").strip()
            sale = float(input(f"Enter the sales for {name}: ").strip())
            sales_data.append({'name': name, 'sale': sale})
        elif choice == '2':
            view_summary(sales_data)
        elif choice == '3':
            save_to_file(sales_data)
        elif choice == '4':
            print("Goodbye, insignificant human!")
            break
        else:
            print("Invalid choice. Please choose a valid option.")

def view_summary(sales_data):
    if not sales_data:
        print("No sales data available.")
        return

    total_sales = sum(person['sale'] for person in sales_data)
    num_salespersons = len(sales_data)
    avg_sales_per_person = total_sales / num_salespersons
    avg_sales_per_day = total_sales / 30  # Assuming 30 days in a month

    summary = f"""
    Sales Data Summary:
    Total number of salespersons: {num_salespersons}
    Total sales: {total_sales}
    Average sales per person: {avg_sales_per_person:.2f}
    Average daily sales for the month: {avg_sales_per_day:.2f}
    """
    print(summary)

def save_to_file(sales_data):
    if not sales_data:
        print("No sales data to save.")
        return

    total_sales = sum(person['sale'] for person in sales_data)
    num_salespersons = len(sales_data)
    avg_sales_per_person = total_sales / num_salespersons
    avg_sales_per_day = total_sales / 30  # Assuming 30 days in a month

    summary = f"""
    Sales Data Summary:
    Total number of salespersons: {num_salespersons}
    Total sales: {total_sales}
    Average sales per person: {avg_sales_per_person:.2f}
    Average daily sales for the month: {avg_sales_per_day:.2f}
    """

    with open("sales_data.txt", "w") as file:
        file.write("Sales Data:\n")
        for person in sales_data:
            file.write(f"{person['name']}: {person['sale']}\n")
        file.write(summary)

    print("Sales data and summary have been saved to 'sales_data.txt'")

if __name__ == "__main__":
    main()
