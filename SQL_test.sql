SELECT uc.email,
       COUNT(*) AS count_links,
       SUM(CASE WHEN link_type = 'website' THEN 1 ELSE 0 END) AS "website",
       SUM(CASE WHEN link_type = 'book' THEN 1 ELSE 0 END) AS "book",
       SUM(CASE WHEN link_type = 'article' THEN 1 ELSE 0 END) AS "article",
       SUM(CASE WHEN link_type = 'music' THEN 1 ELSE 0 END) AS "music",
       SUM(CASE WHEN link_type = 'video' THEN 1 ELSE 0 END) AS "video"
FROM links_userlink lul
JOIN users_customuser uc on uc.id = lul.user_id
GROUP BY uc.email
ORDER BY count_links DESC, MIN(uc.date_joined)
LIMIT 10;