.open f:/Dev/api_yamdb/api_yamdb/db.sqlite3 
.mode csv
.separator , 
.import --skip 1 category.csv titles_category 
.import --skip 1 comments.csv reviews_comment 
.import --skip 1 genre_title.csv titles_title_genre 
.import --skip 1 genre.csv titles_genre 
.import --skip 1 review.csv reviews_review 
.import --skip 1 titles.csv titles_title 
.import --skip 1 users.csv users_user 
.exit 1