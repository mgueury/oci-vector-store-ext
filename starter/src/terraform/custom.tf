## Add your terraform object here

## Add your dependency before building the app
resource "null_resource" "custom_dependency" {
    depends_on = [
        oci_streaming_stream_pool.starter_stream_pool
    ]
}