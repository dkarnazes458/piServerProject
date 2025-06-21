-- ========================================
-- COMPLETE POSTGRESQL BACKUP
-- Created: 2025-06-21T11:46:57.452848
-- Database: pi_server_db
-- Host: 127.0.0.1:5432
-- ========================================

-- ========================================
-- GLOBAL OBJECTS (Users, Roles, etc.)
-- ========================================

--
-- PostgreSQL database cluster dump
--

-- Started on 2025-06-21 11:46:56 EDT

SET default_transaction_read_only = off;

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

--
-- Roles
--

CREATE ROLE admin_user;
ALTER ROLE admin_user WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN NOREPLICATION NOBYPASSRLS PASSWORD 'md5320e17f58abdd29f275d85ac49f20cc0';
CREATE ROLE pi_user;
ALTER ROLE pi_user WITH NOSUPERUSER INHERIT NOCREATEROLE NOCREATEDB LOGIN NOREPLICATION NOBYPASSRLS PASSWORD 'md56fde4e6bfdf68d7787bcc9388b96f09e';
CREATE ROLE postgres;
ALTER ROLE postgres WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN REPLICATION BYPASSRLS;






-- Completed on 2025-06-21 11:46:56 EDT

--
-- PostgreSQL database cluster dump complete
--



-- ========================================
-- DATABASE SCHEMA WITH PERMISSIONS
-- ========================================

--
-- PostgreSQL database dump
--

-- Dumped from database version 13.21 (Raspbian 13.21-0+deb11u1)
-- Dumped by pg_dump version 13.21 (Raspbian 13.21-0+deb11u1)

-- Started on 2025-06-21 11:46:56 EDT

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

DROP DATABASE pi_server_db;
--
-- TOC entry 3128 (class 1262 OID 16625)
-- Name: pi_server_db; Type: DATABASE; Schema: -; Owner: pi_user
--

CREATE DATABASE pi_server_db WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'en_US.UTF-8';


ALTER DATABASE pi_server_db OWNER TO pi_user;

\connect pi_server_db

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
-- TOC entry 200 (class 1259 OID 16626)
-- Name: boats; Type: TABLE; Schema: public; Owner: admin_user
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


ALTER TABLE public.boats OWNER TO admin_user;

--
-- TOC entry 201 (class 1259 OID 16632)
-- Name: boats_id_seq; Type: SEQUENCE; Schema: public; Owner: admin_user
--

CREATE SEQUENCE public.boats_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.boats_id_seq OWNER TO admin_user;

--
-- TOC entry 3131 (class 0 OID 0)
-- Dependencies: 201
-- Name: boats_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin_user
--

ALTER SEQUENCE public.boats_id_seq OWNED BY public.boats.id;


--
-- TOC entry 202 (class 1259 OID 16634)
-- Name: equipment; Type: TABLE; Schema: public; Owner: admin_user
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


ALTER TABLE public.equipment OWNER TO admin_user;

--
-- TOC entry 203 (class 1259 OID 16640)
-- Name: equipment_id_seq; Type: SEQUENCE; Schema: public; Owner: admin_user
--

CREATE SEQUENCE public.equipment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.equipment_id_seq OWNER TO admin_user;

--
-- TOC entry 3134 (class 0 OID 0)
-- Dependencies: 203
-- Name: equipment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin_user
--

ALTER SEQUENCE public.equipment_id_seq OWNED BY public.equipment.id;


--
-- TOC entry 204 (class 1259 OID 16642)
-- Name: events; Type: TABLE; Schema: public; Owner: admin_user
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


ALTER TABLE public.events OWNER TO admin_user;

--
-- TOC entry 205 (class 1259 OID 16648)
-- Name: events_id_seq; Type: SEQUENCE; Schema: public; Owner: admin_user
--

CREATE SEQUENCE public.events_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.events_id_seq OWNER TO admin_user;

--
-- TOC entry 3137 (class 0 OID 0)
-- Dependencies: 205
-- Name: events_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin_user
--

ALTER SEQUENCE public.events_id_seq OWNED BY public.events.id;


--
-- TOC entry 206 (class 1259 OID 16650)
-- Name: gps_route_points; Type: TABLE; Schema: public; Owner: admin_user
--

CREATE TABLE public.gps_route_points (
    id integer NOT NULL,
    trip_id integer NOT NULL,
    latitude numeric(10,8) NOT NULL,
    longitude numeric(11,8) NOT NULL,
    altitude double precision,
    "timestamp" timestamp without time zone NOT NULL,
    elapsed_time_seconds integer,
    speed_knots double precision,
    speed_over_ground double precision,
    course_over_ground double precision,
    heading double precision,
    accuracy double precision,
    satellites_used integer,
    hdop double precision,
    signal_quality character varying(20),
    point_type character varying(20),
    point_name character varying(100),
    water_depth double precision,
    water_temperature double precision,
    air_temperature double precision,
    wind_speed double precision,
    wind_direction double precision,
    barometric_pressure double precision,
    distance_from_previous double precision,
    cumulative_distance double precision,
    engine_rpm integer,
    engine_temperature double precision,
    fuel_flow_rate double precision,
    sail_configuration character varying(100),
    notes text,
    is_significant boolean,
    created_at timestamp without time zone
);


ALTER TABLE public.gps_route_points OWNER TO admin_user;

--
-- TOC entry 207 (class 1259 OID 16656)
-- Name: gps_route_points_id_seq; Type: SEQUENCE; Schema: public; Owner: admin_user
--

CREATE SEQUENCE public.gps_route_points_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gps_route_points_id_seq OWNER TO admin_user;

--
-- TOC entry 3140 (class 0 OID 0)
-- Dependencies: 207
-- Name: gps_route_points_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin_user
--

ALTER SEQUENCE public.gps_route_points_id_seq OWNED BY public.gps_route_points.id;


--
-- TOC entry 208 (class 1259 OID 16658)
-- Name: maintenance_records; Type: TABLE; Schema: public; Owner: admin_user
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


ALTER TABLE public.maintenance_records OWNER TO admin_user;

--
-- TOC entry 209 (class 1259 OID 16664)
-- Name: maintenance_records_id_seq; Type: SEQUENCE; Schema: public; Owner: admin_user
--

CREATE SEQUENCE public.maintenance_records_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.maintenance_records_id_seq OWNER TO admin_user;

--
-- TOC entry 3143 (class 0 OID 0)
-- Dependencies: 209
-- Name: maintenance_records_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin_user
--

ALTER SEQUENCE public.maintenance_records_id_seq OWNED BY public.maintenance_records.id;


--
-- TOC entry 210 (class 1259 OID 16666)
-- Name: system_modules; Type: TABLE; Schema: public; Owner: admin_user
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


ALTER TABLE public.system_modules OWNER TO admin_user;

--
-- TOC entry 211 (class 1259 OID 16672)
-- Name: system_modules_id_seq; Type: SEQUENCE; Schema: public; Owner: admin_user
--

CREATE SEQUENCE public.system_modules_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.system_modules_id_seq OWNER TO admin_user;

--
-- TOC entry 3146 (class 0 OID 0)
-- Dependencies: 211
-- Name: system_modules_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin_user
--

ALTER SEQUENCE public.system_modules_id_seq OWNED BY public.system_modules.id;


--
-- TOC entry 212 (class 1259 OID 16674)
-- Name: trip_participants; Type: TABLE; Schema: public; Owner: admin_user
--

CREATE TABLE public.trip_participants (
    id integer NOT NULL,
    trip_id integer NOT NULL,
    user_id integer NOT NULL,
    role character varying(50),
    is_confirmed boolean,
    experience_level character varying(20),
    joined_at timestamp without time zone,
    left_at timestamp without time zone,
    hours_participated double precision,
    emergency_contact character varying(200),
    medical_notes text,
    dietary_restrictions text,
    cost_share numeric(8,2),
    cost_share_percentage double precision,
    performance_rating integer,
    notes text
);


ALTER TABLE public.trip_participants OWNER TO admin_user;

--
-- TOC entry 213 (class 1259 OID 16680)
-- Name: trip_participants_id_seq; Type: SEQUENCE; Schema: public; Owner: admin_user
--

CREATE SEQUENCE public.trip_participants_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.trip_participants_id_seq OWNER TO admin_user;

--
-- TOC entry 3149 (class 0 OID 0)
-- Dependencies: 213
-- Name: trip_participants_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin_user
--

ALTER SEQUENCE public.trip_participants_id_seq OWNED BY public.trip_participants.id;


--
-- TOC entry 214 (class 1259 OID 16682)
-- Name: trips; Type: TABLE; Schema: public; Owner: admin_user
--

CREATE TABLE public.trips (
    id integer NOT NULL,
    name character varying(200) NOT NULL,
    description text,
    trip_type character varying(50),
    boat_id integer NOT NULL,
    captain_id integer NOT NULL,
    crew_size integer,
    start_date timestamp without time zone NOT NULL,
    end_date timestamp without time zone,
    planned_duration_hours double precision,
    actual_duration_hours double precision,
    start_location character varying(200),
    end_location character varying(200),
    start_latitude numeric(10,8),
    start_longitude numeric(11,8),
    end_latitude numeric(10,8),
    end_longitude numeric(11,8),
    distance_miles double precision,
    distance_calculated double precision,
    max_speed_knots double precision,
    avg_speed_knots double precision,
    max_wind_speed_knots double precision,
    avg_wind_speed_knots double precision,
    wind_direction character varying(50),
    weather_conditions text,
    sea_conditions text,
    visibility character varying(50),
    tide_conditions text,
    fuel_used_gallons double precision,
    fuel_cost numeric(8,2),
    gps_file_path character varying(500),
    gps_file_name character varying(255),
    gps_file_size integer,
    gps_file_type character varying(10),
    route_processed boolean,
    total_route_points integer,
    status character varying(50),
    purpose character varying(100),
    difficulty_level character varying(20),
    emergency_contact character varying(200),
    float_plan_filed boolean,
    float_plan_with character varying(200),
    safety_equipment_check boolean,
    total_cost numeric(10,2),
    cost_breakdown text,
    lessons_learned text,
    highlights text,
    challenges_faced text,
    overall_rating integer,
    would_repeat boolean,
    photos text,
    documents text,
    logbook_entries text,
    is_public boolean,
    is_favorite boolean,
    notes text,
    tags text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.trips OWNER TO admin_user;

--
-- TOC entry 215 (class 1259 OID 16688)
-- Name: trips_id_seq; Type: SEQUENCE; Schema: public; Owner: admin_user
--

CREATE SEQUENCE public.trips_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.trips_id_seq OWNER TO admin_user;

--
-- TOC entry 3152 (class 0 OID 0)
-- Dependencies: 215
-- Name: trips_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin_user
--

ALTER SEQUENCE public.trips_id_seq OWNED BY public.trips.id;


--
-- TOC entry 216 (class 1259 OID 16690)
-- Name: user; Type: TABLE; Schema: public; Owner: admin_user
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


ALTER TABLE public."user" OWNER TO admin_user;

--
-- TOC entry 217 (class 1259 OID 16700)
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: admin_user
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_id_seq OWNER TO admin_user;

--
-- TOC entry 3155 (class 0 OID 0)
-- Dependencies: 217
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin_user
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- TOC entry 218 (class 1259 OID 16702)
-- Name: user_module_permissions; Type: TABLE; Schema: public; Owner: admin_user
--

CREATE TABLE public.user_module_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    module_id integer NOT NULL,
    is_enabled boolean,
    granted_at timestamp without time zone,
    granted_by integer
);


ALTER TABLE public.user_module_permissions OWNER TO admin_user;

--
-- TOC entry 219 (class 1259 OID 16705)
-- Name: user_module_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: admin_user
--

CREATE SEQUENCE public.user_module_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_module_permissions_id_seq OWNER TO admin_user;

--
-- TOC entry 3158 (class 0 OID 0)
-- Dependencies: 219
-- Name: user_module_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin_user
--

ALTER SEQUENCE public.user_module_permissions_id_seq OWNED BY public.user_module_permissions.id;


--
-- TOC entry 220 (class 1259 OID 16707)
-- Name: user_preferences; Type: TABLE; Schema: public; Owner: admin_user
--

CREATE TABLE public.user_preferences (
    id integer NOT NULL,
    user_id integer NOT NULL,
    preference_key character varying(100) NOT NULL,
    preference_value text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.user_preferences OWNER TO admin_user;

--
-- TOC entry 221 (class 1259 OID 16713)
-- Name: user_preferences_id_seq; Type: SEQUENCE; Schema: public; Owner: admin_user
--

CREATE SEQUENCE public.user_preferences_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_preferences_id_seq OWNER TO admin_user;

--
-- TOC entry 3161 (class 0 OID 0)
-- Dependencies: 221
-- Name: user_preferences_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin_user
--

ALTER SEQUENCE public.user_preferences_id_seq OWNED BY public.user_preferences.id;


--
-- TOC entry 2926 (class 2604 OID 16715)
-- Name: boats id; Type: DEFAULT; Schema: public; Owner: admin_user
--

ALTER TABLE ONLY public.boats ALTER COLUMN id SET DEFAULT nextval('public.boats_id_seq'::regclass);


--
-- TOC entry 2927 (class 2604 OID 16716)
-- Name: equipment id; Type: DEFAULT; Schema: public; Owner: admin_user
--

ALTER TABLE ONLY public.equipment ALTER COLUMN id SET DEFAULT nextval('public.equipment_id_seq'::regclass);


--
-- TOC entry 2928 (class 2604 OID 16717)
-- Name: events id; Type: DEFAULT; Schema: public; Owner: admin_user
--

ALTER TABLE ONLY public.events ALTER COLUMN id SET DEFAULT nextval('public.events_id_seq'::regclass);


--
-- TOC entry 2929 (class 2604 OID 16718)
-- Name: gps_route_points id; Type: DEFAULT; Schema: public; Owner: admin_user
--

ALTER TABLE ONLY public.gps_route_points ALTER COLUMN id SET DEFAULT nextval('public.gps_route_points_id_seq'::regclass);


--
-- TOC entry 2930 (class 2604 OID 16719)
-- Name: maintenance_records id; Type: DEFAULT; Schema: public; Owner: admin_user
--

ALTER TABLE ONLY public.maintenance_records ALTER COLUMN id SET DEFAULT nextval('public.maintenance_records_id_seq'::regclass);


--
-- TOC entry 2931 (class 2604 OID 16720)
-- Name: system_modules id; Type: DEFAULT; Schema: public; Owner: admin_user
--

ALTER TABLE ONLY public.system_modules ALTER COLUMN id SET DEFAULT nextval('public.system_modules_id_seq'::regclass);


--
-- TOC entry 2932 (class 2604 OID 16721)
-- Name: trip_participants id; Type: DEFAULT; Schema: public; Owner: admin_user
--

ALTER TABLE ONLY public.trip_participants ALTER COLUMN id SET DEFAULT nextval('public.trip_participants_id_seq'::regclass);


--
-- TOC entry 2933 (class 2604 OID 16722)
-- Name: trips id; Type: DEFAULT; Schema: public; Owner: admin_user
--

ALTER TABLE ONLY public.trips ALTER COLUMN id SET DEFAULT nextval('public.trips_id_seq'::regclass);


--
-- TOC entry 2938 (class 2604 OID 16723)
-- Name: user id; Type: DEFAULT; Schema: public; Owner: admin_user
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- TOC entry 2939 (class 2604 OID 16724)
-- Name: user_module_permissions id; Type: DEFAULT; Schema: public; Owner: admin_user
--

ALTER TABLE ONLY public.user_module_permissions ALTER COLUMN id SET DEFAULT nextval('public.user_module_permissions_id_seq'::regclass);


--
-- TOC entry 2940 (class 2604 OID 16725)
-- Name: user_preferences id; Type: DEFAULT; Schema: public; Owner: admin_user
--

ALTER TABLE ONLY public.user_preferences ALTER COLUMN id SET DEFAULT nextval('public.user_preferences_id_seq'::regclass);


--
-- TOC entry 2958 (class 2606 OID 16727)
-- Name: trip_participants _trip_user_uc; Type: CONSTRAINT; Schema: public; Owner: admin_user
--

ALTER TABLE ONLY public.trip_participants
    ADD CONSTRAINT _trip_user_uc UNIQUE (trip_id, user_id);


--
-- TOC entry 2970 (class 2606 OID 16729)
-- Name: user_module_permissions _user_module_uc; Type: CONSTRAINT; Schema: public; Owner: admin_user
--

ALTER TABLE ONLY public.user_module_permissions
    ADD CONSTRAINT _user_module_uc UNIQUE (user_id, module_id);


--
-- TOC entry 2974 (class 2606 OID 16731)
-- Name: user_preferences _user_preference_uc; Type: CONSTRAINT; Schema: public; Owner: admin_user
--

ALTER TABLE ONLY public.user_preferences
    ADD CONSTRAINT _user_preference_uc UNIQUE (user_id, preference_key);


--
-- TOC entry 2942 (class 2606 OID 16733)
-- Name: boats boats_pkey; Type: CONSTRAINT; Schema: public; Owner: admin_user
--

ALTER TABLE ONLY public.boats
    ADD CONSTRAINT boats_pkey PRIMARY KEY (id);


--
-- TOC entry 2944 (class 2606 OID 16735)
-- Name: boats boats_registration_number_key; Type: CONSTRAINT; Schema: public; Owner: admin_user
--

ALTER TABLE ONLY public.boats
    ADD CONSTRAINT boats_registration_number_key UNIQUE (registration_number);


--
-- TOC entry 2946 (class 2606 OID 16737)
-- Name: equipment equipment_pkey; Type: CONSTRAINT; Schema: public; Owner: admin_user
--

ALTER TABLE ONLY public.equipment
    ADD CONSTRAINT equipment_pkey PRIMARY KEY (id);


--
-- TOC entry 2948 (class 2606 OID 16739)
-- Name: events events_pkey; Type: CONSTRAINT; Schema: public; Owner: admin_user
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_pkey PRIMARY KEY (id);


--
-- TOC entry 2950 (class 2606 OID 16741)
-- Name: gps_route_points gps_route_points_pkey; Type: CONSTRAINT; Schema: public; Owner: admin_user
--

ALTER TABLE ONLY public.gps_route_points
    ADD CONSTRAINT gps_route_points_pkey PRIMARY KEY (id);


--
-- TOC entry 2952 (class 2606 OID 16743)
-- Name: maintenance_records maintenance_records_pkey; Type: CONSTRAINT; Schema: public; Owner: admin_user
--

ALTER TABLE ONLY public.maintenance_records
    ADD CONSTRAINT maintenance_records_pkey PRIMARY KEY (id);


--
-- TOC entry 2954 (class 2606 OID 16745)
-- Name: system_modules system_modules_name_key; Type: CONSTRAINT; Schema: public; Owner: admin_user
--

ALTER TABLE ONLY public.system_modules
    ADD CONSTRAINT system_modules_name_key UNIQUE (name);


--
-- TOC entry 2956 (class 2606 OID 16747)
-- Name: system_modules system_modules_pkey; Type: CONSTRAINT; Schema: public; Owner: admin_user
--

ALTER TABLE ONLY public.system_modules
    ADD CONSTRAINT system_modules_pkey PRIMARY KEY (id);


--
-- TOC entry 2960 (class 2606 OID 16749)
-- Name: trip_participants trip_participants_pkey; Type: CONSTRAINT; Schema: public; Owner: admin_user
--

ALTER TABLE ONLY public.trip_participants
    ADD CONSTRAINT trip_participants_pkey PRIMARY KEY (id);


--
-- TOC entry 2962 (class 2606 OID 16751)
-- Name: trips trips_pkey; Type: CONSTRAINT; Schema: public; Owner: admin_user
--

ALTER TABLE ONLY public.trips
    ADD CONSTRAINT trips_pkey PRIMARY KEY (id);


--
-- TOC entry 2964 (class 2606 OID 16753)
-- Name: user user_email_key; Type: CONSTRAINT; Schema: public; Owner: admin_user
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_email_key UNIQUE (email);


--
-- TOC entry 2972 (class 2606 OID 16755)
-- Name: user_module_permissions user_module_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: admin_user
--

ALTER TABLE ONLY public.user_module_permissions
    ADD CONSTRAINT user_module_permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 2966 (class 2606 OID 16757)
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: admin_user
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- TOC entry 2976 (class 2606 OID 16759)
-- Name: user_preferences user_preferences_pkey; Type: CONSTRAINT; Schema: public; Owner: admin_user
--

ALTER TABLE ONLY public.user_preferences
    ADD CONSTRAINT user_preferences_pkey PRIMARY KEY (id);


--
-- TOC entry 2968 (class 2606 OID 16761)
-- Name: user user_username_key; Type: CONSTRAINT; Schema: public; Owner: admin_user
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_username_key UNIQUE (username);


--
-- TOC entry 2977 (class 2606 OID 16762)
-- Name: boats boats_owner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin_user
--

ALTER TABLE ONLY public.boats
    ADD CONSTRAINT boats_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public."user"(id);


--
-- TOC entry 2978 (class 2606 OID 16767)
-- Name: equipment equipment_boat_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin_user
--

ALTER TABLE ONLY public.equipment
    ADD CONSTRAINT equipment_boat_id_fkey FOREIGN KEY (boat_id) REFERENCES public.boats(id);


--
-- TOC entry 2979 (class 2606 OID 16772)
-- Name: equipment equipment_owner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin_user
--

ALTER TABLE ONLY public.equipment
    ADD CONSTRAINT equipment_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public."user"(id);


--
-- TOC entry 2980 (class 2606 OID 16777)
-- Name: events events_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin_user
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_created_by_fkey FOREIGN KEY (created_by) REFERENCES public."user"(id);


--
-- TOC entry 2981 (class 2606 OID 16782)
-- Name: gps_route_points gps_route_points_trip_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin_user
--

ALTER TABLE ONLY public.gps_route_points
    ADD CONSTRAINT gps_route_points_trip_id_fkey FOREIGN KEY (trip_id) REFERENCES public.trips(id);


--
-- TOC entry 2982 (class 2606 OID 16787)
-- Name: maintenance_records maintenance_records_boat_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin_user
--

ALTER TABLE ONLY public.maintenance_records
    ADD CONSTRAINT maintenance_records_boat_id_fkey FOREIGN KEY (boat_id) REFERENCES public.boats(id);


--
-- TOC entry 2983 (class 2606 OID 16792)
-- Name: maintenance_records maintenance_records_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin_user
--

ALTER TABLE ONLY public.maintenance_records
    ADD CONSTRAINT maintenance_records_created_by_fkey FOREIGN KEY (created_by) REFERENCES public."user"(id);


--
-- TOC entry 2984 (class 2606 OID 16797)
-- Name: maintenance_records maintenance_records_equipment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin_user
--

ALTER TABLE ONLY public.maintenance_records
    ADD CONSTRAINT maintenance_records_equipment_id_fkey FOREIGN KEY (equipment_id) REFERENCES public.equipment(id);


--
-- TOC entry 2985 (class 2606 OID 16802)
-- Name: trip_participants trip_participants_trip_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin_user
--

ALTER TABLE ONLY public.trip_participants
    ADD CONSTRAINT trip_participants_trip_id_fkey FOREIGN KEY (trip_id) REFERENCES public.trips(id);


--
-- TOC entry 2986 (class 2606 OID 16807)
-- Name: trip_participants trip_participants_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin_user
--

ALTER TABLE ONLY public.trip_participants
    ADD CONSTRAINT trip_participants_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- TOC entry 2987 (class 2606 OID 16812)
-- Name: trips trips_boat_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin_user
--

ALTER TABLE ONLY public.trips
    ADD CONSTRAINT trips_boat_id_fkey FOREIGN KEY (boat_id) REFERENCES public.boats(id);


--
-- TOC entry 2988 (class 2606 OID 16817)
-- Name: trips trips_captain_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin_user
--

ALTER TABLE ONLY public.trips
    ADD CONSTRAINT trips_captain_id_fkey FOREIGN KEY (captain_id) REFERENCES public."user"(id);


--
-- TOC entry 2989 (class 2606 OID 16822)
-- Name: user_module_permissions user_module_permissions_granted_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin_user
--

ALTER TABLE ONLY public.user_module_permissions
    ADD CONSTRAINT user_module_permissions_granted_by_fkey FOREIGN KEY (granted_by) REFERENCES public."user"(id);


--
-- TOC entry 2990 (class 2606 OID 16827)
-- Name: user_module_permissions user_module_permissions_module_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin_user
--

ALTER TABLE ONLY public.user_module_permissions
    ADD CONSTRAINT user_module_permissions_module_id_fkey FOREIGN KEY (module_id) REFERENCES public.system_modules(id);


--
-- TOC entry 2991 (class 2606 OID 16832)
-- Name: user_module_permissions user_module_permissions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin_user
--

ALTER TABLE ONLY public.user_module_permissions
    ADD CONSTRAINT user_module_permissions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- TOC entry 2992 (class 2606 OID 16837)
-- Name: user_preferences user_preferences_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin_user
--

ALTER TABLE ONLY public.user_preferences
    ADD CONSTRAINT user_preferences_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- TOC entry 3129 (class 0 OID 0)
-- Dependencies: 3
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

GRANT ALL ON SCHEMA public TO pi_user;


--
-- TOC entry 3130 (class 0 OID 0)
-- Dependencies: 200
-- Name: TABLE boats; Type: ACL; Schema: public; Owner: admin_user
--

GRANT ALL ON TABLE public.boats TO pi_user;


--
-- TOC entry 3132 (class 0 OID 0)
-- Dependencies: 201
-- Name: SEQUENCE boats_id_seq; Type: ACL; Schema: public; Owner: admin_user
--

GRANT ALL ON SEQUENCE public.boats_id_seq TO pi_user;


--
-- TOC entry 3133 (class 0 OID 0)
-- Dependencies: 202
-- Name: TABLE equipment; Type: ACL; Schema: public; Owner: admin_user
--

GRANT ALL ON TABLE public.equipment TO pi_user;


--
-- TOC entry 3135 (class 0 OID 0)
-- Dependencies: 203
-- Name: SEQUENCE equipment_id_seq; Type: ACL; Schema: public; Owner: admin_user
--

GRANT ALL ON SEQUENCE public.equipment_id_seq TO pi_user;


--
-- TOC entry 3136 (class 0 OID 0)
-- Dependencies: 204
-- Name: TABLE events; Type: ACL; Schema: public; Owner: admin_user
--

GRANT ALL ON TABLE public.events TO pi_user;


--
-- TOC entry 3138 (class 0 OID 0)
-- Dependencies: 205
-- Name: SEQUENCE events_id_seq; Type: ACL; Schema: public; Owner: admin_user
--

GRANT ALL ON SEQUENCE public.events_id_seq TO pi_user;


--
-- TOC entry 3139 (class 0 OID 0)
-- Dependencies: 206
-- Name: TABLE gps_route_points; Type: ACL; Schema: public; Owner: admin_user
--

GRANT ALL ON TABLE public.gps_route_points TO pi_user;


--
-- TOC entry 3141 (class 0 OID 0)
-- Dependencies: 207
-- Name: SEQUENCE gps_route_points_id_seq; Type: ACL; Schema: public; Owner: admin_user
--

GRANT ALL ON SEQUENCE public.gps_route_points_id_seq TO pi_user;


--
-- TOC entry 3142 (class 0 OID 0)
-- Dependencies: 208
-- Name: TABLE maintenance_records; Type: ACL; Schema: public; Owner: admin_user
--

GRANT ALL ON TABLE public.maintenance_records TO pi_user;


--
-- TOC entry 3144 (class 0 OID 0)
-- Dependencies: 209
-- Name: SEQUENCE maintenance_records_id_seq; Type: ACL; Schema: public; Owner: admin_user
--

GRANT ALL ON SEQUENCE public.maintenance_records_id_seq TO pi_user;


--
-- TOC entry 3145 (class 0 OID 0)
-- Dependencies: 210
-- Name: TABLE system_modules; Type: ACL; Schema: public; Owner: admin_user
--

GRANT ALL ON TABLE public.system_modules TO pi_user;


--
-- TOC entry 3147 (class 0 OID 0)
-- Dependencies: 211
-- Name: SEQUENCE system_modules_id_seq; Type: ACL; Schema: public; Owner: admin_user
--

GRANT ALL ON SEQUENCE public.system_modules_id_seq TO pi_user;


--
-- TOC entry 3148 (class 0 OID 0)
-- Dependencies: 212
-- Name: TABLE trip_participants; Type: ACL; Schema: public; Owner: admin_user
--

GRANT ALL ON TABLE public.trip_participants TO pi_user;


--
-- TOC entry 3150 (class 0 OID 0)
-- Dependencies: 213
-- Name: SEQUENCE trip_participants_id_seq; Type: ACL; Schema: public; Owner: admin_user
--

GRANT ALL ON SEQUENCE public.trip_participants_id_seq TO pi_user;


--
-- TOC entry 3151 (class 0 OID 0)
-- Dependencies: 214
-- Name: TABLE trips; Type: ACL; Schema: public; Owner: admin_user
--

GRANT ALL ON TABLE public.trips TO pi_user;


--
-- TOC entry 3153 (class 0 OID 0)
-- Dependencies: 215
-- Name: SEQUENCE trips_id_seq; Type: ACL; Schema: public; Owner: admin_user
--

GRANT ALL ON SEQUENCE public.trips_id_seq TO pi_user;


--
-- TOC entry 3154 (class 0 OID 0)
-- Dependencies: 216
-- Name: TABLE "user"; Type: ACL; Schema: public; Owner: admin_user
--

GRANT ALL ON TABLE public."user" TO pi_user;


--
-- TOC entry 3156 (class 0 OID 0)
-- Dependencies: 217
-- Name: SEQUENCE user_id_seq; Type: ACL; Schema: public; Owner: admin_user
--

GRANT ALL ON SEQUENCE public.user_id_seq TO pi_user;


--
-- TOC entry 3157 (class 0 OID 0)
-- Dependencies: 218
-- Name: TABLE user_module_permissions; Type: ACL; Schema: public; Owner: admin_user
--

GRANT ALL ON TABLE public.user_module_permissions TO pi_user;


--
-- TOC entry 3159 (class 0 OID 0)
-- Dependencies: 219
-- Name: SEQUENCE user_module_permissions_id_seq; Type: ACL; Schema: public; Owner: admin_user
--

GRANT ALL ON SEQUENCE public.user_module_permissions_id_seq TO pi_user;


--
-- TOC entry 3160 (class 0 OID 0)
-- Dependencies: 220
-- Name: TABLE user_preferences; Type: ACL; Schema: public; Owner: admin_user
--

GRANT ALL ON TABLE public.user_preferences TO pi_user;


--
-- TOC entry 3162 (class 0 OID 0)
-- Dependencies: 221
-- Name: SEQUENCE user_preferences_id_seq; Type: ACL; Schema: public; Owner: admin_user
--

GRANT ALL ON SEQUENCE public.user_preferences_id_seq TO pi_user;


--
-- TOC entry 1782 (class 826 OID 16844)
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: public; Owner: admin_user
--

ALTER DEFAULT PRIVILEGES FOR ROLE admin_user IN SCHEMA public GRANT ALL ON SEQUENCES  TO pi_user;


--
-- TOC entry 1783 (class 826 OID 16845)
-- Name: DEFAULT PRIVILEGES FOR FUNCTIONS; Type: DEFAULT ACL; Schema: public; Owner: admin_user
--

ALTER DEFAULT PRIVILEGES FOR ROLE admin_user IN SCHEMA public GRANT ALL ON FUNCTIONS  TO pi_user;


--
-- TOC entry 1781 (class 826 OID 16843)
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: admin_user
--

ALTER DEFAULT PRIVILEGES FOR ROLE admin_user IN SCHEMA public GRANT ALL ON TABLES  TO pi_user;


-- Completed on 2025-06-21 11:46:56 EDT

--
-- PostgreSQL database dump complete
--



-- ========================================
-- DATABASE DATA
-- ========================================

--
-- PostgreSQL database dump
--

-- Dumped from database version 13.21 (Raspbian 13.21-0+deb11u1)
-- Dumped by pg_dump version 13.21 (Raspbian 13.21-0+deb11u1)

-- Started on 2025-06-21 11:46:57 EDT

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

--
-- TOC entry 3139 (class 0 OID 16690)
-- Dependencies: 216
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: admin_user
--

COPY public."user" (id, username, email, password_hash, created_at, updated_at, is_active, is_admin, first_name, last_name, phone, emergency_contact, sailing_experience, certifications, default_module, profile_image_path, last_login, timezone) FROM stdin;
1	Dugan	dugan@email.com	$2b$12$TiMoXZI3WSLPw3/HI1Sxau3X6ZMfFWg4.clVri1QRZoYbOsbNO1IW	2025-06-20 14:55:41.920773	2025-06-20 14:55:41.920784	t	t	\N	\N	\N	\N	Beginner	\N	dashboard	\N	\N	UTC
\.


--
-- TOC entry 3123 (class 0 OID 16626)
-- Dependencies: 200
-- Data for Name: boats; Type: TABLE DATA; Schema: public; Owner: admin_user
--

COPY public.boats (id, name, boat_type, length_feet, beam_feet, draft_feet, displacement_lbs, year_built, hull_material, registration_number, hin, documentation_number, owner_id, home_port, current_location, marina_berth, insurance_company, insurance_policy_number, insurance_expiry, engine_make, engine_model, engine_year, engine_hours, fuel_capacity_gallons, water_capacity_gallons, sail_area_sqft, mast_height_feet, keel_type, is_active, condition, last_survey_date, next_survey_due, notes, photos, created_at, updated_at) FROM stdin;
1	Demo Sailboat	Sailboat	35	11.5	6.2	\N	2010	Fiberglass	DEMO001	\N	\N	1	Marina Bay	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	t	Good	\N	\N	\N	\N	2025-06-20 18:17:14.965537	2025-06-20 18:17:14.965548
\.


--
-- TOC entry 3125 (class 0 OID 16634)
-- Dependencies: 202
-- Data for Name: equipment; Type: TABLE DATA; Schema: public; Owner: admin_user
--

COPY public.equipment (id, name, category, subcategory, brand, model, part_number, serial_number, purchase_date, purchase_price, purchase_location, warranty_period_months, warranty_expiry, owner_id, boat_id, location_on_boat, current_location, condition, is_operational, last_inspection_date, next_inspection_due, specifications, quantity, weight_lbs, dimensions, manual_url, photos, documents, notes, created_at, updated_at) FROM stdin;
1	VHF Radio	Navigation	Radio	Standard Horizon	GX1700	\N	\N	\N	\N	\N	\N	\N	1	1	Nav Station	\N	Good	t	\N	\N	\N	1	\N	\N	\N	\N	\N	\N	2025-06-20 18:17:14.985621	2025-06-20 18:17:14.985632
\.


--
-- TOC entry 3127 (class 0 OID 16642)
-- Dependencies: 204
-- Data for Name: events; Type: TABLE DATA; Schema: public; Owner: admin_user
--

COPY public.events (id, name, event_type, description, location, venue, start_date, end_date, all_day, timezone, organizer, organizer_contact, website, registration_required, registration_deadline, registration_fee, max_participants, current_participants, boat_requirements, skill_level_required, age_restrictions, weather_dependent, backup_date, prizes, notes, status, is_public, created_by, created_at, updated_at) FROM stdin;
1	Demo Regatta	Race	Sample sailing event for demonstration	Demo Bay	\N	2025-07-20 14:17:15.017383	\N	f	UTC	Demo Yacht Club	\N	\N	f	\N	\N	\N	0	\N	\N	\N	t	\N	\N	\N	Scheduled	t	1	2025-06-20 18:17:15.022518	2025-06-20 18:17:15.022528
\.


--
-- TOC entry 3137 (class 0 OID 16682)
-- Dependencies: 214
-- Data for Name: trips; Type: TABLE DATA; Schema: public; Owner: admin_user
--

COPY public.trips (id, name, description, trip_type, boat_id, captain_id, crew_size, start_date, end_date, planned_duration_hours, actual_duration_hours, start_location, end_location, start_latitude, start_longitude, end_latitude, end_longitude, distance_miles, distance_calculated, max_speed_knots, avg_speed_knots, max_wind_speed_knots, avg_wind_speed_knots, wind_direction, weather_conditions, sea_conditions, visibility, tide_conditions, fuel_used_gallons, fuel_cost, gps_file_path, gps_file_name, gps_file_size, gps_file_type, route_processed, total_route_points, status, purpose, difficulty_level, emergency_contact, float_plan_filed, float_plan_with, safety_equipment_check, total_cost, cost_breakdown, lessons_learned, highlights, challenges_faced, overall_rating, would_repeat, photos, documents, logbook_entries, is_public, is_favorite, notes, tags, created_at, updated_at) FROM stdin;
1	Wednesday Night Race		Racing	1	1	1	2025-06-17 18:58:00	\N	1	\N			\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	f	0	Planned		Moderate		f		f	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	f	f		\N	2025-06-20 22:58:56.938009	2025-06-20 22:59:06.668488
\.


--
-- TOC entry 3129 (class 0 OID 16650)
-- Dependencies: 206
-- Data for Name: gps_route_points; Type: TABLE DATA; Schema: public; Owner: admin_user
--

COPY public.gps_route_points (id, trip_id, latitude, longitude, altitude, "timestamp", elapsed_time_seconds, speed_knots, speed_over_ground, course_over_ground, heading, accuracy, satellites_used, hdop, signal_quality, point_type, point_name, water_depth, water_temperature, air_temperature, wind_speed, wind_direction, barometric_pressure, distance_from_previous, cumulative_distance, engine_rpm, engine_temperature, fuel_flow_rate, sail_configuration, notes, is_significant, created_at) FROM stdin;
\.


--
-- TOC entry 3131 (class 0 OID 16658)
-- Dependencies: 208
-- Data for Name: maintenance_records; Type: TABLE DATA; Schema: public; Owner: admin_user
--

COPY public.maintenance_records (id, boat_id, equipment_id, maintenance_type, title, description, date_performed, performed_by, performed_by_type, location, cost, labor_hours, currency, parts_used, parts_cost, labor_cost, next_maintenance_due, next_maintenance_hours, maintenance_interval_days, maintenance_interval_hours, photos, documents, notes, status, priority, warranty_work, created_by, created_at, updated_at) FROM stdin;
1	1	\N	Routine	Engine Oil Change	Changed engine oil and filter	2025-06-20	Demo User	Self	\N	\N	\N	USD	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	Completed	Medium	f	1	2025-06-20 18:17:15.006869	2025-06-20 18:17:15.006881
\.


--
-- TOC entry 3133 (class 0 OID 16666)
-- Dependencies: 210
-- Data for Name: system_modules; Type: TABLE DATA; Schema: public; Owner: admin_user
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
-- TOC entry 3135 (class 0 OID 16674)
-- Dependencies: 212
-- Data for Name: trip_participants; Type: TABLE DATA; Schema: public; Owner: admin_user
--

COPY public.trip_participants (id, trip_id, user_id, role, is_confirmed, experience_level, joined_at, left_at, hours_participated, emergency_contact, medical_notes, dietary_restrictions, cost_share, cost_share_percentage, performance_rating, notes) FROM stdin;
\.


--
-- TOC entry 3141 (class 0 OID 16702)
-- Dependencies: 218
-- Data for Name: user_module_permissions; Type: TABLE DATA; Schema: public; Owner: admin_user
--

COPY public.user_module_permissions (id, user_id, module_id, is_enabled, granted_at, granted_by) FROM stdin;
1	1	1	t	2025-06-20 18:50:09.876303	1
2	1	2	t	2025-06-20 18:50:09.885026	1
3	1	3	t	2025-06-20 18:50:09.89112	1
4	1	4	t	2025-06-20 18:50:09.897197	1
5	1	5	t	2025-06-20 18:50:09.903237	1
6	1	6	t	2025-06-20 18:50:09.909218	1
7	1	7	t	2025-06-20 18:50:09.915503	1
8	1	8	t	2025-06-20 18:50:09.921266	1
9	1	9	t	2025-06-20 18:50:09.926223	1
\.


--
-- TOC entry 3143 (class 0 OID 16707)
-- Dependencies: 220
-- Data for Name: user_preferences; Type: TABLE DATA; Schema: public; Owner: admin_user
--

COPY public.user_preferences (id, user_id, preference_key, preference_value, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 3150 (class 0 OID 0)
-- Dependencies: 201
-- Name: boats_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin_user
--

SELECT pg_catalog.setval('public.boats_id_seq', 1, true);


--
-- TOC entry 3151 (class 0 OID 0)
-- Dependencies: 203
-- Name: equipment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin_user
--

SELECT pg_catalog.setval('public.equipment_id_seq', 1, true);


--
-- TOC entry 3152 (class 0 OID 0)
-- Dependencies: 205
-- Name: events_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin_user
--

SELECT pg_catalog.setval('public.events_id_seq', 1, true);


--
-- TOC entry 3153 (class 0 OID 0)
-- Dependencies: 207
-- Name: gps_route_points_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin_user
--

SELECT pg_catalog.setval('public.gps_route_points_id_seq', 1, false);


--
-- TOC entry 3154 (class 0 OID 0)
-- Dependencies: 209
-- Name: maintenance_records_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin_user
--

SELECT pg_catalog.setval('public.maintenance_records_id_seq', 1, true);


--
-- TOC entry 3155 (class 0 OID 0)
-- Dependencies: 211
-- Name: system_modules_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin_user
--

SELECT pg_catalog.setval('public.system_modules_id_seq', 9, true);


--
-- TOC entry 3156 (class 0 OID 0)
-- Dependencies: 213
-- Name: trip_participants_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin_user
--

SELECT pg_catalog.setval('public.trip_participants_id_seq', 1, false);


--
-- TOC entry 3157 (class 0 OID 0)
-- Dependencies: 215
-- Name: trips_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin_user
--

SELECT pg_catalog.setval('public.trips_id_seq', 1, true);


--
-- TOC entry 3158 (class 0 OID 0)
-- Dependencies: 217
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin_user
--

SELECT pg_catalog.setval('public.user_id_seq', 1, true);


--
-- TOC entry 3159 (class 0 OID 0)
-- Dependencies: 219
-- Name: user_module_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin_user
--

SELECT pg_catalog.setval('public.user_module_permissions_id_seq', 9, true);


--
-- TOC entry 3160 (class 0 OID 0)
-- Dependencies: 221
-- Name: user_preferences_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin_user
--

SELECT pg_catalog.setval('public.user_preferences_id_seq', 1, false);


-- Completed on 2025-06-21 11:46:57 EDT

--
-- PostgreSQL database dump complete
--

