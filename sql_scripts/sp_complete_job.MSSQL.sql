USE [MWC_APP]
GO
/****** Object:  StoredProcedure [dbo].[sp_complete_job]    Script Date: 18/10/2017 12:58:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO


-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date,,>
-- Description:	<Description,,>
-- =============================================
ALTER PROCEDURE [dbo].[sp_complete_job] 
	-- Add the parameters for the stored procedure here
	@jobid int, @payment_status int
AS
BEGIN
	
	SET NOCOUNT ON;
	declare @customerID int, @frequency int, @this_date date, @price money, @wc int

	select	@customerID = c.id
			,@frequency = c.frequency
			,@this_date = j.allocated_date 
			,@price = j.price
			,@wc =j.window_cleaner_id
	from customers_customer c inner join worksheets_jobs j on j.customer_id = c.id
	where j.id = @jobid

    update dbo.worksheets_jobs set completed_date = allocated_date, job_status_id = 3 --completed
									, payment_status_id = @payment_status --1 = 'paid', 2 = 'owed'
			where  dbo.worksheets_jobs.id = @jobid
	
	insert into dbo.worksheets_jobs (scheduled_date, customer_id, job_status_id, price, invoiced, window_cleaner_id)
	values (dateadd(w,@frequency,@this_date), @customerID, 1, @price, 0, @wc) -- 1 = 'due'
END


