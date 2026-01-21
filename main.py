import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import datetime

# =========================
# Files
# =========================
SELLER_FILE = "seller.txt"
CUSTOMER_FILE = "customer.txt"
ADMIN_FILE = "admin.txt"
PRODUCT_FILE = "product.txt"
ECON_FILE = "economics.txt"

# =========================
# Headers (manual, no helper funcs)
# =========================
SELLER_HEADER = "no,name,password,id,email,address,phone,cnic\n"
CUSTOMER_HEADER = "no,name,password,id,email,address,phone\n"
ADMIN_HEADER = "no,username,password\n"

PRODUCT_HEADER = "product_id,seller_id,seller_name,product_name,description,category,brand,price,stock,status,rating,created_at\n"
ECON_HEADER = "order_id,date_time,customer_id,customer_name,seller_id,seller_name,product_id,product_name,unit_price,quantity,total_price\n"

# =========================
# Minimal file existence (NO helpers)
# =========================
if not os.path.exists(SELLER_FILE):
    with open(SELLER_FILE, "w", encoding="utf-8") as f:
        f.write(SELLER_HEADER)

if not os.path.exists(CUSTOMER_FILE):
    with open(CUSTOMER_FILE, "w", encoding="utf-8") as f:
        f.write(CUSTOMER_HEADER)

if not os.path.exists(PRODUCT_FILE):
    with open(PRODUCT_FILE, "w", encoding="utf-8") as f:
        f.write(PRODUCT_HEADER)

if not os.path.exists(ECON_FILE):
    with open(ECON_FILE, "w", encoding="utf-8") as f:
        f.write(ECON_HEADER)

if not os.path.exists(ADMIN_FILE):
    with open(ADMIN_FILE, "w", encoding="utf-8") as f:
        f.write(ADMIN_HEADER)

# Ensure at least 1 admin
with open(ADMIN_FILE, "r", encoding="utf-8") as f:
    admin_lines = f.readlines()
if len(admin_lines) <= 1:
    with open(ADMIN_FILE, "a", encoding="utf-8") as f:
        f.write("1,admin,admin123\n")

# =========================
# UI helpers (glassy look)
# =========================
BG = "#0a1020"
CARD = "#121a2b"
ENTRY_BG = "#0e1526"
BORDER = "#2a3553"
TXT = "#e7ecff"
MUTED = "#b9c2e3"
BTN = "#1b2a55"
BTN2 = "#143a2a"
BTN3 = "#3a1b1b"

def glass_card(parent, title):
    card = tk.Frame(parent, bg=CARD, highlightthickness=1, highlightbackground=BORDER)
    card.pack(fill="both", expand=True, padx=14, pady=14)

    top = tk.Frame(card, bg=CARD)
    top.pack(fill="x", padx=14, pady=(12, 6))

    tk.Label(top, text=title, bg=CARD, fg=TXT, font=("Segoe UI", 14, "bold")).pack(side="left")

    body = tk.Frame(card, bg=CARD)
    body.pack(fill="both", expand=True, padx=14, pady=(6, 14))
    return body

def label(parent, t):
    tk.Label(parent, text=t, bg=CARD, fg=TXT, font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(6, 0))

def entry(parent, var, show=None):
    e = tk.Entry(parent, textvariable=var, bg=ENTRY_BG, fg=TXT, insertbackground=TXT,
                 relief="flat", highlightthickness=1, highlightbackground=BORDER,
                 highlightcolor="#6f86ff", font=("Segoe UI", 11))
    if show:
        e.config(show=show)
    e.pack(fill="x", pady=6)
    return e

def button(parent, t, cmd, color=BTN):
    b = tk.Button(parent, text=t, command=cmd, bg=color, fg=TXT,
                  activebackground=color, activeforeground="#ffffff",
                  relief="flat", font=("Segoe UI", 11, "bold"), padx=12, pady=10)
    b.pack(fill="x", pady=6)
    return b

def now_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# =========================
# Analytics (no graphs)
# =========================
def compute_admin_analytics_text():
    with open(ECON_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    seller_rev = {}
    product_rev = {}

    for line in lines[1:]:
        if not line.strip():
            continue
        c = line.strip().split(",")
        # order_id, date_time, customer_id, customer_name, seller_id, seller_name,
        # product_id, product_name, unit_price, quantity, total_price
        seller_key = f"{c[4]} | {c[5]}"
        prod_key = f"{c[6]} | {c[7]} | seller {c[4]}"
        total = float(c[10]) if c[10] else 0.0

        seller_rev[seller_key] = seller_rev.get(seller_key, 0.0) + total
        product_rev[prod_key] = product_rev.get(prod_key, 0.0) + total

    def best_low(d):
        if not d:
            return ("N/A", 0.0), ("N/A", 0.0)
        items = sorted(d.items(), key=lambda x: x[1])
        return items[-1], items[0]

    best_seller, low_seller = best_low(seller_rev)
    best_prod, low_prod = best_low(product_rev)

    out = ""
    out += f"Best Seller (Revenue): {best_seller[0]} -> {best_seller[1]:.2f}\n"
    out += f"Lowest Seller (Revenue): {low_seller[0]} -> {low_seller[1]:.2f}\n\n"
    out += f"Best Product (Revenue): {best_prod[0]} -> {best_prod[1]:.2f}\n"
    out += f"Lowest Product (Revenue): {low_prod[0]} -> {low_prod[1]:.2f}\n\n"

    out += "Revenue by Seller:\n"
    for k, v in sorted(seller_rev.items(), key=lambda x: x[1], reverse=True):
        out += f"  {k} -> {v:.2f}\n"

    out += "\nRevenue by Product:\n"
    for k, v in sorted(product_rev.items(), key=lambda x: x[1], reverse=True):
        out += f"  {k} -> {v:.2f}\n"

    return out

def compute_seller_analytics(seller_id):
    with open(ECON_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    total_rev = 0.0
    prod_rev = {}

    for line in lines[1:]:
        if not line.strip():
            continue
        c = line.strip().split(",")
        if c[4] == seller_id:
            total = float(c[10]) if c[10] else 0.0
            total_rev += total
            key = f"{c[6]} | {c[7]}"
            prod_rev[key] = prod_rev.get(key, 0.0) + total

    if prod_rev:
        items = sorted(prod_rev.items(), key=lambda x: x[1])
        lowest = items[0]
        best = items[-1]
    else:
        best = ("N/A", 0.0)
        lowest = ("N/A", 0.0)

    return total_rev, best, lowest

# =========================
# Main App
# =========================
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("E-Commerce Marketplace (Tkinter GUI)")
        self.geometry("980x620")
        self.minsize(980, 620)
        self.configure(bg=BG)

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview", background=ENTRY_BG, fieldbackground=ENTRY_BG,
                        foreground=TXT, rowheight=28, bordercolor=BORDER,
                        borderwidth=1, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background=CARD, foreground=TXT,
                        font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", "#2a3b7a")])

        self.container = tk.Frame(self, bg=BG)
        self.container.pack(fill="both", expand=True)

        self.current_role = None
        self.current_user = None
        self.cart = []

        self.show_home()

    def clear(self):
        for w in self.container.winfo_children():
            w.destroy()

    def show_home(self):
        self.clear()
        body = glass_card(self.container, "Welcome — Choose Role")
        tk.Label(body, text="Default Admin: admin / admin123",
                 bg=CARD, fg=MUTED, font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 10))

        button(body, "Admin Login", self.show_admin_login)
        button(body, "Seller (Sign up / Login)", self.show_seller_auth)
        button(body, "Customer (Sign up / Login)", self.show_customer_auth)

    # =========================
    # Admin
    # =========================
    def show_admin_login(self):
        self.clear()
        body = glass_card(self.container, "Admin Login")

        u = tk.StringVar()
        p = tk.StringVar()

        label(body, "Username")
        entry(body, u)
        label(body, "Password")
        entry(body, p, show="*")

        def do_login():
            with open(ADMIN_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
            for line in lines[1:]:
                if not line.strip():
                    continue
                c = line.strip().split(",")
                if c[1] == u.get().strip() and c[2] == p.get().strip():
                    self.current_role = "admin"
                    self.current_user = {"username": c[1]}
                    self.show_admin_dashboard()
                    return
            messagebox.showerror("Login Failed", "Invalid admin credentials.")

        button(body, "Login", do_login)
        button(body, "Back", self.show_home, color=BTN3)

    def show_admin_dashboard(self):
        self.clear()
        body = glass_card(self.container, "Admin Dashboard")

        top = tk.Frame(body, bg=CARD)
        top.pack(fill="x", pady=(0, 10))
        tk.Button(top, text="Logout", command=self.logout,
                  bg="#2b1630", fg="#ffd7ef", relief="flat",
                  font=("Segoe UI", 10, "bold"), padx=10, pady=6).pack(side="right")

        tk.Label(body, text="All Sellers", bg=CARD, fg=TXT, font=("Segoe UI", 11, "bold")).pack(anchor="w")

        cols = ("id", "name", "email", "phone", "address", "cnic")
        tree = ttk.Treeview(body, columns=cols, show="headings", height=7)
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=140, anchor="w")
        tree.pack(fill="x", pady=8)

        with open(SELLER_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for line in lines[1:]:
            if not line.strip():
                continue
            c = line.strip().split(",")
            tree.insert("", "end", values=(c[3], c[1], c[4], c[6], c[5], c[7]))

        tk.Label(body, text="Marketplace Analytics (from economics.txt)", bg=CARD, fg=TXT,
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(16, 0))

        out = tk.Text(body, height=10, bg=ENTRY_BG, fg=TXT, insertbackground=TXT,
                      relief="flat", highlightthickness=1, highlightbackground=BORDER,
                      font=("Consolas", 10))
        out.pack(fill="both", expand=True, pady=8)

        def refresh():
            out.delete("1.0", "end")
            out.insert("end", compute_admin_analytics_text())

        button(body, "Refresh Analytics", refresh)
        refresh()

    # =========================
    # Seller
    # =========================
    def show_seller_auth(self):
        self.clear()
        body = glass_card(self.container, "Seller — Sign up / Login")
        button(body, "Sign up (Create Seller)", self.show_seller_signup)
        button(body, "Login", self.show_seller_login)
        button(body, "Back", self.show_home, color=BTN3)

    def show_seller_signup(self):
        self.clear()
        body = glass_card(self.container, "Seller Sign Up")

        name = tk.StringVar()
        sid = tk.StringVar()
        email = tk.StringVar()
        address = tk.StringVar()
        phone = tk.StringVar()
        password = tk.StringVar()
        cnic = tk.StringVar()

        label(body, "Name"); entry(body, name)
        label(body, "Seller ID"); entry(body, sid)
        label(body, "Email"); entry(body, email)
        label(body, "Address"); entry(body, address)
        label(body, "Phone"); entry(body, phone)
        label(body, "Password"); entry(body, password, show="*")
        label(body, "CNIC"); entry(body, cnic)

        def do_signup():
            with open(SELLER_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # uniqueness checks
            for line in lines[1:]:
                if not line.strip():
                    continue
                c = line.strip().split(",")
                if c[3] == sid.get().strip():
                    messagebox.showerror("Error", "Seller ID already exists.")
                    return
                if c[4] == email.get().strip():
                    messagebox.showerror("Error", "Email already exists.")
                    return
                if c[6] == phone.get().strip():
                    messagebox.showerror("Error", "Phone already exists.")
                    return
                if c[7] == cnic.get().strip():
                    messagebox.showerror("Error", "CNIC already exists.")
                    return

            no = len(lines)  # header already included
            with open(SELLER_FILE, "a", encoding="utf-8") as f:
                f.write(f"{no},{name.get().strip()},{password.get().strip()},{sid.get().strip()},"
                        f"{email.get().strip()},{address.get().strip()},{phone.get().strip()},{cnic.get().strip()}\n")

            messagebox.showinfo("Success", "Seller account created.")
            self.show_seller_login()

        button(body, "Create Account", do_signup, color=BTN2)
        button(body, "Back", self.show_seller_auth, color=BTN3)

    def show_seller_login(self):
        self.clear()
        body = glass_card(self.container, "Seller Login")

        uname = tk.StringVar()
        pwd = tk.StringVar()

        label(body, "Seller Name"); entry(body, uname)
        label(body, "Password"); entry(body, pwd, show="*")

        def do_login():
            with open(SELLER_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
            for line in lines[1:]:
                if not line.strip():
                    continue
                c = line.strip().split(",")
                if c[1] == uname.get().strip() and c[2] == pwd.get().strip():
                    self.current_role = "seller"
                    self.current_user = {
                        "name": c[1], "password": c[2], "id": c[3],
                        "email": c[4], "address": c[5], "phone": c[6], "cnic": c[7]
                    }
                    self.show_seller_dashboard()
                    return
            messagebox.showerror("Login Failed", "Invalid seller credentials.")

        button(body, "Login", do_login)
        button(body, "Back", self.show_seller_auth, color=BTN3)

    def show_seller_dashboard(self):
        self.clear()
        seller = self.current_user
        body = glass_card(self.container, f"Seller Dashboard — {seller['name']} (ID: {seller['id']})")

        top = tk.Frame(body, bg=CARD)
        top.pack(fill="x", pady=(0, 10))
        tk.Button(top, text="Logout", command=self.logout,
                  bg="#2b1630", fg="#ffd7ef", relief="flat",
                  font=("Segoe UI", 10, "bold"), padx=10, pady=6).pack(side="right")

        left = tk.Frame(body, bg=CARD)
        right = tk.Frame(body, bg=CARD)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))
        right.pack(side="left", fill="both", expand=True)

        tk.Label(left, text="Add Product", bg=CARD, fg=TXT, font=("Segoe UI", 11, "bold")).pack(anchor="w")

        pname = tk.StringVar()
        desc = tk.StringVar()
        category = tk.StringVar()
        brand = tk.StringVar()
        price = tk.StringVar()
        stock = tk.StringVar()

        label(left, "Product Name"); entry(left, pname)
        label(left, "Description"); entry(left, desc)
        label(left, "Category"); entry(left, category)
        label(left, "Brand"); entry(left, brand)
        label(left, "Price"); entry(left, price)
        label(left, "Stock"); entry(left, stock)

        cols = ("product_id", "product_name", "price", "stock", "status")
        tree = ttk.Treeview(right, columns=cols, show="headings", height=8)
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=140, anchor="w")

        tk.Label(right, text="My Products", bg=CARD, fg=TXT, font=("Segoe UI", 11, "bold")).pack(anchor="w")
        tree.pack(fill="x", pady=8)

        out = tk.Text(right, height=10, bg=ENTRY_BG, fg=TXT, insertbackground=TXT,
                      relief="flat", highlightthickness=1, highlightbackground=BORDER,
                      font=("Consolas", 10))
        tk.Label(right, text="My Analytics (from economics.txt)", bg=CARD, fg=TXT,
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(10, 0))
        out.pack(fill="both", expand=True, pady=8)

        def refresh_products():
            for item in tree.get_children():
                tree.delete(item)
            with open(PRODUCT_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
            for line in lines[1:]:
                if not line.strip():
                    continue
                c = line.strip().split(",")
                if c[1] == seller["id"]:
                    tree.insert("", "end", values=(c[0], c[3], c[7], c[8], c[9]))

        def refresh_analytics():
            out.delete("1.0", "end")
            total_rev, best, lowest = compute_seller_analytics(seller["id"])
            out.insert("end", f"Total Revenue: {total_rev:.2f}\n")
            out.insert("end", f"Best Product: {best[0]} -> {best[1]:.2f}\n")
            out.insert("end", f"Lowest Product: {lowest[0]} -> {lowest[1]:.2f}\n")

        def add_product():
            # next product_id
            with open(PRODUCT_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
            mx = 0
            for line in lines[1:]:
                if not line.strip():
                    continue
                c = line.strip().split(",")
                try:
                    mx = max(mx, int(c[0]))
                except:
                    pass
            pid = mx + 1

            try:
                p = float(price.get().strip())
                s = int(stock.get().strip())
                if p < 0 or s < 0:
                    raise ValueError
            except:
                messagebox.showerror("Error", "Price must be number and Stock must be integer (>=0).")
                return

            created = now_str()
            with open(PRODUCT_FILE, "a", encoding="utf-8") as f:
                f.write(f"{pid},{seller['id']},{seller['name']},{pname.get().strip()},{desc.get().strip()},"
                        f"{category.get().strip()},{brand.get().strip()},{p:.2f},{s},active,0,{created}\n")
            messagebox.showinfo("Success", f"Product added (ID: {pid})")
            refresh_products()
            refresh_analytics()

        button(left, "Add Product", add_product, color=BTN2)
        button(right, "Refresh", lambda: (refresh_products(), refresh_analytics()))
        refresh_products()
        refresh_analytics()

    # =========================
    # Customer
    # =========================
    def show_customer_auth(self):
        self.clear()
        body = glass_card(self.container, "Customer — Sign up / Login")
        button(body, "Sign up (Create Customer)", self.show_customer_signup)
        button(body, "Login", self.show_customer_login)
        button(body, "Back", self.show_home, color=BTN3)

    def show_customer_signup(self):
        self.clear()
        body = glass_card(self.container, "Customer Sign Up")

        name = tk.StringVar()
        cid = tk.StringVar()
        email = tk.StringVar()
        address = tk.StringVar()
        phone = tk.StringVar()
        password = tk.StringVar()

        label(body, "Name"); entry(body, name)
        label(body, "Customer ID"); entry(body, cid)
        label(body, "Email"); entry(body, email)
        label(body, "Address"); entry(body, address)
        label(body, "Phone"); entry(body, phone)
        label(body, "Password"); entry(body, password, show="*")

        def do_signup():
            with open(CUSTOMER_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()

            for line in lines[1:]:
                if not line.strip():
                    continue
                c = line.strip().split(",")
                if c[3] == cid.get().strip():
                    messagebox.showerror("Error", "Customer ID already exists.")
                    return
                if c[4] == email.get().strip():
                    messagebox.showerror("Error", "Email already exists.")
                    return
                if c[6] == phone.get().strip():
                    messagebox.showerror("Error", "Phone already exists.")
                    return

            no = len(lines)
            with open(CUSTOMER_FILE, "a", encoding="utf-8") as f:
                f.write(f"{no},{name.get().strip()},{password.get().strip()},{cid.get().strip()},"
                        f"{email.get().strip()},{address.get().strip()},{phone.get().strip()}\n")

            messagebox.showinfo("Success", "Customer account created.")
            self.show_customer_login()

        button(body, "Create Account", do_signup, color=BTN2)
        button(body, "Back", self.show_customer_auth, color=BTN3)

    def show_customer_login(self):
        self.clear()
        body = glass_card(self.container, "Customer Login")

        uname = tk.StringVar()
        pwd = tk.StringVar()

        label(body, "Customer Name"); entry(body, uname)
        label(body, "Password"); entry(body, pwd, show="*")

        def do_login():
            with open(CUSTOMER_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
            for line in lines[1:]:
                if not line.strip():
                    continue
                c = line.strip().split(",")
                if c[1] == uname.get().strip() and c[2] == pwd.get().strip():
                    self.current_role = "customer"
                    self.current_user = {
                        "name": c[1], "password": c[2], "id": c[3],
                        "email": c[4], "address": c[5], "phone": c[6]
                    }
                    self.cart = []
                    self.show_customer_shop()
                    return
            messagebox.showerror("Login Failed", "Invalid customer credentials.")

        button(body, "Login", do_login)
        button(body, "Back", self.show_customer_auth, color=BTN3)

    def show_customer_shop(self):
        self.clear()
        cust = self.current_user
        body = glass_card(self.container, f"Customer Shop — {cust['name']} (ID: {cust['id']})")

        top = tk.Frame(body, bg=CARD)
        top.pack(fill="x", pady=(0, 10))
        tk.Button(top, text="Logout", command=self.logout,
                  bg="#2b1630", fg="#ffd7ef", relief="flat",
                  font=("Segoe UI", 10, "bold"), padx=10, pady=6).pack(side="right")

        left = tk.Frame(body, bg=CARD)
        right = tk.Frame(body, bg=CARD)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))
        right.pack(side="left", fill="both", expand=True)

        tk.Label(left, text="Search Products", bg=CARD, fg=TXT, font=("Segoe UI", 11, "bold")).pack(anchor="w")
        search_var = tk.StringVar()
        entry(left, search_var)

        pcols = ("product_id", "product_name", "price", "stock", "seller_id", "seller_name")
        ptree = ttk.Treeview(left, columns=pcols, show="headings", height=12)
        for c in pcols:
            ptree.heading(c, text=c)
            ptree.column(c, width=130, anchor="w")
        ptree.pack(fill="both", expand=True, pady=8)

        tk.Label(right, text="Cart", bg=CARD, fg=TXT, font=("Segoe UI", 11, "bold")).pack(anchor="w")
        ccols = ("product_id", "product_name", "unit_price", "quantity", "total")
        ctree = ttk.Treeview(right, columns=ccols, show="headings", height=10)
        for c in ccols:
            ctree.heading(c, text=c)
            ctree.column(c, width=140, anchor="w")
        ctree.pack(fill="x", pady=8)

        qty = tk.StringVar(value="1")
        label(right, "Quantity")
        entry(right, qty)

        total_lbl = tk.Label(right, text="Cart Total: 0.00", bg=CARD, fg=MUTED, font=("Segoe UI", 10, "bold"))
        total_lbl.pack(anchor="w", pady=(10, 0))

        def refresh_products():
            for item in ptree.get_children():
                ptree.delete(item)

            q = search_var.get().strip().lower()

            with open(PRODUCT_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()

            for line in lines[1:]:
                if not line.strip():
                    continue
                c = line.strip().split(",")
                # c indices:
                # 0 product_id, 1 seller_id, 2 seller_name, 3 product_name,
                # 7 price, 8 stock, 9 status
                if c[9].lower() != "active":
                    continue
                try:
                    st = int(c[8])
                except:
                    st = 0
                if st <= 0:
                    continue
                if q and q not in c[3].lower():
                    continue

                ptree.insert("", "end", values=(c[0], c[3], c[7], c[8], c[1], c[2]))

        def refresh_cart():
            for item in ctree.get_children():
                ctree.delete(item)

            total = 0.0
            for it in self.cart:
                ctree.insert("", "end", values=(it["product_id"], it["product_name"], it["unit_price"], it["quantity"], it["total_price"]))
                total += float(it["total_price"])
            total_lbl.config(text=f"Cart Total: {total:.2f}")

        def add_to_cart():
            sel = ptree.selection()
            if not sel:
                messagebox.showerror("Error", "Select a product first.")
                return
            vals = ptree.item(sel[0], "values")
            pid, pname, price, stock, sid, sname = vals

            try:
                q = int(qty.get().strip())
                if q <= 0:
                    raise ValueError
            except:
                messagebox.showerror("Error", "Quantity must be a positive integer.")
                return

            if q > int(stock):
                messagebox.showerror("Error", "Not enough stock.")
                return

            unit = float(price)
            # merge if exists
            for it in self.cart:
                if it["product_id"] == pid:
                    new_q = int(it["quantity"]) + q
                    if new_q > int(stock):
                        messagebox.showerror("Error", "Not enough stock for combined quantity.")
                        return
                    it["quantity"] = str(new_q)
                    it["total_price"] = f"{unit * new_q:.2f}"
                    refresh_cart()
                    return

            self.cart.append({
                "product_id": pid,
                "product_name": pname,
                "unit_price": f"{unit:.2f}",
                "quantity": str(q),
                "total_price": f"{unit * q:.2f}",
                "seller_id": sid,
                "seller_name": sname
            })
            refresh_cart()

        def checkout():
            if not self.cart:
                messagebox.showerror("Error", "Cart is empty.")
                return

            # read product file
            with open(PRODUCT_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()

            header = lines[0]
            products = []
            for line in lines[1:]:
                if line.strip():
                    products.append(line.strip().split(","))

            # map by product_id
            prod_map = {}
            for p in products:
                prod_map[p[0]] = p

            # validate stock
            for it in self.cart:
                pid = it["product_id"]
                q = int(it["quantity"])
                if pid not in prod_map:
                    messagebox.showerror("Error", f"Product {pid} not found.")
                    return
                if int(prod_map[pid][8]) < q:
                    messagebox.showerror("Error", f"Not enough stock for {prod_map[pid][3]}.")
                    return

            # next order_id
            with open(ECON_FILE, "r", encoding="utf-8") as f:
                elines = f.readlines()
            mx = 0
            for line in elines[1:]:
                if line.strip():
                    c = line.strip().split(",")
                    try:
                        mx = max(mx, int(c[0]))
                    except:
                        pass
            order_id = mx + 1

            # update stocks + write econ rows
            for it in self.cart:
                pid = it["product_id"]
                q = int(it["quantity"])

                # reduce stock
                prod_map[pid][8] = str(int(prod_map[pid][8]) - q)

                # write economics
                dt = now_str()
                unit = float(it["unit_price"])
                total = float(it["total_price"])
                with open(ECON_FILE, "a", encoding="utf-8") as f:
                    f.write(f"{order_id},{dt},{cust['id']},{cust['name']},{it['seller_id']},{it['seller_name']},"
                            f"{pid},{it['product_name']},{unit:.2f},{q},{total:.2f}\n")

            # rewrite product file
            new_lines = [header]
            for pid, row in prod_map.items():
                new_lines.append(",".join(row) + "\n")
            with open(PRODUCT_FILE, "w", encoding="utf-8") as f:
                f.writelines(new_lines)

            messagebox.showinfo("Success", f"Purchase successful! Order ID: {order_id}")
            self.cart = []
            refresh_cart()
            refresh_products()

        def clear_cart():
            self.cart = []
            refresh_cart()

        button(right, "Add to Cart", add_to_cart, color=BTN)
        button(right, "Checkout (Buy)", checkout, color=BTN2)
        button(right, "Clear Cart", clear_cart, color=BTN3)

        search_var.trace_add("write", lambda *_: refresh_products())

        refresh_products()
        refresh_cart()

    def logout(self):
        self.current_role = None
        self.current_user = None
        self.cart = []
        self.show_home()

if __name__ == "__main__":
    App().mainloop()
