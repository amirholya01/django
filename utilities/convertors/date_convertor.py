import jdatetime


def convert_shamsi_to_miladi(shamsi_date: str):
    if shamsi_date is not None and shamsi_date is not '':
        year, month, day = shamsi_date.split('/')
        return jdatetime.date(int(year), int(month), int(day)).togregorian()
    else:
        return None
