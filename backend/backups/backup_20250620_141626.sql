--
-- PostgreSQL database dump
--

-- Dumped from database version 13.21 (Raspbian 13.21-0+deb11u1)
-- Dumped by pg_dump version 13.21 (Raspbian 13.21-0+deb11u1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: boats; Type: TABLE; Schema: public; Owner: pi_user
--

CREATE TABLE public.boats (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    boat_type character varying(50),
    length_feet double precision,
    beam_feet double precision,
    draft_feet double precision,
    displacement_lbs integer,
    year_built integer,
    hull_material character varying(50),
    registration_number character varying(50),
    hin character varying(20),
    documentation_number character varying(20),
    owner_id integer NOT NULL,
    home_port character varying(100),
    current_location character varying(100),
    marina_berth character varying(50),
    insurance_company character varying(100),
    insurance_policy_number character varying(50),
    insurance_expiry date,
    engine_make character varying(50),
    engine_model character varying(50),
    engine_year integer,
    engine_hours double precision,
    fuel_capacity_gallons double precision,
    water_capacity_gallons double precision,
    sail_area_sqft double precision,
    mast_height_feet double precision,
    keel_type character varying(50),
    is_active boolean,
    condition character varying(20),
    last_survey_date date,
    next_survey_due date,
    notes text,
    photos text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.boats OWNER TO pi_user;

--
-- Name: boats_id_seq; Type: SEQUENCE; Schema: public; Owner: pi_user
--

CREATE SEQUENCE public.boats_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.boats_id_seq OWNER TO pi_user;

--
-- Name: boats_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pi_user
--

ALTER SEQUENCE public.boats_id_seq OWNED BY public.boats.id;


--
-- Name: equipment; Type: TABLE; Schema: public; Owner: pi_user
--

CREATE TABLE public.equipment (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    category character varying(50),
    subcategory character varying(50),
    brand character varying(50),
    model character varying(100),
    part_number character varying(50),
    serial_number character varying(100),
    purchase_date date,
    purchase_price numeric(10,2),
    purchase_location character varying(100),
    warranty_period_months integer,
    warranty_expiry date,
    owner_id integer NOT NULL,
    boat_id integer,
    location_on_boat character varying(100),
    current_location character varying(100),
    condition character varying(20),
    is_operational boolean,
    last_inspection_date date,
    next_inspection_due date,
    specifications text,
    quantity integer,
    weight_lbs double precision,
    dimensions character varying(100),
    manual_url character varying(255),
    photos text,
    documents text,
    notes text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.equipment OWNER TO pi_user;

--
-- Name: equipment_id_seq; Type: SEQUENCE; Schema: public; Owner: pi_user
--

CREATE SEQUENCE public.equipment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.equipment_id_seq OWNER TO pi_user;

--
-- Name: equipment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pi_user
--

ALTER SEQUENCE public.equipment_id_seq OWNED BY public.equipment.id;


--
-- Name: events; Type: TABLE; Schema: public; Owner: pi_user
--

CREATE TABLE public.events (
    id integer NOT NULL,
    name character varying(200) NOT NULL,
    event_type character varying(50),
    description text,
    location character varying(200),
    venue character varying(100),
    start_date timestamp without time zone NOT NULL,
    end_date timestamp without time zone,
    all_day boolean,
    timezone character varying(50),
    organizer character varying(100),
    organizer_contact character varying(200),
    website character varying(255),
    registration_required boolean,
    registration_deadline timestamp without time zone,
    registration_fee numeric(10,2),
    max_participants integer,
    current_participants integer,
    boat_requirements text,
    skill_level_required character varying(50),
    age_restrictions character varying(100),
    weather_dependent boolean,
    backup_date timestamp without time zone,
    prizes text,
    notes text,
    status character varying(20),
    is_public boolean,
    created_by integer NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.events OWNER TO pi_user;

--
-- Name: events_id_seq; Type: SEQUENCE; Schema: public; Owner: pi_user
--

CREATE SEQUENCE public.events_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.events_id_seq OWNER TO pi_user;

--
-- Name: events_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pi_user
--

ALTER SEQUENCE public.events_id_seq OWNED BY public.events.id;


--
-- Name: maintenance_records; Type: TABLE; Schema: public; Owner: pi_user
--

CREATE TABLE public.maintenance_records (
    id integer NOT NULL,
    boat_id integer,
    equipment_id integer,
    maintenance_type character varying(50) NOT NULL,
    title character varying(200) NOT NULL,
    description text NOT NULL,
    date_performed date NOT NULL,
    performed_by character varying(100),
    performed_by_type character varying(50),
    location character varying(100),
    cost numeric(10,2),
    labor_hours double precision,
    currency character varying(3),
    parts_used text,
    parts_cost numeric(10,2),
    labor_cost numeric(10,2),
    next_maintenance_due date,
    next_maintenance_hours double precision,
    maintenance_interval_days integer,
    maintenance_interval_hours double precision,
    photos text,
    documents text,
    notes text,
    status character varying(20),
    priority character varying(10),
    warranty_work boolean,
    created_by integer NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.maintenance_records OWNER TO pi_user;

--
-- Name: maintenance_records_id_seq; Type: SEQUENCE; Schema: public; Owner: pi_user
--

CREATE SEQUENCE public.maintenance_records_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.maintenance_records_id_seq OWNER TO pi_user;

--
-- Name: maintenance_records_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pi_user
--

ALTER SEQUENCE public.maintenance_records_id_seq OWNED BY public.maintenance_records.id;


--
-- Name: system_modules; Type: TABLE; Schema: public; Owner: pi_user
--

CREATE TABLE public.system_modules (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    display_name character varying(100) NOT NULL,
    description text,
    icon character varying(50),
    is_active boolean,
    requires_admin boolean,
    sort_order integer,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.system_modules OWNER TO pi_user;

--
-- Name: system_modules_id_seq; Type: SEQUENCE; Schema: public; Owner: pi_user
--

CREATE SEQUENCE public.system_modules_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.system_modules_id_seq OWNER TO pi_user;

--
-- Name: system_modules_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pi_user
--

ALTER SEQUENCE public.system_modules_id_seq OWNED BY public.system_modules.id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: pi_user
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    username character varying(50) NOT NULL,
    email character varying(100) NOT NULL,
    password_hash character varying(255) NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    is_active boolean,
    is_admin boolean DEFAULT false,
    first_name character varying(50),
    last_name character varying(50),
    phone character varying(20),
    emergency_contact character varying(200),
    sailing_experience character varying(20) DEFAULT 'Beginner'::character varying,
    certifications text,
    default_module character varying(50) DEFAULT 'dashboard'::character varying,
    profile_image_path character varying(255),
    last_login timestamp without time zone,
    timezone character varying(50) DEFAULT 'UTC'::character varying
);


ALTER TABLE public."user" OWNER TO pi_user;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: pi_user
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_id_seq OWNER TO pi_user;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pi_user
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- Name: user_module_permissions; Type: TABLE; Schema: public; Owner: pi_user
--

CREATE TABLE public.user_module_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    module_id integer NOT NULL,
    is_enabled boolean,
    granted_at timestamp without time zone,
    granted_by integer
);


ALTER TABLE public.user_module_permissions OWNER TO pi_user;

--
-- Name: user_module_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: pi_user
--

CREATE SEQUENCE public.user_module_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_module_permissions_id_seq OWNER TO pi_user;

--
-- Name: user_module_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pi_user
--

ALTER SEQUENCE public.user_module_permissions_id_seq OWNED BY public.user_module_permissions.id;


--
-- Name: user_preferences; Type: TABLE; Schema: public; Owner: pi_user
--

CREATE TABLE public.user_preferences (
    id integer NOT NULL,
    user_id integer NOT NULL,
    preference_key character varying(100) NOT NULL,
    preference_value text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.user_preferences OWNER TO pi_user;

--
-- Name: user_preferences_id_seq; Type: SEQUENCE; Schema: public; Owner: pi_user
--

CREATE SEQUENCE public.user_preferences_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_preferences_id_seq OWNER TO pi_user;

--
-- Name: user_preferences_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pi_user
--

ALTER SEQUENCE public.user_preferences_id_seq OWNED BY public.user_preferences.id;


--
-- Name: boats id; Type: DEFAULT; Schema: public; Owner: pi_user
--

ALTER TABLE ONLY public.boats ALTER COLUMN id SET DEFAULT nextval('public.boats_id_seq'::regclass);


--
-- Name: equipment id; Type: DEFAULT; Schema: public; Owner: pi_user
--

ALTER TABLE ONLY public.equipment ALTER COLUMN id SET DEFAULT nextval('public.equipment_id_seq'::regclass);


--
-- Name: events id; Type: DEFAULT; Schema: public; Owner: pi_user
--

ALTER TABLE ONLY public.events ALTER COLUMN id SET DEFAULT nextval('public.events_id_seq'::regclass);


--
-- Name: maintenance_records id; Type: DEFAULT; Schema: public; Owner: pi_user
--

ALTER TABLE ONLY public.maintenance_records ALTER COLUMN id SET DEFAULT nextval('public.maintenance_records_id_seq'::regclass);


--
-- Name: system_modules id; Type: DEFAULT; Schema: public; Owner: pi_user
--

ALTER TABLE ONLY public.system_modules ALTER COLUMN id SET DEFAULT nextval('public.system_modules_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: pi_user
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- Name: user_module_permissions id; Type: DEFAULT; Schema: public; Owner: pi_user
--

ALTER TABLE ONLY public.user_module_permissions ALTER COLUMN id SET DEFAULT nextval('public.user_module_permissions_id_seq'::regclass);


--
-- Name: user_preferences id; Type: DEFAULT; Schema: public; Owner: pi_user
--

ALTER TABLE ONLY public.user_preferences ALTER COLUMN id SET DEFAULT nextval('public.user_preferences_id_seq'::regclass);


--
-- Data for Name: boats; Type: TABLE DATA; Schema: public; Owner: pi_user
--

COPY public.boats (id, name, boat_type, length_feet, beam_feet, draft_feet, displacement_lbs, year_built, hull_material, registration_number, hin, documentation_number, owner_id, home_port, current_location, marina_berth, insurance_company, insurance_policy_number, insurance_expiry, engine_make, engine_model, engine_year, engine_hours, fuel_capacity_gallons, water_capacity_gallons, sail_area_sqft, mast_height_feet, keel_type, is_active, condition, last_survey_date, next_survey_due, notes, photos, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: equipment; Type: TABLE DATA; Schema: public; Owner: pi_user
--

COPY public.equipment (id, name, category, subcategory, brand, model, part_number, serial_number, purchase_date, purchase_price, purchase_location, warranty_period_months, warranty_expiry, owner_id, boat_id, location_on_boat, current_location, condition, is_operational, last_inspection_date, next_inspection_due, specifications, quantity, weight_lbs, dimensions, manual_url, photos, documents, notes, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: events; Type: TABLE DATA; Schema: public; Owner: pi_user
--

COPY public.events (id, name, event_type, description, location, venue, start_date, end_date, all_day, timezone, organizer, organizer_contact, website, registration_required, registration_deadline, registration_fee, max_participants, current_participants, boat_requirements, skill_level_required, age_restrictions, weather_dependent, backup_date, prizes, notes, status, is_public, created_by, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: maintenance_records; Type: TABLE DATA; Schema: public; Owner: pi_user
--

COPY public.maintenance_records (id, boat_id, equipment_id, maintenance_type, title, description, date_performed, performed_by, performed_by_type, location, cost, labor_hours, currency, parts_used, parts_cost, labor_cost, next_maintenance_due, next_maintenance_hours, maintenance_interval_days, maintenance_interval_hours, photos, documents, notes, status, priority, warranty_work, created_by, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: system_modules; Type: TABLE DATA; Schema: public; Owner: pi_user
--

COPY public.system_modules (id, name, display_name, description, icon, is_active, requires_admin, sort_order, created_at, updated_at) FROM stdin;
1	dashboard	Dashboard	Main dashboard with overview and statistics	dashboard	t	f	1	2025-06-20 17:39:12.122894	2025-06-20 17:39:12.122905
2	boats	Fleet Management	Manage your boats and fleet information	boat	t	f	2	2025-06-20 17:39:12.129733	2025-06-20 17:39:12.129744
3	trips	Trip Logbook	Log and track your sailing trips with GPS support	map	t	f	3	2025-06-20 17:39:12.134975	2025-06-20 17:39:12.134986
4	equipment	Equipment Tracker	Manage your sailing equipment and inventory	tools	t	f	4	2025-06-20 17:39:12.140285	2025-06-20 17:39:12.140296
5	maintenance	Maintenance Log	Track maintenance records and schedules	wrench	t	f	5	2025-06-20 17:39:12.145499	2025-06-20 17:39:12.145511
6	events	Events Calendar	Manage sailing events, races, and gatherings	calendar	t	f	6	2025-06-20 17:39:12.150805	2025-06-20 17:39:12.150816
7	navigation	Weather & Routes	Weather information and route planning tools	compass	t	f	7	2025-06-20 17:39:12.156035	2025-06-20 17:39:12.156046
8	social	Crew Network	Connect with other sailors and crew members	users	t	f	8	2025-06-20 17:39:12.161282	2025-06-20 17:39:12.161294
9	admin	Admin Panel	System administration and user management	settings	t	t	99	2025-06-20 17:39:12.165966	2025-06-20 17:39:12.165977
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: pi_user
--

COPY public."user" (id, username, email, password_hash, created_at, updated_at, is_active, is_admin, first_name, last_name, phone, emergency_contact, sailing_experience, certifications, default_module, profile_image_path, last_login, timezone) FROM stdin;
1	Dugan	dugan@email.com	$2b$12$TiMoXZI3WSLPw3/HI1Sxau3X6ZMfFWg4.clVri1QRZoYbOsbNO1IW	2025-06-20 14:55:41.920773	2025-06-20 14:55:41.920784	t	t	\N	\N	\N	\N	Beginner	\N	dashboard	\N	\N	UTC
\.


--
-- Data for Name: user_module_permissions; Type: TABLE DATA; Schema: public; Owner: pi_user
--

COPY public.user_module_permissions (id, user_id, module_id, is_enabled, granted_at, granted_by) FROM stdin;
\.


--
-- Data for Name: user_preferences; Type: TABLE DATA; Schema: public; Owner: pi_user
--

COPY public.user_preferences (id, user_id, preference_key, preference_value, created_at, updated_at) FROM stdin;
\.


--
-- Name: boats_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pi_user
--

SELECT pg_catalog.setval('public.boats_id_seq', 1, false);


--
-- Name: equipment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pi_user
--

SELECT pg_catalog.setval('public.equipment_id_seq', 1, false);


--
-- Name: events_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pi_user
--

SELECT pg_catalog.setval('public.events_id_seq', 1, false);


--
-- Name: maintenance_records_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pi_user
--

SELECT pg_catalog.setval('public.maintenance_records_id_seq', 1, false);


--
-- Name: system_modules_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pi_user
--

SELECT pg_catalog.setval('public.system_modules_id_seq', 9, true);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pi_user
--

SELECT pg_catalog.setval('public.user_id_seq', 1, true);


--
-- Name: user_module_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pi_user
--

SELECT pg_catalog.setval('public.user_module_permissions_id_seq', 1, false);


--
-- Name: user_preferences_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pi_user
--

SELECT pg_catalog.setval('public.user_preferences_id_seq', 1, false);


--
-- Name: user_module_permissions _user_module_uc; Type: CONSTRAINT; Schema: public; Owner: pi_user
--

ALTER TABLE ONLY public.user_module_permissions
    ADD CONSTRAINT _user_module_uc UNIQUE (user_id, module_id);


--
-- Name: user_preferences _user_preference_uc; Type: CONSTRAINT; Schema: public; Owner: pi_user
--

ALTER TABLE ONLY public.user_preferences
    ADD CONSTRAINT _user_preference_uc UNIQUE (user_id, preference_key);


--
-- Name: boats boats_pkey; Type: CONSTRAINT; Schema: public; Owner: pi_user
--

ALTER TABLE ONLY public.boats
    ADD CONSTRAINT boats_pkey PRIMARY KEY (id);


--
-- Name: boats boats_registration_number_key; Type: CONSTRAINT; Schema: public; Owner: pi_user
--

ALTER TABLE ONLY public.boats
    ADD CONSTRAINT boats_registration_number_key UNIQUE (registration_number);


--
-- Name: equipment equipment_pkey; Type: CONSTRAINT; Schema: public; Owner: pi_user
--

ALTER TABLE ONLY public.equipment
    ADD CONSTRAINT equipment_pkey PRIMARY KEY (id);


--
-- Name: events events_pkey; Type: CONSTRAINT; Schema: public; Owner: pi_user
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_pkey PRIMARY KEY (id);


--
-- Name: maintenance_records maintenance_records_pkey; Type: CONSTRAINT; Schema: public; Owner: pi_user
--

ALTER TABLE ONLY public.maintenance_records
    ADD CONSTRAINT maintenance_records_pkey PRIMARY KEY (id);


--
-- Name: system_modules system_modules_name_key; Type: CONSTRAINT; Schema: public; Owner: pi_user
--

ALTER TABLE ONLY public.system_modules
    ADD CONSTRAINT system_modules_name_key UNIQUE (name);


--
-- Name: system_modules system_modules_pkey; Type: CONSTRAINT; Schema: public; Owner: pi_user
--

ALTER TABLE ONLY public.system_modules
    ADD CONSTRAINT system_modules_pkey PRIMARY KEY (id);


--
-- Name: user user_email_key; Type: CONSTRAINT; Schema: public; Owner: pi_user
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_email_key UNIQUE (email);


--
-- Name: user_module_permissions user_module_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: pi_user
--

ALTER TABLE ONLY public.user_module_permissions
    ADD CONSTRAINT user_module_permissions_pkey PRIMARY KEY (id);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: pi_user
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: user_preferences user_preferences_pkey; Type: CONSTRAINT; Schema: public; Owner: pi_user
--

ALTER TABLE ONLY public.user_preferences
    ADD CONSTRAINT user_preferences_pkey PRIMARY KEY (id);


--
-- Name: user user_username_key; Type: CONSTRAINT; Schema: public; Owner: pi_user
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_username_key UNIQUE (username);


--
-- Name: boats boats_owner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pi_user
--

ALTER TABLE ONLY public.boats
    ADD CONSTRAINT boats_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public."user"(id);


--
-- Name: equipment equipment_boat_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pi_user
--

ALTER TABLE ONLY public.equipment
    ADD CONSTRAINT equipment_boat_id_fkey FOREIGN KEY (boat_id) REFERENCES public.boats(id);


--
-- Name: equipment equipment_owner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pi_user
--

ALTER TABLE ONLY public.equipment
    ADD CONSTRAINT equipment_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public."user"(id);


--
-- Name: events events_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pi_user
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_created_by_fkey FOREIGN KEY (created_by) REFERENCES public."user"(id);


--
-- Name: maintenance_records maintenance_records_boat_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pi_user
--

ALTER TABLE ONLY public.maintenance_records
    ADD CONSTRAINT maintenance_records_boat_id_fkey FOREIGN KEY (boat_id) REFERENCES public.boats(id);


--
-- Name: maintenance_records maintenance_records_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pi_user
--

ALTER TABLE ONLY public.maintenance_records
    ADD CONSTRAINT maintenance_records_created_by_fkey FOREIGN KEY (created_by) REFERENCES public."user"(id);


--
-- Name: maintenance_records maintenance_records_equipment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pi_user
--

ALTER TABLE ONLY public.maintenance_records
    ADD CONSTRAINT maintenance_records_equipment_id_fkey FOREIGN KEY (equipment_id) REFERENCES public.equipment(id);


--
-- Name: user_module_permissions user_module_permissions_granted_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pi_user
--

ALTER TABLE ONLY public.user_module_permissions
    ADD CONSTRAINT user_module_permissions_granted_by_fkey FOREIGN KEY (granted_by) REFERENCES public."user"(id);


--
-- Name: user_module_permissions user_module_permissions_module_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pi_user
--

ALTER TABLE ONLY public.user_module_permissions
    ADD CONSTRAINT user_module_permissions_module_id_fkey FOREIGN KEY (module_id) REFERENCES public.system_modules(id);


--
-- Name: user_module_permissions user_module_permissions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pi_user
--

ALTER TABLE ONLY public.user_module_permissions
    ADD CONSTRAINT user_module_permissions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: user_preferences user_preferences_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pi_user
--

ALTER TABLE ONLY public.user_preferences
    ADD CONSTRAINT user_preferences_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- PostgreSQL database dump complete
--

