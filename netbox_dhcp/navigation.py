from netbox.plugins import PluginMenuItem, PluginMenuButton, PluginMenu

dhcp_server_buttons = [
    PluginMenuButton(
        link='plugins:netbox_dhcp:dhcpserver_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
    )
]

menu = PluginMenu(
    label='DHCP',
    groups=(
        ('DHCP Servers', (
            PluginMenuItem(
                link='plugins:netbox_dhcp:dhcpserver_list',
                link_text='DHCP Servers',
                buttons=dhcp_server_buttons
            ),
        ),),
    ),
    icon_class='mdi mdi-router'
)
