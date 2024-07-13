import tkinter as tk
from tkinter import ttk, simpledialog, messagebox


class CPUSchedulerSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling Simulator")

        self.algorithms = ["FCFS", "SJF", "Round Robin", "SRTF Preemptive", "SRTF Non-Preemptive", "Priority"]

        # Variables
        self.algorithm_var = tk.StringVar(value=self.algorithms[0])
        self.quantum_var = tk.IntVar(value=1)

        # Process data
        self.process_data = []

        # Widgets
        self.create_widgets()

    def create_widgets(self):
        # Labels
        algorithm_label = ttk.Label(self.root, text="Select Algorithm:")
        algorithm_label.grid(row=0, column=0, padx=10, pady=10)

        quantum_label = ttk.Label(self.root, text="Quantum (for Round Robin):")
        quantum_label.grid(row=1, column=0, padx=10, pady=10)

        # Dropdown menu for algorithm selection
        algorithm_menu = ttk.Combobox(self.root, textvariable=self.algorithm_var, values=self.algorithms)
        algorithm_menu.grid(row=0, column=1, padx=10, pady=10)

        # Entry field for quantum
        quantum_entry = ttk.Entry(self.root, textvariable=self.quantum_var)
        quantum_entry.grid(row=1, column=1, padx=10, pady=10)

        # Button to add processes
        add_process_button = ttk.Button(self.root, text="Add Process", command=self.add_process)
        add_process_button.grid(row=2, column=0, columnspan=2, pady=20)

        # Button to simulate
        simulate_button = ttk.Button(self.root, text="Simulate", command=self.simulate)
        simulate_button.grid(row=3, column=0, columnspan=2, pady=20)

        # Text widget to display simulation output
        self.output_text = tk.Text(self.root, height=15, width=50)
        self.output_text.grid(row=4, column=0, columnspan=2, pady=10, padx=10)

    def add_process(self):
        burst_time = simpledialog.askinteger("Burst Time", "Enter Burst Time for the Process:")
        arrival_time = simpledialog.askinteger("Arrival Time", "Enter Arrival Time for the Process:")
        priority = simpledialog.askinteger("Priority", "Enter Priority for the Process:")

        if burst_time is not None and arrival_time is not None and priority is not None:
            process = {"id": len(self.process_data) + 1, "arrival_time": arrival_time, "burst_time": burst_time,
                       "priority": priority}
            self.process_data.append(process)

            messagebox.showinfo("Process Added", f"Process {len(self.process_data)} added successfully.")

    def simulate_fcfs(self, processes):
        waiting_time = 0
        turnaround_time = 0
        current_time = 0

        for process in processes:
            process_start_time = max(current_time, process["arrival_time"])
            waiting_time += process_start_time - process["arrival_time"]
            turnaround_time += process_start_time + process["burst_time"] - process["arrival_time"]
            current_time = process_start_time + process["burst_time"]

            self.output_text.insert(tk.END, f"Process {process['id']} - Start: {process_start_time}, "
                                            f"Finish: {current_time}, Waiting Time: {waiting_time}\n")

        average_waiting_time = waiting_time / len(processes)
        average_turnaround_time = turnaround_time / len(processes)

        self.output_text.insert(tk.END, f"\nAverage Waiting Time: {average_waiting_time}\n")
        self.output_text.insert(tk.END, f"Average Turnaround Time: {average_turnaround_time}\n")

    def simulate_sjf(self, processes):
        processes.sort(key=lambda x: x["burst_time"])

        waiting_time = 0
        turnaround_time = 0
        current_time = 0

        for process in processes:
            process_start_time = max(current_time, process["arrival_time"])
            waiting_time += process_start_time - process["arrival_time"]
            turnaround_time += process_start_time + process["burst_time"] - process["arrival_time"]
            current_time = process_start_time + process["burst_time"]

            self.output_text.insert(tk.END, f"Process {process['id']} - Start: {process_start_time}, "
                                            f"Finish: {current_time}, Waiting Time: {waiting_time}\n")

        average_waiting_time = waiting_time / len(processes)
        average_turnaround_time = turnaround_time / len(processes)

        self.output_text.insert(tk.END, f"\nAverage Waiting Time: {average_waiting_time}\n")
        self.output_text.insert(tk.END, f"Average Turnaround Time: {average_turnaround_time}\n")

    def simulate_round_robin(self, processes, quantum):
        waiting_time = [0] * len(processes)
        turnaround_time = [0] * len(processes)
        current_time = 0
        remaining_burst_time = [process["burst_time"] for process in processes]

        while any(remaining_burst_time):
            for i, process in enumerate(processes):
                if remaining_burst_time[i] > 0:
                    process_start_time = max(current_time, process["arrival_time"])
                    current_time = min(process_start_time + quantum, current_time + remaining_burst_time[i])
                    remaining_burst_time[i] -= min(quantum, remaining_burst_time[i])

                    if remaining_burst_time[i] == 0:
                        turnaround_time[i] = current_time - process["arrival_time"]
                        waiting_time[i] = turnaround_time[i] - process["burst_time"]

                    self.output_text.insert(tk.END, f"Process {process['id']} - Start: {process_start_time}, "
                                                    f"Finish: {current_time}, Waiting Time: {waiting_time[i]}\n")

        average_waiting_time = sum(waiting_time) / len(processes)
        average_turnaround_time = sum(turnaround_time) / len(processes)

        self.output_text.insert(tk.END, f"\nAverage Waiting Time: {average_waiting_time}\n")
        self.output_text.insert(tk.END, f"Average Turnaround Time: {average_turnaround_time}\n")

    def simulate_srtf(self, processes, preemptive=True):
        waiting_time = [0] * len(processes)
        turnaround_time = [0] * len(processes)
        current_time = 0
        remaining_burst_time = [process["burst_time"] for process in processes]

        while any(remaining_burst_time):
            min_burst_time = float("inf")
            next_process = None

            for i, process in enumerate(processes):
                if remaining_burst_time[i] > 0 and process["arrival_time"] <= current_time:
                    if remaining_burst_time[i] < min_burst_time:
                        min_burst_time = remaining_burst_time[i]
                        next_process = i

            if next_process is not None:
                process_start_time = current_time
                current_time += min(remaining_burst_time[next_process], 1) if preemptive else remaining_burst_time[
                    next_process]
                remaining_burst_time[next_process] -= min(remaining_burst_time[next_process], 1) if preemptive else \
                remaining_burst_time[next_process]

                if remaining_burst_time[next_process] == 0:
                    turnaround_time[next_process] = current_time - processes[next_process]["arrival_time"]
                    waiting_time[next_process] = turnaround_time[next_process] - processes[next_process]["burst_time"]

                self.output_text.insert(tk.END,
                                        f"Process {processes[next_process]['id']} - Start: {process_start_time}, "
                                        f"Finish: {current_time}, Waiting Time: {waiting_time[next_process]}\n")
            else:
                current_time += 1

        average_waiting_time = sum(waiting_time) / len(processes)
        average_turnaround_time = sum(turnaround_time) / len(processes)

        self.output_text.insert(tk.END, f"\nAverage Waiting Time: {average_waiting_time}\n")
        self.output_text.insert(tk.END, f"Average Turnaround Time: {average_turnaround_time}\n")

    def simulate_priority(self, processes):
        processes.sort(key=lambda x: x["priority"], reverse=True)

        waiting_time = [0] * len(processes)
        turnaround_time = [0] * len(processes)
        current_time = 0

        for process in processes:
            process_start_time = max(current_time, process["arrival_time"])
            current_time = process_start_time + process["burst_time"]
            waiting_time[process["id"] - 1] = process_start_time - process["arrival_time"]
            turnaround_time[process["id"] - 1] = process_start_time + process["burst_time"] - process["arrival_time"]

            self.output_text.insert(tk.END, f"Process {process['id']} - Start: {process_start_time}, "
                                            f"Finish: {current_time}, Waiting Time: {waiting_time[process['id'] - 1]}\n")

        average_waiting_time = sum(waiting_time) / len(processes)
        average_turnaround_time = sum(turnaround_time) / len(processes)

        self.output_text.insert(tk.END, f"\nAverage Waiting Time: {average_waiting_time}\n")
        self.output_text.insert(tk.END, f"Average Turnaround Time: {average_turnaround_time}\n")

    def simulate(self):
        algorithm = self.algorithm_var.get()
        quantum = self.quantum_var.get()

        if not algorithm or (algorithm == "Round Robin" and not quantum):
            messagebox.showerror("Error", "Please select an algorithm and provide necessary parameters.")
            return

        if not self.process_data:
            messagebox.showerror("Error", "Please add at least one process.")
            return

        self.output_text.delete(1.0, tk.END)  # Clear previous output

        if algorithm == "FCFS":
            self.simulate_fcfs(self.process_data)
        elif algorithm == "SJF":
            self.simulate_sjf(self.process_data)
        elif algorithm == "Round Robin":
            self.simulate_round_robin(self.process_data, quantum)
        elif algorithm == "SRTF Preemptive":
            self.simulate_srtf(self.process_data, preemptive=True)
        elif algorithm == "SRTF Non-Preemptive":
            self.simulate_srtf(self.process_data, preemptive=False)
        elif algorithm == "Priority":
            self.simulate_priority(self.process_data)


if __name__ == "__main__":
    root = tk.Tk()
    app = CPUSchedulerSimulator(root)
    root.mainloop()


















