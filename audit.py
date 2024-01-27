import os
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
import threading

NATIONAL_CUMBUD = "Cumulative BU"
NATIONAL_BUD = "Current BU"
NATIONAL_EOD_FAA = "Entry on Duty Date"
NATIONAL_SCD = "Service Computation Date"


def process_audit(local_df: pd.DataFrame, national_df: pd.DataFrame) -> None:
    local_df.columns = local_df.iloc[0]
    local_df = local_df[1:]

    def format_date(dt: pd.Timestamp) -> str:
        if pd.notna(dt):
            return dt.strftime("%m/%d/%Y").lstrip("0").replace("/0", "/")
        else:
            return dt

    print("\nFormatting dates...")
    local_df.loc[:, "CumBUD"] = local_df["CumBUD"].apply(format_date)
    local_df.loc[:, "BUD"] = local_df["BUD"].apply(format_date)
    local_df.loc[:, "EOD FAA"] = local_df["EOD FAA"].apply(format_date)
    local_df.loc[:, "SCD"] = local_df["SCD"].apply(format_date)

    print("\nAuditing...")
    for _index, row in national_df.iterrows():
        local_member = local_df[local_df["Member Number"] == row["Member Number"]]
        if local_member.empty:
            print(
                "\nNational member not found in local: "
                + str(row["Member Number"])
                + " "
                + row["First Name"]
                + " "
                + row["Last Name"]
            )
            continue
        elif len(local_member) > 1:
            print(
                "\nMultiple local members found for national member: "
                + str(row["Member Number"])
                + " "
                + row["First Name"]
                + " "
                + row["Last Name"]
            )
            continue

        if (
            not pd.isna(row[NATIONAL_CUMBUD])
            and row[NATIONAL_CUMBUD] != local_member["CumBUD"].values[0]
        ):
            print("\nCumalative BU mismatch: " + str(row["Member Number"]))
            print(local_member["Employee"].values[0])
            print("National: " + str(row[NATIONAL_CUMBUD]))
            print("Local: " + str(local_member["CumBUD"].values[0]))
        if (
            not pd.isna(row[NATIONAL_BUD])
            and row[NATIONAL_BUD] != local_member["BUD"].values[0]
        ):
            print("\nCurrent BU mismatch: " + str(row["Member Number"]))
            print(local_member["Employee"].values[0])
            print("National: " + str(row[NATIONAL_BUD]))
            print("Local: " + str(local_member["BUD"].values[0]))
        if (
            not pd.isna(row[NATIONAL_EOD_FAA])
            and row[NATIONAL_EOD_FAA] != local_member["EOD FAA"].values[0]
        ):
            print("\nEntry on Duty Date mismatch: " + str(row["Member Number"]))
            print(local_member["Employee"].values[0])
            print("National: " + str(row[NATIONAL_EOD_FAA]))
            print("Local: " + str(local_member["EOD FAA"].values[0]))
        if (
            not pd.isna(row[NATIONAL_SCD])
            and row[NATIONAL_SCD] != local_member["SCD"].values[0]
        ):
            print("\nService Computation Date mismatch: " + str(row["Member Number"]))
            print(local_member["Employee"].values[0])
            print("National: " + str(row[NATIONAL_SCD]))
            print("Local: " + str(local_member["SCD"].values[0]))


def select_file(file_var: tk.StringVar, label: ttk.Label)-> None:
    filename = filedialog.askopenfilename(
        filetypes=[("XLSX Files", "*.xlsx"), ("CSV Files", "*.csv")]
    )
    file_var.set(filename)
    label.config(text=filename)

def clear_console()-> None:
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For macOS and Linux
    else:
        _ = os.system('clear')


def audit()-> None:
    local_file = local_file_var.get()
    national_file = national_file_var.get()
    try:
        if local_file and national_file:    
            clear_console()
            print("\nReading files...")
            local_df = pd.read_excel(local_file)
            national_df = pd.read_csv(national_file)
            process_audit(local_df, national_df)
            print("\nAudit completed successfully.")
        else:
            messagebox.showwarning(
                "Warning", "Please select both files before auditing."
            )
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        audit_button.config(state=tk.NORMAL)


def start_audit_thread()-> None:
    audit_button.config(state=tk.DISABLED)
    threading.Thread(target=audit).start()


root = tk.Tk()
root.title("File Selection for Audit")
style = ttk.Style()
style.theme_use(
    "alt"
)

local_file_var = tk.StringVar()
national_file_var = tk.StringVar()

frame = ttk.Frame(root)
frame.pack(padx=10, pady=10)

local_label = ttk.Label(frame, text="No file selected")
local_label.grid(row=0, column=1, sticky="ew")
ttk.Button(
    frame,
    text="Select Local Member List",
    command=lambda: select_file(local_file_var, local_label),
).grid(row=0, column=0, pady=5, sticky="ew")

national_label = ttk.Label(frame, text="No file selected")
national_label.grid(row=1, column=1, sticky="ew")
ttk.Button(
    frame,
    text="Select National Member List",
    command=lambda: select_file(national_file_var, national_label),
).grid(row=1, column=0, pady=5, sticky="ew")

audit_button = ttk.Button(frame, text="Audit", command=start_audit_thread)
audit_button.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

root.mainloop()
