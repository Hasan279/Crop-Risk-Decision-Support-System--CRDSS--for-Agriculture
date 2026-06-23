import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

CROP_KNOWLEDGE_BASE = {
    "Wheat": {
        "Vegetative": {"start_day": 0, "end_day": 90, "risk": "frost", "threshold": 0.20},
        "Flowering & Grain Filling": {"start_day": 90, "end_day": 130, "risk": "heat_stress", "threshold": 0.30},
        "Maturity & Harvest": {"start_day": 130, "end_day": 150, "risk": "heavy_rain", "threshold": 0.30}
    },
    "Cotton": {
        "Vegetative": {"start_day": 0, "end_day": 60, "risk": "heat_stress", "threshold": 0.50},
        "Flowering & Boll Formation": {"start_day": 60, "end_day": 120, "risk": "heavy_rain", "threshold": 0.30}
    },
    "Rice": {
        "Vegetative": {"start_day": 0, "end_day": 60, "risk": "heat_stress", "threshold": 0.50},
        "Flowering & Heading": {"start_day": 60, "end_day": 100, "risk": "heat_stress", "threshold": 0.30},
        "Maturity & Harvest": {"start_day": 100, "end_day": 130, "risk": "heavy_rain", "threshold": 0.35}
    },
    "Sugarcane": {
        "Germination & Tillering": {"start_day": 0, "end_day": 120, "risk": "frost", "threshold": 0.25},
        "Grand Growth": {"start_day": 120, "end_day": 270, "risk": "heat_stress", "threshold": 0.50}
    },
    "Maize": {
        "Vegetative": {"start_day": 0, "end_day": 50, "risk": "frost", "threshold": 0.20},
        "Silking & Tasseling": {"start_day": 50, "end_day": 80, "risk": "heat_stress", "threshold": 0.30},
        "Maturity": {"start_day": 80, "end_day": 110, "risk": "heavy_rain", "threshold": 0.30}
    }
}

class AgronomicRulesEngine:
    def __init__(self):
        current_dir = Path(__file__).resolve().parent
        data_path = current_dir.parent / "data" / "processed" / "risk_probabilities.csv"
        
        try:
            self.df = pd.read_csv(data_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"Could not find {data_path}. Did you run probabilistic_model.py first?")
            
    def _get_probability(self, city, doy, risk_type, window_days):
        subset = self.df[
            (self.df['city_name'] == city) &
            (self.df['DOY'] == doy) &
            (self.df['risk_type'] == risk_type) &
            (self.df['window_days'] == window_days)
        ]
        if not subset.empty:
            return subset.iloc[0]['probability']
        return 0.0

    def generate_recommendation(self, city, crop, plant_date_str, window_days=30, lang="en"):
        if lang == "ur":
            err_crop = f"غلطی: فصل '{crop}' ڈیٹا بیس میں موجود نہیں ہے۔"
            err_date = "غلطی: تاریخ کا فارمیٹ درست نہیں۔ براہ کرم 'MM-DD' استعمال کریں۔"
        else:
            err_crop = f"Error: Crop '{crop}' not found in the Knowledge Base."
            err_date = "Error: Invalid date format. Please use 'MM-DD' (e.g., '11-15')."

        if crop not in CROP_KNOWLEDGE_BASE:
            return err_crop
            
        try:
            plant_date = datetime.strptime(f"2023-{plant_date_str}", "%Y-%m-%d")
        except ValueError:
            return err_date

        warnings = []
        crop_rules = CROP_KNOWLEDGE_BASE[crop]
        
        ur_risks = {"frost": "کورے", "heat stress": "گرمی کی شدت", "heavy rain": "شدید بارش"}
        ur_crops = {"Wheat": "گندم", "Cotton": "کپاس", "Rice": "چاول", "Sugarcane": "گنا", "Maize": "مکئی"}
        ur_cities = {"Dera Ghazi Khan": "ڈیرہ غازی خان", "Faisalabad": "فیصل آباد", "Hafizabad": "حافظ آباد", "Okara": "اوکاڑہ", "Sanghar": "سانگھڑ"}
        ur_stages = {
            "Vegetative": "نشوونما",
            "Flowering & Grain Filling": "پھول اور دانے بننے کا عمل",
            "Maturity & Harvest": "پکنا اور کٹائی",
            "Flowering & Boll Formation": "پھول اور ٹینڈے بننے کا عمل",
            "Flowering & Heading": "پھول اور خوشے بننے کا عمل",
            "Germination & Tillering": "اگاؤ اور شگوفے نکلنا",
            "Grand Growth": "تیز نشوونما",
            "Silking & Tasseling": "سِلکنگ اور ٹیسلنگ",
            "Maturity": "پکائی"
        }
        ur_months = {
            "January": "جنوری", "February": "فروری", "March": "مارچ", "April": "اپریل",
            "May": "مئی", "June": "جون", "July": "جولائی", "August": "اگست",
            "September": "ستمبر", "October": "اکتوبر", "November": "نومبر", "December": "دسمبر"
        }
        
        for stage_name, rules in crop_rules.items():
            stage_start_date = plant_date + timedelta(days=rules['start_day'])
            stage_start_doy = stage_start_date.timetuple().tm_yday
            
            risk_type = rules['risk']
            threshold = rules['threshold']
            
            prob = self._get_probability(city, stage_start_doy, risk_type, window_days)
            
            if prob >= threshold:
                risk_pct = int(prob * 100)
                formatted_risk = risk_type.replace('_', ' ')
                date_str = stage_start_date.strftime('%B %d')
                
                if lang == "ur":
                    ur_risk_name = ur_risks.get(formatted_risk, formatted_risk)
                    ur_crop_name = ur_crops.get(crop, crop)
                    ur_stage_name = ur_stages.get(stage_name, stage_name)
                    month_en = stage_start_date.strftime('%B')
                    ur_date_str = date_str.replace(month_en, ur_months.get(month_en, month_en))
                    
                    warnings.append(
                        f"• مرحلہ {ur_stage_name}: آپ کی فصل {ur_crop_name} تقریباً {ur_date_str} کو اس مرحلے میں داخل ہوگی۔ "
                        f"انتباہ: اس دوران {ur_risk_name} کا {risk_pct}% خطرہ ہے۔ یہ بہت زیادہ ہے!"
                    )
                else:
                    warnings.append(
                        f"• {stage_name} Stage: Around {date_str}, your {crop} will be in this stage. "
                        f"Warning: There is a {risk_pct}% chance of {formatted_risk}. This is dangerously high!"
                    )
                
        if not warnings:
            if lang == "ur":
                ur_crop_name = ur_crops.get(crop, crop)
                ur_city_name = ur_cities.get(city, city)
                return f"موسم سازگار ہے: پچھلے {window_days} دنوں کے ریکارڈ کے مطابق، {ur_city_name} میں {plant_date_str} کو {ur_crop_name} کاشت کرنا محفوظ ہے۔"
            return f"Good Weather: Looking at past data for {window_days} days, it looks safe to plant {crop} in {city} on {plant_date_str}."
        else:
            if lang == "ur":
                return "موسمیاتی انتباہ:\n" + "\n".join(warnings) + "\n\nمشورہ: خراب موسم سے بچنے کے لیے اپنی فصل کی کاشت کی تاریخ تبدیل کرنے پر غور کریں۔"
            return "Weather Warning:\n" + "\n".join(warnings) + "\n\nAdvice: Please think about changing your planting date to avoid bad weather."

if __name__ == "__main__":
    engine = AgronomicRulesEngine()
    
    print("--- Test Case 1: Wheat in Hafizabad (Winter Planting) ---")
    print(engine.generate_recommendation(city="Hafizabad", crop="Wheat", plant_date_str="11-15", window_days=30))
    print("\n")
    
    print("--- Test Case 2: Cotton in Sanghar (Late Spring Planting) ---")
    print(engine.generate_recommendation(city="Sanghar", crop="Cotton", plant_date_str="05-15", window_days=30))
    print("\n")
    
    print("--- Test Case 3: Rice in Faisalabad (Summer Planting) ---")
    print(engine.generate_recommendation(city="Faisalabad", crop="Rice", plant_date_str="06-01", window_days=30))
    print("\n")
    
    print("--- Test Case 4: Optimal Scenario (Safe Planting) ---")
    print(engine.generate_recommendation(city="Dera Ghazi Khan", crop="Sugarcane", plant_date_str="02-15", window_days=30))
    print("\n")
