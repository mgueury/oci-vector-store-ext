# Releases notes
- 2025-09-17:
    - Change the OCI starter used to 4.0 (lot of small improvement. env.sh -> terraform.tfvars. Allow creation of the whole stack with Resource Manager)
    - rag_storage mode db26ai 
    - Added web site crawler 
    - sitemap extension
    - convertion to markdown
    - cleanup of the whole structure
    - use new python version and UV
    - ....
- 2025-03-21: 
    - Fix in the APEX app. When the response was bigger than 32K, the response was not shown. Ex: "what is Oracle Analytics failed".
    
- 2025-03-07: 
    - Upgraded libreoffice to 2.8.4.5
    - LibreOffice (.doc, . docx, .ppt, .pptx -> pdf) if not installed default to default parser
    - Catch errors if the streaming cursor is expired and recreate the connection (ex: when document understanding takes too much time, the streaming connection expires)
    
- 2025-02-19: 
    - Fix for non-latin1 files and customized_url_source 
    - LibreOffice (.doc, . docx, .ppt, .pttx -> pdf) enabled as default
    - Chrome+Selenium enabled enabled as default 
    - Remove the auth_token and replace by oci raw-request
