SELECT slug, qtd FROM 
     articles a INNER JOIN 
         (SELECT path, count(*) AS qtd FROM log GROUP BY path) AS l 
         ON '/article/' || a.slug = l.path
    ORDER BY qtd DESC
    LIMIT 3;