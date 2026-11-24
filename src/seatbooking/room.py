
import threading

seats: set = {"A1", "A2", "A3", "A4", "A5", "B1", "B2", "B3", "B4", "B5"}


class Room:
    seats: set
    booked_seats: dict

    def __init__(self):
        self.seats = seats.copy()
        self.booked_seats = dict()
        self._lock = threading.Lock()

    def book_seat(self, seat : str, client_name : str) -> tuple[dict,bool]:
        """ Book a seat for the room  """
        booked = False
        seat = seat.strip()
        client_name = client_name.strip()
        with self._lock:
            if seat not in self.seats or seat in self.booked_seats:
                return dict(), booked
            self.booked_seats[seat] = client_name
            booked = True
            return self.booked_seats[seat], booked

    @property
    def available_seats(self)-> list:
        with self._lock:
            available = self.seats.difference(self.booked_seats.keys())
        available = list(available)
        return available


if __name__ == "__main__":
    room = Room()
    print(f"Room seats : {room.seats}")
    print(f"Available seats: {room.available_seats}")
    room.book_seat("A1","Pascalau")
    print(f"Available seats : {room.available_seats}")
    print(room.booked_seats)