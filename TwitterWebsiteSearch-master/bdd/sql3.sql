/*------------------------------------------------------------
*        Script SQLSERVER 
------------------------------------------------------------*/


/*------------------------------------------------------------
-- Table: tweets
------------------------------------------------------------*/
CREATE TABLE tweets(
	id_Tweets   VARCHAR (50) NOT NULL ,
	nom_user    VARCHAR (50)  ,
	nb_retweets INT  NOT NULL ,
	nb_like     INT  NOT NULL ,
	date_T      DATETIME   ,
	langue      VARCHAR (25)  ,
	CONSTRAINT prk_constraint_tweets PRIMARY KEY NONCLUSTERED (id_Tweets)
);


/*------------------------------------------------------------
-- Table: hashtag
------------------------------------------------------------*/
CREATE TABLE hashtag(
	id_hashtag INT  NOT NULL ,
	hashtag    VARCHAR (50)  ,
	CONSTRAINT prk_constraint_hashtag PRIMARY KEY NONCLUSTERED (id_hashtag)
);


/*------------------------------------------------------------
-- Table: motsCles
------------------------------------------------------------*/
CREATE TABLE motsCles(
	id_mots INT  NOT NULL ,
	mots    VARCHAR (50)  ,
	CONSTRAINT prk_constraint_motsCles PRIMARY KEY NONCLUSTERED (id_mots)
);


/*------------------------------------------------------------
-- Table: mentionnees
------------------------------------------------------------*/
CREATE TABLE mentionnees(
	id_mention  INT  NOT NULL ,
	nom_mention VARCHAR (50)  ,
	CONSTRAINT prk_constraint_mentionnees PRIMARY KEY NONCLUSTERED (id_mention)
);


/*------------------------------------------------------------
-- Table: comp_hashtag
------------------------------------------------------------*/
CREATE TABLE comp_hashtag(
	id_Tweets  VARCHAR (50) NOT NULL ,
	id_hashtag INT  NOT NULL ,
	CONSTRAINT prk_constraint_comp_hashtag PRIMARY KEY NONCLUSTERED (id_Tweets,id_hashtag)
);


/*------------------------------------------------------------
-- Table: comp_mention
------------------------------------------------------------*/
CREATE TABLE comp_mention(
	id_Tweets  VARCHAR (50) NOT NULL ,
	id_mention INT  NOT NULL ,
	CONSTRAINT prk_constraint_comp_mention PRIMARY KEY NONCLUSTERED (id_Tweets,id_mention)
);


/*------------------------------------------------------------
-- Table: comp_motscles
------------------------------------------------------------*/
CREATE TABLE comp_motscles(
	id_Tweets VARCHAR (50) NOT NULL ,
	id_mots   INT  NOT NULL ,
	CONSTRAINT prk_constraint_comp_motscles PRIMARY KEY NONCLUSTERED (id_Tweets,id_mots)
);



ALTER TABLE comp_hashtag ADD CONSTRAINT FK_comp_hashtag_id_Tweets FOREIGN KEY (id_Tweets) REFERENCES tweets(id_Tweets);
ALTER TABLE comp_hashtag ADD CONSTRAINT FK_comp_hashtag_id_hashtag FOREIGN KEY (id_hashtag) REFERENCES hashtag(id_hashtag);
ALTER TABLE comp_mention ADD CONSTRAINT FK_comp_mention_id_Tweets FOREIGN KEY (id_Tweets) REFERENCES tweets(id_Tweets);
ALTER TABLE comp_mention ADD CONSTRAINT FK_comp_mention_id_mention FOREIGN KEY (id_mention) REFERENCES mentionnees(id_mention);
ALTER TABLE comp_motscles ADD CONSTRAINT FK_comp_motscles_id_Tweets FOREIGN KEY (id_Tweets) REFERENCES tweets(id_Tweets);
ALTER TABLE comp_motscles ADD CONSTRAINT FK_comp_motscles_id_mots FOREIGN KEY (id_mots) REFERENCES motsCles(id_mots);
