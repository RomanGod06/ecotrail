# api/agents/tools/trip_planner.py
import logging

logger = logging.getLogger(__name__)

def estimate_trip_cost_and_footprint(
    destination: str,
    distance_km: float,
    transport_mode: str, 
    days: int,
    accommodation: str, 
    diet: str, 
    trek_km: float
) -> str:
    """
    Calculates predicted trip costs and carbon footprint.
    Args:
        destination: Where they are going.
        distance_km: Estimated one-way distance in km.
        transport_mode: 'flight', 'car', or 'bus'
        days: Number of days.
        accommodation: 'hotel' or 'tent'
        diet: 'meat', 'veg', or 'local'
        trek_km: Estimated trekking distance.
    """
    try:
        # --- 1. COST PREDICTION LOGIC (Estimated ₹ INR) ---
        transport_cost = 0
        if transport_mode == 'flight': transport_cost = distance_km * 6 * 2 # Round trip
        elif transport_mode == 'car': transport_cost = distance_km * 12 * 2
        else: transport_cost = distance_km * 2 * 2 # Bus/Train

        stay_cost = (days * 2500) if accommodation == 'hotel' else (days * 800)
        
        food_cost = 0
        if diet == 'meat': food_cost = days * 800
        elif diet == 'veg': food_cost = days * 500
        else: food_cost = days * 300
        
        activity_cost = trek_km * 50 # Guide/Permit fees
        
        total_cost = transport_cost + stay_cost + food_cost + activity_cost

        # --- 2. CARBON FOOTPRINT LOGIC (kg CO2e) ---
        transport_co2 = 0
        if transport_mode == 'flight': transport_co2 = distance_km * 0.12 * 2
        elif transport_mode == 'car': transport_co2 = distance_km * 0.2 * 2
        else: transport_co2 = distance_km * 0.05 * 2

        stay_co2 = (days * 5) if accommodation == 'hotel' else (days * 2.5)
        
        food_co2 = 0
        if diet == 'meat': food_co2 = days * 40.5
        elif diet == 'veg': food_co2 = days * 3
        else: food_co2 = days * 2.25
        
        activity_co2 = trek_km * 0.1
        
        total_co2 = transport_co2 + stay_co2 + food_co2 + activity_co2
        trees_needed = round(total_co2 / 21) # 21kg per tree

        # --- 3. FORMAT THE REPORT FOR GEMINI ---
        report = (
            f"TRIP_ANALYSIS FOR {destination.upper()}:\n"
            f"- Estimated Distance: {distance_km} km (One-way)\n"
            f"- PREDICTED BUDGET: ₹{total_cost:,.2f} INR (Transport: ₹{transport_cost}, Stay: ₹{stay_cost}, Food: ₹{food_cost})\n"
            f"- CARBON FOOTPRINT: {total_co2:.1f} kg CO2e\n"
            f"- OFFSET GOAL: User needs to plant {trees_needed} trees to offset this trip.\n"
            f"INSTRUCTION: Present this data elegantly using markdown tables or bullet points."
        )
        
        logger.info(f"✅ Trip Planned: {destination} | ₹{total_cost} | {total_co2}kg CO2e")
        return report

    except Exception as e:
        logger.error(f"🔥 Trip Planner Error: {str(e)}")
        return "Error calculating trip logistics. Please specify standard modes of transport and accommodation."