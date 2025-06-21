# Social Planning & User Needs

This document describes the social features and user relationships for the Sailor Utility application. The core concept revolves around boat owners, their crew, and event organizers.

## Core Concepts

-   **Boat Owners** can invite users to a "crew pool" for their boat(s).
-   **Roles** are specific to a boat and defined by the owner (e.g., Helm, Foredeck, Pit, or custom roles like "Tactician").
-   **Role-Based Instructions:** Owners can attach documents, pictures, and notes to each role, providing specific instructions for crew members based on their assignment for a given trip or event.

### Example Scenario

> Captain Matt owns the boat "Conundrum". He needs to manage his crew for various events.
>
> -   **Crew Roster & Skills:**
>     -   **Kelly:** Qualified for Foredeck, Headsail.
>     -   **Adam:** Qualified for Helm, Pit.
>     -   **Dugan:** Qualified for Pit, Helm, Headsail.
>     -   **Ben:** Qualified for Headsail, but has limited availability.
>     -   **Mike:** Qualified for Pit, but not available on weekends.
>     -   **Emery:** A new sailor learning the Foredeck role.
>
> -   **Training Needs:** Matt has created boat-specific instructions for each role (Pit, Headsail, Tactician) on "Conundrum". Emery needs access to the Foredeck documentation to prepare.

---

## Statement of Needs by Persona

### As a Captain

-   I need to find available and qualified crew for upcoming races based on the specific positions I need to fill. I need a clear view of my roster and their availability to identify gaps.
-   I need to train new crew members by providing them with my boat-specific documentation for their assigned role.
-   I need the ability to define standard and custom roles for my boat.
-   I need to link specific equipment (e.g., spinnaker pole, anchor windlass) to the roles that use them, so crew members automatically get the correct manuals and instructions.
-   I need to plan for events where I know the crew I need, but also be able to see who is generally available when I'm planning a casual trip.
-   I need to manage different crew requirements for different events (e.g., a full crew for a race vs. a smaller crew for a day sail).
-   I need to be able to contact my crew, either the entire pool or just the crew for a specific trip.

### As a Crew Member

-   I need to keep track of the nuances of different boats and captains, as the same position can have different procedures on each boat.
- When I'm assigned a role for a trip, I want to see not just the role instructions but also the documentation for the specific equipment I'll be using.
-   I need to manage my availability and indicate which boats I'm willing to crew on so captains can find me.
-   I need to be able to find and register for upcoming events, especially those hosted by captains I enjoy sailing with.
-   I may have my own boat for casual sailing but act as a crew member on other boats for races, so I need to manage both roles within the app.
-   I want some privacy controls over my event history, while still allowing my experience (badges, general accomplishments) to be visible to potential captains.

### As a Captain or Crew Member (The Sailor's Resume)

-   I want the system to automatically build a "sailing resume" for me based on the trips and events I participate in.
-   This resume should display key statistics:
    -   Total nautical miles sailed
    -   Total hours on the water
    -   Number of races competed in
    -   A breakdown of time spent in each role (e.g., 40 hours as Helm, 60 hours as Foredeck)
-   I want to view my own resume to track my progress and have a shareable record of my experience.
-   As a Captain, I want to view the resumes of potential crew members to make informed decisions.
-   As a Captain, I want to find available crew based on their bio and general experience (e.g., total number of races).
-   Even if I own a boat, I want to build my own crew resume for when I sail on other people's boats.

### As an Organizer

-   I want to create an "organization" of captains, boats, and crew members.
-   I want to create events that invited users within my organization can register for.
-   I need the ability to create recurring events or event templates for the same groups of invitees.
-   I need communication tools to contact different segments of my organization:
    -   All captains.
    -   All crew members.
    -   Everyone in the organization.
    -   Only members who haven't signed up for a specific event to encourage participation.