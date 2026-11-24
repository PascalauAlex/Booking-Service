import datetime
import logging
from datetime import UTC
from seatbooking import booking_pb2
from seatbooking import booking_pb2_grpc

import grpc
from concurrent import futures

from seatbooking.room import Room

logger = logging.getLogger(__name__)
FORMAT = '%(asctime)s  %(message)s'


class BookingService(booking_pb2_grpc.BookingServiceServicer):

    def __init__(self,room: Room):
        self.room = room


    def BookSeats(self, request_iterator, context):
        for request in request_iterator:
            if request.seat not in self.room.seats:
                yield booking_pb2.BookingResponse(booked=False,
                                                  seat=request.seat,
                                                  status=booking_pb2.StatusEnum.UNABLE_TO_BOOK,
                                                  client_name=request.client_name,
                                                  available_seats=len(self.room.available_seats),
                                                  date=str(datetime.datetime.now(tz=datetime.UTC)),
                                                  )
                continue
            booking, booked = self.room.book_seat(request.seat, request.client_name)
            if not booked:
                yield booking_pb2.BookingResponse(booked=booked,
                                                  seat=request.seat,
                                                  status=booking_pb2.StatusEnum.ALREADY_BOOKED,
                                                  client_name=request.client_name,
                                                  available_seats=len(self.room.available_seats),
                                                  date=str(datetime.datetime.now(tz=datetime.UTC)))
                continue
            print(f"Booking created for : {request.client_name}")
            yield booking_pb2.BookingResponse(booked=booked, status=booking_pb2.BOOKED,
                                              seat=request.seat,
                                              client_name=request.client_name,
                                              available_seats=len(self.room.available_seats),
                                              date=str(datetime.datetime.now(tz=UTC)))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format=FORMAT)
    logger.info("Server started...")
    logger.info(f"GRCP VERSION : {booking_pb2_grpc.GRPC_VERSION}")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    room = Room()
    booking_pb2_grpc.add_BookingServiceServicer_to_server(BookingService(room), server)
    port = server.add_insecure_port("[::]:50052")
    if port == 0:
        raise RuntimeError('Could not bind port 50052')
    server.start()
    logger.info("Streaming server listening to port 50052")
    try:
        server.wait_for_termination()  # wait for shutdown
    except KeyboardInterrupt:
        server.stop(0)
