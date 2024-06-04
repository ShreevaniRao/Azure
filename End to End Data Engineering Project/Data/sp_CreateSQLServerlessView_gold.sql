--- Stored procedure to create views for all tables in the 'gold' storage container--

USE gold_db
GO

CREATE OR ALTER PROC CreateSQLServerlessview_gold @viewname nvachar(100)
AS
BEGIN

DECLARE @statement VARCHAR(MAX)
    SET @statement = N'CREATE OR ALTER VIEW' + @viewname + ' AS
        SELECT *
        FROM
            OPENROWSET(
                BULK ''https://staccdataengproject01.dfs.core.windows.net/gold/SalesLT/'+ @viewname + '/'',
                FORMAT = ''DELTA''
                ) as [result]


EXEC (@statement)
END
GO