import os
# from dotenv import load_dotenv
import stripe
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk

# load_dotenv()

stripe.api_key = "sk_test_51QRpiACc2JL6OkxkK5Nfo42Aa4ipPjJRtz7hUIYkCRQjsTOyp8WDxayV9wK9VTAMz1u2ouGuxWI5nEo2bH1Rkv5a00myCc4KMm"

def main():
    app = tk.Tk()
    app.title("ShopShere")
    app.geometry("800x600")
    app.configure(bg="#C2B3A3") 
    return app

app = main()
 
products = [
    {"Name": "Water Bottle", "price": 999, "img": "water_bottle.png"},
    {"Name": "MacBook", "price": 69999, "img": "macbook.png"},
    {"Name": "Headphones", "price": 15000, "img": "headphones.png"},
    {"Name": "Smartphone", "price": 100000, "img": "smartphone.png"},
    {"Name": "Camera", "price": 90000, "img": "camera.png"},
    {"Name": "Smartwatch", "price":45000, "img": "smartwatch.png"},
    {"Name": "Backpack", "price": 2000, "img": "backpack.png"},
    {"Name": "Tablet", "price": 40000, "img": "tablet.png"},
    {"Name": "Airpod", "price": 25000, "img": "Airpod.webp"},
    {"Name": "Weighing scale", "price": 2000, "img": "Weight-Scale.webp"},
    {"Name": "Mouse", "price": 1500, "img": "mouse.webp"},
    {"Name": "Keyboard", "price": 1800, "img": "keyboard.webp"},
    {"Name": "Smart TV", "price": 4800, "img": "smarttv.webp"},
    {"Name": "Sound Theatre", "price": 4000, "img": "soundtheatre.webp"},
    {"Name": "power bank", "price": 1600, "img": "powerbank.webp"},
    {"Name": "router", "price": 3600, "img": "router.webp"},
]

cart = []

def addToCart(product):
    cart.append(product)
    messagebox.showinfo("Cart", f"{product['Name']} added to cart!")

def displayProducts(app, productFrame):
    columns = 8   
    for idx, product in enumerate(products):
        # Calculate row and column based on the index
        row = idx // columns
        column = idx % columns

        # Load an image for the product
        img = Image.open(product["img"])
        img = img.resize((100, 100))
        photo = ImageTk.PhotoImage(img)

        # Product image
        labelImage = tk.Label(productFrame, image=photo, bg="#1F2123")
        labelImage.image = photo  
        labelImage.grid(row=row * 3, column=column, padx=10, pady=10)   

        # Product label
        label = tk.Label(productFrame, text=f"{product['Name']} - ₹{product['price']}",
                         font=("Roboto", 14), bg="#3B917B", fg="white")
        label.grid(row=row * 3 + 1, column=column, padx=10, pady=10)  

        # Add to Cart button
        button = tk.Button(productFrame, text="Add to Cart", command=lambda p=product: addToCart(p),
                           padx=10, pady=5, bg="#A3CADB", fg="sky blue", font=("Roboto", 14, "bold"))
        button.grid(row=row * 3 + 2, column=column, padx=10, pady=10)   

def viewCart():
    cartWindow = tk.Toplevel(app)
    cartWindow.title("Your Cart")
    cartWindow.geometry("500x300")
    cartWindow.configure(bg="#F3F3F3")

    header = tk.Label(cartWindow, text="Product - Price", font=("Roboto", 14, "bold"), bg="#ecf0f1")
    header.grid(row=0, column=0, padx=10, pady=10)

    for idx, item in enumerate(cart):
        itemLabel = tk.Label(cartWindow, text=f"{item['Name']} - ₹{item['price']}", bg="#ecf0f1")
        itemLabel.grid(row=idx + 1, column=0, padx=10, pady=5)

    checkoutButton = ttk.Button(cartWindow, text="Checkout", command=processPayment)
    checkoutButton.grid(row=len(cart) + 1, column=0, pady=10)

def processPayment():
    try:
        totalAmount = sum(item['price'] for item in cart) * 100  # in paise
        stripe.PaymentIntent.create(
            amount=totalAmount,
            currency='inr',
            payment_method_types=['card']
        )
        showSuccessPopup()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def showSuccessPopup():
    popup = tk.Toplevel(app)
    popup.title("Payment Successful")
    popup.geometry("300x150")
    label = tk.Label(popup, text="Your payment was successful!", font=("Roboto", 12))
    label.pack(pady=20)
    okButton = tk.Button(popup, text="OK", command=popup.destroy)
    okButton.pack(pady=10)

def setupMenu(app):
    menu = tk.Menu(app)
    app.config(menu=menu)
    fileMenu = tk.Menu(menu)
    menu.add_cascade(label="Exit?", menu=fileMenu)
    fileMenu.add_command(label="Yes", command=app.quit)

    helpMenu = tk.Menu(menu)
    menu.add_cascade(label="Help", menu=helpMenu)
    helpMenu.add_command(label="About", command=lambda: messagebox.showinfo("About", "This is an eCommerce app\n\nAuthor: Ayush"))

def setupStatusBar(app):
    status = tk.Label(app, text="Welcome to Shop Sphere!", bd=1, relief=tk.SUNKEN,font=("Arial", 30, "italic"), bg="#FFF0E0",fg="#e63946",anchor=tk.W, padx=15, pady=8,)
    status.place(x=0, y=0)
    

def showLoading():
    loading = tk.Toplevel(app)
    loading.title("Processing Payment")
    loading.geometry("300x100")
    label = tk.Label(loading, text="Processing, please wait...")
    label.pack(pady=20)

    app.after(2000, loading.destroy)

def animateSaleText():
    sale_text = "🎉 HUGE SALE! EVERYTHING AT UNBELIEVABLE PRICES! 🎉"
    label = tk.Label(
        app,
        text=sale_text,
        font=("Arial", 40, "bold"),
        fg="purple",
        bg="#C2B3A3",
    )
    label.place(x=800, y=100)  # Start position (off-screen right)

    def move_text():
        current_x = label.winfo_x()
        new_x = current_x - 5  # Move left by 5 pixels
        if new_x + label.winfo_width() < 0:  # Reset to the right if out of view
            new_x = app.winfo_width()

        label.place(x=new_x, y=100)  # Update position
        app.after(50, move_text)  # Repeat animation every 50 ms

    move_text()  # Start the animation

# Call the function to animate the SALE text
animateSaleText()

productFrame = tk.Frame(app, bg="#F3F3F3")
productFrame.pack(side=tk.LEFT, padx=20)

cartButton = tk.Button(app, text="View Cart", command=viewCart, padx=10, pady=5, bg="#EA9A79", fg="#FC7E01", font=("Roboto", 14, "bold"))
cartButton.place(relx=1.0, y=10, anchor="ne")

displayProducts(app, productFrame)
setupMenu(app)
setupStatusBar(app)
app.mainloop()
