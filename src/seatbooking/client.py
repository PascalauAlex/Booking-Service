import logging
from seatbooking import booking_pb2
import grpc

from seatbooking import booking_pb2_grpc
from seatbooking.room import seats

logger = logging.getLogger(__name__)
FORMAT = '%(asctime)s  %(message)s'

def booking_seat(seat : str, client_name : str):
    yield booking_pb2.BookingRequest(seat=seat,client_name=client_name)


if __name__ == "__main__":
    logging.basicConfig(format=FORMAT,level=logging.INFO)
    logger.info("\nClient started...")
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = booking_pb2_grpc.BookingServiceStub(channel=channel)
        print(f"Seats: {seats}")
        while True:
            print("\n\nBook a seat.\n===Provide seat number, and name===")
            seat = input("\nSeat: ")
            client_name = input("\nName: ")
            result = stub.BookSeats(booking_seat(seat,client_name))
            for r in result:
                print(f"\nServer responded with:\nBooked:{r.booked}\nSeat:{r.seat}\nStatus:{r.status}\nAvailable seats:{r.available_seats}")


