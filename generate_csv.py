import csv
import random
from faker import Faker
from datetime import datetime, timedelta

# Inicializar a biblioteca Faker
fake = Faker()

# Função para gerar dados aleatórios
def generate_data():
    invoice_id = fake.uuid4()[:8]
    branch = random.choice(["A", "B", "C"])
    city = random.choice(["City A", "City B", "City C"])
    customer_type = random.choice(["menbro", "visitante"])
    gender = random.choice(["Male", "Female"])
    product_line = random.choice([
        "Health and beauty", 
        "Eletronic accessories", 
        "Home and life style", 
        "Sport and travel",
        "Food and beverages",
        "Fashion accessories",
    ])
    unit_price = round(random.uniform(10, 100), 2)
    quality = random.randint(1, 10)
    tax = round((unit_price * quality) * 0.05, 2)
    total = round(unit_price * quality + tax, 2)
    date = fake.date_between(start_date="-1y", end_date="today").strftime("%Y-%m-%d")
    time = fake.time(pattern="%H:%M:%S")
    payment = random.choice(["Cash", "Credit Card", "Ewallet"])
    cogs = round(unit_price*quality, 2)
    gross_margin_percentage = 4.76
    gross_income = tax
    rating = round(random.uniform(4, 10), 1)

    return [
        invoice_id, 
        branch, 
        city, 
        customer_type, 
        gender, 
        product_line, 
        unit_price, 
        quality, 
        tax, 
        total, 
        date, 
        time, 
        payment, 
        cogs, 
        gross_margin_percentage, 
        gross_income, 
        rating
    ]

# Cabeçalho do arquivo CSV
header = [
    "Invoice ID", 
    "Branch", 
    "City", 
    "Customer type", 
    "Gender", 
    "Product line", 
    "Unit price", 
    "Quantity", 
    "Tax 5%", 
    "Total", 
    "Date", 
    "Time", 
    "Payment", 
    "COGS", 
    "Gross margin percentage", 
    "Gross income", 
    "Rating"
]

# Gerar dados aleatórios e escrever no arquivo CSV
with open("sales_data.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(header)

    for _ in range(300):
        writer.writerow(generate_data())

print("Arquivo CSV gerado com sucesso!")