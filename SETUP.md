# AutoRescue Setup Guide

## Overview

AutoRescue now runs cleanly on a local SQLite database by default, and can still use MySQL when you explicitly configure it. This makes local development fast while keeping production-style database support available.

## Quick Start

### 1. Install dependencies

```powershell
cd C:\AutoRescue
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Seed demo data

```powershell
.\.venv\Scripts\python.exe init_db.py
```

### 3. Run the app

```powershell
.\.venv\Scripts\python.exe app.py
```

Open `http://127.0.0.1:5000`

## Demo Credentials

- Customer: `customer@example.com` / `password123`
- Mechanic: `mechanic@example.com` / `password123`
- Admin: `admin@example.com` / `admin123`

## Database Modes

### Default local mode

- Uses SQLite file: `autorescue.db`
- No XAMPP or MySQL setup required

### MySQL mode

Set these environment variables before starting the app:

```powershell
$env:DB_ENGINE="mysql"
$env:DB_HOST="localhost"
$env:DB_PORT="3306"
$env:DB_USER="root"
$env:DB_PASSWORD=""
$env:DB_NAME="autorescue_v2"
```

You can also use a full `DATABASE_URL` instead.

## What Was Fixed

- Python 3.13 package compatibility path updated through newer dependency ranges
- Login flow now returns a redirect target instead of relying on brittle HTML string checks
- Admin dashboard route is implemented
- Mechanic and customer dashboards now use real database data
- Available request screens no longer rely on sample placeholder cards
- Registration supports real mechanic profile data
- Request form uses OpenStreetMap instead of a fake Google Maps key
- Error pages are now user-friendly for browser requests and JSON-safe for fetch calls

## Useful Commands

```powershell
.\.venv\Scripts\python.exe -m compileall app.py models static templates
.\.venv\Scripts\python.exe init_db.py
.\.venv\Scripts\python.exe app.py
```
