import json
import os
import matplotlib.pyplot as plt
from kivy.app import App
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from fpdf import FPDF

Window.size = (600, 600)
Window.clearcolor = get_color_from_hex("#FDF6EC")

ROLE_ROADMAPS = {
    "Data Analyst": """3-Month Roadmap:
---------------------
Month 1:
- Master advanced Excel functions and pivot tables.
- Practice writing SQL queries for data extraction and aggregation.

Month 2:
- Build interactive dashboards in Power BI.
- Complete a data cleaning project using Python (pandas).

Month 3:
- Work on a case study combining Excel, SQL, and Power BI.
- Prepare a presentation to showcase your analysis.""",

    "Data Scientist": """3-Month Roadmap:
---------------------
Month 1:
- Study supervised and unsupervised algorithms with scikit-learn.
- Review core statistics: probability, regression, distributions.

Month 2:
- Build a machine learning model using scikit-learn.
- Learn neural networks basics and experiment with simple deep learning.

Month 3:
- Complete an end-to-end data science project.
- Document your workflow and prepare to present your findings."""
}

TARGET_LEVELS = {
    "Data Analyst": {"Excel": 10, "SQL": 10, "Power BI": 10, "Python": 10},
    "Data Scientist": {"Python (Pandas/Numpy etc)": 10, "Machine Learning (Scikit-learn)": 10, "Statistics": 10, "Deep Learning": 10}
}

class SkillGapApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=15, spacing=10, **kwargs)
        self.roles_data = self.load_roles()
        self.user_inputs = {}
        self.latest_user = None
        self.build_ui()

    def load_roles(self):
        with open("roles.json", "r") as f:
            return json.load(f)

    def build_ui(self):
        self.add_widget(Label(text="SKILL GAP ANALYZER", font_size=26, bold=True,
                              size_hint_y=None, height=50, color=get_color_from_hex("#5C4033")))
        self.name_input = TextInput(hint_text="Enter your name", size_hint_y=None,
                                    height=40, background_color=get_color_from_hex("#F5E8C7"))
        self.status_input = TextInput(hint_text="Student / Working", size_hint_y=None,
                                      height=40, background_color=get_color_from_hex("#F5E8C7"))
        self.role_spinner = Spinner(text="Select Aspiring Role",
                                    values=list(self.roles_data.keys()), size_hint_y=None,
                                    height=44, background_color=get_color_from_hex("#E7A977"),
                                    color=get_color_from_hex("#FFFFFF"))
        self.role_spinner.bind(text=self.on_role_select)

        self.skills_layout = GridLayout(cols=2, spacing=10, size_hint_y=None)
        self.skills_layout.bind(minimum_height=self.skills_layout.setter('height'))
        self.scroll = ScrollView()
        self.scroll.add_widget(self.skills_layout)

        self.submit_btn = Button(text="Submit", size_hint_y=None, height=50,
                                 background_color=get_color_from_hex("#E7A977"),
                                 color=get_color_from_hex("#FFFFFF"))
        self.submit_btn.bind(on_press=self.on_submit)

        self.pdf_btn = Button(text="Download PDF", size_hint_y=None, height=50,
                               background_color=get_color_from_hex("#A8E0DF"),
                               color=get_color_from_hex("#333333"))
        self.pdf_btn.bind(on_press=self.generate_pdf)
        self.pdf_btn.disabled = True

        self.add_widget(self.name_input)
        self.add_widget(self.status_input)
        self.add_widget(self.role_spinner)
        self.add_widget(self.scroll)
        self.add_widget(self.submit_btn)
        self.add_widget(self.pdf_btn)

    def on_role_select(self, spinner, role):
        self.skills_layout.clear_widgets()
        self.user_inputs.clear()
        for skill, desc in self.roles_data[role].items():
            self.skills_layout.add_widget(
                Label(text=f"{skill}: {desc}", size_hint_y=None, height=40,
                      color=get_color_from_hex("#000000")))
            layout = BoxLayout(orientation='horizontal', spacing=5,
                                size_hint_y=None, height=40)
            inp = TextInput(text="1", input_filter='int', multiline=False,
                            size_hint=(None, 1), width=40, halign="center",
                            background_color=get_color_from_hex("#E2E8C0"))
            inc = Button(text="+", size_hint=(None, 1), width=30,
                         background_color=get_color_from_hex("#000000"),
                         color=get_color_from_hex("#FFFFFF"))
            dec = Button(text="-", size_hint=(None, 1), width=30,
                         background_color=get_color_from_hex("#000000"),
                         color=get_color_from_hex("#FFFFFF"))
            inc.bind(on_press=lambda x, i=inp: self.adjust_rating(i, 1))
            dec.bind(on_press=lambda x, i=inp: self.adjust_rating(i, -1))
            layout.add_widget(dec)
            layout.add_widget(inp)
            layout.add_widget(inc)
            self.user_inputs[skill] = inp
            self.skills_layout.add_widget(layout)

    def adjust_rating(self, widget, delta):
        try:
            val = int(widget.text)
        except ValueError:
            val = 1
        widget.text = str(max(1, min(10, val + delta)))

    def on_submit(self, instance):
        if not self.name_input.text or not self.status_input.text \
           or self.role_spinner.text == "Select Aspiring Role":
            return self.show_popup("Please complete all fields.")
        user = {"name": self.name_input.text,
                "status": self.status_input.text,
                "aspiring_role": self.role_spinner.text,
                "skills": {k: int(v.text) for k, v in self.user_inputs.items()}}
        self.save_user(user)
        self.latest_user = user
        self.create_chart(user)
        self.show_popup("Skill gap chart saved! Now download the PDF.")
        self.pdf_btn.disabled = False

    def save_user(self, user):
        path = "users.json"
        data = json.load(open(path)) if os.path.exists(path) else []
        data.append(user)
        json.dump(data, open(path, 'w'), indent=2)

    def create_chart(self, user):
        role = user["aspiring_role"]
        targets = TARGET_LEVELS.get(role, {})
        skills = list(targets)
        yours = [user["skills"].get(s, 0) for s in skills]
        goals = [targets[s] for s in skills]
        plt.figure(figsize=(8, 5))
        idx = range(len(skills))
        plt.bar([i-0.2 for i in idx], yours, width=0.4, label="You")
        plt.bar([i+0.2 for i in idx], goals, width=0.4, label="Target")
        plt.xticks(idx, skills, rotation=45, ha='right')
        plt.ylim(0, 10)
        plt.legend()
        plt.tight_layout()
        plt.savefig("skill_gap_chart.png")
        plt.close()

    def generate_pdf(self, instance):
        user = self.latest_user
        role = user["aspiring_role"]
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "SKILL GAP ROADMAP", ln=True, align="C")
        pdf.ln(8)
        pdf.set_font("Arial", "", 12)
        for label, val in [("NAME", user["name"]), ("STATUS", user["status"]),
                           ("ASPIRING ROLE", role)]:
            pdf.cell(0, 8, f"{label}: {val}", ln=True)
        pdf.ln(5)
        if os.path.exists("skill_gap_chart.png"):
            pdf.image("skill_gap_chart.png", x=10, w=180)
        pdf.ln(5)

        # Header row
        pdf.set_font("Arial", "B", 12)
        pdf.cell(40, 10, "Skill", border=1, align='C')
        pdf.cell(20, 10, "Self", border=1, align='C')
        pdf.cell(20, 10, "Target", border=1, align='C')
        pdf.cell(20, 10, "Gap", border=1, align='C')
        pdf.cell(90, 10, "Suggestion", border=1, align='C')
        pdf.ln()

        pdf.set_font("Arial", "", 12)
        for skill, rating in user["skills"].items():
            target = TARGET_LEVELS[role].get(skill, 10)
            gap = max(0, target - rating)
            suggestion = self.get_suggestion(rating)

            y_before = pdf.get_y()

            pdf.multi_cell(40, 10, skill, border=1)
            y_after = pdf.get_y()
            row_height = y_after - y_before

            pdf.set_xy(50, y_before)
            pdf.cell(20, row_height, str(rating), border=1, align='C')
            pdf.cell(20, row_height, str(target), border=1, align='C')
            pdf.cell(20, row_height, str(gap), border=1, align='C')

            x_sug = pdf.get_x()
            y_sug = pdf.get_y()
            pdf.set_xy(x_sug, y_sug)
            pdf.multi_cell(90, 10, suggestion, border=1)

            pdf.set_y(max(y_before + row_height, pdf.get_y()))

        pdf.ln(5)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Personalized 3-Month Roadmap:", ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 8, ROLE_ROADMAPS.get(role, "No roadmap available."))
        pdf.ln(10)
        pdf.set_font("Arial", "I", 10)
        pdf.cell(0, 10, "Generated by Skill Gap Analyzer v1.0", align='C')
        pdf.output("Skill_Roadmap.pdf")
        self.show_popup("PDF saved as Skill_Roadmap.pdf")

    def get_suggestion(self, rating):
        if rating <= 3:
            return "A lot of improvement is needed but nothing is impossible."
        if rating <= 7:
            return "You are almost there... Just need a little more practice."
        return "Woohoo! You're almost a legend here. Keep refining and practicing!"

    def show_popup(self, message):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text=message, halign='center', valign='middle'))
        btn = Button(text='OK', size_hint=(1, None), height=40,
                     background_color=get_color_from_hex("#E7A977"), color=get_color_from_hex("#FFFFFF"))
        layout.add_widget(btn)
        popup = Popup(title="Skill Gap Analyzer", content=layout,
                      size_hint=(None, None), size=(350, 200))
        btn.bind(on_press=popup.dismiss)
        popup.open()

class MyApp(App):
    def build(self):
        return SkillGapApp()

if __name__ == '__main__':
    MyApp().run()
