from typing import Dict, Any, List


class TalentAvailabilityEngine:
    """
    Builds a character x shoot_day availability grid and detects conflicts.

    schedule: either
      - {"daily_schedule": [ {shoot_day, scene, characters, daily_burn}, ... ]}
      - [ {shoot_day, scene, characters, daily_burn}, ... ]

    overrides:
      {
        "CHARACTER": {
          day_int: "available"|"partial"|"unavailable"
        }
      }

    Status meanings:
    - "scheduled": Character is scheduled to work this day
    - "not_required": Character not needed this day
    - "available": Override - character available
    - "partial": Override - character partially available
    - "unavailable": Override - character blocked
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
        char_day_map: Dict[str, set] = {}

        for d in daily:
            day = d.get("shoot_day")
            chars = d.get("characters", [])
            if day is None:
                continue
            all_days.add(day)
            for c in chars:
                all_chars.add(c)
                char_day_map.setdefault(c, set()).add(day)

        # Build base availability grid - only scheduled days
        availability_grid: Dict[str, Dict[int, str]] = {}

        for char in sorted(all_chars):
            availability_grid[char] = {}
            scheduled_days = char_day_map.get(char, set())
            
            for day in sorted(all_days):
                if day in scheduled_days:
                    # Character is scheduled this day
                    availability_grid[char][day] = "scheduled"
                else:
                    # Character not required this day
                    availability_grid[char][day] = "not_required"

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
                    availability_grid[c][day] = override_status

                    # Conflict if character is scheduled but unavailable
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
