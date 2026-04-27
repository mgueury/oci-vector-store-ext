resource "oci_apigateway_deployment" "starter_apigw_deployment-openid" {
  compartment_id = local.lz_app_cmp_ocid
  display_name   = "${var.prefix}-apigw-deployment-openid"
  gateway_id     = local.apigw_ocid
  path_prefix    = "/openid"
  specification {
    # Route the COMPUTE_PRIVATE_IP 
    routes {
      path    = "/chatui/{pathname*}"
      methods = [ "ANY" ]
      backend {
        type = "HTTP_BACKEND"
        url    = "http://${local.apigw_dest_private_ip}:8080/$${request.path[pathname]}"
        connect_timeout_in_seconds = 60
        read_timeout_in_seconds = 120
        send_timeout_in_seconds = 120              
      }
    } 
    routes {
      path    = "/server/{pathname*}"
      methods = [ "ANY" ]
      backend {
        type = "HTTP_BACKEND"
        url    = "http://${local.apigw_dest_private_ip}:2024/$${request.path[pathname]}"
        connect_timeout_in_seconds = 60
        read_timeout_in_seconds = 120
        send_timeout_in_seconds = 120              
      }
      request_policies {
        header_transformations {
          set_headers {
            items {
              if_exists = "OVERWRITE"
              name      = "Authorization"
              values = [
                "Bearer $${request.auth[access_token]}",
              ]
            }
          }
        }   
      }     
    } 
    routes {
      path    = "/userinfo"
      methods = [ "ANY" ]
      backend {
        type = "HTTP_BACKEND"
        url    = "${local.local_idcs_url}oauth2/v1/userinfo"
        connect_timeout_in_seconds = 60
        read_timeout_in_seconds = 120
        send_timeout_in_seconds = 120              
      }
      request_policies {
        header_transformations {
          set_headers {
            items {
              if_exists = "OVERWRITE"
              name      = "Authorization"
              values = [
                "Bearer $${request.auth[access_token]}",
              ]
            }
          }
        }  
      }    
      response_policies {
        header_transformations {
          set_headers {
            items {
              if_exists = "OVERWRITE"
              name      = "X-CSRF-TOKEN"
              values = [
                "$${request.auth[apigw_csrf_token]}",
              ]
            }
          }
        }  
      }    
    }     
    routes {
      path    = "/{pathname*}"
      methods = [ "ANY" ]
      backend {
        type = "HTTP_BACKEND"
        url    = "http://${local.apigw_dest_private_ip}/$${request.path[pathname]}"
      } 
    }  
    routes {
      path    = "/logout"
      methods = [ "GET" ]
      backend {
        type = "OAUTH2_LOGOUT_BACKEND"
        allowed_post_logout_uris = [ "/logout_html", "https://www.oracle.com", "https://${local.apigw_hostname}/", "https://${local.apigw_hostname}/openid/chat.html" ]
      }
    }
    # https://xxxxx.apigateway.eu-frankfurt-1.oci.customer-oci.com/openid/logout?postLogoutUrl=https://xxxxx.apigateway.eu-frankfurt-1.oci.customer-oci.com/openid/chat.html
    routes {
      path    = "/logout_html"
      methods = [ "GET" ]
      backend {
        type = "STOCK_RESPONSE_BACKEND"
        body = "Logout Error: OAUTH2 Token could not be revoked."
        status = 200
      }
    }         
    request_policies {
      authentication {
        type = "TOKEN_AUTHENTICATION"
        token_header = "Authorization"
        token_auth_scheme = "Bearer"
        is_anonymous_access_allowed = false
        validation_policy {
          // Example validation policy using an OAuth2 introspection endpoint
          // (https://datatracker.ietf.org/doc/html/rfc7662) to validate the
          // clients authorization credentials
          type = "REMOTE_DISCOVERY"
          is_ssl_verify_disabled = true
          max_cache_duration_in_hours = 1
          source_uri_details {
            // Discover the OAuth2/OpenID configuration from an RFC8414
            // metadata endpoint (https://www.rfc-editor.org/rfc/rfc8414)
            type = "DISCOVERY_URI"
            uri = "${local.local_idcs_url}.well-known/openid-configuration"
          }
          client_details {
            // Specify the OAuth client id and secret to use with the
            // introspection endpoint
            type                         = "CUSTOM"
            client_id                    = local.openid_client_id
            client_secret_id             = oci_vault_secret.starter_openid_secret.id
            client_secret_version_number = oci_vault_secret.starter_openid_secret.current_version_number
          }
        }
        validation_failure_policy {
          // When a client uses the API without auth credentials, or
          // invalid/expired credentials then invoke the OAuth2 flow using
          // the configuration below.
          type = "OAUTH2"
          scopes = ["openid"]
          response_type = "CODE"
          max_expiry_duration_in_hours = 1
          use_cookies_for_intermediate_steps = true
          use_cookies_for_session = true
          use_pkce = true
          fallback_redirect_path = "/fallback"
          logout_path = "/logout"
          source_uri_details {
            // Use the same discovery URI as the validation policy above.
            type = "VALIDATION_BLOCK"
          }
          client_details {
            // Use the same OAuth2 client details as the validation policy above.
            type = "VALIDATION_BLOCK"
          }
        }
      }
    }      
  }
  freeform_tags = local.api_tags
}      

/*
# resource oci_logging_log starter_apigw_deployment_execution {
  count = var.log_group_ocid == null ? 0 : 1
  log_group_id = var.log_group_ocid
  configuration {
    compartment_id = local.lz_app_cmp_ocid
    source {
      category    = "execution"
      resource    = oci_apigateway_deployment.starter_apigw_deployment.id
      service     = "apigateway"
      source_type = "OCISERVICE"
    }
  }
  display_name = "${var.prefix}-apigw-deployment-execution"
  freeform_tags = local.freeform_tags
  is_enabled         = "true"
  log_type           = "SERVICE"
  retention_duration = "30"
}

# resource oci_logging_log starter_apigw_deployment_access {
  count = var.log_group_ocid == null ? 0 : 1
  log_group_id = var.log_group_ocid
  configuration {
    compartment_id = local.lz_app_cmp_ocid
    source {
      category    = "access"
      resource    = oci_apigateway_deployment.starter_apigw_deployment.id
      service     = "apigateway"
      source_type = "OCISERVICE"
    }
  }
  display_name = "${var.prefix}-apigw-deployment-access"
  freeform_tags = local.freeform_tags
  is_enabled         = "true"
  log_type           = "SERVICE"
  retention_duration = "30"
}
*/

locals {
  openid_client_id = oci_identity_domains_app.starter_confidential_app.name
  openid_client_secret = oci_identity_domains_app.starter_confidential_app.client_secret
}


locals {
  apigw_hostname = oci_apigateway_gateway.starter_apigw.hostname
}

resource "oci_vault_secret" "starter_openid_secret" {
  #Required
  compartment_id = local.lz_app_cmp_ocid
  secret_content {
    #Required
    content_type = "BASE64"

    #Optional
    content = base64encode(local.openid_client_secret)
    name    = "${var.prefix}-openid-secret"
    stage   = "CURRENT"
  }
  key_id      = local.vault_key_ocid
  secret_name = "${var.prefix}-openid-secret-${random_string.id.result}"
  vault_id    = local.vault_ocid
}

resource "oci_identity_domains_app" "starter_confidential_app" {
  active                  = "true"
  all_url_schemes_allowed = "false"
  allow_access_control    = "false"
  allowed_grants = [
    "client_credentials",
    "authorization_code",
  ]
  allowed_operations = [
    "introspect",
  ]
  attr_rendering_metadata {
    name = "aliasApps"
    section = ""
    visible = "false"
    widget  = ""
  }
  based_on_template {
    value         = "CustomWebAppTemplateId"
    well_known_id = "CustomWebAppTemplateId"
  }
  client_ip_checking = "anywhere"
  client_type        = "confidential"
  delegated_service_names = [
  ]
  display_name = "${var.prefix}-confidential-app"
  idcs_endpoint = "${local.local_idcs_url}"
  is_alias_app      = "false"
  is_enterprise_app = "false"
  is_kerberos_realm = "false"
  is_login_target   = "true"
  is_mobile_target  = "false"
  is_oauth_client   = "true"
  is_oauth_resource = "false"
  is_saml_service_provider = "false"
  is_unmanaged_app         = "false"
  is_web_tier_policy       = "false"
  login_mechanism = "OIDC"
  logout_uri = "https://${local.apigw_hostname}/openid/logout"
  post_logout_redirect_uris = [
    "https://www.oracle.com",
    "https://${local.apigw_hostname}/",
    "https://${local.apigw_hostname}/openid/chat.html",
  ]
  redirect_uris = [
    "https://${local.apigw_hostname}/openid/chat.html"
  ]
  schemas = [
    "urn:ietf:params:scim:schemas:oracle:idcs:App"
  ]
  show_in_my_apps = "false"
  trust_scope     = "Account"
}

