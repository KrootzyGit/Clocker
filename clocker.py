import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime, timedelta

class WorkTimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Work Timer Tracker")
        self.root.geometry("400x300")
        self.root.configure(bg="#2c3e50")

        self.clocked_in = False
        self.paused = False
        self.start_time = None
        self.pause_time = None
        self.total_paused = timedelta()
        self.log = []

        self.title_label = tk.Label(root, text="Work Time Tracker", font=("Helvetica", 16, "bold"), fg="white", bg="#2c3e50")
        self.title_label.pack(pady=10)

        self.time_display = tk.Label(root, text="00:00:00", font=("Helvetica", 24), fg="#1abc9c", bg="#2c3e50")
        self.time_display.pack(pady=5)

        self.clock_btn = tk.Button(root, text="Clock In", command=self.toggle_clock, width=20, bg="#3498db", fg="white", font=("Helvetica", 12))
        self.clock_btn.pack(pady=10)

        self.pause_btn = tk.Button(root, text="Pause", command=self.toggle_pause, state='disabled', width=20, bg="#f39c12", fg="white", font=("Helvetica", 12))
        self.pause_btn.pack(pady=10)

        self.log_btn = tk.Button(root, text="Work Log", command=self.show_log, width=20, bg="#9b59b6", fg="white", font=("Helvetica", 12))
        self.log_btn.pack(pady=10)

        self.update_timer()

    def toggle_clock(self):
        if not self.clocked_in:
            self.start_time = datetime.now()
            self.clocked_in = True
            self.total_paused = timedelta()
            self.clock_btn.config(text="Clock Out")
            self.pause_btn.config(state='normal')
        else:
            end_time = datetime.now()
            duration = end_time - self.start_time - self.total_paused

            note = simpledialog.askstring("Session Notes", "Add notes or client name here!", parent=self.root)
            if not note:
                note = "(No notes provided)"

            log_entry = {
                'note': note,
                'start': self.start_time.strftime("%m/%d/%y %H:%M:%S"),
                'end': end_time.strftime("%m/%d/%y %H:%M:%S"),
                'duration': str(duration).split('.')[0]
            }
            self.log.append(log_entry)

            self.clocked_in = False
            self.pause_btn.config(state='disabled')
            self.clock_btn.config(text="Clock In")
            self.time_display.config(text="00:00:00")

            messagebox.showinfo("Session Logged", f"{note}\nWorked from {log_entry['start']} to {log_entry['end']}.\nDuration: {log_entry['duration']}")

    def toggle_pause(self):
        if not self.paused:
            self.pause_time = datetime.now()
            self.paused = True
            self.pause_btn.config(text="Resume")
        else:
            paused_duration = datetime.now() - self.pause_time
            self.total_paused += paused_duration
            self.paused = False
            self.pause_btn.config(text="Pause")

    def show_log(self):
        def refresh_log():
            log_text.delete("1.0", tk.END)
            line_to_log_index.clear()
            current_line = 1
            for i, entry in enumerate(self.log):
                log_text.insert(tk.END, f"{entry['note']}\n", "bold")
                log_text.insert(tk.END, f"Start: {entry['start']}\nEnd: {entry['end']}\nDuration: {entry['duration']}\n\n")
                line_to_log_index[current_line] = i
                current_line += 4

        def on_right_click(event):
            index = log_text.index(f"@{event.x},{event.y}")
            line_num = int(index.split('.')[0])
            log_index = line_to_log_index.get(line_num)

            if log_index is not None:
                context_menu.entryconfig("Rename Note", command=lambda: rename_log(log_index))
                context_menu.entryconfig("Delete Entry", command=lambda: delete_log(log_index))
                context_menu.tk_popup(event.x_root, event.y_root)

        def rename_log(i):
            new_note = simpledialog.askstring("Rename Note", "Edit note:", initialvalue=self.log[i]['note'], parent=log_window)
            if new_note:
                self.log[i]['note'] = new_note
                refresh_log()

        def delete_log(i):
            if messagebox.askyesno("Delete Entry", "Are you sure you want to delete this entry?", parent=log_window):
                del self.log[i]
                refresh_log()

        log_window = tk.Toplevel(self.root)
        log_window.title("Work Log")
        log_window.geometry("500x400")
        log_window.configure(bg="#34495e")

        log_text = tk.Text(log_window, width=60, height=20, bg="#ecf0f1", fg="black", font=("Courier", 10))
        log_text.pack(padx=10, pady=10)
        log_text.tag_configure("bold", font=("Courier", 10, "bold"))

        context_menu = tk.Menu(log_window, tearoff=0)
        context_menu.add_command(label="Rename Note")
        context_menu.add_command(label="Delete Entry")

        line_to_log_index = {}
        refresh_log()
        log_text.bind("<Button-3>", on_right_click)

    def update_timer(self):
        if self.clocked_in and not self.paused:
            current_duration = datetime.now() - self.start_time - self.total_paused
            self.time_display.config(text=str(current_duration).split(".")[0])
        self.root.after(1000, self.update_timer)

if __name__ == "__main__":
    root = tk.Tk()
    app = WorkTimerApp(root)
    root.mainloop()
