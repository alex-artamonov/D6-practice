BEGIN;
--
-- Create constraint unique_user_category on model usercategory
--
CREATE UNIQUE INDEX "unique_user_category" ON "news_usercategory" ("user_id", "category_id");
COMMIT;
