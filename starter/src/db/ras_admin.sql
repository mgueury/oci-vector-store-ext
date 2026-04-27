begin
  update APEX_APP.SUPPORT_SR set EMBEDDING=APEX_APP.ai_plsql.genai_embed( question || chr(13) || answer  );
  commit;
end;
/

grant xs_session_admin, create session to APEX_APP;
grant execute on DBMS_XS_SESSIONS to apex_app;
BEGIN
    -- Grant system privileges
    SYS.XS_ADMIN_CLOUD_UTIL.GRANT_SYSTEM_PRIVILEGE('ADMIN_ANY_SEC_POLICY','APEX_APP',SYS.XS_ADMIN_UTIL.PTYPE_DB,NULL);
END;
/

exec sys.xs_principal.create_role(name => 'employee_role', enabled => true);
exec sys.xs_principal.create_role(name => 'customer_role', enabled => true);

create role ras_role;
grant select on apex_app.support_sr to ras_role;
grant execute on apex_app.ai_plsql to ras_role;
grant ras_role to employee_role;
grant ras_role to customer_role;

exec sys.xs_principal.create_user(name => 'employee', schema => 'APEX_APP');
exec sys.xs_principal.set_password('employee', 'Not__Used1234');
exec sys.xs_principal.create_user(name => 'customer', schema => 'APEX_APP');
exec sys.xs_principal.set_password('customer', 'Not__Used1234');

exec  sys.xs_principal.grant_roles('employee', 'employee_role');
exec  sys.xs_principal.grant_roles('customer', 'customer_role');