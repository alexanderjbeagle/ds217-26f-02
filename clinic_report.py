#!/usr/bin/env python3
"""Summarize one week of clinic encounters and save the two report files."""

from pathlib import Path

from vitals_tools import (
    count_patients,
    mean_systolic,
    patients_at_or_above,
    systolic_readings,
)
import vitals_tools


DATA_PATH = Path("data") / "clinic_encounters.csv"
OUTPUT_DIR = Path("output")


def read_encounters(data_path):
    # tool to identify usable rows and count skipped rows
    usable_encounters = []
    skipped_row_count = 0

    with open(data_path, "r") as file:
        lines = file.readlines()

    # loop through rows to identify usable encounters and count skipped rows
    for line in lines[1:]:
        line = line.strip()

        #3 field check
        fields = line.split(",")
        if len(fields) != 3:
            skipped_row_count += 1
            print(f"I skipped row: {line} because the field count wasn't 3")
            continue 

        #int check on field 3
        try:
            systolic_value = int(fields[2])
        except ValueError as error:
            skipped_row_count += 1
            print(f"I skipped row: {line} because the systolic reading wasn't an integer")
            continue  

        #systolic in range check
        if systolic_value < 60 or systolic_value > 250:
            skipped_row_count += 1
            print(f"I skipped row: {line} because the systolic reading was out of range")
            continue

        usable_encounters.append(fields)  # add the patient ID and encounter date to the usable list    

    return usable_encounters, skipped_row_count

def main():
    # analyzes encounters to identify a summary report and patients who need BP follow-up due to hypertension
    encounters, skipped = read_encounters(DATA_PATH)

    # run calculations using helpers from vitals_tools.py
    readings = vitals_tools.systolic_readings(encounters)
    mean_sbp = vitals_tools.mean_systolic(readings)
    patients_count = vitals_tools.count_patients(encounters)
    highest_sbp = max(readings)
    lowest_sbp = min(readings)

    # write output to vitals_report.txt
    report_path = "output/vitals_report.txt"
    with open(report_path, "w") as report_file:
        report_file.write(f"Usable encounters: {len(encounters)}\n")
        report_file.write(f"Skipped rows: {skipped}\n")
        report_file.write(f"Patients seen: {patients_count}\n")
        report_file.write(f"Mean systolic: {mean_sbp:.1f} mmHg\n") # Format to 1 decimal place
        report_file.write(f"Highest systolic: {highest_sbp} mmHg\n")
        report_file.write(f"Lowest systolic: {lowest_sbp} mmHg\n")

    with open(report_path, "r") as report_file:
        print(report_file.read())

    # set cutoff
    my_cutoff = 160 
    my_reason = "Selected 160 mmHg to target severe HTN."
    followup_patients = vitals_tools.patients_at_or_above(encounters, my_cutoff)

    # write  to followup list ouptut/followup_list.txt
    followup_path = "output/followup_list.txt"
    with open(followup_path, "w") as followup_file:
        followup_file.write(f"Cutoff: {my_cutoff} mmHg\n")
        followup_file.write(f"Reason: {my_reason}\n")
        for patient_id in followup_patients:
            followup_file.write(f"{patient_id}\n")

if __name__ == "__main__":
    main()
