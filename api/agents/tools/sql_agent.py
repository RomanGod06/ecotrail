import logging
from django.db.models import Avg, Sum

logger = logging.getLogger(__name__)

def check_room_availability(location_name: str) -> str:
    """Analyzes aggregate hotel capacity to determine exact crowd density."""
    from api.models import HotelRoom 

    try:
        clean_name = location_name.lower().replace("in ", "").replace("at ", "").strip()
        logger.info(f"👥 [SQL AGENT] Calculating true crowds for: {clean_name}")

        rooms = HotelRoom.objects.filter(location__icontains=clean_name)
        
        if not rooms.exists():
            return f"No live capacity data found for '{clean_name}'."

        # 1. The True Math: Sum up all hotels in the area
        stats = rooms.aggregate(
            total_capacity=Sum('total_rooms'),
            total_available=Sum('available_rooms'),
            avg_price=Avg('price')
        )
        print(f"📡 SUPABASE RESPONDED: {stats}")
        total_capacity = stats['total_capacity'] or 0
        total_available = stats['total_available'] or 0
        avg_price = stats['avg_price'] or 0
        
        # 2. Calculate Exact Crowd Percentage
        booked_rooms = total_capacity - total_available
        occupancy_rate = (booked_rooms / total_capacity) * 100 if total_capacity > 0 else 0
        
        # 3. Crowd Status Logic
        if occupancy_rate >= 85:
            crowd_status = "Overcrowded 🔴"
            advice = "Expect severe trail congestion and packed campsites."
        elif occupancy_rate >= 50:
            crowd_status = "Moderate Crowd 🟡"
            advice = "Standard seasonal footfall. Manageable but busy."
        else:
            crowd_status = "Peaceful 🟢"
            advice = "Excellent time to visit. Very few people on the trail."

        return (
            f"CROWD_REPORT for {clean_name.title()}:\n"
            f"- Status: {crowd_status}\n"
            f"- Area Occupancy: {occupancy_rate:.1f}%\n"
            f"- Rooms Left: {total_available} out of {total_capacity} total area capacity.\n"
            f"- Current Avg Price: ₹{avg_price:.2f}\n"
            f"- Advice: {advice}"
        )

    except Exception as e:
        logger.error(f"🔥 SQL Agent Error: {str(e)}")
        return "Database Error: Could not calculate aggregate crowds."