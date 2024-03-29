from abstract_class import Abstract
from MixinClass import MixinLog


class MyValueError(Exception):
    def __init__(self, message="Tовар с нулевым количеством не может быть добавлен"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class Category:
    title: str
    description: str
    products: list

    total_numbers_of_category = 0
    unique_products = 0

    def __init__(self, title, description, products):
        self.title = title
        self.description = description
        self.__products = products

        Category.total_numbers_of_category += 1
        Category.unique_products += 1

    def __str__(self):
        return f'{self.title}, количество продуктов: {Category.__len__(self)} шт.'

    def __len__(self):
        return len(self.__products)

    def get_name(self):
        return self.title

    def get_description(self):
        return self.description

    def get_products(self):
        return self.__products

    @property
    def products(self):
        list_product = []
        for products in self.__products:
            list_product.append(f"{products.name}, {products.price} руб. Остаток: {products.quantity} шт.\n")
        return list_product

    def add_products(self, value):
        """Проверка что класс объекта является дочерним класса Product или базовым классом Product"""
        if not isinstance(value, Product):
            raise TypeError("Добавлять можно только объекты Product или его наследников")
        # Обрабатываем ситуацию с нулевым количеством товара
        try:
            if value.quantity_in_stock == 0:
                raise MyValueError
        except MyValueError as e:
            print(e.message)
        else:
            self.__products.append(value)
            Category.unique_products += 1
            print(f'Товар "{value.title}" добавлен в категорию "{self.title}"')
        finally:
            print("Обработка добавления товара завершена")

    def avg_price(self):
        """
            Метод подсчитывает средний ценник всех товаров.
            С помощью исключений обработать случай, когда в категории нет товаров
            и сумма всех товаров будет делиться на ноль.
            В случае, если такое происходит, возвращать ноль.
        """
        total_sum = 0
        total_quant = 0
        try:
            for product in self.__products:
                total_sum += product.price * product.quantity
                total_quant += product.quantity
            return total_sum / total_quant
        except ZeroDivisionError:
            return 0


class Product(Abstract, MixinLog):
    title: str
    description: str
    price: float
    quantity_in_stock: int

    def __init__(self, name, description, price, quantity_in_stock):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity_in_stock = quantity_in_stock
        super().__init__()

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity_in_stock} шт."

    def __add__(self, other):
        if isinstance(other, type(self)):
            return self.price * self.quantity_in_stock + other.price * other.quantity_in_stock
        else:
            raise TypeError

    def get_title(self):
        return self.name

    def get_description(self):
        return self.description

    @property
    def price(self):
        return self.__price

    def get_quantity_in_stock(self):
        return self.quantity_in_stock

    @price.setter
    def price(self, value):
        if value <= 0:
            print("Цена введена не корректно")
        elif value < self.__price:
            while True:
                answer = input("Новая цена ниже чем старая, вы уверены что хотите изменить цену (y/n): ").lower()
                if answer == 'y':
                    self.__price = value
                    break
                elif answer == "n":
                    break
        else:
            self.__price = value

    @classmethod
    def create_product(cls, new_product):
        if new_product['quantity'] >= 1:
            return cls(**new_product)
        else:
            raise ValueError

    def average_price(self):
        try:
            av_price = self.price / self.quantity_in_stock
        except ZeroDivisionError:
            print('В категории нет товаров')
        else:
            print(av_price)
