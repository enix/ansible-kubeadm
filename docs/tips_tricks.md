
Hidden (and less stable feature), tips and tricks

### No inventory ? No problem !

```
ansible-playbook -i <on_master_ip_look_at_comma_after>, -b -k -u admin playbooks/00_inventory.yml playbooks/01_site.yml
```