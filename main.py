from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()
addresses = data_manager.get_emails()

ORIGIN_CITY_IATA = "OPO"

if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

for destination in sheet_data:
    flight = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )

    if flight is None:
        continue

    if flight.price < destination["lowestPrice"]]:
        text = f"\nLow price alert! Only {flight.price}€ to fly from {flight.origin_city}-{flight.origin_airport} to" \
               f" {flight.destination_city}-{flight.destination_airport}," \
               f" from {flight.out_date} to {flight.return_date}."

        if flight.stop_overs > 0:
            text += f"\nFlight has {round(flight.stop_overs)} stop over, via {flight.via_city}."

        link_flight = f"https://www.google.com/travel/flights?" \
                      f"q=Flights%20to%20{flight.destination_airport}%20" \
                      f"from%20{flight.origin_airport}%20" \
                      f"on%20{flight.out_date}%20through%20{flight.return_date}"
        # notification_manager.send_sms(
        #     message=text
        # )

        notification_manager.send_emails(
            subject="New Low Price Flight!",
            message=text,
            to_addresses=addresses,
            link=link_flight
        )
