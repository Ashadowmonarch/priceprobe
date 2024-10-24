# PriceProbe
# This has not been maintained in a while and is incomplete, will get back to it one day
**PriceProbe** is a web application designed to help users track price changes for various products across online retailers. Users can monitor products, get notified of price drops, and manage a list of items they're interested in. The project was built using **Django**, **PostgreSQL**, and **Selenium** for scraping retailer websites. It also includes responsive web pages styled with **HTML**, **CSS**, and **JavaScript**.

## Features

- **Product Tracking**: Add and track items from various retailers.
- **Price Drop Alerts**: Receive notifications when a tracked product's price drops.
- **Selenium Integration**: Uses Selenium to scrape product details and prices from websites.
- **PostgreSQL Database**: Stores user data, tracked products, and price histories.
- **Static and Media Handling**: Handles static files (CSS, JavaScript) and media uploads efficiently.

## Tech Stack

- **Backend**: Django 5.0.1
- **Frontend**: HTML, CSS, JavaScript
- **Database**: PostgreSQL
- **Web Scraping**: Selenium
- **Static File Handling**: Whitenoise

## Installation

### Prerequisites

- Python 3.9+
- PostgreSQL
- Selenium WebDriver (configured for the browser you intend to use)

### Steps to Run Locally

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Ashadowmonarch/priceprobe.git
   cd priceprobe
   ```

2. **Create and Activate Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure PostgreSQL**:
   - Make sure you have PostgreSQL installed and running locally.
   - Update the `DATABASES` settings in `settings.py` with your PostgreSQL credentials if necessary.

5. **Apply Migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

7. **Set Up Selenium WebDriver**:
   - Download the WebDriver for your browser (e.g., [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/) for Chrome).
   - Ensure it's in your system's PATH or configure it accordingly in your code.

8. **Access the App**:
   Visit `http://127.0.0.1:8000` in your browser to view the application.

## Usage

1. Navigate to the home page and search for products you'd like to track.
2. Add products to your watchlist.
3. Selenium will periodically scrape prices from configured retailers and alert you when prices drop.
4. You can also receive email notifications for price drops.

## Contribution

Contributions are welcome! Feel free to open issues or submit pull requests to improve the project.

## License

This project is licensed under the MIT License.
