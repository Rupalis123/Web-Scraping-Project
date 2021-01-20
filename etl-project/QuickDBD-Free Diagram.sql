-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- Link to schema: https://app.quickdatabasediagrams.com/#/d/otwbKC
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.


CREATE TABLE Quotes (
    quote_id int   NOT NULL,
    quote varchar   NOT NULL,
    author_name varchar   NOT NULL,
    CONSTRAINT pk_Quotes PRIMARY KEY (
        quote_id,author_name
     )
);

CREATE TABLE Author (
    author_name varchar   NOT NULL,
     author_born  varchar   NOT NULL,
     author_description  varchar   NOT NULL,
    CONSTRAINT  pk_Author  PRIMARY KEY (
         author_name 
     )
);

CREATE TABLE  Quotes_Tags  (
     quote_id  int   NOT NULL,
     tags  varchar   NOT NULL,
    CONSTRAINT  pk_Quotes_Tags  PRIMARY KEY (
         quote_id 
     )
);

ALTER TABLE  Quotes  ADD CONSTRAINT  fk_Quotes_author_name  FOREIGN KEY( author_name )
REFERENCES  Author  ( author_name );


