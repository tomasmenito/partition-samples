# partition-samples
Django + Postgres partitions samples


# Triggers generated after architect

```sql
-- before_insert_bookstore_purchase_trigger
DECLARE
    match bookstore_purchase."purchased_at"%TYPE;
    tablename VARCHAR;
    checks TEXT;

BEGIN
    IF NEW."purchased_at" IS NULL THEN
        tablename := 'bookstore_purchase_null';
        checks := '"purchased_at" IS NULL';
    ELSE
        match := DATE_TRUNC('month', NEW."purchased_at");
        tablename := 'bookstore_purchase_' || TO_CHAR(NEW."purchased_at", '"y"YYYY"m"MM');
        checks := '"purchased_at" >= ''' || match || ''' AND "purchased_at" < ''' || (match + INTERVAL '1 month') || '''';
    END IF;

    IF NOT EXISTS(
        SELECT 1 FROM information_schema.tables WHERE table_name=tablename)
    THEN
        BEGIN
            EXECUTE 'CREATE TABLE ' || tablename || ' (
                CHECK (' || checks || '),
                LIKE "bookstore_purchase" INCLUDING DEFAULTS INCLUDING CONSTRAINTS INCLUDING INDEXES
            ) INHERITS ("bookstore_purchase");';
        EXCEPTION WHEN duplicate_table THEN
            -- pass
        END;
    END IF;

    EXECUTE 'INSERT INTO ' || tablename || ' VALUES (($1).*);' USING NEW;
    RETURN NEW;
END;

```

```sql
-- after_insert_bookstore_purchase_trigger
BEGIN
    DELETE FROM ONLY "bookstore_purchase" WHERE id = NEW.id;
    RETURN NEW;
END; 
```
