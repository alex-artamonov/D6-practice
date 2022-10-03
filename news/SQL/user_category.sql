BEGIN;
--
-- Create model UserCategory
--
CREATE TABLE "news_usercategory" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
    "category_id" bigint NOT NULL 
    REFERENCES "news_category" ("id") DEFERRABLE INITIALLY DEFERRED, 
    "user_id" integer NOT NULL 
    REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Add field user to category
--
CREATE TABLE "new__news_category" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
    "name" varchar(30) NOT NULL UNIQUE);
INSERT INTO "new__news_category" ("id", "name") SELECT "id", "name" FROM "news_category";
DROP TABLE "news_category";
ALTER TABLE "new__news_category" RENAME TO "news_category";
CREATE INDEX "news_usercategory_category_id_d7fc4f27" ON "news_usercategory" ("category_id");
CREATE INDEX "news_usercategory_user_id_41c82bab" ON "news_usercategory" ("user_id");
COMMIT;
