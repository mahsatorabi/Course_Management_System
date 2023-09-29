# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 21:43:03 2023

@author: ASUS
"""

import sys
import sqlite3
import pandas as pd 
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QDialog,
                            QLabel, QLineEdit, QVBoxLayout, QTableWidget,
                            QTableWidgetItem, QComboBox, QMessageBox, QWidget,
                            QFileDialog)
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QDesktopServices, QIcon, QCursor
from PyQt5.QtCore import QUrl


class PasswordDialog(QDialog):
    def __init__(self, correct_password):
        super().__init__()
        self.setStyleSheet("background-color: lightgray; color: black; font-size: 16px; font-family: B Titr;")
        self.setWindowTitle("رمز عبور")
        self.setGeometry(0, 0, 300, 150)  # Set an initial size; it will be centered later.
        # Set the application window icon
        app_icon = QIcon("image/icon.png")
        self.setWindowIcon(app_icon)
        self.correct_password = correct_password
        
        layout = QVBoxLayout()
        label = QLabel("رمز عبور خود را وارد کنید:")
        self.password_edit = QLineEdit()
        self.password_edit.setStyleSheet("background-color: lightblue; color: black; font-size: 16px;")
        self.password_edit.setEchoMode(QLineEdit.Password)  # Display asterisks for input
        submit_button = QPushButton("تایید")
        submit_button.clicked.connect(self.check_password)
        self.apply_button_style(submit_button)
        
        layout.addWidget(label)
        layout.addWidget(self.password_edit)
        layout.addWidget(submit_button)
        self.setLayout(layout)
        
        # Center the dialog on the screen
        self.center_on_screen()

    def center_on_screen(self):
        # Calculate the center position of the screen
        screen_geometry = QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

    def check_password(self):
        entered_password = self.password_edit.text()
        if entered_password == self.correct_password:
            self.accept()  # Password is correct, close the dialog with a success code
        else:
            self.password_edit.clear()
            self.password_edit.setPlaceholderText("رمز عبور اشتباه است. دوباره تلاش کنید.")

    def apply_button_style(self, button):
        button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                font-size: 16px;
                border: 2px solid black;
                border-radius: 5px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: black;
                color: white;
                cursor: pointer;
            }
        """)


class AddCourseDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("افزودن یا ویرایش دروس")
        self.setGeometry(300, 200, 400, 300)

        self.edit_mode = False  # Flag to indicate if the dialog is in edit mode
        
        # Set the application window icon
        app_icon = QIcon("image/icon.png")  # Replace with the path to your icon file
        self.setWindowIcon(app_icon)
        
        self.init_ui()

    def init_ui(self):
        
        self.setStyleSheet("background-color: lightgray; color: black; font-size: 12px; font-family: B Titr")
        
        layout = QVBoxLayout()
    
        label = QLabel("Enter course details here:")
        label.setStyleSheet("font-size: 20px;")
        layout.addWidget(label)

        
        layout = QVBoxLayout()

        #label = QLabel("")
        #layout.addWidget(label)

        self.grade_combo = QComboBox(self)
        self.grade_combo.addItems(["کارشناسی", "کارشناسی ارشد", "دکتری تخصصی"])
        self.grade_combo.setStyleSheet("background-color: lightblue; color: black; font-size: 16px;")
        self.major_edit = QLineEdit(self)
        self.major_edit.setStyleSheet("background-color: lightblue; color: black; font-size: 16px;")
        layout.addWidget(QLabel("رشته:"))
        layout.addWidget(self.major_edit)
        self.term_edit = QLineEdit(self)
        self.term_edit.setStyleSheet("background-color: lightblue; color: black; font-size: 16px;")
        self.course_id_edit = QLineEdit(self)
        self.course_id_edit.setStyleSheet("background-color: lightblue; color: black; font-size: 16px;")
        self.course_name_edit = QLineEdit(self)
        self.course_name_edit.setStyleSheet("background-color: lightblue; color: black; font-size: 16px;")
        self.professor_edit = QLineEdit(self)
        self.professor_edit.setStyleSheet("background-color: lightblue; color: black; font-size: 16px;")
        self.units_edit = QLineEdit(self)
        self.units_edit.setStyleSheet("background-color: lightblue; color: black; font-size: 16px;")
        self.unit_type_combo = QComboBox(self)        
        self.unit_type_combo.addItems(["نظری", "عملی", "نظری و عملی"])
        self.unit_type_combo.setStyleSheet("background-color: lightblue; color: black; font-size: 16px;")
        self.course_type_combo = QComboBox(self)
        self.course_type_combo.addItems(["پایه", "تخصصی اجباری",
                                         "تخصصی اختیاری"])
        self.course_type_combo.setStyleSheet("background-color: lightblue; color: black; font-size: 16px;")
        self.prerequisite_edit = QLineEdit(self)
        self.prerequisite_edit.setStyleSheet("background-color: lightblue; color: black; font-size: 16px;")

        layout.addWidget(QLabel("مقطع:"))
        layout.addWidget(self.grade_combo)
        layout.addWidget(QLabel("ترم:"))
        layout.addWidget(self.term_edit)
        layout.addWidget(QLabel("کد درس:"))
        layout.addWidget(self.course_id_edit)
        layout.addWidget(QLabel("نام درس:"))
        layout.addWidget(self.course_name_edit)
        layout.addWidget(QLabel("نام استاد:"))
        layout.addWidget(self.professor_edit)
        layout.addWidget(QLabel("تعداد واحد:"))
        layout.addWidget(self.units_edit)
        layout.addWidget(QLabel("نوع واحد"))
        layout.addWidget(self.unit_type_combo)
        layout.addWidget(QLabel("نوع درس:"))
        layout.addWidget(self.course_type_combo)
        layout.addWidget(QLabel("پیشنیاز:"))
        layout.addWidget(self.prerequisite_edit)
        
        self.course_id_to_fetch_edit = QLineEdit(self)
        layout.addWidget(QLabel("کد درس جهت ویرایش:"))
        layout.addWidget(self.course_id_to_fetch_edit)
        self.course_id_to_fetch_edit.setStyleSheet("background-color: lightpink; color: black; font-size: 16px;")

        fetch_button = QPushButton("بازیابی درس")
        fetch_button.clicked.connect(self.fetch_course)
        layout.addWidget(fetch_button)
        self.apply_button_style(fetch_button)  # Apply custom style
        
        delete_button = QPushButton("حذف درس")
        delete_button.clicked.connect(self.delete_course)
        layout.addWidget(delete_button)
        self.apply_button_style(delete_button)  # Apply custom style
        
        save_button = QPushButton("ذخیره")
        save_button.clicked.connect(self.save_course)
        layout.addWidget(save_button)
        self.apply_button_style(save_button)  # Apply custom style

        self.course_id_edit.textChanged.connect(self.update_fetch_course_id)

        self.setLayout(layout)
        
    def clear_input_fields(self):
        self.grade_combo.setCurrentIndex(0)
        self.term_edit.clear()
        self.course_id_edit.clear()
        self.course_name_edit.clear()
        self.professor_edit.clear()
        self.units_edit.clear()
        self.unit_type_combo.setCurrentIndex(0)
        self.course_type_combo.setCurrentIndex(0)
        self.prerequisite_edit.clear()
        self.major_edit.clear()

    def apply_button_style(self, button):
        button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                font-size: 16px;
                border: 2px solid black;
                border-radius: 5px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: black;
                color: white;
                cursor: pointer;
            }
        """)

    @pyqtSlot(str)
    def update_fetch_course_id(self, course_id):
        self.course_id_to_fetch_edit.setText(course_id)

    def fetch_course(self):
        # Fetch data from the database based on course ID
        course_id_to_fetch = self.course_id_to_fetch_edit.text()
    
        if not course_id_to_fetch:
            self.show_error_dialog("لطفا کد درس را جهت بازیابی وارد کنید.")
            return
    
        conn = sqlite3.connect("courses.db")
        cursor = conn.cursor()
    
        # Execute a SQL query to fetch course data by course ID
        cursor.execute("SELECT * FROM courses WHERE course_id = ?", (course_id_to_fetch,))
        course_data = cursor.fetchone()
    
        conn.close()
    
        if course_data:
            # Populate input fields with fetched course data
            self.term_edit.setText(course_data[0])
            self.course_id_edit.setText(course_data[1])
            self.course_name_edit.setText(course_data[2])
            self.professor_edit.setText(course_data[3])
            self.units_edit.setText(course_data[4])
            self.unit_type_combo.setCurrentText(course_data[5])
            self.course_type_combo.setCurrentText(course_data[6])
            self.prerequisite_edit.setText(course_data[7])
            self.grade_combo.setCurrentText(course_data[8])
            self.major_edit.setText(course_data[9])
        else:
            # Course not found
            self.show_error_dialog("این درس یافت نشد.")


            
    def delete_course(self):
        # Fetch data from the database based on course ID to fetch
        course_id_to_fetch = self.course_id_to_fetch_edit.text()
    
        if not course_id_to_fetch:
            self.show_error_dialog("لطفا کد درس را جهت حذف آن وارد کنید.")
            return
    
        conn = sqlite3.connect("courses.db")
        cursor = conn.cursor()
    
        # Execute a SQL query to fetch course data by course ID
        cursor.execute("SELECT * FROM courses WHERE course_id = ?", (course_id_to_fetch,))
        course_data = cursor.fetchone()
    
        conn.close()
    
        if not course_data:
            self.show_error_dialog("این درس یافت نشد.")
            return
    
        conn = sqlite3.connect("courses.db")
        cursor = conn.cursor()
    
        # Execute a SQL query to delete course data by course ID
        cursor.execute("DELETE FROM courses WHERE course_id = ?", (course_id_to_fetch,))
        conn.commit()
    
        conn.close()
        self.clear_input_fields()  # Clear input fields after deletion
        self.show_deleted_dialog()
    
    
    def show_deleted_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("حذف درس")
    
        layout = QVBoxLayout()
        label = QLabel("درس با موفقیت حذف شد.")
        ok_button = QPushButton("باشه")
        ok_button.clicked.connect(dialog.accept)
        self.apply_button_style(ok_button)
    
        layout.addWidget(label)
        layout.addWidget(ok_button)
    
        dialog.setLayout(layout)
        dialog.exec_()

    def save_course(self):
        # Get data from input fields
        grade = self.grade_combo.currentText()
        term = self.term_edit.text()
        course_id = self.course_id_edit.text()
        course_name = self.course_name_edit.text()
        professor = self.professor_edit.text()
        units = self.units_edit.text()
        unit_type = self.unit_type_combo.currentText()
        course_type = self.course_type_combo.currentText()
        prerequisite = self.prerequisite_edit.text()
        major = self.major_edit.text()
    
        # Check if any field is empty
        if not (grade and term and course_id and course_name and professor and
                units and unit_type and course_type and prerequisite and major):
            self.show_error_dialog("تمام فیلدها باید پر شود.")
            return
    
        conn = sqlite3.connect("courses.db")
        cursor = conn.cursor()
    
        # Create the 'courses' table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS courses
                          (term TEXT, course_id TEXT, course_name TEXT, professor TEXT,
                          units TEXT, unit_type TEXT, course_type TEXT, prerequisite TEXT, grade TEXT, major TEXT)''')
    
        # Check if the course with the given course_id already exists in the database
        cursor.execute("SELECT * FROM courses WHERE course_id = ?", (course_id,))
        existing_course = cursor.fetchone()
    
        try:
            if existing_course:
                # Update existing course data
                cursor.execute('''UPDATE courses SET term=?, course_name=?, professor=?, units=?, 
                                unit_type=?, course_type=?, prerequisite=?, grade=?, major=?
                                WHERE course_id=?''',
                               (term, course_name, professor, units, unit_type, course_type, prerequisite, grade, major, course_id))
            else:
                # Insert new course data
                cursor.execute('''INSERT INTO courses VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                               (term, course_id, course_name, professor, units, unit_type, course_type, prerequisite, grade, major))
    
            conn.commit()
            conn.close()
    
            self.show_saved_dialog(True)
            self.clear_input_fields()  # Clear input fields after saving
        except sqlite3.Error as e:
            print("خطا: ", e)
            conn.rollback()
            conn.close()
            self.show_saved_dialog(False)

    def show_error_dialog(self, message):
        error_dialog = QDialog(self)
        error_dialog.setWindowTitle("خطا")
        layout = QVBoxLayout()
        error_label = QLabel(message)
        layout.addWidget(error_label)
        ok_button = QPushButton("باشه")
        self.apply_button_style(ok_button)
        ok_button.clicked.connect(error_dialog.accept)
        layout.addWidget(ok_button)
        error_dialog.setLayout(layout)
        error_dialog.exec_()

    def show_saved_dialog(self, saved):
        dialog = QDialog(self)
        dialog.setWindowTitle("ذخیره")

        layout = QVBoxLayout()

        if saved:
            label = QLabel("اطلاعات با موفقیت ذخیره شد.")
        else:
            label = QLabel("خطایی رخ داد، اطلاعات ذخیره نشد.")

        ok_button = QPushButton("باشه")
        ok_button.clicked.connect(dialog.accept)
        self.apply_button_style(ok_button)
        layout.addWidget(label)
        layout.addWidget(ok_button)

        dialog.setLayout(layout)
        dialog.exec_()


class SearchCourseDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("جستجوی دروس")
        self.setGeometry(500, 400, 1500, 900)
        
        
        self.edit_mode = False  # Flag to indicate if the dialog is in edit mode

        # Set the application window icon
        app_icon = QIcon("image/icon.png")  # Replace with the path to your icon file
        self.setWindowIcon(app_icon)

        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: lightgray; color: black; font-size: 16px; font-family: B Titr;")
        layout = QVBoxLayout()

        label = QLabel("جستجوی درس:")
        layout.addWidget(label)

        self.search_edit = QLineEdit(self)
        layout.addWidget(self.search_edit)
        self.search_edit.setStyleSheet("background-color: lightblue; color: black; font-size: 16px;")

        self.search_by_combo = QComboBox(self)
        search_options = ["کد درس", "ترم", "نام درس", "نام استاد", 
                          "تعداد واحد", "نوع واحد", "نوع درس", "مقطع", "رشته"]
        self.search_by_combo.addItems(search_options)
        self.search_by_combo.setStyleSheet("background-color: lightpink; color: black; font-size: 16px;")
        layout.addWidget(self.search_by_combo)

        # Add a QComboBox for selecting grades
        self.grade_filter_combo = QComboBox(self)
        grade_options = ["همه مقاطع", "کارشناسی", "کارشناسی ارشد", "دکتری تخصصی"]
        self.grade_filter_combo.addItems(grade_options)
        self.grade_filter_combo.setStyleSheet("background-color: lightyellow; color: black; font-size: 16px;")
        layout.addWidget(QLabel("مقطع:"))
        layout.addWidget(self.grade_filter_combo)

        # Add a QComboBox for selecting majors
        self.major_filter_combo = QComboBox(self)
        major_options = ["علم اطلاعات", "مدیریت اطلاعات", "علم سنجی", "بازیابی اطلاعات"]
        self.major_filter_combo.addItems(major_options)
        self.major_filter_combo.setStyleSheet("background-color: lightyellow; color: black; font-size: 16px;")
        layout.addWidget(QLabel("رشته:"))
        layout.addWidget(self.major_filter_combo)

        search_button = QPushButton("جستجو")
        search_button.clicked.connect(self.search_courses)
        layout.addWidget(search_button)
        self.apply_button_style(search_button)
        
        export_button = QPushButton("خروجی اکسل", self)
        export_button.clicked.connect(self.export_to_excel)
        layout.addWidget(export_button)
        self.apply_button_style(export_button)

        self.table = QTableWidget(self)
        self.table.setColumnCount(10)  # Updated for the "Grade" column
        self.table.setHorizontalHeaderLabels(["ترم", "کد درس", "نام درس", "نام استاد", "تعداد واحد", "نوع واحد", "نوع درس", "پیشنیاز", "مقطع", "رشته"])
        self.table.setStyleSheet("background-color: lightgreen; color: black; font-size: 16px;")
        layout.addWidget(self.table)

        self.setLayout(layout)
        
    def export_to_excel(self):
        # Get the table data
        table_data = []
        for row in range(self.table.rowCount()):
            row_data = []
            for column in range(self.table.columnCount()):
                item = self.table.item(row, column)
                row_data.append(item.text() if item else "")
            table_data.append(row_data)

        if not table_data:
            self.show_error_dialog("اطلاعاتی جهت گرفتن خروجی نیست.")
            return

        # Create a Pandas DataFrame from the table data
        df = pd.DataFrame(table_data, columns=["ترم", "کد درس", "نام درس", "نام استاد", "تعداد واحد", "نوع واحد", "نوع درس", "پیشنیاز", "مقطع", "رشته"])

        # Open a file dialog to choose where to save the Excel file
        file_dialog = QFileDialog(self)
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setNameFilter("Excel Files (*.xlsx)")
        file_dialog.setDefaultSuffix("xlsx")
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            try:
                df.to_excel(file_path, index=False, engine='openpyxl')
                self.show_error_dialog("خروجی اکسل با موفقیت ذخیره شد.")
            except Exception as e:
                self.show_error_dialog(f"خطایی در هنگام گرفتن خروجی رخ داد:  {str(e)}")

        
        
    def apply_button_style(self, button):
        button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                font-size: 16px;
                border: 2px solid black;
                border-radius: 5px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: black;
                color: white;
                cursor: pointer;
            }
        """)


    def search_courses(self):
        # Fetch data from the database and populate the table
        search_query = self.search_edit.text()
        search_by = self.search_by_combo.currentText()
        grade_filter = self.grade_filter_combo.currentText()  # Get the selected grade filter
        major_filter = self.major_filter_combo.currentText()  # Get the selected major filter

        conn = sqlite3.connect("courses.db")
        cursor = conn.cursor()

        if not search_query:
            self.show_error_dialog("لطفاً فیلد جستجو را پر کنید.")
            return

        # Build the SQL query based on the selected search option and grade filter
        if grade_filter == "همه مقاطع" and major_filter == "علم اطلاعات":
            if search_by == "کد درس":
                cursor.execute("SELECT * FROM courses WHERE course_id LIKE ?", ('%' + search_query + '%',))
            elif search_by == "ترم":
                cursor.execute("SELECT * FROM courses WHERE term LIKE ?", ('%' + search_query + '%',))
            elif search_by == "نام درس":
                cursor.execute("SELECT * FROM courses WHERE course_name LIKE ?", ('%' + search_query + '%',))
            elif search_by == "نام استاد":
                cursor.execute("SELECT * FROM courses WHERE professor LIKE ?", ('%' + search_query + '%',))
            elif search_by == "تعداد واحد":
                cursor.execute("SELECT * FROM courses WHERE units LIKE ?", ('%' + search_query + '%',))
            elif search_by == "نوع واحد":
                cursor.execute("SELECT * FROM courses WHERE unit_type LIKE ?", ('%' + search_query + '%',))
            elif search_by == "نوع درس":
                cursor.execute("SELECT * FROM courses WHERE course_type LIKE ?", ('%' + search_query + '%',))
            elif search_by == "مقطع":
                cursor.execute("SELECT * FROM courses WHERE grade LIKE ?", ('%' + search_query + '%',))
            elif search_by == "رشته":
                cursor.execute("SELECT * FROM courses WHERE major LIKE ?", ('%' + search_query + '%',))
        
        else:
            if search_by == "کد درس":
                cursor.execute("SELECT * FROM courses WHERE course_id LIKE ? AND grade LIKE ? ََََََََِِِAnd major LIKE ?", ('%' + search_query + '%', '%' + grade_filter + '%', '%' + major_filter + '%'))
            elif search_by == "ترم":
                cursor.execute("SELECT * FROM courses WHERE term LIKE ? AND grade LIKE ? And major LIKE ?", ('%' + search_query + '%', '%' + grade_filter + '%', '%' + major_filter + '%'))
            elif search_by == "نام درس":
                cursor.execute("SELECT * FROM courses WHERE course_name LIKE ? AND grade LIKE ? And major LIKE ?", ('%' + search_query + '%', '%' + grade_filter + '%', '%' + major_filter + '%'))
            elif search_by == "نام استاد":
                cursor.execute("SELECT * FROM courses WHERE professor LIKE ? AND grade LIKE ? And major LIKE ?", ('%' + search_query + '%', '%' + grade_filter + '%', '%' + major_filter + '%'))
            elif search_by == "تعداد واحد":
                cursor.execute("SELECT * FROM courses WHERE units LIKE ? AND grade LIKE ? And major LIKE ?", ('%' + search_query + '%', '%' + grade_filter + '%', '%' + major_filter + '%'))
            elif search_by == "نوع واحد":
                cursor.execute("SELECT * FROM courses WHERE unit_type LIKE ? AND grade LIKE ? And major LIKE ?", ('%' + search_query + '%', '%' + grade_filter + '%', '%' + major_filter + '%'))
            elif search_by == "نوع درس":
                cursor.execute("SELECT * FROM courses WHERE course_type LIKE ? AND grade LIKE ? And major LIKE ?", ('%' + search_query + '%', '%' + grade_filter + '%', '%' + major_filter + '%'))
            elif search_by == "مقطع":
                cursor.execute("SELECT * FROM courses WHERE grade LIKE ? AND grade LIKE ? And major LIKE ?", ('%' + search_query + '%', '%' + grade_filter + '%', '%' + major_filter + '%'))
            elif search_by == "رشته":
                cursor.execute("SELECT * FROM courses WHERE major LIKE ? AND grade LIKE ? And major LIKE ?", ('%' + search_query + '%', '%' + grade_filter + '%', '%' + major_filter + '%'))
        search_results = cursor.fetchall()
        conn.close()

        if not search_results:
            self.show_not_found_dialog()  # Show the dialog if no results are found
            self.table.setRowCount(0)  # Clear the table
            return

        # Populate the table with search results
        self.table.setRowCount(len(search_results))
        for row_idx, row_data in enumerate(search_results):
            for col_idx, cell_data in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(cell_data)))

        self.table.resizeColumnsToContents()

    def show_not_found_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("درس یافت نشد")

        layout = QVBoxLayout()
        label = QLabel("اطلاعات درسی که دنبال آن هستید یافت نشد.")
        ok_button = QPushButton("باشه")
        ok_button.clicked.connect(dialog.accept)
        self.apply_button_style(ok_button)
        layout.addWidget(label)
        layout.addWidget(ok_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def show_error_dialog(self, message):
        error_dialog = QDialog(self)
        error_dialog.setWindowTitle("پیام")
        layout = QVBoxLayout()
        error_label = QLabel(message)
        layout.addWidget(error_label)
        ok_button = QPushButton("باشه")
        self.apply_button_style(ok_button)
        ok_button.clicked.connect(error_dialog.accept)
        layout.addWidget(ok_button)
        error_dialog.setLayout(layout)
        error_dialog.exec_()
        
class CourseManagementApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("سامانه مدیریت دروس")
        #window_width = 800
        #window_height = 600
        #self.setGeometry(100, 100, window_width, window_height)
        self.setFixedSize(800, 600)  # Set a fixed window size

        # Set the application window icon
        app_icon = QIcon("image/icon.png")  # Replace with the path to your icon file
        self.setWindowIcon(app_icon)
        # Define the correct password to access the "Add Course" page
        self.correct_password = "is2023"  # Replace with your desired password
        self.init_ui()

    def init_ui(self):
        button_width = 200
        button_height = 80
        
        # Set the cursor to a blue arrow (pointer)
        #self.setCursor(QCursor(Qt.ArrowCursor))

        self.setStyleSheet("font-size: 17px; font-family: B Titr;")

        central_widget = QWidget(self)  # Create a central widget
        self.setCentralWidget(central_widget)  # Set it as the central widget

        # Set the background image for the central widget
        central_widget.setStyleSheet("QWidget { background-image: url(image/background.jpg); background-repeat: no-repeat; background-position: center; }")

        # Create a layout for the central widget
        central_layout = QVBoxLayout(central_widget)

        add_button = QPushButton("افزودن یا ویرایش دروس", self)
        add_button.setGeometry((self.width() - button_width) // 2, 200, button_width,
                               button_height)
        add_button.clicked.connect(self.open_add_course_dialog)
        self.apply_button_style(add_button)  # Apply custom style


        search_button = QPushButton("جستجوی دروس", self)
        search_button.setGeometry((self.width() - button_width) // 2, 350,
                                  button_width, button_height)
        search_button.clicked.connect(self.open_search_course_dialog)
        self.apply_button_style(search_button)  # Apply custom style


        # Create a toolbar
        toolbar = self.addToolBar("نوار ابزار")

        # Add "Contact Us" action to the toolbar
        contact_us_action = toolbar.addAction("ارتباط با ما")
        contact_us_action.triggered.connect(self.show_contact_us)

        # Add a separator
        toolbar.addSeparator()

        # Add "About Us" action to the toolbar
        about_us_action = toolbar.addAction("درباره ما")
        about_us_action.triggered.connect(self.show_about_us)

        # Add the email label at the bottom
        email_label = QLabel("<a href='mailto:your_email@example.com'>Developed by Mahsa Torabi</a>")
        email_label.setOpenExternalLinks(True)
        email_label.setAlignment(Qt.AlignCenter)
        self.statusBar().addWidget(email_label)


    def show_contact_us(self):
        error_dialog = QDialog(self)
        error_dialog.setWindowTitle("ارتباط با ما")
        layout = QVBoxLayout()
        error_label = QLabel("شما می توانید از روش های زیر جهت برقراری ارتباط با ما استفاده کنید:\nmahsatorabi515@gmail.com\nیا\n09908086501")
        layout.addWidget(error_label)
        ok_button = QPushButton("باشه")
        self.apply_button_style(ok_button)
        ok_button.clicked.connect(error_dialog.accept)
        layout.addWidget(ok_button)
        error_dialog.setLayout(layout)
        error_dialog.exec_()

    def show_about_us(self):
        about_us_text = "سامانه مدیریت دروس\nورژن 1.0\n\nطراحی شده توسط: مهسا ترابی"
        error_dialog = QDialog(self)
        error_dialog.setWindowTitle("درباره ما")
        layout = QVBoxLayout()
        error_label = QLabel(about_us_text)
        layout.addWidget(error_label)
        ok_button = QPushButton("باشه")
        ok_button.clicked.connect(error_dialog.accept)
        self.apply_button_style(ok_button)
        layout.addWidget(ok_button)
        error_dialog.setLayout(layout)
        error_dialog.exec_()

    def open_add_course_dialog(self):
        # Create an instance of the PasswordDialog
        password_dialog = PasswordDialog(self.correct_password)
        result = password_dialog.exec_()
        
        if result == QDialog.Accepted:
            # User entered the correct password, allow access to "Add Course" page
            dialog = AddCourseDialog()
            # Calculate the position to center the dialog on the screen
            screen_geometry = QApplication.desktop().screenGeometry()
            x = (screen_geometry.width() - dialog.width()) // 2
            y = (screen_geometry.height() - dialog.height()) // 70  # Adjust as needed
            dialog.move(x, y)
            result = dialog.exec_()
        else:
            # User entered an incorrect password or canceled, show an error message
            self.show_error_dialog("دسترسی مقدور نیست، رمز اشتباه است.")

    def open_search_course_dialog(self):
        dialog = SearchCourseDialog()
        
        # Calculate the position to center the dialog on the screen
        screen_geometry = QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - dialog.width()) // 2
        y = (screen_geometry.height() - dialog.height()) // 4  # Adjust as needed
        dialog.move(x, y)
        
        result = dialog.exec_()
        
    def show_error_dialog(self, message):
        error_dialog = QDialog(self)
        error_dialog.setWindowTitle("خطا")
        layout = QVBoxLayout()
        error_label = QLabel(message)
        layout.addWidget(error_label)
        ok_button = QPushButton("باشه")
        self.apply_button_style(ok_button)
        ok_button.clicked.connect(error_dialog.accept)
        layout.addWidget(ok_button)
        error_dialog.setLayout(layout)
        error_dialog.exec_()
        
    def apply_button_style(self, button):
        button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                font-size: 16px;
                border: 2px solid black;
                border-radius: 5px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: black;
                color: white;
                cursor: pointer;
            }
        """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = CourseManagementApp()
    main_window.show()
    sys.exit(app.exec_())
