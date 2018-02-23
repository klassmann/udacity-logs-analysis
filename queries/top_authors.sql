SELECT name, qtd FROM authors a INNER JOIN (
    SELECT author, count(*) as qtd FROM 
        articles a INNER JOIN 
            (SELECT path FROM log) AS l 
            ON '/article/' || a.slug = l.path
            GROUP BY author
    ) AS qry_article ON qry_article.author = a.id
ORDER BY qtd DESC;