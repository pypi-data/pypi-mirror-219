def update_tracking_info_to_package(pkg_dict, new_pkg_dict):
    """ override a dataset to add tracking summary information """

    pkg_dict['tracking_summary'] = new_pkg_dict['tracking_summary']
    # Add tracking information for each resource
    for resource_dict in pkg_dict.get('resources', []):
        for new_resource_dict in new_pkg_dict.get('resources', []):
            if resource_dict['url'] == new_resource_dict['url']:
                resource_dict['tracking_summary'] = new_resource_dict['tracking_summary']

    return pkg_dict
