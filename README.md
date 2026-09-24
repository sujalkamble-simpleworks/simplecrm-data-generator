# Data Generator

A lightweight Streamlit app for generating realistic test data for SimpleCRM-style modules. It reads module metadata from a configured SimpleCRM instance, builds faker-based field templates, and exports generated records as CSV files for local testing or data seeding.

## Overview

This repository helps you:

- connect to a SimpleCRM API base URL
- select one or more modules to generate records for
- define how many rows to create per module
- generate realistic field values using Faker-based templates
- export the generated data as CSV files

The application is designed primarily for testing and sandbox data creation rather than production data import.

## Features

- Streamlit-based UI for managing modules
- Dynamic module metadata discovery from SimpleCRM endpoints
- CSV generation with headers based on the target module schema
- Support for generating fake values for common field types such as:
  - names
  - email
  - phone
  - URLs
  - decimal and numeric values
  - text fields
  - enums and dynamic enum selections
- Downloadable generated CSV files from the app

## Repository Structure

```text
.
├── datagenerator.py        # Streamlit app entry point
├── recordCreator.py        # Core API and CSV generation logic
├── faker_utils.py          # Fake-data generation templates and field mapping
├── requirements.txt        # Python dependencies
├── utils/
│   ├── payloads.py         # payload helpers (if used by the project)
│   └── text_utils.py       # text helper utilities
├── data/                   # generated CSV outputs are written here
└── README.md               # project documentation
```

## Tech Stack

- Python 3
- Streamlit
- Requests
- Faker
- CSV export support

## Prerequisites

Before running the app, make sure you have:

- Python 3.9+ installed
- Access to a SimpleCRM instance with a valid API base URL
- A valid username/password for authentication

## Installation

Clone the project and install dependencies:

```bash
git clone <your-repo-url>
cd data-gen
pip install -r requirements.txt
```

## Running the App

Start the Streamlit app from the project root:

```bash
streamlit run datagenerator.py
```

The app will open in your browser and let you:

1. paste the SimpleCRM API URL
2. add one or more modules
3. set the record count for each module
4. click Generate Data
5. download the resulting CSV files

## How It Works

The app does the following:

1. Authenticates against the configured SimpleCRM API endpoint
2. Fetches layout metadata for each selected module
3. Builds field templates using the `faker_utils.py` logic
4. Generates records based on the field types
5. Saves each module’s output as a CSV file in the `data/` directory

## Example of a Generated CSV

The exported files will look similar to:

```csv
name,email,phone,website
John Smith,john@example.com,5551234567,https://example.com
```

The exact columns depend on the selected module schema.

## Configuration Notes

The app currently stores a default API URL and credentials in `datagenerator.py`:

- default URL is set to a specific SimpleCRM instance
- default username and password are included in the app state

You should update these values before using the repo in a real environment, especially if you are connecting to a different tenant or instance.

## Important Notes

- This project is intended for test, sandbox, and demo data generation.
- It uses generated fake values and does not guarantee production-safe data quality.
- CSV output is written under the `data/` folder.
- API authentication and module metadata requests depend on the target SimpleCRM instance being reachable and configured correctly.

## Troubleshooting

If generation fails:

- confirm the API URL is correct
- verify the username/password are valid
- ensure the target SimpleCRM instance is reachable
- confirm the selected module names exist in the configured tenant

## License

This project does not currently include a license file. If you plan to share or distribute it publicly, add an appropriate license before doing so.

## Contributing

This repo is a simple internal utility project. Feel free to improve the data generation logic, add more field templates, or extend the export options.
