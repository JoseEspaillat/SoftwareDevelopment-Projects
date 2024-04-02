import flet as ft
 
def main(page: ft.Page):
    page.title = "AGS (Advanced Grading System)"
    page.vertical_alignment = "start"
 
    students_data = {
        "Section A": {},
        "Section B": {}
    }
 
    page.padding = 20
    page.spacing = 10
 
    error_text = ft.Text(value="", color=ft.colors.RED_700)
 
    def show_error(message):
        error_text.value = message
        page.update()
 
    def update_section_dropdown():
        section_dropdown.options = [ft.dropdown.Option(text=section) for section in students_data.keys()]
        page.update()
 
    def update_students_list():
        students_list_container.controls.clear() #evita que se dupliquen
        selected_section = section_dropdown.value
        if selected_section in students_data:
            for student_name, points in students_data[selected_section].items():
                student_row = create_student_row(student_name, points, selected_section)
                students_list_container.controls.append(student_row)
        page.update()
 
    def create_student_row(student_name, points, section):
        points_label = ft.Text(value=f"Points: {points}", width=100)
 
        def modify_points(e, delta):# representa la cantidad de cambio que quieres aplicar a los puntos de un estudiante.
            #Es un valor que puede ser positivo (para aumentar los puntos) o negativo (para disminuir los puntos).
            nonlocal points  # Uso de nonlocal para modificar la variable points definida en el alcance superior
            points += delta  # Modificación de los puntos
            students_data[section][student_name] = points  # Actualización de los datos
            points_label.value = f"Points: {points}"  # Actualización del texto de los puntos en la interfaz de usuario
            page.update()  # Actualización de la página
 
        add_points = ft.IconButton(icon=ft.icons.ADD, on_click=lambda e: modify_points(e, 1), tooltip="Add Point")
        subtract_points = ft.IconButton(icon=ft.icons.REMOVE, on_click=lambda e: modify_points(e, -1), tooltip="Remove Point")
        #TOOLTIP es lo que hace que cuando tu ponga el mouse arriba de los botoncitos de suma o resta se vea como un mensajito de que es lo que hace el boton.
 
        # Retorno de una fila con el nombre del estudiante, puntos y botones para modificar los puntos
        return ft.Row([
            ft.Text(value=student_name, width=200),
            points_label,
            add_points,
            subtract_points
        ], alignment="spaceBetween")
 
    def add_student(e):
        student_name = add_student_name_input.value.strip()
        if not student_name:
            show_error("Student name cannot be empty.")
            return
        try:
            initial_points = int(add_student_points_input.value)
        except ValueError:
            show_error("Initial points must be a number.")
            return
        if student_name in students_data.get(section_dropdown.value, {}):
            show_error(f"{student_name} is already in the section.")
            return
        students_data[section_dropdown.value][student_name] = initial_points
        update_students_list()
        add_student_name_input.value = ""
        add_student_points_input.value = "0"
        show_error("")
 
 
        #ERROR HANDLING:
    def remove_student(e):
        student_name = remove_student_name_input.value.strip( )#.strimp elimina espacion inecesarios
        if student_name not in students_data.get(section_dropdown.value, {}):
            show_error(f"{student_name} is not in the section.")
            return
        del students_data[section_dropdown.value][student_name]# Elimina el registro del estudiante seleccionado de los datos almacenados
        update_students_list() # Actualiza la lista de estudiantes en la UI para reflejar la eliminación
        remove_student_name_input.value = ""# Limpia el campo de entrada de nombre del estudiante a eliminar
        show_error("") # Limpia cualquier mensaje de error que se esté mostrando
 
 
    def add_section(e):
        new_section = add_section_input.value.strip()
        if not new_section:
            show_error("Section name cannot be empty.")
            return
        if new_section in students_data:
            show_error(f"Section {new_section} already exists.")
            return
        students_data[new_section] = {}
        update_section_dropdown()
        add_section_input.value = "" # Limpia el campo de texto donde el usuario introduce el nombre de la nueva sección
        show_error("")
 
 
    def remove_section(e):
        section_to_remove = remove_section_input.value.strip()
        if section_to_remove not in students_data:
            show_error(f"Section {section_to_remove} does not exist.")
            return
        del students_data[section_to_remove]
        update_section_dropdown()
        remove_section_input.value = ""
        update_students_list()
        show_error("")
 
    section_dropdown = ft.Dropdown(label="Select Section", width=300, on_change=update_students_list)
    update_section_dropdown()
 
    students_list_container = ft.ListView(expand=True)
 
    add_student_name_input = ft.TextField(label="Student Name", width=300)
    add_student_points_input = ft.TextField(label="Initial Points", value="0", width=100)
    add_student = ft.ElevatedButton(text="Add Student", on_click=add_student)
 
    remove_student_name_input = ft.TextField(label="Student Name to Remove", width=300)
    remove_student = ft.ElevatedButton(text="Remove Student", on_click=remove_student)
 
    add_section_input = ft.TextField(label="New Section Name", width=300)
    add_section = ft.ElevatedButton(text="Add Section", on_click=add_section)
 
    remove_section_input = ft.TextField(label="Section Name to Remove", width=300)
    remove_section = ft.ElevatedButton(text="Remove Section", on_click=remove_section)
 
    # Adding the error text to the page, which will display messages as needed
    page.add(error_text)
 
    # Adding components to the page
    page.add(
        section_dropdown,
        students_list_container,
        ft.Row([add_student_name_input, add_student_points_input, add_student], alignment="spaceBetween"),
        ft.Row([remove_student_name_input, remove_student], alignment="spaceBetween"),
        ft.Row([add_section_input, add_section], alignment="spaceBetween"),
        ft.Row([remove_section_input, remove_section], alignment="spaceBetween"),
    )
 
ft.app(target=main)