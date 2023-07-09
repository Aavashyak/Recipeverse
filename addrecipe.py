import PySimpleGUI as sg
import sqlite3

def create_database():
    conn = sqlite3.connect("recipes.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS recipes (
                dishname text,
                time integer,
                ingredients text,
                process text
                )""")
    conn.commit()
    conn.close()

def retrieve_recipes():
    stored = []
    conn = sqlite3.connect("recipes.db")
    c = conn.cursor()
    query = "SELECT dishname, time, ingredients, process from recipes"
    c.execute(query)
    for row in c:
        stored.append(list(row))
    conn.close()
    return stored

def get_recipe_records():
    recipe_records_array = retrieve_recipes()
    return recipe_records_array

def create_recipes_window():
    recipe_records_array = get_recipe_records()
    headings = ["Dish Name", "Prep Time", "Ingredients", "Process"]
    layout_for_display = [
        [sg.Table(values=recipe_records_array,
                  headings=headings,
                  max_col_width=35,
                  auto_size_columns=True,
                  display_row_numbers=True,
                  justification="left",
                  num_rows=10,
                  key="RECIPETABLE",
                  row_height=60,
                  enable_events=True,
                  tooltip="All Recipes")]
    ]
    windr = sg.Window("Recipes in The Recipeverse", layout_for_display, modal=True)
    while True:
        event, values = windr.read()
        if event == sg.WINDOW_CLOSED:
            break
    windr.close()

def add_recipe_window():
    sg.theme("SandyBeach")
    layout = [
        [sg.Text("Adding Recipe", justification="center")],
        [sg.Text("Search Recipe", size=43),sg.Input(tooltip="Input Dish Name to Search",enable_events=True,key="SEARCH")],
        [sg.Text("Dish Name:"), sg.Push(), sg.Input(key="DINAME")],
        [sg.Text("Preparation Time (Min):"), sg.Push(), sg.Input(key="TIME")],
        [sg.Text("Ingredients:"), sg.Push(), sg.ML(size=(43, 10), key="ING")],
        [sg.Text("Process:"), sg.Push(), sg.ML(size=(43, 10), key="PRO")],
        [sg.Button("Clear"), sg.Push(), sg.Button("Insert Recipe")],
        [sg.Button("View Other Recipes")],
        [sg.Button("Return to Hub")]
    ]

    window = sg.Window(title="Wanna Contribute?", layout=layout)

    def clear_inputs():
        window["DINAME"].update("")
        window["TIME"].update("")
        window["ING"].update("")
        window["PRO"].update("")

    def save_to_database(values):
        conn = sqlite3.connect("recipes.db")
        c = conn.cursor()
        c.execute("INSERT INTO recipes VALUES (:dishname, :time, :ingredients, :process)",
                  {
                      "dishname": values["DINAME"],
                      "time": values["TIME"],
                      "ingredients": values["ING"],
                      "process": values["PRO"]
                  })
        conn.commit()
        conn.close()

    def retrieve_info():
        if values["SEARCH"].strip() == " ":
            sg.Popup("Enter a Valid Name to Search")
        else:
            conn = sqlite3.connect("recipes.db")
            c = conn.cursor()
            record_id = values["SEARCH"]
            c.execute("SELECT * FROM recipes WHERE dishname = ?", (record_id,))
            records = c.fetchall()
            for record in records:
                window["DINAME"].update(record[0])
                window["TIME"].update(record[1])
                window["ING"].update(record[2])
                window["PRO"].update(record[3])
            conn.commit()
            conn.close()

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "Return to Hub":
            break
        if event == "Clear":
            clear_inputs()
        if event == "View Other Recipes":
            create_recipes_window()
        if event == "SEARCH":
            retrieve_info()
        if event == "Insert Recipe":
            diname = values["DINAME"]
            time = values["TIME"]
            ing = values["ING"]
            pro = values["PRO"]
            if not (diname and time and ing and pro):
                sg.Popup("Missing Fields, Please check your Recipe")
            else:
                try:
                    summary_list = "This Recipe will be Inserted into Recipeverse"
                    summary_list += "\nDish Name: " + diname
                    summary_list += "\nPrep Time: " + time
                    summary_list += "\nIngredients: " + ing
                    summary_list += "\nProcess: " + pro
                    choice = sg.PopupOKCancel(summary_list, "Is This The Recipe?")
                    if choice == "OK":
                        clear_inputs()
                        save_to_database(values)
                        sg.PopupQuick("Recipe Inserted")
                    else:
                        sg.PopupOK("Editing Recipe")
                except Exception as e:
                    sg.Popup("An error occurred:", str(e))

    window.close()

def search_recipe_window():
    # Add your code for the search recipe window here
    pass

def main_menu_window():
    sg.theme("SandyBeach")
    layout = [
        [sg.Text("Welcome to the Recipeverse", justification='center')],
        [sg.Push(), sg.Button("Enter The Recipeverse"), sg.Push()],
        [sg.Push(), sg.Button("Exit"), sg.Push()],
    ]

    window = sg.Window(title="Recipeverse", layout=layout)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WINDOW_CLOSED:
            break
        if event == "Enter The Recipeverse":
            add_recipe_window()
        if event == "Search For A Recipe":
            search_recipe_window()

    window.close()

create_database()
main_menu_window()