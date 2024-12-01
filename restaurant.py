import hashlib
import datetime

# Вспомогательная функция для хэширования паролей
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Структуры данных
users = {
    "admin": {"password": hash_password("123123"), "role": "admin"},
    "client": {"password": hash_password("321321"), "role": "client"}
}

menu_items = [
    {"item_id": 1, "name": "Паста Альфредо", "price": 300.00, "description": "Макароны с кремовым соусом Альфредо."},
    {"item_id": 2, "name": "Салат Цезарь", "price": 250.00, "description": "Салат с курицей, сухариками и пармезаном."},
    {"item_id": 3, "name": "Стейк Рибай", "price": 850.00, "description": "Нежный стейк из говядины."},
    {"item_id": 4, "name": "Шоколадный торт", "price": 200.00, "description": "Десерт с богатым шоколадным вкусом."},
    {"item_id": 5, "name": "Куриный суп", "price": 150.00, "description": "Легкий и ароматный куриный бульон."}
]

services = []  # Услуги в ресторане
purchase_history = []

# Рабочие функции
def login():
    print("\n--- Вход в систему ---")
    username = input("Введите имя пользователя: ")
    password = input("Введите пароль: ")
    if username in users and users[username]['password'] == hash_password(password):
        print(f"Добро пожаловать, {username}!")
        return username, users[username]['role']
    else:
        print("Неверное имя пользователя или пароль.")
        return None, None

def view_menu():
    if not menu_items:
        print("Нет доступных блюд.")
    else:
        print("\n--- Доступные блюда ---")
        for item in menu_items:
            print(f"ID: {item['item_id']}, Название: {item['name']}, Цена: {item['price']:.2f}, Описание: {item['description']}")

def order_menu_item(username):
    item_id = int(input("Введите ID блюда для заказа: "))
    item = next((itm for itm in menu_items if itm['item_id'] == item_id), None)
    if item:
        purchase_history.append({
            "purchase_id": len(purchase_history) + 1,
            "username": username,
            "item_id": item_id,
            "date": str(datetime.datetime.now())
        })
        print(f"Вы успешно заказали: {item['name']}")
    else:
        print("Блюдо с таким ID не найдено.")

def view_order_history(username):
    print("\n--- История заказов ---")
    for order in purchase_history:
        if order['username'] == username:
            item = next(iter(filter(lambda itm: itm['item_id'] == order['item_id'], menu_items)), None)
            print(f"ID заказа: {order['purchase_id']}, Блюдо: {item['name'] if item else 'Неизвестно'}, Дата: {order['date']}")
    if not any(order['username'] == username for order in purchase_history):
        print("Вы ещё ничего не заказали.")

def filter_menu_by_price():
    price_limit = float(input("Введите максимальную цену для фильтрации: "))
    filtered_items = list(filter(lambda itm: itm['price'] <= price_limit, menu_items))
    print("\n--- Блюда до указанной цены ---")
    if filtered_items:
        for item in filtered_items:
            print(f"ID: {item['item_id']}, Название: {item['name']}, Цена: {item['price']:.2f}")
    else:
        print("Нет блюд, соответствующих вашему критерию.")

def update_profile(username):
    new_password = input("Введите новый пароль: ")
    users[username]['password'] = hash_password(new_password)
    
    print("Пароль успешно обновлен.")

# Функции администратора
def add_menu_item():
    item_id = len(menu_items) + 1
    name = input("Введите название блюда: ")
    price = float(input("Введите цену блюда: "))
    description = input("Введите описание блюда: ")
    menu_items.append({
        "item_id": item_id,
        "name": name,
        "price": price,
        "description": description
    })
    print("Блюдо успешно добавлено.")

def remove_menu_item():
    item_id = int(input("Введите ID блюда для удаления: "))
    global menu_items
    menu_items = [itm for itm in menu_items if itm['item_id'] != item_id]
    print("Блюдо успешно удалено.")

def edit_menu_item():
    item_id = int(input("Введите ID блюда для редактирования: "))
    item = next((itm for itm in menu_items if itm['item_id'] == item_id), None)
    if item:
        name = input("Введите новое название блюда: ")
        price = float(input("Введите новую цену блюда: "))
        description = input("Введите новое описание блюда: ")
        item.update({"name": name, "price": price, "description": description})
        print("Блюдо успешно обновлено.")
    else:
        print("Блюдо с таким ID не найдено.")

def view_statistics():
    total_orders = len(purchase_history)
    print(f"Количество заказанных блюд: {total_orders}")

def manage_users():
    while True:
        action = input("Введите 'add' для добавления пользователя или 'remove' для удаления, 'exit' для выхода: ")
        if action == 'add':
            username = input("Введите имя нового пользователя: ")
            password = input("Введите пароль для нового пользователя: ")
            if username not in users:
                users[username] = {"password": hash_password(password), "role": "client"}
                print("Пользователь успешно добавлен.")
            else:
                print("Пользователь уже существует.")
        elif action == 'remove':
            username = input("Введите имя пользователя для удаления: ")
            if username in users:
                del users[username]
                print("Пользователь успешно удален.")
            else:
                print("Пользователь не найден.")
        elif action == 'exit':
            break

# Главная функция
def main():
    current_user, role = login()
    
    while current_user and role:
        if role == "client":
            while True:
                print("\--- Меню Клиента ---")
                print("1. Просмотр меню блюд")
                print("2. Заказать блюдо")
                print("3. Просмотр истории заказов")
                print("4. Фильтр блюд по цене")
                print("5. Обновление профиля")
                print("6. Выход")
                choice = input("Выберите действие: ")
                
                if choice == '1':
                    view_menu()
                elif choice == '2':
                    order_menu_item(current_user)
                elif choice == '3':
                    view_order_history(current_user)
                elif choice == '4':
                    filter_menu_by_price()
                elif choice == '5':
                    update_profile(current_user)
                elif choice == '6':
                    break
                else:
                    print("Некорректный ввод.")
        
        elif role == "admin":
            while True:
                print("\--- Меню Администратора ---")
                print("1. Добавить блюдо")
                print("2. Удалить блюдо")
                print("3. Редактировать блюдо")
                print("4. Просмотреть статистику")
                print("5. Управление пользователями")
                print("6. Выход")
                choice = input("Выберите действие: ")

                if choice == '1':
                    add_menu_item()
                elif choice == '2':
                    remove_menu_item()
                elif choice == '3':
                    edit_menu_item()
                elif choice == '4':
                    view_statistics()
                elif choice == '5':
                    manage_users()
                elif choice == '6':
                    break
                else:
                    print("Некорректный ввод.")

if __name__ == "__main__":
    main()
