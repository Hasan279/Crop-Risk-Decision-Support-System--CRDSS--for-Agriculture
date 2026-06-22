# **Software Requirements Specification (SRS)**

## **Project: Crop Risk Decision Support System (CRDSS) for Pakistani Farmers**

### **1\. Introduction**

**1.1 Purpose**

The purpose of this document is to define the software requirements for the Crop Risk Decision Support System (CRDSS). This system provides location-specific, probabilistic risk forecasts (frost, heat stress, heavy rain) mapped to specific crop growth stages to aid Pakistani farmers in agricultural decision-making.

**1.2 Scope**

The system will ingest 15-20 years of historical daily weather data for 4-5 key agricultural hubs in Pakistan. It will output calibrated risk probabilities using empirical distributions adjusted for recent climate trends. The final product will be a user-facing Streamlit web application. Out of scope: Live IoT sensor integration, real-time yield prediction, and financial/market price forecasting.

**1.3 Definitions and Acronyms**

* **CRDSS:** Crop Risk Decision Support System.  
* **Target Events:** Specific weather thresholds causing crop damage (e.g., Consecutive days \> 35°C).  
* **PARC:** Pakistan Agricultural Research Council (Source of agronomic thresholds).  
* **DOY:** Day of Year (1-365).

### **2\. Overall Description**

**2.1 User Characteristics**

* **Primary Persona (Target):** Agronomists, extension workers, or literate farmers in Pakistan seeking data-backed planting/harvesting windows.  
* **Secondary Persona (Actual Evaluator):** Hiring managers and Data Science recruiters evaluating the project for end-to-end machine learning product lifecycle skills.

**2.2 Operating Environment**

* **Backend/Data Processing:** Python 3.10+, Pandas, NumPy, Scikit-learn/Statsmodels.  
* **Frontend/UI:** Streamlit Community Cloud.  
* **Data Source:** Open-Meteo Historical Archive API.

**2.3 Design and Implementation Constraints**

* **Time Constraint:** Must be completed within a strict 5-week summer timeframe.  
* **Infrastructure Constraint:** Must run entirely within the memory and compute limits of the free tier of Streamlit Community Cloud.  
* **Algorithmic Constraint:** A single unified probabilistic method must be used across all risk types to maintain scope.

### **3\. Functional Requirements**

**3.1 Data Ingestion Module**

* **FR-1.1:** The system shall fetch daily minimum temperature, maximum temperature, and precipitation sum data for the past 15-20 years.  
* **FR-1.2:** The system shall support 4-5 predefined coordinates representing Multan, Hyderabad, Peshawar, Quetta, and Gilgit.  
* **FR-1.3:** The system shall consolidate raw data into a master dataframe with location identifiers.

**3.2 Target Engineering Module**

* **FR-2.1:** The system shall calculate the "last spring frost date" per location per year.  
* **FR-2.2:** The system shall identify "heat-stress events" defined by sustained consecutive days above a location/crop-specific threshold.  
* **FR-2.3:** The system shall identify "heavy-rain events" defined by a 3-day rolling precipitation sum exceeding a specific threshold.

**3.3 Probabilistic Forecasting Engine**

* **FR-3.1:** The system shall calculate the probability of a risk event occurring after a given DOY for a specific location.  
* **FR-3.2:** The model shall utilize an empirical distribution approach with a trend-adjustment penalty/weighting to account for climate shifts over the last 5-10 years.

**3.4 Agronomic Logic Engine**

* **FR-4.1:** The system shall store a knowledge base of crop sensitivities (e.g., Wheat, Rice, Cotton) mapping growth stages to specific weather thresholds.  
* **FR-4.2:** Given user inputs (Location, Crop, Decision/Growth Stage, Date), the system shall evaluate the generated probabilistic forecast against the agronomic knowledge base.  
* **FR-4.3:** The system shall output plain-English recommendations (e.g., "High risk of heat stress during flowering if planted on \[Date\]. Consider delaying by 2 weeks.").

**3.5 User Interface (Streamlit)**

* **FR-5.1:** The UI shall provide dropdown selectors for Location, Crop, and Decision Type, and a date picker.  
* **FR-5.2:** The UI shall display a clear textual summary of the risk (e.g., "20% risk of frost").  
* **FR-5.3:** The UI shall render an interactive visual chart plotting the risk probability curve over the coming weeks.

### **4\. Non-Functional Requirements**

**4.1 Performance & Responsiveness**

* **NFR-1.1:** The UI must reflect updated forecasts and charts within 3 seconds of a user changing an input parameter. (Requires aggressive caching of the historical dataset and model inferences via @st.cache\_data).

**4.2 Reliability & Calibration**

* **NFR-2.1:** The risk forecasts must undergo a 5-year holdout backtest.  
* **NFR-2.2:** The system shall generate a calibration report indicating the reliability of its probability scores (e.g., events predicted at 20% probability actually occurred \~20% of the time).

**4.3 Usability**

* **NFR-3.1:** The application must be usable by an individual with no data science background. Visualizations must include clear axes, legends, and plain-English tooltips.

### **5\. Appendices: Validation & Deployment**

* **Milestone 1 (Week 1):** Master dataset and target variables cleanly engineered and plotted.  
* **Milestone 2 (Week 2):** Probabilistic model generating calibrated curves for all 3 risk types.  
* **Milestone 3 (Week 3):** Agronomic rules hard-coded and passing manual test cases.  
* **Milestone 4 (Week 4):** Streamlit UI wired and styled.  
* **Milestone 5 (Week 5):** Backtesting complete, metrics documented, application deployed to Streamlit Cloud, and README finalized.