# BookBloom Requirements Document

## Project Overview

**Application Name:** BookBloom  
**Caption:** "Books Reborn, Knowledge Renewed"  
**Description:** A web-based e-commerce application for browsing and purchasing books from a catalog.

---

## Functional Requirements

### 1. User Interface & Navigation

#### 1.1 Header Component
- **FR-1.1.1:** The header must display the application name "BookBloom" and caption "Books Reborn, Knowledge Renewed" on all pages
- **FR-1.1.2:** The header must remain consistent across all pages of the application
- **FR-1.1.3:** The header must include navigation links to main sections (Home, Login/Profile, Cart)

#### 1.2 Landing Page
- **FR-1.2.1:** The landing page must display a list of available books in tile format
- **FR-1.2.2:** The landing page must provide a search functionality for books
- **FR-1.2.3:** Books must be displayed as tiles showing basic information

### 2. Book Catalog Management

#### 2.1 Book Information
- **FR-2.1.1:** Each book must contain the following attributes:
  - Title
  - Author
  - ISBN
  - Year of release
  - Price
  - Category
  - State (good, fair, normal, like new)

#### 2.2 Book Display
- **FR-2.2.1:** Books must always be displayed in tile format regardless of location (landing page, search results)
- **FR-2.2.2:** Each book tile must show all book attributes clearly
- **FR-2.2.3:** Book tiles must be responsive and visually consistent

### 3. Search Functionality

#### 3.1 Search Criteria
- **FR-3.1.1:** Users must be able to search books by title
- **FR-3.1.2:** Users must be able to search books by author
- **FR-3.1.3:** Search functionality must be available from the landing page
- **FR-3.1.4:** Search results must be displayed in the same tile format as the landing page

#### 3.2 Search Behavior
- **FR-3.2.1:** Search must support partial matching for titles and authors
- **FR-3.2.2:** Search must be case-insensitive
- **FR-3.2.3:** Search results must be displayed immediately after user input

### 4. User Account Management

#### 4.1 User Registration
- **FR-4.1.1:** New users must be able to register with the following minimal information:
  - First name
  - Last name
  - Email address
  - Password
  - One social handle URL (optional)

#### 4.2 User Authentication
- **FR-4.2.1:** Registered users must be able to log in using email and password
- **FR-4.2.2:** Users must be able to log out from any page
- **FR-4.2.3:** System must maintain user session until logout

#### 4.3 Password Management
- **FR-4.3.1:** Users must be able to reset forgotten passwords
- **FR-4.3.2:** Password reset must be initiated via email address
- **FR-4.3.3:** Users must receive password reset instructions via email

### 5. Shopping Cart Functionality

#### 5.1 Cart Access
- **FR-5.1.1:** Only logged-in users can add books to the cart
- **FR-5.1.2:** Anonymous users must be redirected to login when attempting to add items to cart

#### 5.2 Cart Operations
- **FR-5.2.1:** Users must be able to add books to their cart
- **FR-5.2.2:** Users must be able to view cart contents
- **FR-5.2.3:** Users must be able to remove books from their cart
- **FR-5.2.4:** Users must be able to modify quantities in their cart

#### 5.3 Checkout Process
- **FR-5.3.1:** Users must be able to proceed to checkout from their cart
- **FR-5.3.2:** Checkout process must collect shipping information
- **FR-5.3.3:** Checkout process must display order summary
- **FR-5.3.4:** No payment processing is required (placeholder checkout completion)

---

## Non-Functional Requirements

### 1. Performance Requirements

#### 1.1 Response Time
- **NFR-1.1.1:** Page load time must not exceed 3 seconds under normal conditions
- **NFR-1.1.2:** Search results must be displayed within 1 second of query submission
- **NFR-1.1.3:** Database queries must execute within 500ms for standard operations

#### 1.2 Throughput
- **NFR-1.2.1:** System must support at least 100 concurrent users
- **NFR-1.2.2:** System must handle at least 1000 page views per hour

### 2. Security Requirements

#### 2.1 Authentication & Authorization
- **NFR-2.1.1:** User passwords must be hashed and salted before storage
- **NFR-2.1.2:** User sessions must be secured with appropriate session management
- **NFR-2.1.3:** Cart access must be restricted to authenticated users only

#### 2.2 Data Protection
- **NFR-2.2.1:** All user data must be validated on both client and server sides
- **NFR-2.2.2:** SQL injection protection must be implemented for all database queries
- **NFR-2.2.3:** Cross-site scripting (XSS) protection must be implemented

#### 2.3 Communication Security
- **NFR-2.3.1:** All data transmission should use HTTPS in production environments
- **NFR-2.3.2:** API endpoints must implement proper CORS policies

### 3. Availability Requirements

#### 3.1 Uptime
- **NFR-3.1.1:** System must maintain 99% uptime during business hours
- **NFR-3.1.2:** Planned maintenance windows must not exceed 2 hours

#### 3.2 Error Handling
- **NFR-3.2.1:** System must gracefully handle and display user-friendly error messages
- **NFR-3.2.2:** System must log all errors for debugging purposes
- **NFR-3.2.3:** System must recover gracefully from temporary database unavailability

### 4. Scalability Requirements

#### 4.1 Data Growth
- **NFR-4.1.1:** System must support up to 10,000 books in the catalog
- **NFR-4.1.2:** System must support up to 1,000 registered users
- **NFR-4.1.3:** Database must handle growth without significant performance degradation

#### 4.2 Load Handling
- **NFR-4.2.1:** System architecture must allow for horizontal scaling if needed
- **NFR-4.2.2:** Database queries must be optimized for performance as data grows

---

## Technical Requirements

### 1. Backend Technology Stack

#### 1.1 Framework & Language
- **TR-1.1.1:** Backend must be implemented using Python
- **TR-1.1.2:** FastAPI framework must be used for API development
- **TR-1.1.3:** RESTful API design principles must be followed

#### 1.2 API Specifications
- **TR-1.2.1:** API must provide endpoints for user authentication
- **TR-1.2.2:** API must provide endpoints for book catalog operations
- **TR-1.2.3:** API must provide endpoints for cart management
- **TR-1.2.4:** API responses must be in JSON format

### 2. Frontend Technology Stack

#### 2.1 Primary Technology
- **TR-2.1.1:** Frontend must be implemented using vanilla HTML, CSS, and JavaScript where possible
- **TR-2.1.2:** React framework may be used only if vanilla JavaScript becomes insufficient

#### 2.2 User Interface
- **TR-2.2.1:** Frontend must be responsive and work on desktop and mobile devices
- **TR-2.2.2:** CSS must be organized and maintainable
- **TR-2.2.3:** JavaScript must handle API communication asynchronously

### 3. Database Requirements

#### 3.1 Database Technology
- **TR-3.1.1:** SQLite must be used as the database system
- **TR-3.1.2:** Database must be file-based for simplicity

#### 3.2 Database Schema
- **TR-3.2.1:** Database must contain exactly two tables: `books` and `users`

#### 3.3 Books Table Structure
- **TR-3.3.1:** Books table must include the following columns:
  - `id` (Primary Key, Integer, Auto-increment)
  - `title` (Text, Not Null)
  - `author` (Text, Not Null)
  - `isbn` (Text, Unique)
  - `year_of_release` (Integer)
  - `price` (Decimal)
  - `category` (Text)
  - `state` (Text, Check constraint: 'good', 'fair', 'normal', 'like new')

#### 3.4 Users Table Structure
- **TR-3.4.1:** Users table must include the following columns:
  - `id` (Primary Key, Integer, Auto-increment)
  - `first_name` (Text, Not Null)
  - `last_name` (Text, Not Null)
  - `email` (Text, Unique, Not Null)
  - `password_hash` (Text, Not Null)
  - `social_handle_url` (Text, Optional)
  - `created_at` (DateTime, Default: Current Timestamp)

### 4. Development & Deployment

#### 4.1 Code Quality
- **TR-4.1.1:** Code must follow PEP 8 standards for Python
- **TR-4.1.2:** Code must be well-commented and documented
- **TR-4.1.3:** Error handling must be implemented throughout the application

#### 4.2 Testing
- **TR-4.2.1:** Unit tests must be written for critical backend functions
- **TR-4.2.2:** API endpoints must be tested for proper functionality

#### 4.3 Documentation
- **TR-4.3.1:** API documentation must be generated using FastAPI's automatic documentation
- **TR-4.3.2:** README file must include setup and installation instructions

---

## Constraints & Assumptions

### Constraints
- Database limited to SQLite with only two tables
- No payment processing integration required
- Minimal user information collection
- Simple frontend technology stack preferred

### Assumptions
- Users have modern web browsers with JavaScript enabled
- Application will run in a controlled environment
- Initial user base will be relatively small
- Books catalog will be pre-populated

---

## Acceptance Criteria

1. All functional requirements must be implemented and tested
2. Performance requirements must be met under specified load conditions
3. Security measures must be in place and tested
4. System must demonstrate 99% availability during testing period
5. Code must pass quality checks and be properly documented
6. Database schema must be implemented exactly as specified
7. API endpoints must be functional and well-documented