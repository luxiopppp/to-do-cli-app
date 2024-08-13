# to-do-cli-app/main.py

import os
import json
import questionary

import importlib.resources as pkg_resources

TASKS_PATH = pkg_resources.files("to_do_cli_app") / "tasks"
CONFIG_FILE = pkg_resources.files("to_do_cli_app") / "config.json"
INIT_FILE = TASKS_PATH / "0_tasks.txt"
INIT_FILENUM = 0
MAIN_CHOICES = ["Add task", "View tasks", "Delete task", "New task file", "Change task file", "Delete task file", "Quit"]

def check_tasks(file):
    tasks = []

    # Asegurarse de que el archivo existe
    with file.open("a"):
      pass

    with file.open("r") as f:
        lines = f.readlines()
        if lines:
            tasks.extend(line.strip() for line in lines)

    return tasks

def update_tasks(file, tasks):
  with file.open("w") as f:
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
  task_files = [
    file.stem
    for file in TASKS_PATH.iterdir()
    if file.is_file() and file.suffix == ".txt"
  ]
  task_numbers = sorted([int(file.split("_")[0]) for file in task_files])

  nt_id = 0  # new task ID
  for num in task_numbers:
    if num == nt_id:
      nt_id += 1
    else:
      break
  
  with (TASKS_PATH / f"{nt_id}_tasks.txt").open("w") as f:
    set_active_file(f"{nt_id}_tasks.txt")
    print(f"New task file created properly at {os.getcwd()}/tasks/")

def change_file():
  """"""
  task_files = [os.path.splitext(f)[0] for f in os.listdir(TASKS_PATH) if os.path.splitext(f)[1] == ".txt"]
  task_files.sort(key=lambda x: int(x.split("_")[0]))

  if not task_files:
    return

  choice = questionary.select("Select the task file to change to", task_files).ask()

  set_active_file(choice + ".txt")

def delete_file():
  """"""
  task_files = [
    file.stem
    for file in TASKS_PATH.iterdir()
    if file.is_file() and file.suffix == ".txt"
  ]
  task_files.sort(key=lambda x: int(x.split("_")[0]))

  if not task_files:
    return

  form = questionary.form(
    choice = questionary.select("Select the task file to remove", task_files),
    confirm = questionary.confirm(f"Are you sure you want to delete it? This proccess is permanent.", default=False)
  ).ask()

  if form["confirm"]:
    if get_active_file() != form["choice"] + ".txt":
      file_to_remove = str(TASKS_PATH / (form["choice"] + ".txt"))
      os.remove(file_to_remove)
      questionary.press_any_key_to_continue(f"File {form['choice']}.txt has been deleted. (Press any key to return)").ask()
    else:
      questionary.press_any_key_to_continue("You can't delete the file you are in. First change to another... (Press any key to return)").ask()

def set_active_file(file):
  if CONFIG_FILE.is_file():
    with CONFIG_FILE.open("r") as f:
      config = json.load(f)
  else:
    config = {}
  
  config["active_file"] = file
  
  with open(CONFIG_FILE, "w") as f:
    json.dump(config, f, indent=4)

def get_active_file():
  if CONFIG_FILE.is_file():
    with CONFIG_FILE.open("r") as f:
      config = json.load(f)
      if (TASKS_PATH / config.get("active_file")).is_file():
        return config.get("active_file")
      else:
        return INIT_FILE
  return None

def main_selection(tasks, filenum):
  print("======TO DO List App======")
  choice = questionary.select(f'You are in task file number {filenum}. Select an option', choices=MAIN_CHOICES, qmark='↓').ask()

  if choice == MAIN_CHOICES[0]:
    add_task(tasks)
  elif choice == MAIN_CHOICES[1]:
    view_tasks(tasks)
  elif choice == MAIN_CHOICES[2]:
    del_task(tasks)
  elif choice == MAIN_CHOICES[3]:
    new_file()
  elif choice == MAIN_CHOICES[4]:
    change_file()
  elif choice == MAIN_CHOICES[5]:
    delete_file()
  elif choice == MAIN_CHOICES[-1]:
    return -1

def main():
  print("Welcome!")

  if not TASKS_PATH.is_dir():
    tasks_path = str(TASKS_PATH)
    os.mkdir(tasks_path)

  while True:
    try:
      file_path = TASKS_PATH / get_active_file()
      filenum = os.path.basename(get_active_file()).split("_")[0]
    except:
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

