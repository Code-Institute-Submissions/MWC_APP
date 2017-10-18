-- FUNCTION: public.rand_between(integer, integer)

-- DROP FUNCTION public.rand_between(integer, integer);

CREATE OR REPLACE FUNCTION public.rand_between(
	low integer,
	high integer)
    RETURNS integer
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE STRICT 
    ROWS 0
AS $BODY$

BEGIN
   RETURN floor(random()* (high-low + 1) + low);
END;

$BODY$;
