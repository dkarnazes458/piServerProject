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

