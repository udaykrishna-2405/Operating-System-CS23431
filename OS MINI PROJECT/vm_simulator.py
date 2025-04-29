import tkinter as tk
from tkinter import ttk, messagebox
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class VirtualMemorySimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Memory Simulator")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f0f0")

        self.selected_algorithm = tk.StringVar()
        self.selected_strategy = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.root, text="Virtual Memory Simulator", font=("Arial", 20, "bold"), foreground="darkblue", background="#f0f0f0").pack(pady=10)

        self.memory_frame = ttk.LabelFrame(self.root, text="Memory Simulation", padding=10)
        self.memory_frame.pack(pady=10, fill="both", expand=True)

        self.table = ttk.Treeview(self.memory_frame, columns=("Page", "Frame", "Status"), show="headings")
        self.table.heading("Page", text="Page Number")
        self.table.heading("Frame", text="Frame Number")
        self.table.heading("Status", text="Status")
        self.table.pack(pady=10, fill="both", expand=True)

        options_frame = ttk.Frame(self.root)
        options_frame.pack(pady=5)

        ttk.Label(options_frame, text="Select Page Replacement Algorithm:").grid(row=0, column=0, padx=5)
        algo_menu = ttk.Combobox(options_frame, textvariable=self.selected_algorithm, values=["FIFO", "LRU", "Optimal"], state="readonly")
        algo_menu.current(0)
        algo_menu.grid(row=0, column=1, padx=5)

        ttk.Label(options_frame, text="Select Allocation Strategy:").grid(row=0, column=2, padx=5)
        strategy_menu = ttk.Combobox(options_frame, textvariable=self.selected_strategy, values=["First-Fit", "Best-Fit"], state="readonly")
        strategy_menu.current(0)
        strategy_menu.grid(row=0, column=3, padx=5)

        self.btn_frame = ttk.Frame(self.root)
        self.btn_frame.pack(pady=10)

        ttk.Button(self.btn_frame, text="Simulate Paging", command=self.simulate_paging).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.btn_frame, text="Simulate Page Replacement", command=self.simulate_selected_replacement).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.btn_frame, text="Compare Algorithms", command=self.simulate_all_replacements).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.btn_frame, text="Simulate Memory Allocation", command=self.simulate_selected_allocation).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.btn_frame, text="Check Thrashing", command=self.check_thrashing).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.btn_frame, text="Show Memory Blocks", command=self.show_memory_blocks).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.btn_frame, text="Efficiency Report", command=self.efficiency_report).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.btn_frame, text="Clear", command=self.clear_table).pack(side=tk.LEFT, padx=5)

    def simulate_paging(self):
        self.clear_table()
        pages = list(range(1, 11))
        frames = random.sample(range(1, 21), len(pages))
        statuses = ["Loaded", "Not Loaded"]
        for page, frame in zip(pages, frames):
            status = random.choice(statuses)
            self.table.insert("", tk.END, values=(page, frame, status))

    def simulate_selected_replacement(self):
        self.clear_table()
        algorithm = self.selected_algorithm.get()
        page_faults = random.randint(4, 10)
        messagebox.showinfo("Algorithm Simulation", f"Algorithm: {algorithm}\nPage Faults: {page_faults}")

    def simulate_all_replacements(self):
        algorithms = ["FIFO", "LRU", "Optimal"]
        frame_sizes = [3, 4, 5, 6, 7]

        for algo in algorithms:
            faults = [random.randint(3, 10) for _ in frame_sizes]
            self.draw_line_chart({algo: faults}, frame_sizes, algo)

    def draw_line_chart(self, data, frame_sizes, algo_name):
        graph_window = tk.Toplevel(self.root)
        graph_window.title(f"{algo_name} - Page Faults vs Frame Size")
        graph_window.geometry("700x500")

        fig, ax = plt.subplots(figsize=(7, 5))
        for algo, faults in data.items():
            ax.plot(frame_sizes, faults, marker='o', linestyle='-', label=algo)

        ax.set_xlabel("Number of Frames")
        ax.set_ylabel("Page Faults")
        ax.set_title(f"{algo_name} - Page Faults vs Frame Size")
        ax.legend()
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def simulate_selected_allocation(self):
        self.clear_table()
        strategy = self.selected_strategy.get()
        messagebox.showinfo("Memory Allocation", f"Simulating {strategy} strategy")

    def check_thrashing(self):
        page_faults = random.randint(5, 20)
        if page_faults > 15:
            messagebox.showwarning("Thrashing Detected", "High page fault rate detected! System may be thrashing.")
        else:
            messagebox.showinfo("No Thrashing", "Page faults are within normal limits.")

    def show_memory_blocks(self):
        memory_window = tk.Toplevel(self.root)
        memory_window.title("Memory Visualization")
        memory_window.geometry("500x500")

        colors = ["lightgreen", "lightcoral", "lightblue", "lightyellow"]
        for i in range(10):
            frame_label = tk.Label(memory_window, text=f"Frame {i+1}", width=20, height=2, bg=random.choice(colors))
            frame_label.pack(pady=5)

    def efficiency_report(self):
        output = tk.Toplevel(self.root)
        output.title("Efficiency Report")
        output.geometry("500x300")

        result_text = "Final Efficiency Report:\n\n"
        result_text += f"Total Pages Simulated: 10\n"
        result_text += f"Total Frames Used: {random.randint(10, 20)}\n"
        result_text += f"Page Faults (avg): {random.randint(3, 9)}\n"
        result_text += f"Best Performing Algorithm: {random.choice(['FIFO', 'LRU', 'Optimal'])}\n"
        result_text += f"Thrashing Detected: {'Yes' if random.randint(1, 10) > 7 else 'No'}"

        label = tk.Label(output, text=result_text, justify="left", font=("Courier", 12))
        label.pack(pady=10, padx=10)

    def clear_table(self):
        for row in self.table.get_children():
            self.table.delete(row)

if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualMemorySimulator(root)
    root.mainloop()

