import gradio as gr
from accounts import Account, get_share_price

# Inicializar una cuenta global para la demostración
account = None

def create_account(user_id, initial_deposit):
    global account
    try:
        initial_deposit = float(initial_deposit)
        if initial_deposit <= 0:
            return "El depósito inicial debe ser mayor que cero."
        account = Account(user_id, initial_deposit)
        return f"Cuenta creada con éxito para {user_id} con un depósito inicial de ${initial_deposit:.2f}"
    except ValueError as e:
        return f"Error: {str(e)}"

def deposit(amount):
    global account
    if account is None:
        return "Error: Primero debes crear una cuenta."
    try:
        amount = float(amount)
        account.deposit(amount)
        return f"Depósito de ${amount:.2f} realizado con éxito. Nuevo saldo: ${account.balance:.2f}"
    except ValueError as e:
        return f"Error: {str(e)}"

def withdraw(amount):
    global account
    if account is None:
        return "Error: Primero debes crear una cuenta."
    try:
        amount = float(amount)
        account.withdraw(amount)
        return f"Retiro de ${amount:.2f} realizado con éxito. Nuevo saldo: ${account.balance:.2f}"
    except ValueError as e:
        return f"Error: {str(e)}"

def buy_stock(symbol, quantity):
    global account
    if account is None:
        return "Error: Primero debes crear una cuenta."
    try:
        quantity = int(quantity)
        price = get_share_price(symbol)
        
        if price == 0:
            return f"Error: El símbolo {symbol} no está disponible. Símbolos válidos: AAPL, TSLA, GOOGL."
        
        total_cost = price * quantity
        
        if total_cost > account.balance:
            return f"Error: Fondos insuficientes. Se necesitan ${total_cost:.2f} pero solo tienes ${account.balance:.2f}"
        
        account.buy_stock(symbol, quantity)
        return f"Compra exitosa: {quantity} acciones de {symbol} a ${price:.2f} por acción. Total: ${total_cost:.2f}. Saldo restante: ${account.balance:.2f}"
    except ValueError as e:
        return f"Error: {str(e)}"

def sell_stock(symbol, quantity):
    global account
    if account is None:
        return "Error: Primero debes crear una cuenta."
    try:
        quantity = int(quantity)
        
        if symbol not in account.positions or account.positions[symbol] < quantity:
            current = account.positions.get(symbol, 0)
            return f"Error: No tienes suficientes acciones. Intentaste vender {quantity} de {symbol}, pero solo tienes {current}."
        
        price = get_share_price(symbol)
        total_value = price * quantity
        
        account.sell_stock(symbol, quantity)
        return f"Venta exitosa: {quantity} acciones de {symbol} a ${price:.2f} por acción. Total: ${total_value:.2f}. Nuevo saldo: ${account.balance:.2f}"
    except ValueError as e:
        return f"Error: {str(e)}"

def get_account_info():
    global account
    if account is None:
        return "Error: Primero debes crear una cuenta."
    
    portfolio_value = account.get_portfolio_value()
    profit_loss = account.get_profit_loss()
    
    info = f"ID de Usuario: {account.user_id}\n"
    info += f"Depósito inicial: ${account.initial_deposit:.2f}\n"
    info += f"Saldo en efectivo: ${account.balance:.2f}\n"
    info += f"Valor total del portafolio: ${portfolio_value:.2f}\n"
    
    if profit_loss >= 0:
        info += f"Ganancia: ${profit_loss:.2f} (+{(profit_loss/account.initial_deposit)*100:.2f}%)\n"
    else:
        info += f"Pérdida: ${abs(profit_loss):.2f} (-{(abs(profit_loss)/account.initial_deposit)*100:.2f}%)\n"
    
    return info

def get_holdings_info():
    global account
    if account is None:
        return "Error: Primero debes crear una cuenta."
    
    if not account.positions:
        return "No tienes acciones actualmente."
    
    holdings = "Tus acciones actuales:\n"
    total_value = 0
    
    for symbol, quantity in account.positions.items():
        price = get_share_price(symbol)
        value = price * quantity
        total_value += value
        holdings += f"- {symbol}: {quantity} acciones a ${price:.2f} = ${value:.2f}\n"
    
    holdings += f"\nValor total en acciones: ${total_value:.2f}"
    return holdings

def get_transactions_info():
    global account
    if account is None:
        return "Error: Primero debes crear una cuenta."
    
    if not account.transactions:
        return "No has realizado transacciones todavía."
    
    transactions = "Historial de transacciones:\n"
    
    for i, (action, symbol, quantity, price, total) in enumerate(account.transactions, 1):
        transactions += f"{i}. {action}: {quantity} x {symbol} a ${price:.2f} = ${total:.2f}\n"
    
    return transactions

def get_stock_price_info(symbol):
    if not symbol:
        return "Introduce un símbolo para verificar su precio."
    
    price = get_share_price(symbol)
    if price == 0:
        return f"El símbolo {symbol} no está disponible. Símbolos válidos: AAPL, TSLA, GOOGL."
    return f"Precio actual de {symbol}: ${price:.2f}"

# Interfaz de usuario con Gradio
with gr.Blocks(title="Simulador de Trading") as demo:
    gr.Markdown("# Simulador de Trading")
    
    with gr.Tab("Crear Cuenta"):
        with gr.Row():
            user_id_input = gr.Textbox(label="ID de Usuario")
            initial_deposit_input = gr.Textbox(label="Depósito Inicial ($)")
        create_btn = gr.Button("Crear Cuenta")
        create_output = gr.Textbox(label="Resultado")
        create_btn.click(create_account, [user_id_input, initial_deposit_input], create_output)
    
    with gr.Tab("Depósito/Retiro"):
        with gr.Row():
            deposit_amount = gr.Textbox(label="Cantidad a Depositar ($)")
            deposit_btn = gr.Button("Depositar")
        deposit_output = gr.Textbox(label="Resultado del Depósito")
        deposit_btn.click(deposit, [deposit_amount], deposit_output)
        
        with gr.Row():
            withdraw_amount = gr.Textbox(label="Cantidad a Retirar ($)")
            withdraw_btn = gr.Button("Retirar")
        withdraw_output = gr.Textbox(label="Resultado del Retiro")
        withdraw_btn.click(withdraw, [withdraw_amount], withdraw_output)
    
    with gr.Tab("Comprar/Vender Acciones"):
        gr.Markdown("### Verificar Precio de Acciones")
        with gr.Row():
            price_check_symbol = gr.Textbox(label="Símbolo de la Acción (AAPL, TSLA, GOOGL)")
            price_check_btn = gr.Button("Verificar Precio")
        price_check_output = gr.Textbox(label="Precio Actual")
        price_check_btn.click(get_stock_price_info, [price_check_symbol], price_check_output)
        
        gr.Markdown("### Comprar Acciones")
        with gr.Row():
            buy_symbol = gr.Textbox(label="Símbolo de la Acción")
            buy_quantity = gr.Textbox(label="Cantidad de Acciones")
        buy_btn = gr.Button("Comprar")
        buy_output = gr.Textbox(label="Resultado de la Compra")
        buy_btn.click(buy_stock, [buy_symbol, buy_quantity], buy_output)
        
        gr.Markdown("### Vender Acciones")
        with gr.Row():
            sell_symbol = gr.Textbox(label="Símbolo de la Acción")
            sell_quantity = gr.Textbox(label="Cantidad de Acciones")
        sell_btn = gr.Button("Vender")
        sell_output = gr.Textbox(label="Resultado de la Venta")
        sell_btn.click(sell_stock, [sell_symbol, sell_quantity], sell_output)
    
    with gr.Tab("Información de la Cuenta"):
        account_info_btn = gr.Button("Obtener Información de la Cuenta")
        account_info_output = gr.Textbox(label="Información de la Cuenta")
        account_info_btn.click(get_account_info, [], account_info_output)
        
        holdings_btn = gr.Button("Ver Mis Acciones")
        holdings_output = gr.Textbox(label="Mis Acciones")
        holdings_btn.click(get_holdings_info, [], holdings_output)
        
        transactions_btn = gr.Button("Ver Historial de Transacciones")
        transactions_output = gr.Textbox(label="Historial de Transacciones")
        transactions_btn.click(get_transactions_info, [], transactions_output)

if __name__ == "__main__":
    demo.launch()