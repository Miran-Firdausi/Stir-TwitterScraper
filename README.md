# Twitter Trending Topics Scraper

A full-stack web application built with Django (backend) and React (frontend) to scrape Twitter's top 5 trending topics using Selenium and BeautifulSoup, and store the data in MongoDB. The application allows users to get the latest trending topics with a timestamp and IP address used during the scraping process.

## Features

- Scrapes the top 5 trending topics from Twitter's Explore section.
- Uses **Selenium** to automate browser actions and **BeautifulSoup** for parsing the content.
- Stores scraped data in **MongoDB** with details like trend names and IP addresses.
- Exposes a single API endpoint to retrieve the trending topics data.
- Displays trends along with the timestamp of scraping and the IP address used.
- React frontend to display scraped data to users.

## Tech Stack
- **Django** - Web framework for building RESTful API.
- **Django REST Framework** - For API handling.
- **Selenium** - For automating Twitter scraping.
- **BeautifulSoup** - For parsing the scraped HTML content.
- **MongoDB** - NoSQL database to store scraped data.
- **ProxyMesh** - To use rotating proxies for scraping.
- **React** - Frontend framework.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.x
- Node.js
- MongoDB (Local or Remote)

## Installation

### 1. **Clone the Repository**
Clone the repo to your local machine:

```bash
git clone https://github.com/Miran-Firdausi/Stir-TwitterScraper.git
cd Stir-TwitterScraper
```

### 2. **Backend Setup (Django)**

#### Install Dependencies
Navigate to the `backend` directory and install the required Python packages:

```bash
cd backend
pip install -r requirements.txt
```

#### Configure Environment Variables

Create a `.env` file in the backend folder and add the following environment variables:
An example .env is provided

- Replace with your actual credentials.
- `MONGO_URI` should point to your MongoDB instance.

#### Run the Backend Server

Start the Django development server:

```bash
python manage.py runserver
```

The backend API will be available at `http://localhost:8000`.

### 3. **Frontend Setup (React)**

#### Install Dependencies
Navigate to the `frontend` directory and install the required Node.js packages:

```bash
cd frontend
npm install
```

#### Start the React Development Server

Run the following command to start the React development server:

```bash
npm run dev
```

The React app will be available at `http://localhost:5173`.

---

## API Endpoints

### **GET /api/get=trending-data/**

Retrieves the top 5 trending topics, timestamp, and IP address used during the scraping process.

#### **Response Format:**

```json
{
  "timestamp": "2024-12-30 14:00:00",
  "ip_address": "xxx.xxx.xxx.xxx",
  "trending_topics": [
    {
      "name": "Topic 1"
    },
    {
      "name": "Topic 2"
    },
    {
      "name": "Topic 3"
    },
    {
      "name": "Topic 4"
    },
    {
      "name": "Topic 5"
    }
  ]
}
```

## Functionality

### **1. Scraping Twitter**
The backend uses **Selenium** to load the Twitter login page, authenticate, and navigate to the trending topics section. Once the page loads, **BeautifulSoup** is used to parse the HTML and extract the top 5 trending topics.

The application handles retries in case of failures and uses **ProxyMesh** for rotating IPs to avoid being blocked by Twitter.

### **2. Storing Data in MongoDB**
The scraped data (top 5 trending topics, timestamp, and IP address used) is stored in a **MongoDB** collection. Each record includes:
- Timestamp of when the scraping was done.
- List of top 5 trending topics.
- The IP address used during the scraping.

### **3. Displaying Data on Frontend**
The frontend is built with **React** and fetches the data from the Django backend via a REST API. The topics are displayed along with the timestamp and the IP address used.

---

## How to Use

1. **Frontend:**
   - Open `http://localhost:5173` in your browser.
   - Click on the "Get Trending Topics" button to fetch the top 5 trending topics.

2. **Backend:**
   - The backend will automatically scrape Twitter for trending topics and store the results in MongoDB.
   - The `GET /api/get-trending-data/` endpoint is available to fetch the latest scraped data.

---