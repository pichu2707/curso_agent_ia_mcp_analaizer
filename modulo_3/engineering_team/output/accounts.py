# accounts.py

def get_share_price(symbol: str) -> float:
    """
    Devuelve el precio actual de una acción. Esta es una implementación de prueba.
    
    :param symbol: Símbolo de la acción.
    :return: Precio actual de la acción.
    """
    prices = {
        "AAPL": 150.0,
        "TSLA": 700.0,
        "GOOGL": 2800.0
    }
    return prices.get(symbol, 0.0)


class Account:
    """
    Representa una cuenta de usuario en la plataforma de simulación de trading.
    Permite gestionar saldos, realizar transacciones y calcular el valor del portafolio.
    """

    def __init__(self, user_id: str, initial_deposit: float):
        """
        Inicializa una nueva cuenta de usuario.
        
        :param user_id: Identificación única del usuario.
        :param initial_deposit: Depósito inicial para la cuenta.
        """
        self.user_id = user_id
        self.initial_deposit = initial_deposit
        self.balance = initial_deposit
        self.positions = {}  # Diccionario para mantener las posiciones de acciones
        self.transactions = []  # Lista para registrar transacciones realizadas

    def deposit(self, amount: float) -> None:
        """
        Deposita una cantidad de dinero en la cuenta.
        
        :param amount: Cantidad de dinero a depositar.
        """
        if amount <= 0:
            raise ValueError("El monto del depósito debe ser mayor que cero.")
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        """
        Retira una cantidad de dinero de la cuenta si hay suficiente saldo.
        
        :param amount: Cantidad de dinero a retirar.
        """
        if amount <= 0:
            raise ValueError("El monto del retiro debe ser mayor que cero.")
        if self.balance - amount < 0:
            raise ValueError("Retiro no permitido: saldo insuficiente.")
        self.balance -= amount

    def buy_stock(self, symbol: str, quantity: int) -> None:
        """
        Compra acciones de una compañía especificada si hay suficiente saldo.
        
        :param symbol: Símbolo del stock a comprar.
        :param quantity: Cantidad de acciones a comprar.
        """
        price_per_share = get_share_price(symbol)
        total_price = price_per_share * quantity
        
        if total_price > self.balance:
            raise ValueError("Compra no permitida: fondos insuficientes.")
        
        self.balance -= total_price
        self.positions[symbol] = self.positions.get(symbol, 0) + quantity
        self.transactions.append(("BUY", symbol, quantity, price_per_share, total_price))

    def sell_stock(self, symbol: str, quantity: int) -> None:
        """
        Vende acciones de una compañía especificada si el usuario posee suficientes acciones.
        
        :param symbol: Símbolo del stock a vender.
        :param quantity: Cantidad de acciones a vender.
        """
        if symbol not in self.positions or self.positions[symbol] < quantity:
            raise ValueError("Venta no permitida: no se poseen suficientes acciones.")
        
        price_per_share = get_share_price(symbol)
        total_price = price_per_share * quantity
        
        self.balance += total_price
        self.positions[symbol] -= quantity
        if self.positions[symbol] == 0:
            del self.positions[symbol]
        self.transactions.append(("SELL", symbol, quantity, price_per_share, total_price))

    def get_portfolio_value(self) -> float:
        """
        Calcula el valor total del portafolio del usuario basado en el saldo y en las acciones.
        
        :return: Valor total del portafolio.
        """
        total_value = self.balance
        for symbol, quantity in self.positions.items():
            total_value += get_share_price(symbol) * quantity
        return total_value

    def get_profit_loss(self) -> float:
        """
        Calcula la ganancia o pérdida del portafolio respecto al depósito inicial.
        
        :return: Ganancia o pérdida.
        """
        return self.get_portfolio_value() - self.initial_deposit

    def get_holdings(self) -> dict:
        """
        Retorna las posiciones actuales de acciones del usuario.
        
        :return: Un diccionario con las posiciones de acciones.
        """
        return self.positions

    def get_transactions(self) -> list:
        """
        Retorna un registro de todas las transacciones realizadas por el usuario.
        
        :return: Lista de transacciones.
        """
        return self.transactions