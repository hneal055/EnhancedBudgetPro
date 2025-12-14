from typing import Dict, Any, List


class TalentAvailabilityEngine:
    """
    Builds a character x shoot_day availability grid and detects hard-block conflicts.

    schedule: either
      - {"daily_schedule": [ {shoot_day, scene, characters, daily_burn}, ... ]}
      - [ {shoot_day, scene, characters, daily_burn}, ... ]

    overrides:
      {
        "CHARACTER": {
          day_int: "available"|"partial"|"unavailable"
        }
      }
    """

    def analyze(
        self,
        schedule: Any,
        overrides: Dict[str, Dict[int, str]],
    ) -> Dict[str, Any]:
        # Normalize schedule
        if isinstance(schedule, dict):
            daily = schedule.get("daily_schedule", []) or []
        elif isinstance(schedule, list):
            daily = schedule
        else:
            daily = []

        # Determine all characters + days present
        all_chars = set()
        all_days = set()

        for d in daily:
            day = d.get("shoot_day")
            chars = d.get("characters", [])
            if day is None:
                continue
            all_days.add(day)
            for c in chars:
                all_chars.add(c)

        # Build base availability grid
        availability_grid: Dict[str, Dict[int, str]] = {}

        for char in sorted(all_chars):
            availability_grid[char] = {}
            for day in sorted(all_days):
                availability_grid[char][day] = "available"  # scheduled day baseline

        # Apply overrides and detect conflicts
        conflicts: List[Dict[str, Any]] = []

        for d in daily:
            day = d.get("shoot_day")
            scene = d.get("scene", "")
            chars = d.get("characters", [])

            for c in chars:
                # Apply override if present
                override_status = overrides.get(c, {}).get(day)
                if override_status:
                    availability_grid.setdefault(c, {})[day] = override_status

                    if override_status == "unavailable":
                        conflicts.append(
                            {
                                "character": c,
                                "shoot_day": day,
                                "scene": scene,
                                "status": override_status,
                            }
                        )

        return {
            "availability_grid": availability_grid,
            "conflicts": conflicts,
        }

