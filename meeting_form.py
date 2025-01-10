import streamlit as st
from datetime import datetime, timedelta
from calendar_source import OutlookCalendar

def convert_duration_to_minutes(duration_str):
    """Convert duration string to minutes"""
    return int(duration_str.split()[0])

def create_calendar_event(form_data):
    """Create calendar event from form data"""
    # Convert date and time to datetime
    start_time = datetime.combine(form_data['date'], form_data['time'])
    
    # Calculate end time based on duration
    duration_minutes = convert_duration_to_minutes(form_data['duration'])
    end_time = start_time + timedelta(minutes=duration_minutes)
    
    # Prepare meeting details
    meeting_info = {
        'subject': f"Coffee Chat with {form_data['name']}: {form_data['subject']}",
        'start_time': start_time,
        'end_time': end_time,
        'attendees': [form_data['email']],
        'description': f"""Coffee Chat with {form_data['name']}
Topic: {form_data['subject']}
Duration: {form_data['duration']}""",
        'is_online': True,  # You can make this configurable if needed
        'location': "Microsoft Teams"  # You can make this configurable if needed
    }
    
    # Create the calendar event
    calendar = OutlookCalendar()
    try:
        new_meeting = calendar.create_meeting(meeting_info)
        return True, "Meeting scheduled successfully!"
    except Exception as e:
        return False, f"Error scheduling meeting: {str(e)}"

def insert_meeting_form():
    with st.form(key="coffee_chat_form"):
        name = st.text_input("Name", value="")
        subject = st.text_input("Subject", value="Pickleball")
        date = st.date_input("Date", value=datetime.now().date())
        time = st.time_input("Time", value=datetime.now().time())
        duration = st.selectbox("Duration", options=["15 minutes", "30 minutes", "45 minutes", "60 minutes"], index=1)
        email = st.text_input("Email", value="")
    
        if st.form_submit_button("Schedule Chat"):
            # This code runs when the form is submitted
            st.subheader("Data Submitted:")
            st.write(f"Name: {name}")
            st.write(f"Subject: {subject}")
            st.write(f"Date: {date}")
            st.write(f"Time: {time}")
            st.write(f"Duration: {duration}")
            st.write(f"Email: {email}")

            form_data = {
                'name': name,
                'subject': subject,
                'date': date,
                'time': time,
                'duration': duration,
                'email': email
            }

            success, message = create_calendar_event(form_data)

            if success:
                st.success(message)
                # You might want to show the scheduled time in a user-friendly format
                start_time = datetime.combine(date, time)
                end_time = start_time + timedelta(minutes=convert_duration_to_minutes(duration))
                st.write(f"Meeting scheduled for {start_time.strftime('%B %d, %Y at %I:%M %p')} - "
                        f"{end_time.strftime('%I:%M %p')}")
            else:
                st.error(message)