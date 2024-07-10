# PRóxico

PRóxico (`proxico.py`) is an application designed to analyze and visualize data from the Toxics Release Inventory (TRI) Program for Puerto Rico (PR).

## Features

The primary goal of PRóxico is to allow users to explore toxic emissions data in Puerto Rico in a visual and interactive manner. Key features include:

- **Year Selection**: Users can select the year for which they want to view data.
- **Physical Location**: Users are required to input their physical address (street, town, zipcode) to focus the visualization on their area of residence.
- **Data Visualization**: The application presents charts and tables displaying relevant information on toxic emissions in Puerto Rico.

## Components

### Bubble Map

- Displays factories by municipalities, focusing on the user's town of residence.
- Shows the total pounds of toxic substance emissions in and outside the user's town.
- Identifies whether the factory is under federal jurisdiction and its industrial sector.
- Points and colors correspond to the total emissions in the town of residence.

### Pie Chart

- Presents the total percentage of toxic substance emissions by emission category in the user's town of residence.

### Table

- Details information about factories in the user's town of residence.
- Indicates the type of chemical released, whether it is a metal or non-metal, whether it is carcinogenic, and its classification:
  - TRI = General EPCRA Section 313 Chemical
  - PBT = Persistent Bioaccumulative and Toxic
  - DIOXIN = Dioxin or Dioxin-like compound.
- Shows the amount of the chemical emitted.

### Choropleth Map

- Displays the total toxic substance emissions in each municipality of Puerto Rico.

### Bar Chart

- Presents the top 5 factories in Puerto Rico with the highest total toxic substance emissions.

## Future Enhancements

- **Exact Location**: Consider the exact address of the user to obtain longitude and latitude, allowing for more specific visualization of nearby factories.
- **Health Impact**: Evaluate how emissions of toxic substances could affect the health of nearby residents, considering their proximity to factories.
- **Water Body Contamination**: Analyze if nearby water bodies are being contaminated by the released substances.

## Additional Notes

Currently, the application focuses on providing island-wide information and details about factories that release toxic substances in the user's town of residence. Future versions are expected to continue improving and expanding its functionalities.
