from calendar_source import OutlookCalendar
from datetime import datetime, timedelta


# Initialize calendar
calendar = OutlookCalendar()

# # Get events for next week
# events = calendar.get_calendar_events()
# print("Upcoming events:", events)

# # Create a new event
# start_time = datetime.now() + timedelta(days=1)  # tomorrow
# end_time = start_time + timedelta(hours=1)       # 1 hour duration
# new_event = calendar.create_event(
#     "Test Meeting",
#     start_time,
#     end_time,
#     "This is a test meeting"
# )
# print("Created event:", new_event)



# Check availability for tomorrow
tomorrow = datetime.now().date() + timedelta(days=1)
available_slots = calendar.check_availability(tomorrow, duration_minutes=30)
print("\nAvailable 30-minute slots tomorrow:")
for slot in available_slots:
    print(f"From {slot['start'].strftime('%I:%M %p')} to {slot['end'].strftime('%I:%M %p')}")