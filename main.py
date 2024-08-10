import os
import json
import questionary

TASKS_PATH = "./tasks/"
INIT_FILE = "0_tasks.txt"
INIT_FILENUM = 0
OPTIONS = ["Add task", "View tasks", "Delete task", "New task file", "Change task file", "Delete task file", "Quit"]
CONFIG_FILE = "config.json"

def check_tasks(file):
    tasks = []

    # Asegurarse de que el archivo existe
    open(file, "a").close()

    with open(file, "r") as f: # with ya cierra el archivo, no hace falta el f.close()
        lines = f.readlines()
        if lines:
            tasks.extend(line.strip() for line in lines)

    return tasks

def update_tasks(file, tasks):
  with open(file, "w") as f:
    for task in tasks:
      f.writelines(task + '\n')

def add_task(tasks):
  print("======Add======")

  task = input("Enter the task (Press enter to cancel): ")
  if task != "":
    if task not in tasks:
      tasks.append(task)
      print(f"Task '{task}' successfully added")
    else:
      print(f"Task '{task}' already exists")

def view_tasks(tasks):
  print("======Tasks======")

  if len(tasks) == 0:
    print("There is no tasks here...")
  else:
    print("list of tasks:")
    for i, task in enumerate(tasks):
      print(f'{i + 1}. {task}')
  
  questionary.press_any_key_to_continue().ask()

def del_task(tasks):
  print("======Delete======")

  if len(tasks) == 0:
    print("No task to delete")
    questionary.press_any_key_to_continue("Press any key to return...").ask()
  else:
    choices = questionary.checkbox("Select the task to delete", choices=tasks, qmark="🗑 ").ask()

    if len(choices) > 0:
      try:
        tasks[:] = [task for task in tasks if task not in choices]
        for task in choices:
          print(f"Task '{task}' successfully deleted")
      except IndexError:
        print("Error: An unexpected error occurred while deleting tasks.")
    else:
        print("No task selected")

def new_file():
  """"""
  task_files = [os.path.splitext(f)[0] for f in os.listdir("./tasks") if os.path.splitext(f)[1] == ".txt"]
  task_numbers = sorted([int(file.split("_")[0]) for file in task_files])

  nt_id = 0  # new task ID
  for num in task_numbers:
    if num == nt_id:
      nt_id += 1
    else:
      break
  
  open(f"./tasks/{nt_id}_tasks.txt", "a").close()
  print(f"New task file created properly at {os.getcwd()}/tasks/")
  questionary.press_any_key_to_continue("Press any key to return...").ask()

def change_file():
  """"""
  task_files = [os.path.splitext(f)[0] for f in os.listdir("./tasks") if os.path.splitext(f)[1] == ".txt"]
  task_files.sort(key=lambda x: int(x.split("_")[0]))

  if not task_files:
    return

  choice = questionary.select("Select the task file to change to", task_files).ask()

  set_active_file(choice + ".txt")

def delete_file():
  """"""
  task_files = [os.path.splitext(f)[0] for f in os.listdir("./tasks") if os.path.splitext(f)[1] == ".txt"]
  task_files.sort(key=lambda x: int(x.split("_")[0]))

  if not task_files:
    return

  form = questionary.form(
    choice = questionary.select("Select the task file to remove", task_files),
    confirm = questionary.confirm(f"Are you sure you want to delete it? This proccess is permanent.", default=False)
  ).ask()

  if form["confirm"]:
    if get_active_file() != form["choice"] + ".txt":
      os.remove(TASKS_PATH + form["choice"] + ".txt")
      questionary.press_any_key_to_continue(f"File {form['choice']}.txt has been deleted. (Press any key to return)").ask()
    else:
      questionary.press_any_key_to_continue("You can't delete the file you are in. First change to another... (Press any key to return)").ask()

def set_active_file(file):
  if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r") as f:
      config = json.load(f)
  else:
    config = {}
  
  config["active_file"] = file
  
  with open(CONFIG_FILE, "w") as f:
    json.dump(config, f, indent=4)

def get_active_file():
  if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r") as f:
      config = json.load(f)
      if os.path.exists(TASKS_PATH + config.get("active_file")):
        return config.get("active_file")
      else:
        return INIT_FILE
  return None

def main_selection(tasks, filenum):
  print("======TO DO List App======")
  choice = questionary.select(f'You are in task file number {filenum}. Select an option', choices=OPTIONS, qmark='↓').ask()

  if choice == OPTIONS[0]:
    add_task(tasks)
  elif choice == OPTIONS[1]:
    view_tasks(tasks)
  elif choice == OPTIONS[2]:
    del_task(tasks)
  elif choice == OPTIONS[3]:
    new_file()
  elif choice == OPTIONS[4]:
    change_file()
  elif choice == OPTIONS[5]:
    delete_file()
  elif choice == OPTIONS[-1]:
    return -1

def main():
  print("Welcome!")

  if not os.path.exists(TASKS_PATH):
    os.mkdir(TASKS_PATH)

  while True:
    try:
      file_path = TASKS_PATH + get_active_file()
      filenum = get_active_file().split("_")[0]
    except NameError:
      file_path = INIT_FILE
      filenum = INIT_FILENUM
    tasks = check_tasks(file_path)

    ms = main_selection(tasks, filenum)

    if ms != -1:
      update_tasks(file_path, tasks)
    else:
      print("Goodbye!")
      break

if __name__ == "__main__":
  main()

