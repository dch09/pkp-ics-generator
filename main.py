import pdfplumber
from ics import Calendar, Event
from datetime import datetime
import pytz
import pathlib


def extract_data(path_to_file):
    def create_dict_from_table(table):
        return {'departure_hour': table[1].split('-')[0].strip(),
                'arrival_hour': table[1].split('-')[1].strip(),
                'date': table[2],
                'carrier': table[3].replace('\n', ' '),
                'train': table[4].replace('\n', ' '),
                'wagon': table[6],
                'seats': table[7]}

    table: dict

    with pdfplumber.open(path_to_file) as pdf:
        first_page = pdf.pages[0]

        origin = first_page.extract_text().split('\n')[1].split('\n')[
            0].split('  ')[0].strip()
        destination = first_page.extract_text().split(
            '\n')[1].split('\n')[0].split('  ')[1].strip()
        table = create_dict_from_table(first_page.extract_table()[1])

        return {'origin': origin, 'destination': destination, 'info': table}


def localize_datetimes(departure, arrival, date):
    local_tz = pytz.timezone('Europe/Warsaw')

    departure = local_tz.localize(datetime.strptime(
        f"{date} {departure}", "%d.%m.%Y %H:%M"))
    arrival = local_tz.localize(datetime.strptime(
        f"{date} {arrival}", "%d.%m.%Y %H:%M"))

    return departure, arrival


def create_calendar(data):

    calendar = Calendar()
    event = Event()
    event.name = f"{data['origin']} > {data['destination']}"
    event.begin, event.end = localize_datetimes(
        data['info']['departure_hour'], data['info']['arrival_hour'], data['info']['date'])
    event.description = f"Pociąg {data['info']['carrier']} {data['info']['train']}.\nWagon {data['info']['wagon']}, miejsce {data['info']['seats']}"

    calendar.events.add(event)

    return calendar


def start():
    path = input("Drag & drop ticket pdf file or enter path manually: \n").replace(
        "'", " ").strip()
    output_path = pathlib.Path.home() / 'Desktop'
    filename = path.split('/')[-1].split('.')[0]
    with open(output_path / f"{filename}.ics", 'w') as file:
        file.write(str(create_calendar(extract_data(path))))

    print(f"File '{filename}.ics' successfully saved on the desktop.")


if __name__ == "__main__":
    start()
