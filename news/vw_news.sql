create view vw_news_filter as
select n.id as id, 
n.title as 'Название_статьи', 
n.created_dtm as 'Дата_создания', 
u.username as 'Имя_пользователя',
n.content
from news_post as n 
join news_author as a
on n.author_id = a.id
join auth_user as u
on a.user_id = u.id;
