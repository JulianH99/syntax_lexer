CREATE PROCEDURE
proc_name(my_param_name int)

BEGIN
    select name as full_name from
     my_table where cond = (col + 1) and col = 'hola';


 END