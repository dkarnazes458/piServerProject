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
    is_active boolean
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
-- Data for Name: system_modules; Type: TABLE DATA; Schema: public; Owner: pi_user
--

COPY public.system_modules (id, name, display_name, description, icon, is_active, requires_admin, sort_order, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: pi_user
--

COPY public."user" (id, username, email, password_hash, created_at, updated_at, is_active) FROM stdin;
1	Dugan	dugan@email.com	$2b$12$TiMoXZI3WSLPw3/HI1Sxau3X6ZMfFWg4.clVri1QRZoYbOsbNO1IW	2025-06-20 14:55:41.920773	2025-06-20 14:55:41.920784	t
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
-- Name: system_modules_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pi_user
--

SELECT pg_catalog.setval('public.system_modules_id_seq', 1, false);


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

