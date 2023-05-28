import os
import sys
import tkinter as tk
import subprocess
from tkinter import messagebox


def add_app_to_settings(project_name, app_name):
    for root, dirs, files in os.walk(project_name):
        if "settings.py" in files:
            settings_file = os.path.join(root, "settings.py")
            break
    else:
        raise FileNotFoundError(
            f"Settings file 'settings.py' not found in the project directory.")

    with open(settings_file, "r") as file:
        lines = file.readlines()

    installed_apps_line = None
    for i, line in enumerate(lines):
        if line.startswith("INSTALLED_APPS"):
            installed_apps_line = i
            break

    if installed_apps_line is not None:
        app_line = f"    '{app_name}',\n"
        lines.insert(installed_apps_line + 1, app_line)

        with open(settings_file, "w") as file:
            file.writelines(lines)

        console_text.insert(tk.END, "Added the app to settings.py.\n")
        console_text.update()


def create_django_project(project_name, app_name):
    try:
        subprocess.run(['mkdir', project_name], check=True)
        os.chdir(project_name)

        console_text.config(state="normal")

        console_text.delete("1.0", tk.END)

        console_text.insert(tk.END, "Creating virtual environment...\n")
        console_text.update()

        subprocess.run(['pipenv', 'install', 'django'],
                       check=True, stdout=subprocess.PIPE)

        console_text.insert(tk.END, "Creating Django project...\n")
        console_text.update()

        subprocess.run(['pipenv', 'run', 'django-admin', 'startproject',
                       project_name, '.'], check=True, stdout=subprocess.PIPE)

        console_text.insert(tk.END, "Creating Django app...\n")
        console_text.update()

        subprocess.run(['pipenv', 'run', 'python', 'manage.py',
                       'startapp', app_name], check=True, stdout=subprocess.PIPE)

        add_app_to_settings(project_name, app_name)

        console_text.insert(tk.END, "Django project created successfully!\n")
        console_text.update()
        console_text.config(state="disabled")

        console_text.insert(
            tk.END, "Launching project in Visual Studio Code...\n")
        console_text.update()

        if sys.platform == "win32":
            code_command = "code.cmd"
        else:
            code_command = "code"

        console_text.config(state="normal")

        console_text.insert(
            tk.END, "Launching project in Visual Studio Code...\n")
        console_text.update()

        console_text.config(state="disabled")

        subprocess.run([code_command, '.'], check=True)

        messagebox.showinfo(
            "Success", f"Django project '{project_name}' with app '{app_name}' created successfully!")

    except subprocess.CalledProcessError as e:
        console_text.config(state="normal")
        console_text.insert(tk.END, f"Error: {e}\n")
        console_text.config(state="disabled")
        messagebox.showerror("Error", f"An error occurred: {e}")

    except FileNotFoundError as e:
        console_text.config(state="normal")
        console_text.insert(tk.END, f"Error: {e}\n")
        console_text.config(state="disabled")
        messagebox.showerror("Error", f"An error occurred: {e}")


def create_project():
    project_name = entry_project.get()
    app_name = entry_app.get()
    create_django_project(project_name, app_name)


window = tk.Tk()
window.title("Django Project Creator")
window.geometry("500x500")
window.iconbitmap("G:\ME\Programare\Python\django_project\django.ico")
window.eval('tk::PlaceWindow . center')

label_project = tk.Label(window, text="Project Name:")
label_project.pack()
entry_project = tk.Entry(window)
entry_project.pack()

label_app = tk.Label(window, text="App Name:")
label_app.pack()
entry_app = tk.Entry(window)
entry_app.pack()

btn_create = tk.Button(window, text="Create Project", command=create_project)
btn_create.pack()

console_text = tk.Text(window, height=10, state="disabled")
console_text.pack()

window.mainloop()
