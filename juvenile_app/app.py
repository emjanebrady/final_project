from shiny import App, render, ui, reactive
import pandas as pd
import matplotlib.pyplot as plt

# Define the mapping between UI labels and dataframe variables
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

# Reverse mapping for legends
variable_to_label = {v: k for k, v in label_to_variable.items()}

# Define the Shiny app UI
app_ui = ui.page_fluid(
    ui.panel_title("Exploring How School Behavior is Correlated with Recidivism"),
    ui.input_select(
        id="recidivism",
        label="Choose a recidivism measure:",
        choices=list(label_to_variable.keys())[:3],  # First three options for recidivism
    ),
    ui.input_select(
        id="education",
        label="Choose an education measure:",
        choices=list(label_to_variable.keys())[3:],  # Remaining options for education
    ),
    ui.output_plot("ts"),
)

# Define the server logic
def server(input, output, session):
    @reactive.Calc
    def df():
        return pd.read_csv('juvenile_data.csv')

    @output
    @render.plot
    def ts():
        # Load the data
        data = df()

        # Map selected UI labels to dataframe variables
        education_var = label_to_variable[input.education()]
        recidivism_var = label_to_variable[input.recidivism()]

        # Aggregate data for plotting
        counts = data.groupby([education_var, recidivism_var]).size().unstack(fill_value=0)
        proportions = counts.div(counts.sum(axis=1), axis=0)

        # Create the plot
        fig, ax = plt.subplots(figsize=(8, 6))
        proportions.plot(kind="line", ax=ax, marker="o")
        ax.set_title(f"{input.education()} by {input.recidivism()}")
        ax.set_xlabel(input.education())
        ax.set_ylabel("Proportion")
        # Ensure all x-axis labels are shown
        if education_var in ["school_enrollment_status", "school_dropout_status", "school_graduation_status"]:
            ax.set_xticks([0, 1])  # Set positions for the ticks
            ax.set_xticklabels(["0 - No", "1 - Yes"])  # Explicitly set the labels


        ax.legend(title=input.recidivism())

        return fig
# Create the Shiny app
app = App(app_ui, server)