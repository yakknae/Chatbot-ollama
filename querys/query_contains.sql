SELECT 
    p.id, 
    p.nombre AS producto, 
    p.descripcion, 
    p.precio_costo, 
    p.precio_venta, 
    p.stock, 
    m.nombre AS marca, 
    c.nombre AS categoria
FROM productos p 
INNER JOIN marcas m ON p.marca_id = m.id 
INNER JOIN categorias c ON p.categoria_id = c.id
WHERE LOWER(p.nombre) LIKE %s
AND NOT LOWER(p.nombre) LIKE %s
ORDER BY p.nombre ASC;