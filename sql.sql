CREATE PROCEDURE
proc_name (in my_param_name int)
BEGIN

    select name , *
    from my_table where cond = (col + 1) and col > 12;

 END