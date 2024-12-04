from shiny import App, render, ui, reactive
import pandas as pd
import matplotlib.pyplot as plt

label_to_variable = {
    "Rearrested Within 1 Year": "rearrest_within_1yr",
    "Readjudicated Within 1 Year": "readjudicated_within_1yr",
    "Placement/Incarceration within 1 Year": "incarcerated_within_1yr",
    "School Enrollment Status": "school_enrollment_status",
    "School Dropout Status": "school_dropout_status",
    "School Graduation/GED Status": "school_graduation_status",
    "Recent School Conduct": "recent_school_conduct",
    "Recent School Attendance": "recent_school_attendance",
    "Recent Academic Performance": "recent_academic_performance",
}

variable_to_label = {v: k for k, v in label_to_variable.items()}

app_ui = ui.page_fluid(
    ui.panel_title("Exploring How School Behavior is Correlated with Recidivism"),
    ui.input_select(
        id="recidivism",
        label="Choose a recidivism measure:",
        choices=list(label_to_variable.keys())[:3],
    ),
    ui.input_select(
        id="education",
        label="Choose an education measure:",
        choices=list(label_to_variable.keys())[3:],
    ),
    ui.output_plot("ts"),
)

def server(input, output, session):
    @reactive.Calc
    def df():
        return pd.read_csv('juvenile_data.csv')

    @output
    @render.plot
    def ts():
      
        data = df()

        education_var = label_to_variable[input.education()]
        recidivism_var = label_to_variable[input.recidivism()]

        counts = data.groupby([education_var, recidivism_var]).size().unstack(fill_value=0)
        proportions = counts.div(counts.sum(axis=1), axis=0)

        fig, ax = plt.subplots(figsize=(8, 6))
        proportions.plot(kind="line", ax=ax, marker="o")
        ax.set_title(f"{input.education()} by {input.recidivism()}")
        ax.set_xlabel(input.education())
        ax.set_ylabel("Proportion")
        
        if education_var in ["school_enrollment_status", "school_dropout_status", "school_graduation_status"]:
            ax.set_xticks([0, 1])
            ax.set_xticklabels(["0 - No", "1 - Yes"])

        ax.legend(title=input.recidivism())

        return fig

app = App(app_ui, server)