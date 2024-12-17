import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to create the radar chart


def create_radar_chart(data_1, data_2, labels):
    # Number of variables (angles)
    num_vars = len(labels)

    # Compute angle for each axis
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    # Repeat the first value to close the radar chart
    data_1 += data_1[:1]
    data_2 += data_2[:1]
    angles += angles[:1]

    # Create the radar chart
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    # Plot data
    ax.plot(angles, data_1, linewidth=2, linestyle='solid',
            label='Front /90 deg (5V)', color='blue')
    ax.plot(angles, data_2, linewidth=2, linestyle='solid',
            label='Front /0 deg (5V)', color='red')

    # Fill the area
    ax.fill(angles, data_1, alpha=0.25, color='blue')
    ax.fill(angles, data_2, alpha=0.25, color='red')

    # Set the labels and title
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])  # Remove last tick
    ax.set_xticklabels(labels)
    ax.set_title("Radar Chart of RF Data", size=16)

    # Add a legend
    ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))

    # Return the figure object to embed in Tkinter window
    return fig



def on_generate_click():
    
    data = text_area.get("1.0", "end-1c").strip()

    if not data:
        messagebox.showerror(
            "Error", "Please paste the data into the text area.")
        return

    try:
       
        rows = data.split('\n')

        data_1 = []
        data_2 = []
        labels = []

        for row in rows:
           
            cols = [col.strip() for col in row.split('\t')]

            if len(cols) == 2:
                try:
                    # Try to convert to float and print for debugging
                    data_1_value = float(cols[0])
                    data_2_value = float(cols[1])
                    data_1.append(data_1_value)
                    data_2.append(data_2_value)
                except ValueError as e:
                    print(f"Error converting row: {row} -> {e}")
                    messagebox.showerror(
                        "Error", f"Invalid number format in row: {row}")
                    return
            elif len(cols) == 1:  
                try:
                    data_1_value = float(cols[0])
                   
                    data_2.append(0.0)
                    data_1.append(data_1_value)
                except ValueError as e:
                    print(f"Error converting row: {row} -> {e}")
                    messagebox.showerror(
                        "Error", f"Invalid number format in row: {row}")
                    return
            else:
                
                messagebox.showerror(
                    "Error", f"Invalid data format in row: {row}")
                return

        # Create labels for the angles
        labels = [f'{i*360/len(data_1):.1f}°' for i in range(len(data_1))]

        # Create radar chart using Matplotlib
        fig = create_radar_chart(data_1, data_2, labels)

        # Embed the chart in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().grid(row=3, column=0, columnspan=2)

    except Exception as e:
        messagebox.showerror("Error", f"Error processing data: {str(e)}")


# Create the main Tkinter window
window = tk.Tk()
window.title("Radar Chart Generator")
window.geometry("800x600")

# Create a label for the title
label = tk.Label(window, text="Paste your RF data here", font=("Arial", 16))
label.grid(row=0, column=0, padx=10, pady=10)

# Create a TextArea widget for pasting data
text_area = tk.Text(window, width=80, height=15)
text_area.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Create a button to generate the radar chart
generate_button = tk.Button(
    window, text="Generate Radar Chart", command=on_generate_click, font=("Arial", 12))
generate_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Start the Tkinter event loop
window.mainloop()
