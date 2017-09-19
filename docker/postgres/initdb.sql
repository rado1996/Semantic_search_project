CREATE TABLE page (
    pageid 		SERIAL PRIMARY KEY 	NOT NULL,
    title		CHAR(100)			NOT NULL,	
	pagetext	TEXT	
);

CREATE TABLE category (
    categoryid 	SERIAL PRIMARY KEY	NOT NULL,
    parentcategory	BOOLEAN,
    title		CHAR(100)			NOT NULL
);

CREATE TABLE page_category (
	page_category_id	SERIAL PRIMARY KEY	NOT NULL,
	pageid 				INTEGER 			NOT NULL,
	categoryid  		INTEGER				NOT NULL,
	CONSTRAINT pageid_fkey FOREIGN KEY (pageid)
    REFERENCES page (pageid),
  	CONSTRAINT categoryid_fkey FOREIGN KEY (categoryid)
    REFERENCES category (categoryid)
);
