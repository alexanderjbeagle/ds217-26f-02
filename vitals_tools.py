"""Reusable helpers for summarizing clinic systolic readings."""

def systolic_readings(encounters):
    # this pulls SBP values from the encounters into a list of integers
    sbp_list = []
    for encounter in encounters:
        sbp_list.append(int(encounter[2]))
    return sbp_list


def mean_systolic(readings):
    # this returns an error when there is nohing to avergae, but otherwise returns the mean of readings list
    if len(readings) == 0:
        raise ValueError("None")
    else:
        return sum(readings) / len(readings)

def count_patients(encounters):
    # return a deduplicated list of patient IDs from the encounters and ID count
    patient_ids = []
    for encounter in encounters:
        patient_ids.append(encounter[0])
    return list(set(patient_ids)), len(set(patient_ids))


def patients_at_or_above(encounters, cutoff):
    # make a list of patients whose sbp is above cutoff, then return a deduplicated list
    patient_ids = []
    for encounter in encounters:
        if int(encounter[2]) >= cutoff:
            patient_ids.append(encounter[0])
    return list(set(patient_ids))
