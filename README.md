# Crop Risk Decision Support System (CRDSS) for Farmers

The Crop Risk Decision Support System (CRDSS) is a tool designed to help farmers analyze historical weather data and predict crop risks such as Frost, Heat Stress, and Heavy Rain for the top agricultural regions in Pakistan.

## Project Structure
- `docs/`: Contains the Software Requirements Specification (SRS) and project planning documentation.
- `week1/`: Contains initial scripts for weather data ingestion and target engineering (e.g., historical data fetching using Open-Meteo).

## Targeted Crops & Locations
The system analyzes weather risks for 5 primary agricultural crops and regions in Pakistan:

| Crop | Location (District/City) | Province | Latitude | Longitude |
| :--- | :--- | :--- | :--- | :--- |
| **Wheat** | Dera Ghazi Khan | Punjab | 30.03° N | 70.64° E |
| **Cotton** | Sanghar | Sindh | 26.04° N | 68.95° E |
| **Rice** | Hafizabad | Punjab | 32.07° N | 73.69° E |
| **Sugarcane** | Faisalabad | Punjab | 31.42° N | 73.09° E |
| **Maize** | Okara | Punjab | 30.81° N | 73.45° E |

## Data
Historical weather data spans 21 years (2005 - 2026) for these five locations. Data files are excluded from version control to keep the repository lightweight.
