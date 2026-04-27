# -- StreamLit / NLB ---------------------------------------------------------

resource "oci_network_load_balancer_network_load_balancer" "starter_nlb" {
  compartment_id = local.lz_app_cmp_ocid
  subnet_id = data.oci_core_subnet.starter_web_subnet.id
  display_name = "${var.prefix}-nlb"
  is_private=false
}

resource "oci_network_load_balancer_network_load_balancers_backend_sets_unified" "starter_nlb_bes_8080" {
  name                     = "${var.prefix}-nlb-bes-8080"
  network_load_balancer_id = oci_network_load_balancer_network_load_balancer.starter_nlb.id
  policy                   = "FIVE_TUPLE"  
  health_checker {
    port                   = "8080"
    protocol               = "TCP"
    timeout_in_millis      = 10000
    interval_in_millis     = 10000
    retries                = 3
  }
}

resource "oci_network_load_balancer_listener" "starter_listener_8080" {
    #Required
    name = "${var.prefix}-nlb-listener-8080"
    network_load_balancer_id = oci_network_load_balancer_network_load_balancer.starter_nlb.id
    default_backend_set_name = "${var.prefix}-nlb-bes-8080"
    port = 8080
    protocol = "TCP"
    depends_on = [
        oci_network_load_balancer_network_load_balancers_backend_sets_unified.starter_nlb_bes_8080 
    ]    
}

resource "oci_network_load_balancer_backend" "starter_nlb_be_8080" {
    #Required
    backend_set_name = "${var.prefix}-nlb-bes-8080"
    network_load_balancer_id = oci_network_load_balancer_network_load_balancer.starter_nlb.id
    port = 8080

    #Optional
    is_backup = false
    is_drain = false
    is_offline = false
    name = "${var.prefix}-nlb-be-8080"
    target_id = oci_core_instance.starter_compute.id
    weight = 1

    depends_on = [
        oci_network_load_balancer_network_load_balancers_backend_sets_unified.starter_nlb_bes_8080
    ]
}

resource "oci_network_load_balancer_network_load_balancers_backend_sets_unified" "starter_nlb_bes_2024" {
  name                     = "${var.prefix}-nlb-bes-2024"
  network_load_balancer_id = oci_network_load_balancer_network_load_balancer.starter_nlb.id
  policy                   = "FIVE_TUPLE"  
  health_checker {
    port                   = "2024"
    protocol               = "TCP"
    timeout_in_millis      = 10000
    interval_in_millis     = 10000
    retries                = 3
  }
}

resource "oci_network_load_balancer_listener" "starter_listener_2024" {
    #Required
    name = "${var.prefix}-nlb-listener-2024"
    network_load_balancer_id = oci_network_load_balancer_network_load_balancer.starter_nlb.id
    default_backend_set_name = "${var.prefix}-nlb-bes-2024"
    port = 2024
    protocol = "TCP"
    depends_on = [
        oci_network_load_balancer_network_load_balancers_backend_sets_unified.starter_nlb_bes_2024 
    ]    
}

resource "oci_network_load_balancer_backend" "starter_nlb_be_2024" {
    #Required
    backend_set_name = "${var.prefix}-nlb-bes-2024"
    network_load_balancer_id = oci_network_load_balancer_network_load_balancer.starter_nlb.id
    port = 2024

    #Optional
    is_backup = false
    is_drain = false
    is_offline = false
    name = "${var.prefix}-nlb-be-2024"
    target_id = oci_core_instance.starter_compute.id
    weight = 1

    depends_on = [
        oci_network_load_balancer_network_load_balancers_backend_sets_unified.starter_nlb_bes_2024
    ]
}