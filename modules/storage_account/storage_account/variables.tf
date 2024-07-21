variable "storage_account_name" {
    description = "this the description of resource gropu"
    type = string
  
}
variable "resource_group_name" {
    description = "this the description of resource gropu"
    type = string
  
}
variable "location" {
    description="this is description of location"
    type = string
  
}
variable "source_folder_name" {
    description = "this is source file."
    type = string
  
}
variable "destination_folder_name" {
    description = "this is destination file."
    type = string
  
}
variable "container_access_type" {
    description = "the access type of storage account container"
    type = string
    default = "private"
}
