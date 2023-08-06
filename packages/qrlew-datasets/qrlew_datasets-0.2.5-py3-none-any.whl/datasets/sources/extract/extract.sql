--
-- PostgreSQL database dump
--

-- Dumped from database version 15.3 (Debian 15.3-1.pgdg110+1)
-- Dumped by pg_dump version 15.3 (Debian 15.3-1.pgdg110+1)

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
-- Name: extract; Type: SCHEMA; Schema: -; Owner: pg_database_owner
--

CREATE SCHEMA extract;


ALTER SCHEMA extract OWNER TO pg_database_owner;

--
-- Name: SCHEMA extract; Type: COMMENT; Schema: -; Owner: pg_database_owner
--

COMMENT ON SCHEMA extract IS 'standard extract schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: beacon; Type: TABLE; Schema: extract; Owner: postgres
--

CREATE TABLE extract.beacon (
    "検知日時" timestamp without time zone,
    "UserId" character varying(35),
    "所属部署" character varying,
    "フロア名" character varying,
    "Beacon名" character varying,
    "RSSI" integer,
    "マップのX座標" integer,
    "マップのY座標" integer
);


ALTER TABLE extract.beacon OWNER TO postgres;

--
-- Name: census; Type: TABLE; Schema: extract; Owner: postgres
--

CREATE TABLE extract.census (
    age integer,
    workclass character varying(20),
    fnlwgt character varying(20),
    education character varying(20),
    education_num integer,
    marital_status character varying(30),
    occupation character varying(20),
    relationship character varying(20),
    race character varying(20),
    sex character varying(20),
    capital_gain integer,
    capital_loss integer,
    hours_per_week integer,
    native_country character varying(30),
    income character varying(20)
);


ALTER TABLE extract.census OWNER TO postgres;

--
-- Data for Name: beacon; Type: TABLE DATA; Schema: extract; Owner: postgres
--

COPY extract.beacon ("検知日時", "UserId", "所属部署", "フロア名", "Beacon名", "RSSI", "マップのX座標", "マップのY座標") FROM stdin;
2021-07-05 06:52:33	15e312ba59601abc91fdb52a70d29895	3階	３階	3階執務9	78	81	70
2021-07-05 06:54:33	15e312ba59601abc91fdb52a70d29895	3階	３階	3階執務9	84	81	70
2021-07-05 06:56:38	15e312ba59601abc91fdb52a70d29895	3階	３階	3階執務9	81	81	70
2021-07-05 06:58:09	15e312ba59601abc91fdb52a70d29895	3階	３階	3階執務9	82	81	70
2021-07-05 07:00:50	fe2859394ac81a68d486925dc6343e49	4階	１階	喫煙ルーム（社内）	76	74	205
2021-07-05 07:01:28	fdfec2f921ca5ae92e36e6d16c4bb881	3階	３階	まちづくり執務1	80	253	228
2021-07-05 07:03:52	fdfec2f921ca5ae92e36e6d16c4bb881	3階	３階	まちづくり執務2	84	201	226
2021-07-05 07:04:33	fdfec2f921ca5ae92e36e6d16c4bb881	3階	３階	まちづくり執務2	79	201	226
2021-07-05 07:04:59	e90fd3187c30793b2d21dbff7572603f	4階	４階	4階執務1	85	506	75
2021-07-05 07:05:45	fe2859394ac81a68d486925dc6343e49	4階	１階	喫煙ルーム（社内）	74	74	205
2021-07-05 07:06:20	fdfec2f921ca5ae92e36e6d16c4bb881	3階	３階	まちづくり執務2	84	201	226
2021-07-05 07:07:06	fe2859394ac81a68d486925dc6343e49	4階	４階	4階執務2	87	504	231
2021-07-05 07:08:10	fe2859394ac81a68d486925dc6343e49	4階	４階	4階執務2	85	504	231
2021-07-05 07:08:19	fe2859394ac81a68d486925dc6343e49	4階	４階	4階執務2	95	504	231
2021-07-05 07:08:34	fdfec2f921ca5ae92e36e6d16c4bb881	3階	３階	まちづくり執務1	80	253	228
2021-07-05 07:08:42	50a09785c81cc5b14261f4342fd6fe8e	4階	４階	4階執務1	78	506	75
2021-07-05 07:08:54	e90fd3187c30793b2d21dbff7572603f	4階	４階	4階執務1	85	506	75
2021-07-05 07:09:26	fdfec2f921ca5ae92e36e6d16c4bb881	3階	３階	まちづくり執務1	83	253	228
2021-07-05 07:09:43	50a09785c81cc5b14261f4342fd6fe8e	4階	４階	4階執務1	75	506	75
2021-07-05 07:10:35	e90fd3187c30793b2d21dbff7572603f	4階	４階	4階執務1	81	506	75
2021-07-05 07:10:36	50a09785c81cc5b14261f4342fd6fe8e	4階	４階	4階執務1	80	506	75
2021-07-05 07:10:39	fdfec2f921ca5ae92e36e6d16c4bb881	3階	３階	まちづくり執務1	81	253	228
2021-07-05 07:12:17	e90fd3187c30793b2d21dbff7572603f	4階	４階	4階執務1	80	506	75
2021-07-05 07:13:08	fdfec2f921ca5ae92e36e6d16c4bb881	3階	３階	まちづくり執務1	80	253	228
2021-07-05 07:14:13	fdfec2f921ca5ae92e36e6d16c4bb881	3階	３階	まちづくり執務1	81	253	228
2021-07-05 07:15:00	50a09785c81cc5b14261f4342fd6fe8e	4階	４階	4階執務1	78	506	75
2021-07-05 07:15:10	50a09785c81cc5b14261f4342fd6fe8e	4階	４階	4階執務1	79	506	75
2021-07-05 07:15:20	cc952708879cdb9336eef72e6e97da6b	3階	３階	3階執務3	83	627	229
2021-07-05 07:16:21	dda5e65a9d33778f65f226b51cea4b60	3階	３階	営本打ち合わせスペース3	77	486	287
2021-07-05 07:16:25	cc952708879cdb9336eef72e6e97da6b	3階	３階	3階執務4	81	527	228
2021-07-05 07:17:45	dda5e65a9d33778f65f226b51cea4b60	3階	３階	3階執務4	78	527	228
2021-07-05 07:18:01	15e312ba59601abc91fdb52a70d29895	3階	３階	3階執務9	83	81	70
2021-07-05 07:18:13	50a09785c81cc5b14261f4342fd6fe8e	4階	４階	4階執務1	70	506	75
2021-07-05 07:18:18	fdfec2f921ca5ae92e36e6d16c4bb881	3階	３階	まちづくり執務2	86	201	226
2021-07-05 07:18:24	dda5e65a9d33778f65f226b51cea4b60	3階	３階	営本打ち合わせスペース3	77	486	287
2021-07-05 07:19:08	fdfec2f921ca5ae92e36e6d16c4bb881	3階	３階	まちづくり執務1	84	253	228
2021-07-05 07:19:09	cc952708879cdb9336eef72e6e97da6b	3階	３階	3階執務4	82	527	228
2021-07-05 07:20:00	50a09785c81cc5b14261f4342fd6fe8e	4階	４階	4階執務1	82	506	75
2021-07-05 07:20:32	fdfec2f921ca5ae92e36e6d16c4bb881	3階	３階	まちづくり執務1	83	253	228
2021-07-05 07:20:48	cc952708879cdb9336eef72e6e97da6b	3階	３階	営本打ち合わせスペース1	88	645	290
2021-07-05 07:22:08	cc952708879cdb9336eef72e6e97da6b	3階	３階	営本打ち合わせスペース2	80	526	287
2021-07-05 07:22:11	dda5e65a9d33778f65f226b51cea4b60	3階	３階	3階執務4	78	527	228
2021-07-05 07:22:21	dda5e65a9d33778f65f226b51cea4b60	3階	３階	営本打ち合わせスペース3	77	486	287
2021-07-05 07:22:34	fdfec2f921ca5ae92e36e6d16c4bb881	3階	３階	まちづくり執務1	84	253	228
2021-07-05 07:23:21	fdfec2f921ca5ae92e36e6d16c4bb881	3階	３階	まちづくり執務3	76	150	225
2021-07-05 07:23:22	cc952708879cdb9336eef72e6e97da6b	3階	３階	営本打ち合わせスペース2	80	526	287
2021-07-05 07:23:29	fdfec2f921ca5ae92e36e6d16c4bb881	3階	３階	まちづくり執務3	76	150	225
2021-07-05 07:23:30	dda5e65a9d33778f65f226b51cea4b60	3階	３階	営本打ち合わせスペース3	78	486	287
2021-07-05 07:24:43	dda5e65a9d33778f65f226b51cea4b60	3階	３階	営本打ち合わせスペース3	72	486	287
2021-07-05 07:24:54	cc952708879cdb9336eef72e6e97da6b	3階	３階	3階執務4	83	527	228
2021-07-05 07:25:33	dda5e65a9d33778f65f226b51cea4b60	3階	３階	営本打ち合わせスペース3	75	486	287
2021-07-05 07:26:17	fdfec2f921ca5ae92e36e6d16c4bb881	3階	３階	まちづくり執務1	78	253	228
2021-07-05 07:26:42	fdfec2f921ca5ae92e36e6d16c4bb881	3階	３階	まちづくり執務1	83	253	228
2021-07-05 07:26:54	cc952708879cdb9336eef72e6e97da6b	3階	３階	3階執務3	84	627	229
2021-07-05 07:27:29	fdfec2f921ca5ae92e36e6d16c4bb881	3階	３階	まちづくり執務1	83	253	228
2021-07-05 07:29:02	cc952708879cdb9336eef72e6e97da6b	3階	３階	営本打ち合わせスペース2	82	526	287
2021-07-05 07:29:06	dda5e65a9d33778f65f226b51cea4b60	3階	３階	営本打ち合わせスペース3	75	486	287
2021-07-05 07:29:36	fdfec2f921ca5ae92e36e6d16c4bb881	3階	３階	まちづくり執務1	88	253	228
2021-07-05 07:29:53	cc952708879cdb9336eef72e6e97da6b	3階	３階	営本打ち合わせスペース2	79	526	287
2021-07-05 07:29:57	3223c59750514585158af4186fc3c095	3階	３階	まちづくり執務1	79	253	228
2021-07-05 07:30:15	15e312ba59601abc91fdb52a70d29895	3階	３階	3階執務9	80	81	70
2021-07-05 07:31:05	15e312ba59601abc91fdb52a70d29895	3階	３階	3階執務9	79	81	70
2021-07-05 07:31:44	fdfec2f921ca5ae92e36e6d16c4bb881	3階	３階	まちづくり執務2	87	201	226
2021-07-05 07:31:51	cc952708879cdb9336eef72e6e97da6b	3階	３階	営本打ち合わせスペース2	83	526	287
2021-07-05 07:32:34	fdfec2f921ca5ae92e36e6d16c4bb881	3階	３階	まちづくり執務1	84	253	228
2021-07-05 07:33:22	cc952708879cdb9336eef72e6e97da6b	3階	３階	営本打ち合わせスペース2	84	526	287
2021-07-05 07:33:34	fdfec2f921ca5ae92e36e6d16c4bb881	3階	３階	まちづくり執務1	82	253	228
2021-07-05 07:34:22	fdfec2f921ca5ae92e36e6d16c4bb881	3階	３階	まちづくり執務1	85	253	228
2021-07-05 07:34:40	50a09785c81cc5b14261f4342fd6fe8e	4階	４階	4階執務1	81	506	75
2021-07-05 07:35:40	15e312ba59601abc91fdb52a70d29895	3階	３階	3階執務9	76	81	70
2021-07-05 07:35:50	15e312ba59601abc91fdb52a70d29895	3階	３階	3階執務9	76	81	70
2021-07-05 07:36:37	50a09785c81cc5b14261f4342fd6fe8e	4階	４階	4階執務1	75	506	75
2021-07-05 07:37:45	e90fd3187c30793b2d21dbff7572603f	4階	４階	4階執務1	85	506	75
2021-07-05 07:37:57	50a09785c81cc5b14261f4342fd6fe8e	4階	４階	4階執務1	76	506	75
2021-07-05 07:39:16	cc952708879cdb9336eef72e6e97da6b	3階	３階	3階執務4	80	527	228
2021-07-05 07:39:20	fdfec2f921ca5ae92e36e6d16c4bb881	3階	３階	まちづくり執務1	83	253	228
2021-07-05 07:39:30	fdfec2f921ca5ae92e36e6d16c4bb881	3階	３階	まちづくり執務1	84	253	228
2021-07-05 07:40:39	e90fd3187c30793b2d21dbff7572603f	4階	４階	4階執務1	86	506	75
2021-07-05 07:41:58	66413034a0d2e6f4f1597e0a5c74caa0	3階	３階	まちづくり執務1	83	253	228
2021-07-05 07:42:40	66413034a0d2e6f4f1597e0a5c74caa0	3階	３階	まちづくり執務2	88	201	226
2021-07-05 07:43:13	cc952708879cdb9336eef72e6e97da6b	3階	３階	3階執務4	86	527	228
2021-07-05 07:43:20	66413034a0d2e6f4f1597e0a5c74caa0	3階	３階	まちづくり執務1	87	253	228
2021-07-05 07:43:52	cc952708879cdb9336eef72e6e97da6b	3階	３階	3階執務4	86	527	228
2021-07-05 07:44:17	15e312ba59601abc91fdb52a70d29895	3階	３階	まちづくり執務2	81	201	226
2021-07-05 07:44:27	15e312ba59601abc91fdb52a70d29895	3階	３階	3階執務9	86	81	70
2021-07-05 07:45:02	3223c59750514585158af4186fc3c095	3階	３階	3階執務1	83	577	77
2021-07-05 07:46:07	fdfec2f921ca5ae92e36e6d16c4bb881	3階	３階	まちづくり執務1	81	253	228
2021-07-05 07:46:17	3223c59750514585158af4186fc3c095	3階	３階	3階執務1	83	577	77
2021-07-05 07:46:52	fdfec2f921ca5ae92e36e6d16c4bb881	3階	３階	まちづくり執務1	84	253	228
2021-07-05 07:47:02	3223c59750514585158af4186fc3c095	3階	３階	3階執務1	87	577	77
2021-07-05 07:47:06	cc952708879cdb9336eef72e6e97da6b	3階	３階	3階執務4	85	527	228
2021-07-05 07:47:49	fdfec2f921ca5ae92e36e6d16c4bb881	3階	３階	まちづくり執務1	85	253	228
2021-07-05 07:48:14	d76f3a8a7706a25f986c0c838c70c332	4階	４階	4階執務2	79	504	231
2021-07-05 07:48:37	d76f3a8a7706a25f986c0c838c70c332	4階	４階	4階執務2	79	504	231
2021-07-05 07:48:58	cc952708879cdb9336eef72e6e97da6b	3階	３階	3階執務4	84	527	228
2021-07-05 07:49:37	fdfec2f921ca5ae92e36e6d16c4bb881	3階	３階	まちづくり執務2	84	201	226
2021-07-05 07:49:47	15e312ba59601abc91fdb52a70d29895	3階	３階	3階執務9	80	81	70
2021-07-05 07:49:52	fe2859394ac81a68d486925dc6343e49	4階	４階	4階執務2	94	504	231
2021-07-05 07:50:33	3223c59750514585158af4186fc3c095	3階	３階	3階執務1	87	577	77
2021-07-05 07:50:37	fdfec2f921ca5ae92e36e6d16c4bb881	3階	３階	まちづくり執務1	86	253	228
\.


--
-- Data for Name: census; Type: TABLE DATA; Schema: extract; Owner: postgres
--

COPY extract.census (age, workclass, fnlwgt, education, education_num, marital_status, occupation, relationship, race, sex, capital_gain, capital_loss, hours_per_week, native_country, income) FROM stdin;
90	?	77053	HS-grad	9	Widowed	?	Not-in-family	White	Female	0	4356	40	United-States	<=50K
82	Private	132870	HS-grad	9	Widowed	Exec-managerial	Not-in-family	White	Female	0	4356	18	United-States	<=50K
66	?	186061	Some-college	10	Widowed	?	Unmarried	Black	Female	0	4356	40	United-States	<=50K
54	Private	140359	7th-8th	4	Divorced	Machine-op-inspct	Unmarried	White	Female	0	3900	40	United-States	<=50K
41	Private	264663	Some-college	10	Separated	Prof-specialty	Own-child	White	Female	0	3900	40	United-States	<=50K
34	Private	216864	HS-grad	9	\N	Other-service	Unmarried	White	Female	0	3770	45	United-States	<=50K
38	Private	150601	10th	6	Separated	Adm-clerical	Unmarried	White	Male	0	3770	40	United-States	<=50K
74	State-gov	88638	Doctorate	16	Never-married	Prof-specialty	Other-relative	White	Female	0	3683	20	United-States	>50K
\N	Federal-gov	422013	HS-grad	9	Divorced	Prof-specialty	Not-in-family	White	Female	0	3683	40	United-States	<=50K
41	Private	70037	Some-college	10	Never-married	Craft-repair	Unmarried	White	Male	0	3004	60	?	>50K
45	Private	172274	Doctorate	16	Divorced	Prof-specialty	Unmarried	Black	Female	0	3004	35	United-States	>50K
38	Self-emp-not-inc	164526	Prof-school	15	Never-married	Prof-specialty	Not-in-family	White	Male	0	2824	45	United-States	>50K
52	Private	129177	Bachelors	13	Widowed	Other-service	Not-in-family	White	Female	0	2824	20	United-States	>50K
32	Private	136204	Masters	14	Separated	Exec-managerial	Not-in-family	White	Male	0	2824	55	United-States	>50K
51	?	172175	Doctorate	16	Never-married	?	Not-in-family	White	Male	0	2824	40	United-States	>50K
46	Private	45363	Prof-school	15	Divorced	Prof-specialty	Not-in-family	White	Male	0	2824	40	United-States	>50K
45	Private	172822	11th	7	Divorced	Transport-moving	Not-in-family	White	Male	0	2824	76	United-States	>50K
57	Private	317847	Masters	14	\N	Exec-managerial	Not-in-family	White	Male	0	2824	50	United-States	>50K
22	Private	119592	Assoc-acdm	12	Never-married	Handlers-cleaners	Not-in-family	Black	Male	0	2824	40	?	>50K
34	Private	203034	Bachelors	13	Separated	Sales	Not-in-family	White	Male	0	2824	50	United-States	>50K
37	Private	188774	Bachelors	13	Never-married	Exec-managerial	Not-in-family	White	Male	0	2824	40	United-States	>50K
\N	Private	77009	11th	7	\N	Sales	Not-in-family	White	Female	0	2754	42	United-States	<=50K
61	Private	29059	HS-grad	9	Divorced	Sales	Unmarried	White	Female	0	2754	25	United-States	<=50K
51	Private	153870	Some-college	10	Married-civ-spouse	Transport-moving	Husband	White	Male	0	2603	40	United-States	<=50K
61	?	135285	HS-grad	9	Married-civ-spouse	?	Husband	White	Male	0	2603	32	United-States	<=50K
21	Private	34310	Assoc-voc	11	\N	Craft-repair	Husband	White	Male	0	2603	40	United-States	<=50K
33	Private	228696	1st-4th	2	Married-civ-spouse	Craft-repair	Not-in-family	White	Male	0	2603	32	Mexico	<=50K
49	Private	122066	5th-6th	3	Married-civ-spouse	Other-service	Husband	White	Male	0	2603	40	Greece	<=50K
37	Self-emp-inc	107164	10th	6	Never-married	Transport-moving	Not-in-family	White	Male	0	2559	50	United-States	>50K
38	Private	175360	10th	6	Never-married	Prof-specialty	Not-in-family	White	Male	0	2559	90	United-States	>50K
23	Private	44064	Some-college	10	Separated	Other-service	Not-in-family	White	Male	0	2559	40	United-States	>50K
59	Self-emp-inc	107287	10th	6	Widowed	Exec-managerial	Unmarried	White	Female	0	2559	50	United-States	>50K
52	Private	198863	Prof-school	15	Divorced	Exec-managerial	Not-in-family	White	Male	0	2559	60	United-States	>50K
51	Private	123011	Bachelors	13	Divorced	Exec-managerial	Not-in-family	White	Male	0	2559	50	United-States	>50K
60	Self-emp-not-inc	205246	HS-grad	9	Never-married	Exec-managerial	Not-in-family	Black	Male	0	2559	50	United-States	>50K
63	Federal-gov	39181	Doctorate	16	Divorced	Exec-managerial	Not-in-family	White	Female	0	2559	60	United-States	>50K
\N	Private	149650	HS-grad	9	Never-married	Sales	Not-in-family	White	Male	0	2559	48	United-States	>50K
51	Private	197163	Prof-school	15	Never-married	Prof-specialty	Not-in-family	White	Female	0	2559	50	United-States	>50K
37	Self-emp-not-inc	137527	Doctorate	16	Never-married	Prof-specialty	Not-in-family	White	Female	0	2559	60	United-States	>50K
54	Private	161691	Masters	14	Divorced	Prof-specialty	Not-in-family	White	Female	0	2559	40	United-States	>50K
44	Private	326232	Bachelors	13	Divorced	Exec-managerial	Unmarried	White	Male	0	2547	50	United-States	>50K
43	Private	115806	Masters	14	Divorced	Exec-managerial	Unmarried	White	Female	0	2547	40	United-States	>50K
51	Private	115066	Some-college	10	Divorced	Adm-clerical	Unmarried	White	Female	0	2547	40	United-States	>50K
43	Private	289669	Masters	14	Divorced	Prof-specialty	Unmarried	White	Female	0	2547	40	United-States	>50K
71	?	100820	HS-grad	9	Married-civ-spouse	?	Husband	White	Male	0	2489	15	United-States	<=50K
48	Private	121253	Bachelors	13	Married-spouse-absent	Sales	Unmarried	White	Female	0	2472	70	United-States	>50K
71	Private	110380	HS-grad	9	Married-civ-spouse	Sales	Husband	White	Male	0	2467	52	United-States	<=50K
73	Self-emp-not-inc	233882	HS-grad	9	Married-civ-spouse	Farming-fishing	Husband	Asian-Pac-Islander	Male	0	2457	40	Vietnam	<=50K
68	?	192052	Some-college	10	Married-civ-spouse	?	Wife	White	Female	0	2457	40	United-States	<=50K
67	?	174995	Some-college	10	Married-civ-spouse	?	Husband	White	Male	0	2457	40	United-States	<=50K
40	Self-emp-not-inc	335549	Prof-school	15	Never-married	Prof-specialty	Not-in-family	White	Male	0	2444	45	United-States	>50K
50	Private	237729	HS-grad	9	Widowed	Sales	Not-in-family	White	Female	0	2444	72	United-States	>50K
\N	State-gov	68898	Assoc-voc	11	Divorced	Tech-support	Not-in-family	White	Male	0	2444	39	United-States	>50K
42	Private	107276	Some-college	10	Never-married	Exec-managerial	Not-in-family	White	Female	0	2444	40	United-States	>50K
39	Private	141584	Masters	14	Never-married	Sales	Not-in-family	White	Male	0	2444	45	United-States	>50K
32	Private	207668	Bachelors	13	Never-married	Exec-managerial	Other-relative	White	Male	0	2444	50	United-States	>50K
53	Private	313243	Some-college	10	Separated	Craft-repair	Not-in-family	White	Male	0	2444	45	United-States	>50K
40	Local-gov	147372	Some-college	10	Never-married	Protective-serv	Not-in-family	White	Male	0	2444	40	United-States	>50K
38	Private	237608	Bachelors	13	Never-married	Sales	Not-in-family	White	Female	0	2444	45	United-States	>50K
33	Private	194901	Assoc-voc	11	Separated	Craft-repair	Not-in-family	White	Male	0	2444	42	United-States	>50K
43	Private	155106	Assoc-acdm	12	Divorced	Craft-repair	Not-in-family	White	Male	0	2444	70	United-States	>50K
50	Self-emp-inc	121441	11th	7	Never-married	Exec-managerial	Other-relative	White	Male	0	2444	40	United-States	>50K
44	Private	162028	Some-college	10	Married-civ-spouse	Adm-clerical	Wife	White	Female	0	2415	6	United-States	>50K
51	Self-emp-not-inc	160724	Bachelors	13	Married-civ-spouse	Sales	Husband	Asian-Pac-Islander	Male	0	2415	40	China	>50K
41	Private	132222	Prof-school	15	Married-civ-spouse	Prof-specialty	Husband	White	Male	0	2415	40	United-States	>50K
60	Self-emp-inc	226355	Assoc-voc	11	Married-civ-spouse	Machine-op-inspct	Husband	White	Male	0	2415	70	?	>50K
37	Private	329980	Masters	14	Married-civ-spouse	Exec-managerial	Husband	White	Male	0	2415	60	United-States	>50K
55	Self-emp-inc	124137	Prof-school	15	Married-civ-spouse	Prof-specialty	Husband	White	Male	0	2415	35	Greece	>50K
39	Self-emp-inc	329980	Bachelors	13	Married-civ-spouse	Sales	Husband	White	Male	0	2415	60	United-States	>50K
42	Self-emp-inc	187702	Prof-school	15	Married-civ-spouse	Prof-specialty	Husband	White	Male	0	2415	60	United-States	>50K
49	Private	199029	Bachelors	13	Married-civ-spouse	Sales	Husband	White	Male	0	2415	55	United-States	>50K
47	Self-emp-not-inc	145290	HS-grad	9	Married-civ-spouse	Exec-managerial	Husband	White	Male	0	2415	50	United-States	>50K
41	Local-gov	297248	Prof-school	15	Married-civ-spouse	Prof-specialty	Husband	White	Male	0	2415	45	United-States	>50K
55	Self-emp-inc	227856	Bachelors	13	Married-civ-spouse	Exec-managerial	Husband	White	Male	0	2415	50	United-States	>50K
39	Private	179731	Masters	14	Married-civ-spouse	Exec-managerial	Wife	White	Female	0	2415	65	United-States	>50K
42	Private	154374	Bachelors	13	Married-civ-spouse	Exec-managerial	Husband	White	Male	0	2415	60	United-States	>50K
\N	?	27187	Assoc-voc	11	Married-civ-spouse	?	Husband	White	Male	0	2415	12	United-States	>50K
46	Private	326857	Masters	14	Married-civ-spouse	Sales	Husband	White	Male	0	2415	65	United-States	>50K
40	Private	160369	Masters	14	Married-civ-spouse	Exec-managerial	Husband	White	Male	0	2415	45	United-States	>50K
32	Private	396745	Bachelors	13	Married-civ-spouse	Prof-specialty	Husband	White	Male	0	2415	48	United-States	>50K
41	Self-emp-inc	151089	Some-college	10	Married-civ-spouse	Exec-managerial	Husband	White	Male	0	2415	55	United-States	>50K
60	Self-emp-inc	336188	Prof-school	15	Married-civ-spouse	Prof-specialty	Husband	White	Male	0	2415	80	United-States	>50K
31	Private	279015	Masters	14	Married-civ-spouse	Exec-managerial	Husband	White	Male	0	2415	70	Taiwan	>50K
58	Self-emp-not-inc	43221	Some-college	10	Married-civ-spouse	Farming-fishing	Husband	White	Male	0	2415	40	United-States	>50K
37	Self-emp-inc	30529	Bachelors	13	Married-civ-spouse	Sales	Husband	White	Male	0	2415	50	United-States	>50K
44	Self-emp-not-inc	201742	Bachelors	13	Married-civ-spouse	Exec-managerial	Husband	White	Male	0	2415	50	United-States	>50K
39	Self-emp-not-inc	218490	Prof-school	15	Married-civ-spouse	Prof-specialty	Husband	White	Male	0	2415	50	?	>50K
43	Federal-gov	156996	Prof-school	15	Married-civ-spouse	Prof-specialty	Husband	Asian-Pac-Islander	Male	0	2415	55	?	>50K
55	Self-emp-inc	298449	Bachelors	13	Married-civ-spouse	Exec-managerial	Husband	White	Male	0	2415	50	United-States	>50K
44	Self-emp-inc	191712	Masters	14	Married-civ-spouse	Prof-specialty	Husband	White	Male	0	2415	55	United-States	>50K
39	Private	198654	Prof-school	15	Married-civ-spouse	Prof-specialty	Husband	Asian-Pac-Islander	Male	0	2415	67	India	>50K
46	Self-emp-not-inc	102308	Bachelors	13	Married-civ-spouse	Sales	Husband	White	Male	0	2415	40	United-States	>50K
39	Private	348521	Some-college	10	Married-civ-spouse	Farming-fishing	Husband	White	Male	0	2415	99	United-States	>50K
62	Self-emp-inc	56248	Bachelors	13	Married-civ-spouse	Farming-fishing	Husband	White	Male	0	2415	60	United-States	>50K
31	Self-emp-not-inc	252752	HS-grad	9	Married-civ-spouse	Other-service	Wife	White	Female	0	2415	40	United-States	>50K
46	Private	192963	Bachelors	13	Married-civ-spouse	Adm-clerical	Husband	Asian-Pac-Islander	Male	0	2415	35	Philippines	>50K
46	Self-emp-not-inc	198759	Prof-school	15	Married-civ-spouse	Prof-specialty	Husband	White	Male	0	2415	80	United-States	>50K
39	Self-emp-inc	143123	Assoc-voc	11	Married-civ-spouse	Craft-repair	Husband	White	Male	0	2415	40	United-States	>50K
39	Private	237713	Prof-school	15	Married-civ-spouse	Sales	Husband	White	Male	0	2415	99	United-States	>50K
59	Private	81929	Doctorate	16	Married-civ-spouse	Prof-specialty	Husband	White	Male	0	2415	45	United-States	>50K
50	Self-emp-inc	167793	Prof-school	15	Married-civ-spouse	Prof-specialty	Husband	White	Male	0	2415	60	United-States	>50K
46	Private	456062	Doctorate	16	Married-civ-spouse	Prof-specialty	Husband	White	Male	0	2415	55	United-States	>50K
53	Self-emp-not-inc	105478	Bachelors	13	Married-civ-spouse	Exec-managerial	Husband	White	Male	0	2415	40	United-States	>50K
50	Self-emp-not-inc	42402	Prof-school	15	Married-civ-spouse	Prof-specialty	Husband	White	Male	0	2415	30	United-States	>50K
41	Self-emp-inc	114580	Prof-school	15	Married-civ-spouse	Exec-managerial	Wife	White	Female	0	2415	55	United-States	>50K
36	Private	346478	Bachelors	13	Married-civ-spouse	Sales	Husband	White	Male	0	2415	45	United-States	>50K
38	Private	187870	Prof-school	15	Married-civ-spouse	Prof-specialty	Husband	White	Male	0	2415	90	United-States	>50K
54	Private	35576	Some-college	10	Married-civ-spouse	Sales	Husband	White	Male	0	2415	50	United-States	>50K
50	Private	102346	Bachelors	13	Married-civ-spouse	Exec-managerial	Wife	White	Female	0	2415	20	United-States	>50K
47	Private	148995	Bachelors	13	Married-civ-spouse	Exec-managerial	Husband	White	Male	0	2415	60	United-States	>50K
47	Self-emp-inc	102308	Prof-school	15	Married-civ-spouse	Prof-specialty	Husband	White	Male	0	2415	45	United-States	>50K
67	Private	105252	Bachelors	13	Widowed	Exec-managerial	Not-in-family	White	Male	0	2392	40	United-States	>50K
67	Self-emp-inc	106175	Bachelors	13	Married-civ-spouse	Exec-managerial	Husband	White	Male	0	2392	75	United-States	>50K
72	Self-emp-not-inc	52138	Doctorate	16	Married-civ-spouse	Prof-specialty	Husband	White	Male	0	2392	25	United-States	>50K
72	?	118902	Doctorate	16	Married-civ-spouse	?	Husband	White	Male	0	2392	6	United-States	>50K
46	Self-emp-inc	191978	Masters	14	Married-civ-spouse	Exec-managerial	Husband	White	Male	0	2392	50	United-States	>50K
78	Self-emp-inc	188044	Bachelors	13	Married-civ-spouse	Exec-managerial	Husband	White	Male	0	2392	40	United-States	>50K
71	Self-emp-inc	66624	Bachelors	13	Married-civ-spouse	Exec-managerial	Husband	White	Male	0	2392	60	United-States	>50K
83	Self-emp-inc	153183	Bachelors	13	Married-civ-spouse	Exec-managerial	Husband	White	Male	0	2392	55	United-States	>50K
68	Private	211287	Masters	14	Married-civ-spouse	Exec-managerial	Husband	White	Male	0	2392	40	United-States	>50K
26	Private	181655	Assoc-voc	11	Married-civ-spouse	Adm-clerical	Husband	White	Male	0	2377	45	United-States	<=50K
68	State-gov	235882	Doctorate	16	Married-civ-spouse	Prof-specialty	Husband	White	Male	0	2377	60	United-States	>50K
49	Self-emp-inc	158685	HS-grad	9	Married-civ-spouse	Adm-clerical	Wife	White	Female	0	2377	40	United-States	>50K
36	Private	370767	HS-grad	9	Married-civ-spouse	Prof-specialty	Husband	White	Male	0	2377	60	United-States	<=50K
70	Self-emp-not-inc	155141	Bachelors	13	Married-civ-spouse	Craft-repair	Husband	White	Male	0	2377	12	United-States	>50K
27	Private	156516	Some-college	10	Married-civ-spouse	Adm-clerical	Wife	Black	Female	0	2377	20	United-States	<=50K
35	Local-gov	177305	Some-college	10	Married-civ-spouse	Exec-managerial	Husband	White	Male	0	2377	40	United-States	<=50K
23	Private	162945	HS-grad	9	Married-civ-spouse	Sales	Husband	White	Male	0	2377	40	United-States	<=50K
81	Private	177408	HS-grad	9	Married-civ-spouse	Exec-managerial	Husband	White	Male	0	2377	26	United-States	>50K
66	Self-emp-not-inc	427422	Doctorate	16	Married-civ-spouse	Sales	Husband	White	Male	0	2377	25	United-States	>50K
71	Private	152307	HS-grad	9	Married-civ-spouse	Exec-managerial	Husband	White	Male	0	2377	45	United-States	>50K
68	Private	218637	Some-college	10	Married-civ-spouse	Sales	Husband	White	Male	0	2377	55	United-States	>50K
68	State-gov	202699	Masters	14	Married-civ-spouse	Prof-specialty	Husband	White	Male	0	2377	42	?	>50K
65	?	240857	Bachelors	13	Married-civ-spouse	?	Husband	White	Male	0	2377	40	United-States	>50K
52	Private	222405	HS-grad	9	Married-civ-spouse	Sales	Husband	Black	Male	0	2377	40	United-States	<=50K
40	Self-emp-inc	110862	Assoc-acdm	12	Married-civ-spouse	Craft-repair	Husband	White	Male	0	2377	50	United-States	<=50K
68	?	257269	Bachelors	13	Married-civ-spouse	?	Husband	White	Male	0	2377	35	United-States	>50K
21	Private	377931	Some-college	10	Married-civ-spouse	Exec-managerial	Husband	White	Male	0	2377	48	United-States	<=50K
35	Private	192923	HS-grad	9	Married-civ-spouse	Craft-repair	Husband	White	Male	0	2377	40	United-States	<=50K
70	Self-emp-inc	207938	Bachelors	13	Married-civ-spouse	Exec-managerial	Husband	White	Male	0	2377	50	United-States	>50K
61	Self-emp-not-inc	36671	HS-grad	9	Married-civ-spouse	Farming-fishing	Husband	White	Male	0	2352	50	United-States	<=50K
65	Self-emp-inc	81413	HS-grad	9	Married-civ-spouse	Farming-fishing	Husband	White	Male	0	2352	65	United-States	<=50K
46	Private	214955	5th-6th	3	Divorced	Craft-repair	Not-in-family	White	Female	0	2339	45	United-States	<=50K
26	Local-gov	166295	Bachelors	13	Never-married	Prof-specialty	Not-in-family	White	Male	0	2339	55	United-States	<=50K
59	Local-gov	147707	HS-grad	9	Widowed	Farming-fishing	Unmarried	White	Male	0	2339	40	United-States	<=50K
61	Private	43554	5th-6th	3	Never-married	Handlers-cleaners	Not-in-family	Black	Male	0	2339	40	United-States	<=50K
60	State-gov	358893	Bachelors	13	Divorced	Prof-specialty	Not-in-family	White	Female	0	2339	40	United-States	<=50K
49	Self-emp-inc	141058	Some-college	10	Divorced	Exec-managerial	Not-in-family	White	Male	0	2339	50	United-States	<=50K
34	Private	25322	Bachelors	13	Married-spouse-absent	Machine-op-inspct	Not-in-family	Asian-Pac-Islander	Male	0	2339	40	?	<=50K
25	Private	77071	Bachelors	13	Never-married	Prof-specialty	Own-child	White	Female	0	2339	35	United-States	<=50K
55	Private	158702	Some-college	10	Never-married	Adm-clerical	Not-in-family	Black	Female	0	2339	45	?	<=50K
59	Local-gov	171328	HS-grad	9	Separated	Protective-serv	Other-relative	Black	Female	0	2339	40	United-States	<=50K
28	State-gov	381789	Some-college	10	Separated	Exec-managerial	Own-child	White	Male	0	2339	40	United-States	<=50K
43	?	152569	Assoc-voc	11	Widowed	?	Not-in-family	White	Female	0	2339	36	United-States	<=50K
56	Self-emp-not-inc	346635	Masters	14	Divorced	Sales	Unmarried	White	Female	0	2339	60	United-States	<=50K
41	Private	162140	HS-grad	9	Divorced	Craft-repair	Not-in-family	White	Male	0	2339	40	United-States	<=50K
42	Private	191765	HS-grad	9	Never-married	Adm-clerical	Other-relative	Black	Female	0	2339	40	Trinadad&Tobago	<=50K
28	Private	251905	Prof-school	15	Never-married	Prof-specialty	Not-in-family	White	Male	0	2339	40	Canada	<=50K
40	Self-emp-not-inc	33310	Prof-school	15	Divorced	Other-service	Not-in-family	White	Female	0	2339	35	United-States	<=50K
69	Private	228921	Bachelors	13	Widowed	Prof-specialty	Not-in-family	White	Male	0	2282	40	United-States	>50K
66	Local-gov	36364	HS-grad	9	Married-civ-spouse	Craft-repair	Husband	White	Male	0	2267	40	United-States	<=50K
69	Private	124930	5th-6th	3	Married-civ-spouse	Machine-op-inspct	Husband	White	Male	0	2267	40	United-States	<=50K
55	Local-gov	176046	Masters	14	Married-civ-spouse	Prof-specialty	Wife	White	Female	0	2267	40	United-States	<=50K
57	Federal-gov	370890	HS-grad	9	Never-married	Adm-clerical	Not-in-family	White	Male	0	2258	40	United-States	<=50K
20	Self-emp-not-inc	157145	Some-college	10	Never-married	Farming-fishing	Own-child	White	Male	0	2258	10	United-States	<=50K
33	Private	288825	HS-grad	9	Divorced	Craft-repair	Not-in-family	White	Male	0	2258	84	United-States	<=50K
30	Self-emp-not-inc	257295	Some-college	10	Never-married	Sales	Other-relative	Asian-Pac-Islander	Male	0	2258	40	South	<=50K
40	Private	287983	Bachelors	13	Never-married	Tech-support	Not-in-family	Asian-Pac-Islander	Female	0	2258	48	Philippines	<=50K
38	Private	101978	Some-college	10	Separated	Machine-op-inspct	Not-in-family	White	Male	0	2258	55	United-States	>50K
46	State-gov	192779	Assoc-acdm	12	Divorced	Adm-clerical	Unmarried	White	Male	0	2258	38	United-States	>50K
29	Private	135296	Bachelors	13	Never-married	Exec-managerial	Not-in-family	White	Female	0	2258	45	United-States	>50K
57	Federal-gov	199114	Bachelors	13	Never-married	Adm-clerical	Not-in-family	White	Male	0	2258	40	United-States	<=50K
39	Private	156897	HS-grad	9	Never-married	Craft-repair	Own-child	White	Male	0	2258	42	United-States	>50K
47	Private	138107	Bachelors	13	Divorced	Exec-managerial	Not-in-family	White	Male	0	2258	40	United-States	>50K
26	Private	279833	Bachelors	13	Never-married	Exec-managerial	Not-in-family	White	Male	0	2258	45	United-States	>50K
27	Self-emp-not-inc	208577	HS-grad	9	Never-married	Craft-repair	Not-in-family	White	Male	0	2258	50	United-States	<=50K
23	Private	102942	Bachelors	13	Never-married	Prof-specialty	Own-child	White	Female	0	2258	40	United-States	>50K
34	Private	36385	Masters	14	Never-married	Prof-specialty	Not-in-family	White	Male	0	2258	50	United-States	<=50K
33	Private	176185	12th	8	Divorced	Craft-repair	Not-in-family	White	Male	0	2258	42	United-States	<=50K
38	Local-gov	162613	Masters	14	Never-married	Prof-specialty	Not-in-family	White	Female	0	2258	60	United-States	<=50K
57	Private	121362	Some-college	10	Widowed	Adm-clerical	Unmarried	White	Female	0	2258	38	United-States	>50K
36	Private	145933	HS-grad	9	Never-married	Exec-managerial	Not-in-family	White	Male	0	2258	70	United-States	<=50K
44	Federal-gov	29591	Bachelors	13	Divorced	Tech-support	Not-in-family	White	Male	0	2258	40	United-States	>50K
49	State-gov	269417	Doctorate	16	Never-married	Exec-managerial	Not-in-family	White	Female	0	2258	50	United-States	>50K
44	Self-emp-inc	178510	Some-college	10	Never-married	Sales	Not-in-family	White	Male	0	2258	60	United-States	<=50K
55	Private	41108	Some-college	10	Widowed	Farming-fishing	Not-in-family	White	Male	0	2258	62	United-States	>50K
45	Private	187901	HS-grad	9	Divorced	Farming-fishing	Not-in-family	White	Male	0	2258	44	United-States	>50K
48	Private	175070	HS-grad	9	Divorced	Exec-managerial	Not-in-family	White	Female	0	2258	40	United-States	>50K
31	Private	263561	Bachelors	13	Married-civ-spouse	Exec-managerial	Husband	White	Male	0	2246	45	United-States	>50K
55	Local-gov	99131	HS-grad	9	Married-civ-spouse	Prof-specialty	Other-relative	White	Female	0	2246	40	United-States	>50K
70	Self-emp-not-inc	143833	Some-college	10	Married-civ-spouse	Exec-managerial	Husband	White	Male	0	2246	40	United-States	>50K
70	Self-emp-not-inc	124449	Masters	14	Married-civ-spouse	Exec-managerial	Husband	White	Male	0	2246	8	United-States	>50K
73	Private	336007	Bachelors	13	Married-civ-spouse	Prof-specialty	Husband	White	Male	0	2246	40	United-States	>50K
72	Self-emp-not-inc	285408	Prof-school	15	Married-civ-spouse	Prof-specialty	Husband	White	Male	0	2246	28	United-States	>50K
31	Private	327825	HS-grad	9	Separated	Machine-op-inspct	Unmarried	White	Female	0	2238	40	United-States	<=50K
28	Private	129460	10th	6	Widowed	Adm-clerical	Unmarried	White	Female	0	2238	35	United-States	<=50K
23	Self-emp-not-inc	258298	Bachelors	13	Never-married	Adm-clerical	Own-child	White	Male	0	2231	40	United-States	>50K
49	Local-gov	102359	9th	5	Widowed	Handlers-cleaners	Unmarried	White	Male	0	2231	40	United-States	>50K
27	Local-gov	92431	Some-college	10	Never-married	Protective-serv	Not-in-family	White	Male	0	2231	40	United-States	>50K
\.


--
-- PostgreSQL database dump complete
--

