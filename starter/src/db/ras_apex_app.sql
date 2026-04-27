-- CREATE INDEX SUPPORT_SR_QUESTION_IDX ON SUPPORT_SR(question) INDEXTYPE IS CTXSYS.CONTEXT;    
-- CREATE INDEX SUPPORT_SR_ANSWER_IDX ON SUPPORT_SR(answer) INDEXTYPE IS CTXSYS.CONTEXT;   
-- EXEC CTX_DDL.SYNC_INDEX('SUPPORT_SR_QUESTION_IDX');
-- EXEC CTX_DDL.SYNC_INDEX('SUPPORT_SR_ANSWER_IDX');

CREATE VECTOR INDEX APEX_APP.SUPPORT_SR_HNSW_IDX ON APEX_APP.SUPPORT_SR(embedding) ORGANIZATION INMEMORY NEIGHBOR GRAPH DISTANCE COSINE WITH TARGET ACCURACY 95;

begin
    sys.xs_security_class.create_security_class(
    name => 'SUPPORT_SR_SEC_CLASS',
    description => 'Security Class',
    parent_list => XS$NAME_LIST('SYS.DML'),
    priv_list => xs$privilege_list(xs$privilege('internal_sr')));
end;
/

-- Creation of the ACL & mapping of the previously created roles : 
declare  
  aces xs$ace_list := xs$ace_list();  
begin 
  aces.extend(1);
  aces(1) := xs$ace_type(privilege_list => xs$name_list('select'),
                    principal_name  => 'PUBLIC',
                    principal_type  => XS_ACL.PTYPE_DB);
                    -- principal_name => 'customer_role');
  sys.xs_acl.create_acl(name => 'customer_acl',
                    ace_list  => aces,
                    sec_class => 'SUPPORT_SR_SEC_CLASS');

  aces(1) := xs$ace_type(privilege_list => xs$name_list('select','internal_sr'),
                             principal_name => 'employee_role');
  sys.xs_acl.create_acl(name => 'employee_acl',
                    ace_list  => aces,
                    sec_class => 'SUPPORT_SR_SEC_CLASS');

  aces(1) := xs$ace_type(privilege_list => xs$name_list('select'),
                             principal_name => 'APEX_APP',
                             principal_type=>XS_ACL.PTYPE_DB);
  sys.xs_acl.create_acl(name => 'apex_app_acl',
                    ace_list  => aces,
                    sec_class => 'SUPPORT_SR_SEC_CLASS');                    
end;
/

-- Creation of a policy 
declare
  realms   xs$realm_constraint_list := xs$realm_constraint_list();      
  cols     xs$column_constraint_list := xs$column_constraint_list();
begin  
  realms.extend(3);
  realms(1) := xs$realm_constraint_type(
    realm=> '1=1',acl_list => xs$name_list('employee_acl'));
  
  realms(2) := xs$realm_constraint_type(
    realm=> 'internal=0',acl_list => xs$name_list('customer_acl'));

  realms(3) := xs$realm_constraint_type(
    realm=> '1=1',acl_list => xs$name_list('apex_app_acl'));    

  sys.xs_data_security.create_policy(
    name                   => 'support_sr_policy',
    realm_constraint_list  => realms);
end;
/

-- Apply the policy to the table
begin
    XS_DATA_SECURITY.apply_object_policy(
        schema=>'apex_app', 
        object=>'support_sr',
        policy=>'support_sr_policy',
        statement_types=>'SELECT');
end;    
/  

begin
  if (sys.xs_diag.validate_workspace()) then
    dbms_output.put_line('All configurations are correct.');
  else
    dbms_output.put_line('Some configurations are incorrect.');
  end if;
end;
/
select * from xs$validation_table order by 1, 2, 3, 4;
/
exit;