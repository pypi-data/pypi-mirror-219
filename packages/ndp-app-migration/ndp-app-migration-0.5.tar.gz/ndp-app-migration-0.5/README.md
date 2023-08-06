### Usage and Installation
```
pip3 install ndp-app-migration==0.5

from ndp_migration.objects_migration import migration_data_objects

migration_data_objects(folder_path,key_decrypt,api_url,jar_file_name,option_for_backup,target_host,target_user_id,target_password,con_name,pipe_name,object_type)

migration_data_objects(source_email_address, source_password, folder_path, source_api_url, option_for_backup,target_api_url, ,target_user_id,target_password,con_name,pipe_name,object_type)

```