-- FUNCTION: public.random_jobs()

-- DROP FUNCTION public.random_jobs();

CREATE OR REPLACE FUNCTION public.random_jobs(
	)
    RETURNS boolean
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE 
    ROWS 0
AS $BODY$

DECLARE
 var_custid int;
 var_I INT;
 var_D DATE; 
 var_P MONEY; 
 var_J INT;
 var_C INT;
 var_delta INT;
 cust_var   RECORD;
 
declare cust_cursor CURSOR for select * from customers_customer;

BEGIN  
open cust_cursor;
  	LOOP
    	var_delta := rand_between(1,7);
        var_D :=  CURRENT_DATE + var_delta; --LATEST JOB DATE    
        var_P := rand_between(5,45); --PRICE
        var_J := rand_between(5,25); --JOBS
        var_C := case when random() >0.5 then 6 else 8 end; --WCs
        
        fetch cust_cursor into cust_var;
   		EXIT WHEN NOT FOUND;
   		raise notice 'cust: %', cust_var.id;
        
         --INSERT 1ST JOB
         INSERT INTO worksheets_job
                 (scheduled_date
                 ,allocated_date           
                 ,price
                 ,job_notes
                 ,customer_id
                 ,job_status_id          
                 ,window_cleaner_id
                 ,invoiced)
         VALUES
                 (var_D
                 ,var_D           
                 ,var_P
                 ,lipsum(rand_between(10,200))
                 ,cust_var.id        
                 ,1
                 ,var_C
                 ,true);

		
        
        WHILE var_J > 0     LOOP  
        	var_D := var_D + -7 * INTERVAL '1 day';
          
          	INSERT INTO worksheets_job
                 (scheduled_date
                 ,allocated_date
                 ,completed_date
                 ,price
                 ,job_notes
                 ,customer_id
                 ,job_status_id
                 ,payment_status_id
                 ,window_cleaner_id
                 ,invoiced)
      		VALUES
                 (var_D
                 ,var_D
                 ,var_D
                 ,var_P
                 ,lipsum(rand_between(10,200))
                 ,cust_var.id
                 ,3
                 ,CASE WHEN rand_between(1,100) >= 95 THEN 2 ELSE 1 END
                 ,var_C
                 ,FALSE);
          
          	var_J:=var_J-1;
          	raise notice 'cust: %, JOB: %', cust_var.id, var_J;

      	END LOOP;
        
        
	END LOOP;
CLOSE cust_cursor;  
UPDATE worksheets_job SET invoiced = FALSE WHERE completed_date >= CURRENT_DATE - 14;
RETURN FALSE;
END; 

$BODY$;
