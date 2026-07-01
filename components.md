Here is a detailed breakdown of the UI design, layout, styling, and content of the "Crop Risk DSS" application, specifically organized to help you recreate it in Figma:

### 🎨 1. Global Design System & Tokens
**Typography:**
*   **Primary Font:** `DM Sans` (Weights: 400, 500, 600, 700)
*   **Secondary Font:** `Noto Nastaliq Urdu` (For Urdu translation support)
*   **Base Text Color:** `--ink` (#111827)

**Color Palette:**
*   `--forest`: `#1a4731` (Dark green, used for the sidebar background)
*   `--fern`: `#2d6a4f` (Medium green, used for accents & badges)
*   `--sage`: `#52b788` (Light green, used for card highlights)
*   `--mist`: `#f0f7f4` (Very light green, used for tab strip backgrounds)
*   `--soil`: `#3d2b1f` (Dark brown)
*   `--sand`: `#f5f0eb` (Off-white)
*   `--ink`: `#111827` (Almost black, primary text)
*   `--slate`: `#4b5563` (Dark gray, secondary text)
*   `--smoke`: `#9ca3af` (Medium gray, labels and disclaimers)
*   `--surface`: `#ffffff` (White, card backgrounds)
*   `--page`: `#f4f7f5` (Light grayish-green, main page background)
*   `--border`: `#e4ede8` (Light border color)
*   `--red`: `#c0392b`
*   `--amber`: `#b45309`

**Shadows & Radii:**
*   **Border Radius (`--radius`):** `14px` for main cards and elements.
*   **Shadows:** Soft, modern shadows with slight vertical offset and blur (e.g., `0 1px 3px rgba(17,24,39,0.06)` for small shadows, slightly larger on hover).

---

### 📱 2. General Layout Structure
The page uses a standard dashboard layout consisting of a **Left Sidebar** and a **Main Content Area**.
*   **Max-Width of Main Content:** `1160px` (centered).

---

### 🗄️ 3. Sidebar (Left Panel)
*   **Background Color:** `--forest` (`#1a4731`).
*   **Text Colors:** Light muted greens (`#d1e8dc`, `#e8f5ee`).

**Elements (Top to Bottom):**
1.  **Language Toggle:** Radio buttons for "🌐 Language / زبان" (English / اردو).
2.  **Header:** "⚗️ Options" (Styled as an `h2`).
3.  **Divider Line:** Faint transparent white line.
4.  **Dropdown 1:** "Select City"
5.  **Dropdown 2:** "Select Crop"
6.  **Date Picker:** "Planting Date"
7.  **Dropdown 3:** "Check Next (Days)" (Options: 15, 30, 45, 60, 90).
    *   *Input Field Styling:* Dark semi-transparent backgrounds (`rgba(255,255,255,0.08)`), rounded corners (`8px`), and a faint border.
8.  **Divider Line**
9.  **Info Alert Box:** "💡 **Tip:** Change the options above to see past weather risks for your crop."
    *   *Box Styling:* Semi-transparent background, `10px` border radius, lighter green text.

---

### 📄 4. Main Content Area (Right Panel)
**Background Color:** `--page` (`#f4f7f5`).

#### **Header Section**
*   **Main Title:** "🌾 Past Weather Risks"
    *   *Styling:* `2.1rem`, Bold (`700`), `--ink` color.
*   **Status Pill (Next to title):** "DSS"
    *   *Styling:* Small (`0.7rem`), uppercase, `--fern` background (`#2d6a4f`), white text, fully rounded (`99px` radius).
*   **Subtitle:** "See the chance of bad weather for your crop over the year."
    *   *Styling:* `1rem`, regular weight, `--slate` color.

#### **Section 1: Current Selection (KPI Cards)**
*   **Section Label:** "CURRENT SELECTION" (Small `0.7rem`, uppercase, bold, `--fern` color, with a horizontal line trailing to the right).
*   **Grid:** 3 columns.
*   **KPI Cards (x3):**
    *   *Content:*
        1. City (e.g., "Faisalabad")
        2. Crop (e.g., "Wheat")
        3. Days Checked (e.g., "30 Days")
    *   *Card Styling:* White (`--surface`) background, `--border` outline, `14px` border radius, soft drop shadow.
    *   *Accent:* A `4px` vertical `--sage` (`#52b788`) colored bar on the far left inner edge of the card.
    *   *Typography:* Labels are uppercase, small, and `--smoke` colored. Values are large (`1.65rem`), bold, and `--ink` colored.
    *   *Hover Effect:* Card lifts slightly up and shadow increases.

#### **Section 2: Farming Advice**
*   **Section Label:** "FARMING ADVICE"
*   **Dynamic Insight Card:** A wide banner card that changes based on the data. It has three states. All states share a layout: A circular icon on the left (`58x58px`, white background, soft shadow) and title/text on the right.
    *   *State 1 (Optimal/Good):* Background gradient (light greens `#f0fdf5` to `#dcfce7`), `5px` thick left border (`#22c55e`). Icon: "✅". Title: "Good Time to Plant" (dark green text).
    *   *State 2 (Warning/High Risk):* Background gradient (light reds `#fff5f5` to `#fee2e2`), `5px` thick left border (`#ef4444`). Icon: "🚨". Title: "High Weather Risk Detected" (dark red text).
    *   *State 3 (Medium Risk):* Background gradient (light yellows `#fffbeb` to `#fef3c7`), `5px` thick left border (`#f59e0b`). Icon: "⚠️". Title: "Medium Weather Risk" (dark brown text).
*   **Disclaimer Text:** Placed right below the card, right-aligned, small italic font (`0.78rem`), `--smoke` color, with a top border above it. Text: "*Disclaimer: This advice is based purely on historical weather probabilities and should not substitute professional agronomic consultation.*"

#### **Section 3: Detailed Analysis (Tabs & Charts)**
*   **Section Label:** "DETAILED ANALYSIS"
*   **Tabs UI:**
    *   *Container:* `--mist` background, `10px` border radius, `4px` padding.
    *   *Inactive Tabs:* Transparent background, `--slate` color text.
    *   *Active Tab:* White background, `--ink` text, soft shadow, bold font.
    *   *Tab Names:* "🎯 Risk Distribution", "📅 Yearly Trend", "🌱 Crop Lifecycle".
*   **Tab 1 Content (Risk Distribution):**
    *   A **Radar/Spider Chart** titled "Risk Exposure (Next X Days)".
    *   Displays vertices for "Frost", "Heat Stress", and "Heavy Rain".
    *   Polygon fill is `--fern` with 15% opacity (`rgba(45, 106, 79, 0.15)`); the outline is solid `--fern`.
*   **Tab 2 Content (Yearly Trend):**
    *   A **Line Chart (Spline/Curved)** titled "Weather Risk Chances".
    *   X-Axis: Day of the Year. Y-Axis: Chance of Bad Weather (Percentages).
    *   Three lines (Frost: Blue `#3b82f6`, Heat Stress: Red `#ef4444`, Heavy Rain: Green `#10b981`).
    *   Lines have a soft gradient fill to zero underneath them (opacity 8%).
    *   A vertical dashed grey line marks the "Planting Date".
    *   A small range-slider is at the bottom of the X-axis for zooming.
*   **Tab 3 Content (Crop Lifecycle):**
    *   A **Gantt Chart (Timeline)** titled "Crop Growth Timeline".
    *   Y-Axis lists crop growth stages (e.g., Vegetative, Flowering & Grain Filling, Maturity).
    *   X-Axis is dates.
    *   Horizontal bars denote the duration of each stage, color-coded based on the primary risk for that stage (Blue, Red, or Green matching the line chart colors).
