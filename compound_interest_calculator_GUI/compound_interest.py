import PySimpleGUI as sg

sg.change_look_and_feel('DarkAmber')
layout = [[sg.Text('Calculate your compound interest')],
          [sg.Text('How many years are you planning to save?'), sg.InputText(size=(10,1), key='years')],
          [sg.Text('How much do you currently have in your account?'), sg.InputText(size=(10,1), key='current_amount')],
          [sg.Text('How much money do you plan in investing on a monthly basis?'), sg.InputText(size=(10,1), key='monthly_invest')],
          [sg.Text('How much do you think will be the YEARLY interest of this investment?'), sg.InputText(size=(10,1), key='interest')],
          [sg.OK(), sg.Cancel()],
          [sg.Text("Your total balance would be:")],
          [sg.Text('', size=(10,1), key='output')]]

window = sg.Window('Compound Interest Calculator', layout)
while True:
    event, values = window.read()
    if event in (None, 'Cancel'):
        break
    if event is not None:
        try:
            years, current_amount, monthly_invest, interest = int(values['years']), float(values['current_amount']), float(values['monthly_invest']), float(values['interest'])
            total_amount = current_amount
            yearly_invest = monthly_invest * 12.0
            interest = 1 + interest
            print(current_amount, current_amount * 12.0)
            for i in range(0, years):
                total_amount = (total_amount + yearly_invest) * (interest)
                print(yearly_invest)
        except:
            total_amount = 'Invalid'
        window['output'].update(total_amount)
    else:
        break


window.close()

## Calculate compound interest
def command_line_compound_interest():
    print("How many years are you planning to save?")
    years = int(input('Enter Years (e.g 1, 2 10): '))

    print("How much do you currently have in your account?")
    current_amount = float(input("Enter current amount in your account: "))

    print("How much money do you plan in investing on a monthly basis?")
    monthly_invest = float(input("Enter your monthly investing amount: "))

    print("How much do you think will be the YEARLY interest of this investment?")
    interest = float(input("Enter interest (e.g 10% = 0.1): "))

    print(' ')

    total_amount = current_amount
    yearly_invest = monthly_invest * 12 ## Yearly amount

    for i in range(0, years):
        total_amount = total_amount + yearly_invest * (1 + interest)

    print("Your total balance after {} years will be: ".format(years) + str(total_amount))
