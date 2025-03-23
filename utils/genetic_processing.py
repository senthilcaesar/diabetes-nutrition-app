"""
Genetic data processing module for the Diabetes Nutrition Plan application.
Contains functions for processing genetic data and generating nutrition insights.
"""

"""
Genetic data processing module for the Diabetes Nutrition Plan application.
Contains functions for processing genetic data and generating nutrition insights.
"""

import json
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Any

# Define key genetic markers related to diabetes and metabolism
# Make this a module-level variable so it can be imported
DIABETES_GENETIC_MARKERS = {
    # Carbohydrate metabolism
    "TCF7L2": {
        "rs7903146": {
            "C/C": {"risk": "low", "carb_sensitivity": "normal"},
            "C/T": {"risk": "increased", "carb_sensitivity": "higher"},
            "T/T": {"risk": "high", "carb_sensitivity": "high"}
        }
    },
    "PPARG": {
        "rs1801282": {
            "C/C": {"risk": "baseline", "insulin_sensitivity": "normal"},
            "C/G": {"risk": "reduced", "insulin_sensitivity": "improved"},
            "G/G": {"risk": "reduced", "insulin_sensitivity": "significantly improved"}
        }
    },
    # Fat metabolism
    "APOA2": {
        "rs5082": {
            "C/C": {"saturated_fat_sensitivity": "high"},
            "C/T": {"saturated_fat_sensitivity": "moderate"},
            "T/T": {"saturated_fat_sensitivity": "normal"}
        }
    },
    "FTO": {
        "rs9939609": {
            "T/T": {"risk": "normal", "satiety_response": "normal"},
            "A/T": {"risk": "increased", "satiety_response": "reduced"},
            "A/A": {"risk": "high", "satiety_response": "significantly reduced"}
        }
    },
    # Vitamin metabolism
    "MTHFR": {
        "rs1801133": {
            "C/C": {"folate_processing": "normal"},
            "C/T": {"folate_processing": "reduced"},
            "T/T": {"folate_processing": "significantly reduced"}
        }
    },
    # Caffeine metabolism
    "CYP1A2": {
        "rs762551": {
            "A/A": {"caffeine_metabolism": "fast"},
            "A/C": {"caffeine_metabolism": "slow"},
            "C/C": {"caffeine_metabolism": "very slow"}
        }
    },
    # Inflammation response
    "IL6": {
        "rs1800795": {
            "G/G": {"inflammatory_response": "elevated"},
            "G/C": {"inflammatory_response": "moderate"},
            "C/C": {"inflammatory_response": "normal"}
        }
    }
}

def load_genetic_data(file_path: str) -> Dict:
    """
    Load genetic data from a file (supports 23andMe, Ancestry, and VCF formats).
    
    Args:
        file_path (str): Path to the genetic data file
        
    Returns:
        Dict: Dictionary containing the processed genetic data
    """
    try:
        if file_path.endswith('.txt'):
            # Assuming 23andMe or Ancestry format
            return _process_23andme_or_ancestry(file_path)
        elif file_path.endswith('.vcf'):
            # VCF format
            return _process_vcf(file_path)
        elif file_path.endswith('.json'):
            # Our own JSON format
            with open(file_path, 'r') as f:
                return json.load(f)
        else:
            raise ValueError(f"Unsupported file format: {file_path}")
    except Exception as e:
        print(f"Error loading genetic data: {e}")
        return {}

def _process_23andme_or_ancestry(file_path: str) -> Dict:
    """
    Process genetic data in 23andMe or Ancestry format.
    
    Args:
        file_path (str): Path to the genetic data file
        
    Returns:
        Dict: Dictionary containing the processed genetic data
    """
    data = {}
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue
            parts = line.strip().split()
            if len(parts) >= 4:
                rsid = parts[0]
                genotype = parts[3]
                data[rsid] = genotype
    return data

def _process_vcf(file_path: str) -> Dict:
    """
    Process genetic data in VCF format.
    
    Args:
        file_path (str): Path to the genetic data file
        
    Returns:
        Dict: Dictionary containing the processed genetic data
    """
    data = {}
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue
            parts = line.strip().split()
            if len(parts) >= 10:
                info = parts[7]
                if 'RS=' in info:
                    rsid = 'rs' + info.split('RS=')[1].split(';')[0]
                    genotype = parts[9].split(':')[0].replace('|', '/')
                    if genotype in ['0/0', '0/1', '1/1']:
                        alleles = [parts[3], parts[4]]
                        if genotype == '0/0':
                            data[rsid] = alleles[0] + '/' + alleles[0]
                        elif genotype == '0/1':
                            data[rsid] = alleles[0] + '/' + alleles[1]
                        elif genotype == '1/1':
                            data[rsid] = alleles[1] + '/' + alleles[1]
    return data

def analyze_carb_metabolism(genetic_data: Dict) -> Dict:
    """
    Analyze genetic markers related to carbohydrate metabolism.
    
    Args:
        genetic_data (Dict): Dictionary containing genetic data
        
    Returns:
        Dict: Carbohydrate metabolism insights
    """
    insights = {
        "carb_sensitivity": "normal",
        "explanation": "",
        "recommendations": []
    }
    
    # Check TCF7L2 gene
    tcf7l2_marker = "rs7903146"
    if tcf7l2_marker in genetic_data:
        genotype = genetic_data[tcf7l2_marker]
        if genotype in DIABETES_GENETIC_MARKERS["TCF7L2"][tcf7l2_marker]:
            marker_data = DIABETES_GENETIC_MARKERS["TCF7L2"][tcf7l2_marker][genotype]
            insights["carb_sensitivity"] = marker_data["carb_sensitivity"]
            
            if marker_data["carb_sensitivity"] == "high":
                insights["explanation"] = "Your TCF7L2 gene variant indicates you may have a higher sensitivity to carbohydrates, affecting your glucose response."
                insights["recommendations"] = [
                    "Focus on complex carbohydrates with lower glycemic index",
                    "Reduce portion sizes of carbohydrate-rich foods",
                    "Pair carbohydrates with protein and healthy fats to slow absorption",
                    "Consider a lower carbohydrate dietary approach"
                ]
            elif marker_data["carb_sensitivity"] == "higher":
                insights["explanation"] = "Your TCF7L2 gene variant suggests a moderately increased sensitivity to carbohydrates."
                insights["recommendations"] = [
                    "Be mindful of carbohydrate quality and quantity",
                    "Focus on whole food sources of carbohydrates",
                    "Monitor your glucose response to high-carb meals"
                ]
    
    # Check PPARG gene for insulin sensitivity
    pparg_marker = "rs1801282"
    if pparg_marker in genetic_data:
        genotype = genetic_data[pparg_marker]
        if genotype in DIABETES_GENETIC_MARKERS["PPARG"][pparg_marker]:
            marker_data = DIABETES_GENETIC_MARKERS["PPARG"][pparg_marker][genotype]
            
            if marker_data["insulin_sensitivity"] == "improved":
                insights["explanation"] += " Your PPARG gene variant suggests potentially improved insulin sensitivity."
                insights["recommendations"].append("Omega-3 fatty acids may be particularly beneficial for your metabolism")
            elif marker_data["insulin_sensitivity"] == "significantly improved":
                insights["explanation"] += " Your PPARG gene variant suggests significantly improved insulin sensitivity."
                insights["recommendations"].append("Your body may respond particularly well to monounsaturated fats")
    
    return insights

def analyze_fat_metabolism(genetic_data: Dict) -> Dict:
    """
    Analyze genetic markers related to fat metabolism.
    
    Args:
        genetic_data (Dict): Dictionary containing genetic data
        
    Returns:
        Dict: Fat metabolism insights
    """
    insights = {
        "saturated_fat_sensitivity": "normal",
        "explanation": "",
        "recommendations": []
    }
    
    # Check APOA2 gene
    apoa2_marker = "rs5082"
    if apoa2_marker in genetic_data:
        genotype = genetic_data[apoa2_marker]
        if genotype in DIABETES_GENETIC_MARKERS["APOA2"][apoa2_marker]:
            insights["saturated_fat_sensitivity"] = DIABETES_GENETIC_MARKERS["APOA2"][apoa2_marker][genotype]["saturated_fat_sensitivity"]
            
            if insights["saturated_fat_sensitivity"] == "high":
                insights["explanation"] = "Your APOA2 gene variant indicates a higher sensitivity to saturated fats."
                insights["recommendations"] = [
                    "Limit saturated fat intake to less than 7% of daily calories",
                    "Choose lean proteins and low-fat dairy options",
                    "Use olive oil, avocado, and nuts as primary fat sources"
                ]
            elif insights["saturated_fat_sensitivity"] == "moderate":
                insights["explanation"] = "Your APOA2 gene variant suggests moderate sensitivity to saturated fats."
                insights["recommendations"] = [
                    "Be mindful of saturated fat intake",
                    "Focus on unsaturated fat sources like olive oil, avocados, and nuts"
                ]
    
    # Check FTO gene for satiety response
    fto_marker = "rs9939609"
    if fto_marker in genetic_data:
        genotype = genetic_data[fto_marker]
        if genotype in DIABETES_GENETIC_MARKERS["FTO"][fto_marker]:
            marker_data = DIABETES_GENETIC_MARKERS["FTO"][fto_marker][genotype]
            
            if marker_data["satiety_response"] == "reduced":
                insights["explanation"] += " Your FTO gene variant suggests you may have a reduced feeling of fullness after meals."
                insights["recommendations"].extend([
                    "Include more protein and fiber in meals to enhance satiety",
                    "Practice mindful eating techniques",
                    "Consider smaller, more frequent meals"
                ])
            elif marker_data["satiety_response"] == "significantly reduced":
                insights["explanation"] += " Your FTO gene variant suggests a significantly reduced satiety response."
                insights["recommendations"].extend([
                    "Prioritize protein at every meal",
                    "Include high-fiber foods with each meal and snack",
                    "Monitor portion sizes carefully"
                ])
    
    return insights

def analyze_vitamin_metabolism(genetic_data: Dict) -> Dict:
    """
    Analyze genetic markers related to vitamin metabolism.
    
    Args:
        genetic_data (Dict): Dictionary containing genetic data
        
    Returns:
        Dict: Vitamin metabolism insights
    """
    insights = {
        "folate_processing": "normal",
        "explanation": "",
        "recommendations": []
    }
    
    # Check MTHFR gene
    mthfr_marker = "rs1801133"
    if mthfr_marker in genetic_data:
        genotype = genetic_data[mthfr_marker]
        if genotype in DIABETES_GENETIC_MARKERS["MTHFR"][mthfr_marker]:
            insights["folate_processing"] = DIABETES_GENETIC_MARKERS["MTHFR"][mthfr_marker][genotype]["folate_processing"]
            
            if insights["folate_processing"] == "reduced":
                insights["explanation"] = "Your MTHFR gene variant indicates reduced ability to process certain forms of folate."
                insights["recommendations"] = [
                    "Emphasize leafy greens and other folate-rich foods",
                    "Consider methylated forms of B vitamins if supplementing",
                    "Include folate-rich foods like leafy greens, beans, and lentils regularly"
                ]
            elif insights["folate_processing"] == "significantly reduced":
                insights["explanation"] = "Your MTHFR gene variant indicates a significantly reduced ability to process certain forms of folate."
                insights["recommendations"] = [
                    "Prioritize methylfolate-containing foods in your diet",
                    "Discuss specific B-vitamin supplementation with your healthcare provider",
                    "Emphasize a diet rich in various B vitamins from whole foods"
                ]
    
    return insights

def analyze_inflammation_response(genetic_data: Dict) -> Dict:
    """
    Analyze genetic markers related to inflammation response.
    
    Args:
        genetic_data (Dict): Dictionary containing genetic data
        
    Returns:
        Dict: Inflammation response insights
    """
    insights = {
        "inflammatory_response": "normal",
        "explanation": "",
        "recommendations": []
    }
    
    # Check IL6 gene
    il6_marker = "rs1800795"
    if il6_marker in genetic_data:
        genotype = genetic_data[il6_marker]
        if genotype in DIABETES_GENETIC_MARKERS["IL6"][il6_marker]:
            insights["inflammatory_response"] = DIABETES_GENETIC_MARKERS["IL6"][il6_marker][genotype]["inflammatory_response"]
            
            if insights["inflammatory_response"] == "elevated":
                insights["explanation"] = "Your IL6 gene variant indicates a tendency toward elevated inflammatory responses."
                insights["recommendations"] = [
                    "Emphasize anti-inflammatory foods in your diet (fatty fish, turmeric, berries)",
                    "Limit processed foods and refined carbohydrates",
                    "Include omega-3 rich foods regularly",
                    "Consider ways to manage stress, which can exacerbate inflammation"
                ]
            elif insights["inflammatory_response"] == "moderate":
                insights["explanation"] = "Your IL6 gene variant suggests a moderately increased inflammatory response."
                insights["recommendations"] = [
                    "Include anti-inflammatory foods regularly",
                    "Be mindful of processed food intake",
                    "Consider the impact of stress on your metabolic health"
                ]
    
    return insights

def analyze_caffeine_metabolism(genetic_data: Dict) -> Dict:
    """
    Analyze genetic markers related to caffeine metabolism.
    
    Args:
        genetic_data (Dict): Dictionary containing genetic data
        
    Returns:
        Dict: Caffeine metabolism insights
    """
    insights = {
        "caffeine_metabolism": "normal",
        "explanation": "",
        "recommendations": []
    }
    
    # Check CYP1A2 gene
    cyp1a2_marker = "rs762551"
    if cyp1a2_marker in genetic_data:
        genotype = genetic_data[cyp1a2_marker]
        if genotype in DIABETES_GENETIC_MARKERS["CYP1A2"][cyp1a2_marker]:
            insights["caffeine_metabolism"] = DIABETES_GENETIC_MARKERS["CYP1A2"][cyp1a2_marker][genotype]["caffeine_metabolism"]
            
            if insights["caffeine_metabolism"] == "slow":
                insights["explanation"] = "Your CYP1A2 gene variant indicates you metabolize caffeine at a slower rate."
                insights["recommendations"] = [
                    "Limit caffeine consumption, especially in the afternoon",
                    "Be aware that caffeine may have a stronger and longer-lasting effect on your blood glucose",
                    "Consider testing how different caffeinated beverages affect your glucose levels"
                ]
            elif insights["caffeine_metabolism"] == "very slow":
                insights["explanation"] = "Your CYP1A2 gene variant indicates you metabolize caffeine at a very slow rate."
                insights["recommendations"] = [
                    "Significantly limit caffeine intake",
                    "Avoid caffeine after morning hours",
                    "Be aware that even small amounts of caffeine may impact your sleep and glucose levels"
                ]
            elif insights["caffeine_metabolism"] == "fast":
                insights["explanation"] = "Your CYP1A2 gene variant indicates you metabolize caffeine quickly."
                insights["recommendations"] = [
                    "Moderate caffeine consumption may be metabolized efficiently by your body",
                    "Still monitor your personal response to caffeine, as individual responses vary"
                ]
    
    return insights

def generate_genetic_nutrition_profile(genetic_data: Dict) -> Dict:
    """
    Generate a comprehensive nutrition profile based on genetic data.
    
    Args:
        genetic_data (Dict): Dictionary containing genetic data
        
    Returns:
        Dict: Comprehensive genetic nutrition profile
    """
    profile = {
        "carb_metabolism": analyze_carb_metabolism(genetic_data),
        "fat_metabolism": analyze_fat_metabolism(genetic_data),
        "vitamin_metabolism": analyze_vitamin_metabolism(genetic_data),
        "inflammation_response": analyze_inflammation_response(genetic_data),
        "caffeine_metabolism": analyze_caffeine_metabolism(genetic_data),
        "overall_summary": "",
        "key_recommendations": []
    }
    
    # Generate overall summary based on all insights
    insights_list = []
    if profile["carb_metabolism"]["carb_sensitivity"] != "normal":
        insights_list.append(f"higher sensitivity to carbohydrates ({profile['carb_metabolism']['carb_sensitivity']})")
        
    if profile["fat_metabolism"]["saturated_fat_sensitivity"] != "normal":
        insights_list.append(f"{profile['fat_metabolism']['saturated_fat_sensitivity']} sensitivity to saturated fats")
        
    if profile["vitamin_metabolism"]["folate_processing"] != "normal":
        insights_list.append(f"{profile['vitamin_metabolism']['folate_processing']} folate processing ability")
        
    if profile["inflammation_response"]["inflammatory_response"] != "normal":
        insights_list.append(f"{profile['inflammation_response']['inflammatory_response']} inflammatory response")
        
    if profile["caffeine_metabolism"]["caffeine_metabolism"] != "normal":
        insights_list.append(f"{profile['caffeine_metabolism']['caffeine_metabolism']} caffeine metabolism")
    
    if insights_list:
        profile["overall_summary"] = f"Your genetic profile indicates {', '.join(insights_list[:-1])}{' and ' if len(insights_list) > 1 else ''}{insights_list[-1] if insights_list else ''}."
    else:
        profile["overall_summary"] = "Based on the genetic markers analyzed, your metabolism appears to follow typical patterns without significant variations that would require specific dietary adjustments."
    
    # Compile key recommendations
    all_recommendations = []
    for category in ["carb_metabolism", "fat_metabolism", "vitamin_metabolism", "inflammation_response", "caffeine_metabolism"]:
        all_recommendations.extend(profile[category]["recommendations"])
    
    # Remove duplicates and select top recommendations
    profile["key_recommendations"] = list(dict.fromkeys(all_recommendations))[:5]
    
    return profile

def create_sample_genetic_data() -> Dict:
    """
    Create sample genetic data for demonstration purposes.
    
    Returns:
        Dict: Sample genetic data
    """
    return {
        "rs7903146": "C/T",  # TCF7L2 - moderate carb sensitivity
        "rs1801282": "C/G",  # PPARG - improved insulin sensitivity
        "rs5082": "C/T",     # APOA2 - moderate saturated fat sensitivity
        "rs9939609": "A/T",  # FTO - reduced satiety response
        "rs1801133": "C/T",  # MTHFR - reduced folate processing
        "rs762551": "A/C",   # CYP1A2 - slow caffeine metabolism
        "rs1800795": "G/C"   # IL6 - moderate inflammatory response
    }