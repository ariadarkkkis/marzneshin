export interface AdminType {
    id: number;
    username: string;
    enabled: boolean;
    is_sudo: boolean;
    all_services_access: boolean;
    add_users_access: boolean;
    edit_users_access: boolean;
    delete_users_access: boolean;
    delete_expired_users_access: boolean;
    reset_users_usage_access: boolean;
    toggle_users_status_access: boolean;
    revoke_users_sub_access: boolean;
    service_ids: number[];
    subscription_url_prefix: string;
    users_data_usage: number;
}

