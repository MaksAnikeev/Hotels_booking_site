--
-- PostgreSQL database dump
--

-- Dumped from database version 14.5
-- Dumped by pg_dump version 14.5

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
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


--
-- Name: booking; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.booking (
    id integer NOT NULL,
    room_id integer NOT NULL,
    user_id integer NOT NULL,
    date_from date NOT NULL,
    date_to date NOT NULL,
    price integer NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: booking_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.booking_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: booking_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.booking_id_seq OWNED BY public.booking.id;


--
-- Name: facilities; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.facilities (
    id integer NOT NULL,
    title character varying(200) NOT NULL
);


--
-- Name: facilities_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.facilities_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: facilities_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.facilities_id_seq OWNED BY public.facilities.id;


--
-- Name: hotels; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.hotels (
    id integer NOT NULL,
    title character varying(100) NOT NULL,
    location character varying NOT NULL,
    description character varying
);


--
-- Name: hotels_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.hotels_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: hotels_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.hotels_id_seq OWNED BY public.hotels.id;


--
-- Name: rooms; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.rooms (
    id integer NOT NULL,
    hotel_id integer NOT NULL,
    title character varying(100) NOT NULL,
    description character varying,
    price integer NOT NULL,
    quantity integer NOT NULL
);


--
-- Name: rooms_facilities; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.rooms_facilities (
    id integer NOT NULL,
    facility_id integer NOT NULL,
    room_id integer NOT NULL
);


--
-- Name: rooms_facilities_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.rooms_facilities_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: rooms_facilities_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.rooms_facilities_id_seq OWNED BY public.rooms_facilities.id;


--
-- Name: rooms_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.rooms_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: rooms_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.rooms_id_seq OWNED BY public.rooms.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id integer NOT NULL,
    email character varying(200) NOT NULL,
    hashed_password character varying(200) NOT NULL,
    first_name character varying(100),
    last_name character varying(100),
    is_active boolean NOT NULL,
    role character varying(50) NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: booking id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.booking ALTER COLUMN id SET DEFAULT nextval('public.booking_id_seq'::regclass);


--
-- Name: facilities id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facilities ALTER COLUMN id SET DEFAULT nextval('public.facilities_id_seq'::regclass);


--
-- Name: hotels id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hotels ALTER COLUMN id SET DEFAULT nextval('public.hotels_id_seq'::regclass);


--
-- Name: rooms id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rooms ALTER COLUMN id SET DEFAULT nextval('public.rooms_id_seq'::regclass);


--
-- Name: rooms_facilities id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rooms_facilities ALTER COLUMN id SET DEFAULT nextval('public.rooms_facilities_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.alembic_version (version_num) FROM stdin;
87080ad390e5
\.


--
-- Data for Name: booking; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.booking (id, room_id, user_id, date_from, date_to, price, created_at) FROM stdin;
4	13	14	2026-01-30	2026-02-02	45000	2026-01-29 14:25:41.100316+00
5	1	14	2026-01-30	2026-02-02	3500	2026-01-29 14:26:18.725597+00
6	13	14	2026-01-31	2026-02-10	45000	2026-01-29 14:28:28.585083+00
7	6	16	2026-02-15	2026-02-28	3500	2026-01-29 15:27:32.037236+00
9	1	14	2026-01-30	2026-02-02	3500	2026-01-30 07:51:45.612721+00
10	1	14	2026-01-31	2026-02-08	3500	2026-01-30 07:52:01.042515+00
12	1	14	2026-02-03	2026-02-05	3500	2026-01-30 07:53:43.17294+00
13	2	14	2026-01-30	2026-02-02	3500	2026-01-30 15:27:57.999046+00
11	1	14	2026-01-15	2026-01-29	3500	2026-01-30 07:52:21.027833+00
14	13	16	2026-01-15	2026-02-02	45000	2026-01-31 16:07:37.891763+00
15	10	16	2026-01-30	2026-02-02	4500	2026-01-31 16:24:36.277258+00
17	12	8	2026-01-30	2026-02-02	3900	2026-01-31 16:24:36.277258+00
18	12	8	2026-01-30	2026-02-02	3900	2026-01-31 16:24:36.277258+00
19	13	14	2026-02-18	2026-02-20	45000	2026-02-18 17:57:40.189531+00
16	14	8	2026-03-30	2026-04-02	45000	2026-01-31 16:24:36.277258+00
20	1	14	2026-01-31	2026-02-02	3900	2026-03-02 07:45:35.53289+00
23	13	14	2026-02-15	2026-03-02	45000	2026-03-10 14:38:17.825089+00
24	1	14	2026-01-30	2026-02-02	3500	2026-03-16 10:32:31.514789+00
\.


--
-- Data for Name: facilities; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.facilities (id, title) FROM stdin;
1	кондиционер
2	холодильник
3	 WiFi
4	туалет
5	душ
\.


--
-- Data for Name: hotels; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.hotels (id, title, location, description) FROM stdin;
8	Resort spa Emir	Около ТаджМахала	Крутой отель в Египте
9	Resort spa Emir	Около ТаджМахала	Крутой отель в Египте
11	Sochy curort spa	в центре Сочи	\N
12	Sochy curort spa	в центре Сочи	\N
13	Resort spa Emir	Около ТаджМахала	Крутой отель в Египте
15	Sochi	Сочи	\N
16	Dybai	Дубай	отель в Дубаях
19	Москва	moscow	Самый крутой отель в Москве
22	Sochi	Сочи	\N
26	Москва	moscow	Самый крутой отель в Москве
2	Resort spa Emir	Около ТаджМахала	Крутой отель в Египте
5	Resort spa Emir66666	Около ТаджМахала555555555	Крутой отель в Египт555555555555е
3	Resort spa Emir333	Около Тад333жМахала	Крутой отель в Египт333е
10	Resort spa Emir	Около ТаджМахала	Крутой отель в Египте
4	New Sochi hotel444444444	Около ТаджМахала	Крутой отель в Египте
1	Resort spa Emir	Около ТаджМахала	Крутой отель в Египте
\.


--
-- Data for Name: rooms; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.rooms (id, hotel_id, title, description, price, quantity) FROM stdin;
1	1	Standard	Обычный двухместный номер	3500	50
6	11	Standard	Обычный двухместный номер	3500	15
7	11	Standard	Обычный двухместный номер	3800	5
10	2	Standard	Обычный двухместный номер	3500	7
13	1	1/2 Lux	Двухместный номер с большой кроватью	45000	2
14	15	1/2 Lux	Двухместный номер с большой кроватью	45000	1
12	3	Standard+	Обычный двухместный номер	3900	2
3	2	Standard+	Двухместный номер с большой кроватью	3900	5
18	3	Standard	Обычный двухместный номер	3500	3
19	3	Standard+	Обычный двухместный номер	3500	3
38	22	Standard	Обычный двухместный номер	3500	50
20	3	Standard	Обычный двухместный номер	3500	50
2	1	Standard	Обычный двухместный номер	3500	50
21	22	Standard	Обычный двухместный номер	3500	50
\.


--
-- Data for Name: rooms_facilities; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.rooms_facilities (id, facility_id, room_id) FROM stdin;
1	1	18
2	2	18
3	1	19
37	1	1
39	1	20
40	2	20
41	1	2
42	2	2
43	1	21
44	2	21
55	2	1
72	1	38
73	3	38
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users (id, email, hashed_password, first_name, last_name, is_active, role, created_at, updated_at) FROM stdin;
8	anikeev.mks2@rambler.com	$argon2id$v=19$m=65536,t=3,p=4$zeANcwb3oiHBIkoazTU3Eg$YMezxiF+aTSOScZTm6Pa7fYpanjlWx51LpApGhk+UTU	Maks	Ananimus	t	user	2026-01-24 13:27:02.646415+00	2026-01-24 13:27:02.646415+00
14	anikeev.mks@rambler.com	$argon2id$v=19$m=65536,t=3,p=4$bLrB0yHVTF/9so/jaPbtoQ$oTuQQ7EmejoxvV03EHWWchivWMPAoZ6Y1BVfqqQT38E	Maks	Ananimus	t	user	2026-01-25 08:45:34.693663+00	2026-01-25 08:45:34.693663+00
16	luchy@rambler.com	$argon2id$v=19$m=65536,t=3,p=4$tKE2eL/+qb4cWyYPvTEVnw$rKlG0VFc456Fcf2UYMdeyzB96vOoKQcrSTZgQ9HtztU	\N	\N	t	user	2026-01-25 08:45:44.625711+00	2026-01-25 08:45:44.625711+00
18	1anikeev.mks@rambler.com	$argon2id$v=19$m=65536,t=3,p=4$XwCYdlTq4o9Sfp4dketOBA$uZWutWoLyyrRRI+6pOsPsGiVDTJsXqMTtHCMF52QEzA	Maks	Ananimus	t	user	2026-01-25 08:46:08.376541+00	2026-01-25 08:46:08.376541+00
28	anikeev.maks@rambler.com	$argon2id$v=19$m=65536,t=3,p=4$+9z7e8vgd82UZIT7HszVuQ$VgitBTiOPV6a8ltz1Rg+OQRwV3ItbAz3rigq8oMDKrc	Maks	Ananimus	t	user	2026-03-16 13:53:32.992735+00	2026-03-16 13:53:32.992735+00
\.


--
-- Name: booking_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.booking_id_seq', 24, true);


--
-- Name: facilities_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.facilities_id_seq', 11, true);


--
-- Name: hotels_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.hotels_id_seq', 35, true);


--
-- Name: rooms_facilities_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.rooms_facilities_id_seq', 76, true);


--
-- Name: rooms_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.rooms_id_seq', 38, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_id_seq', 33, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: booking booking_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.booking
    ADD CONSTRAINT booking_pkey PRIMARY KEY (id);


--
-- Name: facilities facilities_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facilities
    ADD CONSTRAINT facilities_pkey PRIMARY KEY (id);


--
-- Name: hotels hotels_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hotels
    ADD CONSTRAINT hotels_pkey PRIMARY KEY (id);


--
-- Name: rooms_facilities rooms_facilities_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rooms_facilities
    ADD CONSTRAINT rooms_facilities_pkey PRIMARY KEY (id);


--
-- Name: rooms rooms_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rooms
    ADD CONSTRAINT rooms_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: booking booking_room_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.booking
    ADD CONSTRAINT booking_room_id_fkey FOREIGN KEY (room_id) REFERENCES public.rooms(id);


--
-- Name: booking booking_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.booking
    ADD CONSTRAINT booking_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: rooms_facilities rooms_facilities_facility_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rooms_facilities
    ADD CONSTRAINT rooms_facilities_facility_id_fkey FOREIGN KEY (facility_id) REFERENCES public.facilities(id);


--
-- Name: rooms_facilities rooms_facilities_room_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rooms_facilities
    ADD CONSTRAINT rooms_facilities_room_id_fkey FOREIGN KEY (room_id) REFERENCES public.rooms(id) ON DELETE CASCADE;


--
-- Name: rooms rooms_hotel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rooms
    ADD CONSTRAINT rooms_hotel_id_fkey FOREIGN KEY (hotel_id) REFERENCES public.hotels(id);


--
-- PostgreSQL database dump complete
--

