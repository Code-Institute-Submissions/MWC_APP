-- FUNCTION: public.sp_complete_job(integer, integer)

-- DROP FUNCTION public.sp_complete_job(integer, integer);

CREATE OR REPLACE FUNCTION public.sp_complete_job(
	jobid integer,
	payment_status integer)
    RETURNS void
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE 
    ROWS 0
AS $BODY$

DECLARE
  customerID INTEGER;
  frequency INTEGER;
  this_date DATE;
  price MONEY; 
  wc INTEGER;
 
BEGIN 

SELECT c.id, c.frequency, j.allocated_date, j.price, j.window_cleaner_id
INTO customerID ,frequency, this_date ,price, wc 
FROM customers_customer AS c inner join worksheets_job AS j on j.customer_id = c.id
WHERE j.id = jobid;
    
UPDATE worksheets_job set completed_date = allocated_date, job_status_id = 3 --completed
									, payment_status_id = payment_status --1 = 'paid', 2 = 'owed'
			WHERE  worksheets_job.id = jobid;
	
	INSERT INTO worksheets_job (scheduled_date, customer_id, job_status_id, price, invoiced, window_cleaner_id)
	VALUES ((this_date + 7 * frequency), customerID, 1, price, False, wc); -- 1 = 'due
END; 

$BODY$;

