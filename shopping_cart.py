import datetime
import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()

SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "OOPS, please set env var called 'SENDGRID_API_KEY'")
SENDGRID_TEMPLATE_ID = os.environ.get("SENDGRID_TEMPLATE_ID", "OOPS, please set env var called 'SENDGRID_TEMPLATE_ID")
MY_EMAIL_ADDRESS = os.environ.get("MY_EMAIL_ADDRESS", "OOPS, please set env var called 'MY_EMAIL_ADDRESS'")



products = [
    {"id":1, "name": "Chocolate Sandwich Cookies", "department": "snacks", "aisle": "cookies cakes", "price": 3.50},
    {"id":2, "name": "All-Seasons Salt", "department": "pantry", "aisle": "spices seasonings", "price": 4.99},
    {"id":3, "name": "Robust Golden Unsweetened Oolong Tea", "department": "beverages", "aisle": "tea", "price": 2.49},
    {"id":4, "name": "Smart Ones Classic Favorites Mini Rigatoni With Vodka Cream Sauce", "department": "frozen", "aisle": "frozen meals", "price": 6.99},
    {"id":5, "name": "Green Chile Anytime Sauce", "department": "pantry", "aisle": "marinades meat preparation", "price": 7.99},
    {"id":6, "name": "Dry Nose Oil", "department": "personal care", "aisle": "cold flu allergy", "price": 21.99},
    {"id":7, "name": "Pure Coconut Water With Orange", "department": "beverages", "aisle": "juice nectars", "price": 3.50},
    {"id":8, "name": "Cut Russet Potatoes Steam N' Mash", "department": "frozen", "aisle": "frozen produce", "price": 4.25},
    {"id":9, "name": "Light Strawberry Blueberry Yogurt", "department": "dairy eggs", "aisle": "yogurt", "price": 6.50},
    {"id":10, "name": "Sparkling Orange Juice & Prickly Pear Beverage", "department": "beverages", "aisle": "water seltzer sparkling water", "price": 2.99},
    {"id":11, "name": "Peach Mango Juice", "department": "beverages", "aisle": "refrigerated", "price": 1.99},
    {"id":12, "name": "Chocolate Fudge Layer Cake", "department": "frozen", "aisle": "frozen dessert", "price": 18.50},
    {"id":13, "name": "Saline Nasal Mist", "department": "personal care", "aisle": "cold flu allergy", "price": 16.00},
    {"id":14, "name": "Fresh Scent Dishwasher Cleaner", "department": "household", "aisle": "dish detergents", "price": 4.99},
    {"id":15, "name": "Overnight Diapers Size 6", "department": "babies", "aisle": "diapers wipes", "price": 25.50},
    {"id":16, "name": "Mint Chocolate Flavored Syrup", "department": "snacks", "aisle": "ice cream toppings", "price": 4.50},
    {"id":17, "name": "Rendered Duck Fat", "department": "meat seafood", "aisle": "poultry counter", "price": 9.99},
    {"id":18, "name": "Pizza for One Suprema Frozen Pizza", "department": "frozen", "aisle": "frozen pizza", "price": 12.50},
    {"id":19, "name": "Gluten Free Quinoa Three Cheese & Mushroom Blend", "department": "dry goods pasta", "aisle": "grains rice dried goods", "price": 3.99},
    {"id":20, "name": "Pomegranate Cranberry & Aloe Vera Enrich Drink", "department": "beverages", "aisle": "juice nectars", "price": 4.25}
] # based on data from Instacart: https://www.instacart.com/datasets/grocery-shopping-2017

product_list = []
for ids in range(0, len(products)):
    product_list.append(products[ids]['id'])

shopping_list = []
done_flag = False

def add_to_cart(what_to_add):
    for item in range(0, len(products)):
        if int(what_to_add) == int(products[item]['id']):
            shopping_list.append(products[item])
        else:
            pass

template_data = {
    "total_price_usd": "$14.95",
    "human_friendly_timestamp": "June 1st, 2019 10:00 AM",
    "products":[
        {"id":1, "name": "Product 1"},
        {"id":2, "name": "Product 2"},
        {"id":3, "name": "Product 3"},
        {"id":2, "name": "Product 2"},
        {"id":1, "name": "Product 1"}
    ]
}    


def email_out ():
    client = SendGridAPIClient(SENDGRID_API_KEY)
    print("CLIENT:", type(client))
    from_email = MY_EMAIL_ADDRESS
    to_email = MY_EMAIL_ADDRESS
    message = Mail(from_email, to_email)
    print("MESSAGE:", type(message))

    message.template_id = SENDGRID_TEMPLATE_ID # see receipt.html for the template's structure
    message.dynamic_template_data = template_data
    
    try:
        response = client.send(message)
        print("RESPONSE", type(response))
        print(response.status_code)
        print(response.body)
        print(response.headers)

    except Exception as e:
        print('OOPS', e)



while done_flag == False:
    from_user = input('Please put something in your cart. Type Done when you are finished  ')
    if from_user == 'Done':
        email_y_n = input("Would you like a copy of the receipt emailed to you ('Yes' or 'No') ")
        if email_y_n == 'Yes':
            send_to = input('Please input your email address ')
            print (send_to)
            email_out()
        done_flag = True
    elif from_user.isdigit() == False:
        print("Please only input numbers")
    elif int(from_user) not in product_list:
        print('Sorry we are out of stock, please pick something else.')
    else:
        add_to_cart(from_user)
#print(shopping_list)
subtotal = 0
time_of_purchase = datetime.datetime.now()
print('--------------------')
print('Sheetz Corp.') #my favorite food spot when back in PA
print('--------------------')
print('Web: www.sheetzco.com') 
print('Phone: +1-814-978-0000')
print('Time of purchase:', time_of_purchase.strftime("%b %d %Y %H:%M:%S") )
print('--------------------')
print('Shopping Cart Items')
#iterate through my shopping list to print items and calculate subtotal
for purchases in range(0, len(shopping_list)):
    print('+', shopping_list[purchases]['name'], "(${:,.2f})".format(shopping_list[purchases]['price']) )
    subtotal += float(shopping_list[purchases]['price'])
tax = subtotal * 0.08875
total = subtotal + tax
print('--------------------')
print('Subtotal', "        (${:,.2f})".format(subtotal))
print('NYC Tax (8.875%)', "(${:,.2f})".format(tax))
print('Subtotal', "        (${:,.2f})".format(total))
print('--------------------')

#help with the date time format from here
#https://stackabuse.com/how-to-format-dates-in-python/

#help with the isdigit elif statment
#https://www.programiz.com/python-programming/methods/string/isdigit

## Take items out of cart


