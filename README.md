# Fishing Assistant App

#### Video Demo: [https://youtu.be/zNXk8H_2uEw?si=Q6gz65qVCLeHHui2]

#### Description

The Fishing Assistant App is a command-line Python application designed to assist artisanal fishers by providing useful information before and during fishing activities. The objective of the project is to demonstrate how simple software can contribute to safer fishing operations by combining weather forecasts, marine conditions, fishery regulations, and emergency communication into a single application.

The inspiration for this project comes from my background in oceanography and my interest in developing digital tools that can support sustainable fisheries in Togo. Small-scale fishers often depend on weather conditions and local knowledge before going to sea. However, access to marine forecasts and emergency reporting tools is not always straightforward. This project simulates how these services could be integrated into one lightweight application.

The application is written entirely in Python and follows the requirements of the CS50P final project. The main program is located in **project.py**, while the automated tests are implemented in **test_project.py** using pytest.

When the application starts, it displays a menu with five options.

The first option allows the user to obtain localized weather and marine forecasts. The application simulates the current GPS position of a fishing boat near the Port of Lomé by generating slightly different latitude and longitude values around the real location. These coordinates are then sent to the Open-Meteo Weather API and the Open-Meteo Marine API. The program retrieves atmospheric variables such as temperature, precipitation probability, visibility, and wind speed, together with marine variables including wave height, wave direction, ocean current velocity, and ocean current direction. These values are combined into a single timeline and displayed in a formatted forecast table. Each forecast is also classified into one of three navigation safety levels: SAFE, CAUTION, or DANGER, depending on the forecasted wind speed, wave height, and visibility.

The second option provides biological and regulatory information for commonly exploited fish species in Togo. Currently, the application contains information for Sardinella and Anchovy. For each species, the application displays the scientific name, minimum legal size, exploitation status, and a simple management recommendation. If the requested species is not available in the local database, the user can voluntarily contribute new information. These contributions are saved in a JSON file called **User_contribution.json**, allowing the database to be expanded over time.

The third option implements an SOS emergency system. When a fisher is in danger, the application generates an emergency report containing the fisher identification code, the simulated GPS coordinates, and a Google Maps link pointing to the reported location. The information is saved inside **sos_repository.json**, which represents a simplified emergency repository that could be accessed by rescue teams or a shore command center. Before saving the alert, the application validates the latitude and longitude values to ensure they are geographically valid.

The fourth option reads all emergency reports stored inside the SOS repository and displays them in a structured format. If no emergency alerts are available, the application simply informs the user that there are currently no active incidents.

The project contains several custom functions, each responsible for one specific task. The **simulate_gps()** function generates realistic fishing positions around Lomé. The **get_combined_marine_forecast()** function downloads and combines weather and marine forecasts from the Open-Meteo services. The **calculate_safety_flag()** function evaluates navigation conditions according to predefined safety thresholds. The **get_species_advice()** function retrieves fisheries information or records new user contributions. The **trigger_sos()** function creates emergency reports, while **read_shore_alerts()** safely reads all stored SOS reports from the JSON repository.

The project also includes automated tests written with pytest. The tests verify the navigation safety classification, the fish species information database, the SOS alert generation process, the emergency repository reader, GPS coordinate simulation, and the validation of invalid geographic coordinates. Internet-dependent functions were intentionally not tested because they rely on external services whose availability cannot be guaranteed during automated grading.

Several design decisions were made during development. I chose JSON files instead of a database because they are lightweight, human-readable, and perfectly adequate for a small command-line application. I also decided to separate weather retrieval, safety evaluation, fish regulations, and SOS management into independent functions. This modular design makes the program easier to maintain, understand, and test.

Although this application is only a prototype, it demonstrates how Python can be used to integrate APIs, file handling, data validation, and automated testing into a practical tool that addresses real-world challenges faced by artisanal fishers. In the future, I would like to transform this project into a mobile application with real GPS integration, offline capabilities, multilingual support, and direct communication with national fisheries and maritime safety authorities.
