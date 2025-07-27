
import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime


class Service:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def display_info(self):
        return f"{self.name}: ${self.price:.2f}"

class Appointment(Service):
    def __init__(self, name, price, date, time):
        super().__init__(name, price)
        self.date = date
        self.time = time

    def summary(self):
        return f"{self.name} - ${self.price:.2f} on {self.date} at {self.time}"

services = {
    1: Service("Dog Grooming", 49.99),
    2: Service("Cat Grooming", 39.99),
    3: Service("Pet Bathing", 29.99),
    4: Service("Pet Nail Clipping", 19.99),
    5: Service("Pet Sitting", 24.99),
    6: Service("Pet Walking", 14.99),
    7: Service("Pet Training", 59.99),
    8: Service("Pet Boarding", 89.99),
    9: Service("Pet Transportation", 39.99),
    10: Service("Pet Photography", 99.99)
}


# --- GUI Implementation ---

class AppointmentGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mobile Pet Spa Appointment System")
        self.selected_services = []
        self.selected_date = None
        self.selected_time = None
        self.current_frame = None
        self.create_service_selection_frame()

    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True)

    def create_service_selection_frame(self):
        self.clear_frame()
        tk.Label(self.current_frame, text="************************************************", font=("Arial", 12)).pack()
        tk.Label(self.current_frame, text="Welcome to the Mobile Pet Spa Appointment System", font=("Arial", 14, "bold")).pack(pady=5)
        tk.Label(self.current_frame, text="Please select services from the list below:", font=("Arial", 12)).pack(pady=5)
        tk.Label(self.current_frame, text="************************************************", font=("Arial", 12)).pack()

        self.service_listbox = tk.Listbox(self.current_frame, selectmode=tk.MULTIPLE, width=40, height=10)
        for key, service_obj in services.items():
            self.service_listbox.insert(tk.END, f"{key}. {service_obj.display_info()}")
        self.service_listbox.pack(pady=10)
        self.service_listbox.bind("<MouseWheel>", lambda event: self.service_listbox.yview_scroll(int(-1*(event.delta/120)), "units"))

        self.selected_label = tk.Label(self.current_frame, text="", font=("Arial", 11))
        self.selected_label.pack()

        btn_frame = tk.Frame(self.current_frame)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Show Selection", command=self.update_selected_services).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Next: Select Date", command=self.go_to_date_selection).pack(side="left", padx=5)

    def update_selected_services(self):
        self.selected_services = []
        selected_indices = self.service_listbox.curselection()
        for idx in selected_indices:
            service_id = idx + 1
            try:
                # Try to access the service to ensure it exists
                _ = services[service_id]
                self.selected_services.append(service_id)
            except KeyError:
                messagebox.showerror("Service Error", f"Service with ID {service_id} not found.")
        if self.selected_services:
            try:
                total_cost = sum(services[sid].price for sid in self.selected_services)
                selected_names = ", ".join(services[sid].name for sid in self.selected_services)
                self.selected_label.config(text=f"Selected: {selected_names}\nTotal: ${total_cost:.2f}")
            except KeyError as e:
                self.selected_label.config(text="Error in selection.")
        else:
            self.selected_label.config(text="No services selected.")

    def go_to_date_selection(self):
        self.update_selected_services()
        if not self.selected_services:
            messagebox.showwarning("No Service", "Please select at least one service to continue.")
            return
        self.create_date_selection_frame()

    def create_date_selection_frame(self):
        self.clear_frame()
        tk.Label(self.current_frame, text="Select Appointment Date:", font=("Arial", 13, "bold")).pack(pady=10)
        self.cal = Calendar(self.current_frame, selectmode='day', year=2025, month=10, day=1)
        self.cal.pack(pady=10)
        tk.Button(self.current_frame, text="Next: Select Time", command=self.go_to_time_selection).pack(pady=10)
        tk.Button(self.current_frame, text="Back", command=self.create_service_selection_frame).pack()

    def go_to_time_selection(self):
        self.selected_date = self.cal.get_date()
        self.create_time_selection_frame()

    def create_time_selection_frame(self):
        self.clear_frame()
        tk.Label(self.current_frame, text="Enter Appointment Time (HH:MM):", font=("Arial", 13, "bold")).pack(pady=10)
        self.time_entry = tk.Entry(self.current_frame, font=("Arial", 12))
        self.time_entry.pack(pady=10)
        btn_frame = tk.Frame(self.current_frame)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Next: Confirm", command=self.go_to_confirmation).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Back", command=self.create_date_selection_frame).pack(side="left", padx=5)

    def go_to_confirmation(self):
        time_val = self.time_entry.get().strip()
        if not time_val:
            messagebox.showwarning("No Time", "Please enter an appointment time.")
            return
        # Validate time format
        try:
            datetime.strptime(time_val, "%H:%M")
        except ValueError:
            messagebox.showerror("Invalid Time", "Please enter time in HH:MM format (24-hour).")
            return
        self.selected_time = time_val
        self.create_confirmation_frame()

    def create_confirmation_frame(self):
        self.clear_frame()
        tk.Label(self.current_frame, text="Confirm Your Appointment", font=("Arial", 14, "bold")).pack(pady=10)
        info = ""
        for sid in self.selected_services:
            service_obj = services[sid]
            appointment = Appointment(service_obj.name, service_obj.price, self.selected_date, self.selected_time)
            info += f"{appointment.summary()}\n"
        total_cost = sum(services[sid].price for sid in self.selected_services)
        info += f"\nTotal Cost: ${total_cost:.2f}\n"
        text_box = tk.Text(self.current_frame, font=("Arial", 12), height=10, wrap="word")
        text_box.insert(tk.END, info)
        text_box.config(state=tk.DISABLED)
        text_box.pack(padx=10, pady=10, fill="both", expand=True)
        btn_frame = tk.Frame(self.current_frame)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Confirm & Save", command=self.output_order_summary).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Back", command=self.create_time_selection_frame).pack(side="left", padx=5)

    def output_order_summary(self):
        try:
            with open("order_summary.txt", "w") as file:
                file.write("************************************************\n")
                file.write("Mobile Pet Spa Appointment Order Summary\n")
                file.write("************************************************\n")
                file.write("Order Summary:\n")
                file.write("Selected Services:\n")
                for sid in self.selected_services:
                    try:
                        service_obj = services[sid]
                        appointment = Appointment(service_obj.name, service_obj.price, self.selected_date, self.selected_time)
                        file.write(f"{appointment.summary()}\n")
                    except Exception as appt_err:
                        file.write(f"Error processing service ID {sid}: {appt_err}\n")
                try:
                    total_cost = sum(services[sid].price for sid in self.selected_services)
                    file.write(f"Total Cost: ${total_cost:.2f}\n")
                except Exception as cost_err:
                    file.write(f"Error calculating total cost: {cost_err}\n")
                file.write("Thank you for your order!\n")
            messagebox.showinfo("Order Saved", "Order summary has been saved to order_summary.txt")
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save order summary: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = AppointmentGUI(root)
    root.geometry("600x500")
    root.mainloop()
