# Schedule Source Grid Generator

## Overview
The Schedule Source Grid Generator(SSGG) is a specialized tool designed to automate the process of creating visual time grids for employee availability schedules. It interfaces with the Schedule Source API to fetch employee availability data and generates formatted Excel spreadsheets with highlighted time blocks.

## Features
- **API Integration**: Secure authentication and data retrieval from Schedule Source API
- **Automated Grid Generation**: Converts raw availability data into visual Excel grids
- **Web Interface**: Simple user interface for inputting employee IDs
- **Time Processing**: Handles complex time range conversions and formatting
- **Error Handling**: Robust error management and session handling

## Technology Stack
- Python 3.12
- Flask (Web Framework)
- openpyxl (Excel Processing)
- Requests (API Communication)

## Architecture

### Components
1. **Authentication Module**
   - Handles API authentication
   - Manages session tokens
   - Ensures secure communication

2. **API Integration**
   - Manages Schedule Source API communication
   - Handles data retrieval
   - Processes API responses

3. **Grid Generator**
   - Processes availability data
   - Generates Excel grids
   - Applies visual formatting
