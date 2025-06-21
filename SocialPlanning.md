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

---

## Technical Implementation Plan

### Integration with Existing Sailor Utility Architecture

This social module will be built as **Phase 4.5** of the Sailor Utility development plan, integrating seamlessly with the existing modular architecture.

### Database Schema Implementation

#### New Tables Required (8 tables)

**Organizations & Membership:**
```sql
Organizations: id, name, description, created_by, is_active, created_at, updated_at
Organization_Members: id, organization_id, user_id, role, joined_at, is_active
```

**Crew Pool System:**
```sql
Crew_Pool_Invitations: id, boat_id, invited_user_id, invited_by, status, invited_at, responded_at, message
Boat_Roles: id, boat_id, role_name, description, is_custom, created_by, created_at, updated_at
```

**Role & Equipment Integration:**
```sql
Role_Instructions: id, boat_role_id, title, content, attachment_path, attachment_type, created_by, created_at, updated_at
Equipment_Role_Links: id, equipment_id, boat_role_id, usage_notes, is_primary, created_at
```

**Experience & Availability:**
```sql
Sailing_Experience_Log: id, user_id, trip_id, event_id, role, hours, nautical_miles, experience_type, notes, created_at
User_Availability: id, user_id, start_date, end_date, availability_type, recurring, recurring_pattern, notes, created_at, updated_at
```

#### Enhanced Existing Tables
- **Events:** Add `organization_id` for organization-scoped events
- **Trip_Participants:** Add `boat_role_id` for role-specific trip assignments
- **Boat_Crew:** Add `boat_role_id` for linking crew to specific boat roles

### API Architecture (25 New Endpoints)

#### Organization Management (8 endpoints)
- Full CRUD operations for organizations
- Member management and role assignment
- Organization-scoped event creation

#### Crew Pool Operations (4 endpoints)
- Invitation system with acceptance/decline workflow
- Crew pool visibility and management
- Integration with boat ownership permissions

#### Role & Instruction System (10 endpoints)
- Boat-specific role definition and customization
- Role instruction management with file attachments
- Equipment-to-role linking system

#### Experience & Resume (3 endpoints)
- Automatic experience logging from trips/events
- Public and private resume display
- Manual experience entry for external activities

### Frontend Module Structure

```
src/modules/social/
├── components/
│   ├── SocialDashboard.jsx           # Main social hub with quick stats
│   ├── organizations/
│   │   ├── OrganizationsList.jsx     # List all user's organizations
│   │   ├── OrganizationForm.jsx      # Create/edit organization
│   │   ├── OrganizationDetail.jsx    # Organization details & events
│   │   └── MemberManagement.jsx      # Add/remove members, assign roles
│   ├── crew-pool/
│   │   ├── CrewPoolDashboard.jsx     # Overview of all crew pools user is in
│   │   ├── CrewInvitations.jsx       # Manage incoming/outgoing invitations
│   │   ├── AvailabilityManager.jsx   # Set availability periods
│   │   └── CrewSearch.jsx            # Find and invite new crew members
│   ├── roles/
│   │   ├── RoleManager.jsx           # Define boat-specific roles
│   │   ├── RoleInstructions.jsx      # Attach instructions to roles
│   │   └── EquipmentRoleLinks.jsx    # Link equipment to roles
│   └── resume/
│       ├── SailingResume.jsx         # Display user's sailing resume
│       ├── ExperienceLogger.jsx      # Manual experience entry
│       └── PublicProfile.jsx         # Public-facing resume view
├── services/
│   ├── socialApi.js                  # Main social API service
│   ├── organizationsApi.js           # Organization-specific calls
│   ├── crewPoolApi.js               # Crew pool management
│   └── resumeApi.js                 # Experience and resume APIs
├── hooks/
│   ├── useSocial.js                 # Main social data hook
│   ├── useOrganizations.js          # Organization management
│   ├── useCrewPool.js               # Crew pool operations
│   └── useSailingResume.js          # Resume and experience data
└── utils/
    └── socialUtils.js               # Social utility functions
```

### Cross-Module Integration Points

#### Enhanced Boats Module
- **Crew Pool Tab:** Manage invited crew members for each boat
- **Roles Management:** Define boat-specific roles (Helm, Foredeck, Pit, custom roles)
- **Role Instructions:** Attach documentation, photos, and notes to each role
- **Equipment Integration:** Link boat equipment to specific roles

#### Enhanced Trips Module
- **Crew Selection:** Choose crew from boat's crew pool
- **Role Assignment:** Assign specific roles to trip participants
- **Automatic Experience Logging:** Log hours and miles for each participant's role
- **Role-Specific Preparation:** Show role instructions to crew before trips

#### Enhanced Equipment Module
- **Role Assignment:** Assign equipment to boat-specific roles
- **Role-Based Instructions:** Attach usage instructions specific to each role
- **Automatic Documentation:** Show relevant equipment manuals based on assigned trip role

#### Enhanced Events Module
- **Organization Events:** Create events scoped to specific organizations
- **Crew Recruitment:** Recruit crew from organization members
- **Role-Based Registration:** Register for events with specific role preferences

#### Enhanced User Profile
- **Sailing Resume:** Prominent display of automatically-generated sailing resume
- **Availability Calendar:** Integrated availability management
- **Crew Pool Memberships:** Overview of all boats user crews on
- **Privacy Controls:** Granular settings for profile and experience visibility

### Implementation Workflow

1. **Database Migration:** Create new tables and enhance existing ones
2. **Backend API Development:** Implement 25 new social endpoints
3. **Frontend Components:** Build modular social interface components
4. **Cross-Module Integration:** Enhance existing modules with social features
5. **Testing & Validation:** Comprehensive testing of social workflows

### Data Flow Architecture

**Automatic Experience Logging:**
- Trip completion → Experience log entry (hours, miles, role)
- Event participation → Experience log entry (competition type, role)
- Resume calculation → Aggregate experience by role and type

**Crew Pool Workflow:**
- Captain invites sailor → Invitation record created
- Sailor accepts → Added to boat's crew pool
- Trip planning → Captain selects crew from pool
- Role assignment → Trip participant linked to boat role
- Trip completion → Experience automatically logged

**Role-Based Instruction System:**
- Captain defines boat roles → Boat_Roles records
- Captain attaches instructions → Role_Instructions records
- Captain links equipment → Equipment_Role_Links records
- Crew assignment → Sailor gets role-specific instructions and equipment manuals

### Privacy & Security Considerations

- **Experience Visibility:** Users control which experience is public vs. private
- **Organization Privacy:** Organizations can be public or invite-only
- **Crew Pool Access:** Only boat owners can manage their crew pools
- **Role Instructions:** Only crew pool members see boat-specific instructions
- **Data Ownership:** Users own their experience data and can export/delete

This technical implementation transforms the individual boat management system into a comprehensive social sailing community platform while maintaining the existing modular architecture and user experience patterns.