def test_manual_schedule_update():
    scenes = [
        {"scene_id": 1, "heading": "INT. OFFICE"},
        {"scene_id": 2, "heading": "EXT. PARK"},
        {"scene_id": 3, "heading": "INT. HOUSE"},
    ]
    edited_days = {1: 2, 2: 1, 3: 2}
    # Simulate manual schedule update logic
    new_daily_schedule = []
    for day_num in range(1, 3):
        scenes_for_day = [scene for scene in scenes if edited_days[scene["scene_id"]] == day_num]
        new_daily_schedule.append({"day": day_num, "scenes": scenes_for_day})
    assert new_daily_schedule[0]["scenes"][0]["scene_id"] == 2
    assert new_daily_schedule[1]["scenes"][0]["scene_id"] == 1
    assert new_daily_schedule[1]["scenes"][1]["scene_id"] == 3
    print("Manual stripboard schedule update test passed.")

if __name__ == "__main__":
    test_manual_schedule_update()
