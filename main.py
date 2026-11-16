import csv
from pathlib import Path
from datetime import datetime
from collections import defaultdict


class StudyTracker:

    def __init__(self):
        self.file_path = Path("study_sessions.csv")
        self.sessions = []
        self.load_sessions()

    # Create the CSV file if it does not exist
    def create_file(self):
        if not self.file_path.exists():
            with open(self.file_path, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=["id", "subject", "topic", "date", "minutes", "notes"]
                )
                writer.writeheader()

    # Load saved sessions from CSV
    def load_sessions(self):
        self.create_file()

        try:
            with open(self.file_path, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                self.sessions = list(reader)

        except (OSError, csv.Error) as error:
            print(f"Error loading data: {error}")
            self.sessions = []

    # Save sessions to CSV
    def save_sessions(self):
        try:
            with open(self.file_path, "w", newline="", encoding="utf-8") as file:
                fieldnames = ["id", "subject", "topic", "date", "minutes", "notes"]

                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.sessions)

        except (OSError, csv.Error) as error:
            print(f"Error saving data: {error}")

    # Add a new study session
    def add_session(self):
        print("\n--- Add New Study Session ---")

        subject = input("Subject: ").strip()
        topic = input("Topic: ").strip()

        if not subject or not topic:
            print("Subject and topic cannot be empty.")
            return

        date_text = input("Date (YYYY-MM-DD), press Enter for today: ").strip()

        if not date_text:
            date_text = datetime.today().strftime("%Y-%m-%d")

        try:
            datetime.strptime(date_text, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format.")
            return

        try:
            minutes = int(input("Study duration (minutes): "))

            if minutes <= 0:
                print("Duration must be greater than zero.")
                return

        except ValueError:
            print("Please enter a valid number.")
            return

        notes = input("Notes (optional): ").strip()

        if self.sessions:
            new_id = max(int(session["id"]) for session in self.sessions) + 1
        else:
            new_id = 1

        session = {
            "id": str(new_id),
            "subject": subject,
            "topic": topic,
            "date": date_text,
            "minutes": str(minutes),
            "notes": notes
        }

        self.sessions.append(session)
        self.save_sessions()

        print("\nStudy session added successfully!")

    # Display all study sessions
    def show_sessions(self):
        print("\n--- All Study Sessions ---")

        if not self.sessions:
            print("No study sessions found.")
            return

        for session in self.sessions:
            print("-" * 45)
            print(f"ID: {session['id']}")
            print(f"Subject: {session['subject']}")
            print(f"Topic: {session['topic']}")
            print(f"Date: {session['date']}")
            print(f"Duration: {session['minutes']} minutes")
            print(f"Notes: {session['notes']}")

        print("-" * 45)

    # Search sessions by subject
    def search_sessions(self):
        print("\n--- Search Study Sessions ---")

        keyword = input("Enter subject name: ").strip().casefold()

        results = [
            session for session in self.sessions
            if keyword in session["subject"].casefold()
        ]

        if not results:
            print("No matching sessions found.")
            return
        for session in results:
            print(
                f"ID: {session['id']} | "
                f"Subject: {session['subject']} | "
                f"Topic: {session['topic']} | "
                f"Duration: {session['minutes']} minutes"
            )

    # Delete a study session
    def delete_session(self):
        print("\n--- Delete Study Session ---")

        session_id = input("Enter session ID: ").strip()

        for session in self.sessions:
            if session["id"] == session_id:
                self.sessions.remove(session)
                self.save_sessions()
                print("Session deleted successfully!")
                return

        print("Session ID not found.")

    # Calculate and display study statistics
    def show_statistics(self):
        print("\n--- Study Statistics ---")

        if not self.sessions:
            print("No data available for statistics.")
            return

        total_minutes = sum(
            int(session["minutes"]) for session in self.sessions
        )

        total_sessions = len(self.sessions)

        average_minutes = total_minutes / total_sessions

        subject_minutes = defaultdict(int)

        for session in self.sessions:
            subject = session["subject"]
            minutes = int(session["minutes"])
            subject_minutes[subject] += minutes

        print(f"\nTotal sessions: {total_sessions}")
        print(f"Total study time: {total_minutes // 60} hours "
              f"and {total_minutes % 60} minutes")
        print(f"Average session: {average_minutes:.1f} minutes")

        print("\n--- Study Time by Subject ---")

        for subject, minutes in sorted(subject_minutes.items()):
            print(f"{subject}: {minutes} minutes ({minutes / 60:.1f} hours)")

    # Main menu
    def run(self):

        while True:
            print("\n========== STUDY TRACK ==========")
            print("1. Add Study Session")
            print("2. Show All Sessions")
            print("3. Search Sessions")
            print("4. Delete Session")
            print("5. Show Statistics")
            print("6. Exit")
            print("================================")

            choice = input("Choose an option (1-6): ").strip()

            if choice == "1":
                self.add_session()

            elif choice == "2":
                self.show_sessions()

            elif choice == "3":
                self.search_sessions()

            elif choice == "4":
                self.delete_session()

            elif choice == "5":
                self.show_statistics()

            elif choice == "6":
                print("Thank you for using StudyTrack!")
                break

            else:
                print("Invalid choice. Please select 1 to 6.")


if __name__ == "__main__":
    app = StudyTracker()
    app.run()