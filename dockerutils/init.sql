CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

DROP TABLE IF EXISTS "logs";
CREATE TABLE "public"."logs" (
    "logs_id" uuid DEFAULT uuid_generate_v4() NOT NULL,
    "computer" character varying(255) NOT NULL,
    "user" character varying(255) NOT NULL,
    "date" timestamp NOT NULL,
    CONSTRAINT "logs_id" PRIMARY KEY ("logs_id")
) WITH (oids = false);
