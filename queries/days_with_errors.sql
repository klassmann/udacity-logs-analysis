SELECT date(time) as dt, (100.0 * error_log.qtd / request_log.qtd) AS perc 
FROM log 
JOIN (select date(time) AS de, 
        count(*) AS qtd 
        FROM log 
        WHERE status != '200 OK' 
        GROUP BY de) AS error_log
ON date(log.time) = error_log.de
JOIN (SELECT date(time) AS ds, 
        count(*) AS qtd 
        FROM log 
        GROUP BY ds) AS request_log
ON date(log.time) = request_log.ds
WHERE ((100.0 * error_log.qtd) / request_log.qtd) > 1.0
GROUP BY dt, perc;