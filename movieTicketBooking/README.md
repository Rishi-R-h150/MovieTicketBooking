# Movie Ticket Booking Console App

A **console-based movie ticket booking system** in Python that allows users to browse movies, book seats, cancel bookings, and receive notifications. The system supports multiple theatres, halls, shows, and seat types.

---

## Features

- Add and manage **Theatres** and **Halls**.
- Add and manage **Movies** and **Shows**.
- Book **Seats** for a specific show with **Economy** and **Premium** seat types.
- Cancel bookings with seat release.
- Track customer bookings and payments.
- Support **CASH** and **CREDIT_CARD** payment methods.
- Notify customers via console messages about new movies, booking confirmations, and cancellations.
- Search shows by **Title**, **Location**, **Genre**, or **Language**.

---

## Classes Overview

### Core Classes
- **Seat** – Represents a seat in a hall (Economy or Premium).
- **Hall** – Represents a hall in a theatre.
- **Theatre** – Represents a theatre with multiple halls.
- **Movie** – Represents a movie with details like genre, duration, language, release date.
- **Show** – Represents a movie show at a specific hall and time.
- **Customer** – Represents a user who can book and cancel seats.

### Services
- **BookingManagerService** – Handles booking and cancellation logic.
- **PaymentService** – Processes customer payments.
- **NotificationService** – Sends booking and cancellation notifications.
- **CatalogSearchService** – Allows searching shows based on criteria.
- **CentralBookingSystem** – Central system to manage theatres, shows, and customers.

---

## Installation

1. Clone the repository:

```bash
git clone <repo-url>
cd movie-ticket-booking-console-app
