class AvailabilityReschedulerEngine:
    """
    Automatically rebuilds a shooting schedule based on talent availability.
    Preserves original scene order as much as possible.
    """

    def optimize(self, original_schedule, availability_grid):
        optimized = []
        day_cursor = 1

        for entry in original_schedule:
            scene = entry["scene"]
            characters = entry["characters"]
            daily_burn = entry["daily_burn"]

            # ✅ Find earliest valid day for all required characters
            valid_day = None
            while valid_day is None:
                conflicts = False
                for char in characters:
                    status = availability_grid.get(char, {}).get(day_cursor, "available")
                    if status == "unavailable":
                        conflicts = True
                        break

                if conflicts:
                    day_cursor += 1
                else:
                    valid_day = day_cursor

            optimized.append({
                "shoot_day": valid_day,
                "scene": scene,
                "characters": characters,
                "daily_burn": daily_burn
            })

            day_cursor += 1

        return {
            "daily_schedule": optimized,
            "total_days": len(optimized)
        }
