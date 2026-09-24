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

## Running the App

Start the Streamlit app from the project root:
```bash
streamlit run datagenerator.py
```

## How It Works

The app does the following:
1. Authenticates against the configured SimpleCRM API endpoint
2. Fetches layout metadata for each selected module
3. Builds field templates using the `faker_utils.py` logic
4. Generates records based on the field types
5. Saves each module’s output as a CSV file in the `data/` directory

## Important Notes

- This project is intended for test, sandbox, and demo data generation.
- It uses generated fake values and does not guarantee production-safe data quality.
- CSV output is written under the `data/` folder.
- API authentication and module metadata requests depend on the target SimpleCRM instance being reachable and configured correctly.

## License

This project does not currently include a license file. If you plan to share or distribute it publicly, add an appropriate license before doing so.

## Contributing

This repo is a simple internal utility project. Feel free to improve the data generation logic, add more field templates, or extend the export options.
