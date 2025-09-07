from datetime import datetime, timedelta
from enum import Enum
from collections import defaultdict
from typing import List, Dict

# Enums for seat type and status
class SeatType(Enum):
    ECONOMY = "economy"
    PREMIUM = "premium"

class SeatStatus(Enum):
    AVAILABLE = "available"
    OCCUPIED = "occupied"

# Seat class
class Seat:
    def __init__(self, seatId: str, seatType: str, status: str):
        self.seatId = seatId
        self.seatType = seatType
        self.status = status

    def isAvailable(self) -> bool:
        return self.status == SeatStatus.AVAILABLE.value

    def getDetails(self) -> dict:
        return {
            "seatId": self.seatId,
            "seatType": self.seatType,
            "status": self.status
        }

    def reserve(self) -> bool:
        if self.isAvailable():
            self.status = SeatStatus.OCCUPIED.value
            return True
        return False

    def release(self) -> bool:
        if self.status == SeatStatus.OCCUPIED.value:
            self.status = SeatStatus.AVAILABLE.value
            return True
        return False

# Hall class
class Hall:
    def __init__(self, hallId: str):
        self.hallId = hallId
        self.showList: List[Show] = []

    def addShow(self, show: 'Show') -> bool:
        self.showList.append(show)
        return True

    def removeShow(self, show: 'Show') -> bool:
        if show in self.showList:
            self.showList.remove(show)
            return True
        return False

# Show class
class Show:
    def __init__(self, showId: str, startTime: datetime, endTime: datetime, hall: Hall = None, movie: 'Movie' = None, theatre: 'Theatre' = None):
        self.showId = showId
        self.startTime = startTime
        self.endTime = endTime
        self.hall = hall
        self.movie = movie
        self.playedAt = theatre
        self.seatList: List[Seat] = []

    def addSeat(self, seat: Seat) -> bool:
        self.seatList.append(seat)
        return True

    def removeSeat(self, seat: Seat) -> bool:
        if seat in self.seatList:
            self.seatList.remove(seat)
            return True
        return False

    def isAvailable(self, seat: Seat) -> bool:
        return seat in self.seatList and seat.isAvailable()

    def returnAllAvailable(self) -> List[dict]:
        return [seat.getDetails() for seat in self.seatList if seat.isAvailable()]

# Theatre class
class Theatre:
    def __init__(self, theatreId: str, location: str):
        self.theatreId = theatreId
        self.location = location
        self.hallList: List[Hall] = []

    def addHall(self, hall: Hall) -> bool:
        self.hallList.append(hall)
        return True

    def removeHall(self, hall: Hall) -> bool:
        if hall in self.hallList:
            self.hallList.remove(hall)
            return True
        return False

    def getDetails(self) -> dict:
        return {
            "theatreId": self.theatreId,
            "location": self.location,
            "halls": [hall.hallId for hall in self.hallList]
        }

# Movie class
class Movie:
    def __init__(self, movieId: str, movieName: str, genre: str, duration: int, language: str, releaseDate: datetime = None):
        self.movieId = movieId
        self.movieName = movieName
        self.genre = genre
        self.duration = duration
        self.language = language
        self.releaseDate = releaseDate
        self.showList: List[Show] = []
       
    def getDetails(self) -> dict:
        return {
            "movieId": self.movieId,
            "movieName": self.movieName,
            "genre": self.genre,
            "duration": self.duration,
            "language": self.language,
            "releaseDate": self.releaseDate
        }

# Customer class (Updated)
class Customer:
    def __init__(self, custId: str, custName: str, email: str, bookingManagerService: 'BookingManagerService'):
        self.custId = custId
        self.custName = custName
        self.email = email
        self.totalPayable = 0
        self.mpShowToSeat = defaultdict(list)  # Maps show to list of seats
        self.totalCash = 1000  # Initial cash for simplicity
        self.bookingManagerService = bookingManagerService

    def makeBookings(self, show: Show, seat: Seat, seatType: str = None, paymentMethod: str = "CASH") -> bool:
        return self.bookingManagerService.makeBooking(self, show, seat, paymentMethod) != False

    def viewBookings(self) -> Dict[Show, List[Seat]]:
        return dict(self.mpShowToSeat)

    def cancelBooking(self, show: Show, seat: Seat, seatType: str = None) -> bool:
        return self.bookingManagerService.cancelBooking(self, show, seat)

# PaymentService class 
class PaymentService:
    def processPayment(self, customer: Customer, amount: int, paymentMethod: str) -> bool:
        if paymentMethod == "CASH" and customer.totalCash >= amount:
            customer.totalCash -= amount
            customer.totalPayable += amount
            return True
        elif paymentMethod == "CREDIT_CARD":
            customer.totalPayable += amount
            return True
        return False

# NotificationService class
class NotificationService:
    @staticmethod
    def notifyNewMovie(customer: Customer, movie: Movie):
        print(f"Email to {customer.email}: New movie '{movie.movieName}' added!")

    @staticmethod
    def notifyBooking(customer: Customer, show: Show, seat: Seat):
        print(f"Email to {customer.email}: Booking confirmed for show {show.showId}, seat {seat.seatId}")

    @staticmethod
    def notifyCancellation(customer: Customer, show: Show, seat: Seat):
        print(f"Email to {customer.email}: Booking cancelled for show {show.showId}, seat {seat.seatId}")

# CatalogSearchService class
class CatalogSearchService:
    def __init__(self, shows: List[Show], theatres: Dict[str, Theatre]):
        self.shows = shows
        self.theatres = theatres

    def searchByTitle(self, title: str) -> List[Show]:
        return [show for show in self.shows if show.movie and show.movie.movieName.lower() == title.lower()]

    def searchByLoc(self, location: str) -> List[Show]:
        return [show for show in self.shows if show.playedAt and show.playedAt.location.lower() == location.lower()]

    def searchByGenre(self, genre: str) -> List[Show]:
        return [show for show in self.shows if show.movie and show.movie.genre.lower() == genre.lower()]

    def searchByLang(self, language: str) -> List[Show]:
        return [show for show in self.shows if show.movie and show.movie.language.lower() == language.lower()]

# BookingManagerService class 
class BookingManagerService:
    def __init__(self, paymentService: PaymentService, notificationService: NotificationService):
        self.paymentService = paymentService
        self.notificationService = notificationService

    def makeBooking(self, customer: Customer, show: Show, seat: Seat, paymentMethod: str) -> int:
        if show.isAvailable(seat) and seat.reserve():
            amount = 100 if seat.seatType == SeatType.ECONOMY.value else 190
            if self.paymentService.processPayment(customer, amount, paymentMethod):
                customer.mpShowToSeat[show].append(seat)
                self.notificationService.notifyBooking(customer, show, seat)
                return amount
        return False
#no refund policy
    def cancelBooking(self, customer: Customer, show: Show, seat: Seat) -> bool:
        if show in customer.mpShowToSeat and seat in customer.mpShowToSeat[show]:
            if seat.release():
                customer.mpShowToSeat[show].remove(seat)
                if not customer.mpShowToSeat[show]:  # Remove show if no seats booked
                    del customer.mpShowToSeat[show]
                self.notificationService.notifyCancellation(customer, show, seat)
                return True
        return False

# CentralBookingSystem class
class CentralBookingSystem:
    def __init__(self):
        self.bookingManagerService = BookingManagerService(PaymentService(), NotificationService())
        self.catalogSearchService = CatalogSearchService([], {})
        self.locationToTheatre: Dict[str, Theatre] = {}
        self.shows: List[Show] = []
        self.customers: List[Customer] = []

    def addCustomer(self, customer: Customer) -> bool:
        self.customers.append(customer)
        return True

    def removeCustomer(self, customer: Customer) -> bool:
        if customer in self.customers:
            self.customers.remove(customer)
            return True
        return False

    def addTheatre(self, theatre: Theatre) -> bool:
        self.locationToTheatre[theatre.location] = theatre
        self.catalogSearchService.theatres = self.locationToTheatre
        return True

    def removeTheatre(self, theatre: Theatre) -> bool:
        if theatre.location in self.locationToTheatre:
            del self.locationToTheatre[theatre.location]
            self.catalogSearchService.theatres = self.locationToTheatre
            return True
        return False

    def addShow(self, show: Show) -> bool:
        self.shows.append(show)
        self.catalogSearchService.shows = self.shows
        return True

    def makeBooking(self, customer: Customer, show: Show, seat: Seat, paymentMethod: str) -> bool:
        result = self.bookingManagerService.makeBooking(customer, show, seat, paymentMethod)
        return result != False

    def cancelBooking(self, customer: Customer, show: Show, seat: Seat) -> bool:
        return self.bookingManagerService.cancelBooking(customer, show, seat)

    def search(self, criteria: str, value: str) -> List[Show]:
        if criteria == "title":
            return self.catalogSearchService.searchByTitle(value)
        elif criteria == "location":
            return self.catalogSearchService.searchByLoc(value)
        elif criteria == "genre":
            return self.catalogSearchService.searchByGenre(value)
        elif criteria == "language":
            return self.catalogSearchService.searchByLang(value)
        return []

# Testing code
if __name__ == "__main__":
    # Initialize system
    cbs = CentralBookingSystem()
    booking_manager = cbs.bookingManagerService  # Get BookingManagerService instance

    # Create theatre and hall
    theatre1 = Theatre("T1", "New York")
    hall1 = Hall("H1")
    theatre1.addHall(hall1)
    cbs.addTheatre(theatre1)

    # Create movie
    movie1 = Movie("M1", "Inception", "Sci-Fi", 148, "English", datetime(2025, 8, 1))

    # Create show
    show1 = Show("SH1", datetime.now(), datetime.now() + timedelta(hours=3), hall1, movie1, theatre1)
    hall1.addShow(show1)
    cbs.addShow(show1)

    # Create seats
    s1 = Seat("A12", SeatType.ECONOMY.value, SeatStatus.AVAILABLE.value)
    s2 = Seat("A13", SeatType.ECONOMY.value, SeatStatus.AVAILABLE.value)
    s3 = Seat("A14", SeatType.PREMIUM.value, SeatStatus.OCCUPIED.value)
    show1.addSeat(s1)
    show1.addSeat(s2)
    show1.addSeat(s3)

    # Create customer with BookingManagerService
    customer1 = Customer("C1", "John Doe", "john@example.com", booking_manager)
    cbs.addCustomer(customer1)

    # Test booking
    print("Available seats:", show1.returnAllAvailable())
    customer1.makeBookings(show1, s1, paymentMethod="CASH")
    print("Customer bookings:", {show.showId: [seat.seatId for seat in seats] for show, seats in customer1.viewBookings().items()})
    print("Customer cash:", customer1.totalCash)

    # Test cancellation
    customer1.cancelBooking(show1, s1)
    print("Customer bookings after cancellation:", {show.showId: [seat.seatId for seat in seats] for show, seats in customer1.viewBookings().items()})
    print("Available seats after cancellation:", show1.returnAllAvailable())

    # Test search
    print("Search by title:", [show.showId for show in cbs.search("title", "Inception")])
    print("Search by location:", [show.showId for show in cbs.search("location", "New York")])