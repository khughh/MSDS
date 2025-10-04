-- Question 1 Write and execute the SQL command to list the total sales by region and customer. Your output should be sorted by region and customer.
SELECT 
    V.V_STATE AS "Region",
    I.CUS_CODE AS "Customer",
    SUM(L.LINE_UNITS * L.LINE_PRICE) AS "Total Sales"
FROM 
    LINE L
JOIN INVOICE I ON L.INV_NUMBER = I.INV_NUMBER
JOIN PRODUCT P ON L.P_CODE = P.P_CODE
JOIN VENDOR V ON P.V_CODE = V.V_CODE
GROUP BY 
    V.V_STATE, 
    I.CUS_CODE
ORDER BY 
    V.V_STATE, 
    I.CUS_CODE;
	
-- Question 2
SELECT 
    i.CUS_CODE AS "Customer Code", 
    EXTRACT(MONTH FROM i.INV_DATE) AS "Month", 
    LINE.P_CODE AS "Product Code", 
    SUM(LINE.LINE_UNITS * LINE.LINE_PRICE) AS "Total Sales"
FROM 
    INVOICE i
JOIN 
    LINE ON i.INV_NUMBER = LINE.INV_NUMBER
GROUP BY 
    i.CUS_CODE, 
    EXTRACT(MONTH FROM i.INV_DATE), 
    LINE.P_CODE;
	
-- Question 3
SELECT 
    I.CUS_CODE AS "Customer",
    L.P_CODE AS "Product",
    SUM(L.LINE_UNITS * L.LINE_PRICE) AS "Total Sales"
FROM 
    LINE L
JOIN INVOICE I ON L.INV_NUMBER = I.INV_NUMBER
GROUP BY 
    I.CUS_CODE, 
    L.P_CODE
ORDER BY 
    I.CUS_CODE, 
    L.P_CODE;

-- Question 4
-- Assumption is that V_CODE (Vendor Code) is representative of product catagory 
-- based upon the vendor. 
-- Also P_DESCRIPTION could be considered, but it is not catagorical other than 
-- being the literal description
SELECT 
    EXTRACT(MONTH FROM i.INV_DATE) AS "Month", 
    p.V_CODE AS "Product Category",
    SUM(l.LINE_UNITS * l.LINE_PRICE) AS "Total Sales"
FROM 
    INVOICE i
JOIN 
    LINE l ON i.INV_NUMBER = l.INV_NUMBER
JOIN 
    PRODUCT p ON l.P_CODE = p.P_CODE
GROUP BY 
    "Month", "Product Category"
ORDER BY 
    "Month", "Product Category";

-- Question 5
SELECT 
    EXTRACT(MONTH FROM i.INV_DATE) AS "Month", 
    COUNT(*) AS "Number of Product Sales",
    SUM(l.LINE_UNITS * l.LINE_PRICE) AS "Total Sales"
FROM 
    INVOICE i
JOIN 
    LINE l ON i.INV_NUMBER = l.INV_NUMBER
GROUP BY 
    "Month"
ORDER BY 
    "Month";

-- Question 6 
-- Again assuming that product catagory corresponds to "V_CODE"
SELECT 
    EXTRACT(MONTH FROM i.INV_DATE) AS "Month", 
    p.V_CODE AS "Product Category",
    COUNT(*) AS "Number of Product Sales",
    SUM(l.LINE_UNITS * l.LINE_PRICE) AS "Total Sales"
FROM 
    INVOICE i
JOIN 
    LINE l ON i.INV_NUMBER = l.INV_NUMBER
JOIN 
    PRODUCT p ON l.P_CODE = p.P_CODE
GROUP BY 
    "Month", "Product Category"
ORDER BY 
    "Month", "Product Category";

--Question 7 
SELECT 
    EXTRACT(MONTH FROM i.INV_DATE) AS "Month", 
    p.V_CODE AS "Product Category",
    l.P_CODE AS "Product",
    COUNT(*) AS "Number of Product Sales",
    SUM(l.LINE_UNITS * l.LINE_PRICE) AS "Total Sales"
FROM 
    INVOICE i
JOIN 
    LINE l ON i.INV_NUMBER = l.INV_NUMBER
JOIN 
    PRODUCT p ON l.P_CODE = p.P_CODE
GROUP BY 
    "Month", "Product Category", "Product"
ORDER BY 
    "Month", "Product Category", "Product";

