"""
Задание состоит из двух частей. 
1 часть – написать программу в соответствии со своим вариантом задания. 
Написать 2 варианта формирования (алгоритмический и с помощью функций Питона), 
сравнив по времени их выполнение.
2 часть – усложнить написанную программу, введя по своему усмотрению в условие 
минимум одно ограничение на характеристики объектов (которое будет сокращать 
количество переборов)  и целевую функцию для нахождения оптимального  решения.

Вариант 26. В фирме К сотрудников. Сформируйте разные варианты их участия в Т выстовках.

Требуется для своего варианта второй части л.р. №6 (усложненной программы) разработать реализацию с использованием графического интерфейса. Допускается использовать любую графическую библиотеку питона.  
"""

from tkinter import *
from tkinter import ttk, messagebox
import random as r
import itertools
import time

def generate_combinations(employees, exhibitions):
    def product_with_repeat(n, r):
        if r == 0:
            yield ()
        else:
            for i in range(n):
                for p in product_with_repeat(n, r - 1):
                    yield (i,) + p

    valid_combinations = []
    for comb in product_with_repeat(2, len(employees) * exhibitions):
        comb_matrix = [
            [employees[j] if comb[i * len(employees) + j] == 1 else None for j in range(len(employees))]
            for i in range(exhibitions)
        ]
        flat_comb = [emp for sublist in comb_matrix for emp in sublist]
        if all(flat_comb.count(emp) <= 1 for emp in employees):
            valid_combinations.append([[emp for emp in ex if emp is not None] for ex in comb_matrix])
    return valid_combinations

def create_employees(num):
    employees = [f'{r.choice("МЖ")}{i+1}' for i in range(num)]
    employee_parameters = {emp: r.randint(0, 100) for emp in employees}
    employee_list = ', '.join(f'{k} {v}' for k, v in employee_parameters.items())
    return employees, employee_parameters, employee_list

def filter_employees(employees, employee_parameters):
    return [emp for emp in employees if employee_parameters[emp] >= 50]

def itertools_combinations_hard(employees, exhibitions):
    all_combinations = itertools.product(range(2), repeat=len(employees) * exhibitions)
    valid_combinations = []
    for comb in all_combinations:
        comb_matrix = [
            [employees[j] if comb[i * len(employees) + j] == 1 else None for j in range(len(employees))]
            for i in range(exhibitions)
        ]
        flat_comb = [emp for sublist in comb_matrix for emp in sublist]
        if all(flat_comb.count(emp) <= 1 for emp in employees):
            valid_combinations.append([[emp for emp in ex if emp is not None] for ex in comb_matrix])
    return valid_combinations

def print_combinations(combinations):
    result = []
    for i, combination in enumerate(combinations, start=1):
        variant = f"Вариант {i}:"
        exhibitions = []
        for j, exhibition in enumerate(combination, start=1):
            present_employees = [emp for emp in exhibition if emp is not None]
            exhibitions.append(f"  Выставка {j}: {present_employees if present_employees else 'никто'}")
        result.append(variant + '\n' + '\n'.join(exhibitions))
    return '\n\n'.join(result)

def run_program():
    K = int(employees_entry.get())
    T = int(exhibitions_entry.get())

    option = version.get()
    employees, employee_parameters, employee_list = create_employees(K)

    if option == 0:
        start_time = time.time()
        combinations = generate_combinations(employees, T)
        algo_time = time.time() - start_time

        result_text = print_combinations(combinations)
        result_text = f"Алгоритмический метод:\n{result_text}\n\nВремя выполнения: {algo_time:.5f} сек"

    else:
        employees = filter_employees(employees, employee_parameters)
        result_text = print_combinations(itertools_combinations_hard(employees, T))
        result_text = f"{employee_list}\n\nРезультаты выполнения с учетом рейтинга:\n\n{result_text}"

    display_results(result_text)

def display_results(result_text):
    result_window = Toplevel(root)
    result_window.title("Результаты")

    text = Text(result_window, wrap="word", width=80, height=20)
    text.insert(1.0, result_text)
    text.config(state=DISABLED)
    text.grid(row=0, column=0, sticky="nsew")

    scrollbar = Scrollbar(result_window, command=text.yview)
    scrollbar.grid(row=0, column=1, sticky='ns')
    text.config(yscrollcommand=scrollbar.set)

    result_window.grid_rowconfigure(0, weight=1)
    result_window.grid_columnconfigure(0, weight=1)

# Создание графического интерфейса
root = Tk()
root.title("Программа для генерации комбинаций")

mainframe = ttk.Frame(root, padding="10 10 10 10")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

employees_label = ttk.Label(mainframe, text="Количество сотрудников:")
employees_label.grid(column=1, row=1, sticky=W)

employees_entry = ttk.Entry(mainframe)
employees_entry.grid(column=2, row=1, sticky=(W, E))

exhibitions_label = ttk.Label(mainframe, text="Количество выставок:")
exhibitions_label.grid(column=1, row=2, sticky=W)

exhibitions_entry = ttk.Entry(mainframe)
exhibitions_entry.grid(column=2, row=2, sticky=(W, E))

version = IntVar()
simple_radio = ttk.Radiobutton(mainframe, text="Обычная версия", variable=version, value=0)
simple_radio.grid(column=1, row=3, sticky=W)
complex_radio = ttk.Radiobutton(mainframe, text="Усложнённая версия", variable=version, value=1)
complex_radio.grid(column=2, row=3, sticky=W)

run_button = ttk.Button(mainframe, text="Запустить программу", command=run_program)
run_button.grid(column=1, row=4, columnspan=2)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

employees_entry.focus()
root.bind('<Return>', lambda event: run_program())

root.mainloop()
