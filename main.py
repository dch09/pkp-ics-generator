import pdfplumber
from ics import Calendar, Event
from datetime import datetime
import pytz
import pathlib
import argparse


def get_arguments() -> str:
    """
    Initializes the argparser and returns input and output filepaths
    """
    parser = argparse.ArgumentParser(
        description="Export ics calendar event from intercity ticket in pdf file format.")
    parser.add_argument('-i',
                        '--input',
                        type=str,
                        metavar="ticket_filepath",
                        help="Path to the ticket pdf file (eg., ~/Desktop/eic_151993996.pdf")
    parser.add_argument('-o',
                        '--output',
                        metavar="exported_event_filepath",
                        type=str,
                        help="Path where ics calendar event file should be saved.")

    args = parser.parse_args()
    return args.input, args.output


def __validate_path__(filepath: str, is_input: bool = True) -> bool:
    """
    Checks if string is a correct absolute path, returns True if yes and False if not
    """
    try:
        pathlib.Path(filepath).resolve()
        if not is_input:
            return True

        try:
            open(filepath, 'r')
            return True
        except OSError:
            return False
    except Exception:
        return False


def validate_arguments(input_arg: str, output_arg) -> bool:
    """
    Validates script arguments and returns True if requirements are met
    """

    # Check if input arg is a valid string path
    input_arg_is_valid = type(
        input_arg) is str and __validate_path__(input_arg)

    # Early return if there's no output arg
    if output_arg is None:
        return input_arg_is_valid

    # Check if output arg is a valid string path
    output_arg_is_valid = type(output_arg) is str and __validate_path__(
        output_arg, is_input=False)

    # Return if both input and output args are valid
    return input_arg_is_valid and output_arg_is_valid


def extract_data(filepath: str) -> dict:
    """
    Extracts data from pdf file and returns a dictionary
    """
    def create_dict_from_table(table):
        return {'departure_hour': table[1].split('-')[0].strip(),
                'arrival_hour': table[1].split('-')[1].strip(),
                'date': table[2],
                'carrier': table[3].replace('\n', ' '),
                'train': table[4].replace('\n', ' '),
                'wagon': table[6],
                'seats': table[7]}

    table: dict

    with pdfplumber.open(filepath) as pdf:
        first_page = pdf.pages[0]

        origin = first_page.extract_text().split('\n')[1].split('\n')[
            0].split('  ')[0].strip()
        destination = first_page.extract_text().split(
            '\n')[1].split('\n')[0].split('  ')[1].strip()
        table = create_dict_from_table(first_page.extract_table()[1])

        return {'origin': origin, 'destination': destination, 'info': table}


def localize_datetime(time: datetime, date: datetime) -> datetime:
    local_timezone = pytz.timezone('Europe/Warsaw')

    formatted_datetime = datetime.strptime(
        f"{date} {time}", "%d.%m.%Y %H:%M")

    return local_timezone.localize(formatted_datetime)


def create_calendar(data: dict):
    """
    Creates Calendar with new Event object
    """
    calendar = Calendar()
    event = Event()

    # eg. Kraków > Wrocław
    event.name = f"{data['origin']} > {data['destination']}"

    event_start_datetime = data['info']['departure_hour']
    event_end_datetime = data['info']['arrival_hour']
    event_date = data['info']['date']

    event.begin = localize_datetime(event_start_datetime, event_date)
    event.end = localize_datetime(event_end_datetime, event_date)

    event.description = f"Pociąg {data['info']['carrier']} {data['info']['train']}.\nWagon {data['info']['wagon']}, miejsce {data['info']['seats']}"

    calendar.events.add(event)

    return calendar


def get_original_filename(path: str) -> str:
    """
    Returns filename from path string
    """
    return path.split('/')[-1].split('.')[0]

# TODO: validation


def save_calendar_to_file(calendar: Calendar, output_path: str):
    """
    Writes calendar event data to .ics file
    """
    try:
        with open(output_path, 'w') as file:
            file.write(calendar.serialize())
    except IOError:
        print("Exception while writing to file.")


def start():
    input_path, output_path = get_arguments()

    # If there's no output path argument specified, use the input one with corresponding extension
    if output_path is None:
        output_path = input_path.replace(".pdf", ".ics")

    # Abort exectution if there's no input argument
    if input_path is None:
        print(
            "In order to process pdf ticket file, please add it using -i (or --input) [path/to/file.pdf] argument.")
    elif validate_arguments(input_path, output_path):
        extracted_data = extract_data(input_path)
        calendar = create_calendar(extracted_data)
        save_calendar_to_file(calendar, output_path)
        # TODO: success confirmation message
    else:
        print("Incorrect arguments were passed.")


if __name__ == "__main__":
    start()
